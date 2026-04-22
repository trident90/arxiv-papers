#!/usr/bin/env python3
"""
arXiv 논문 큐레이션 스크립트
- 화요일~토요일 아침 6시에 실행
- 전날 발표된 논문 중 실무 적용 가능한 TOP 5 선정
- Claude를 이용해 요약을 한글로 번역
- GitHub에 커밋 및 푸시
"""

import requests
import re
import json
import subprocess
from datetime import datetime, timedelta
import time
import os

CATEGORIES = ['cs.AI', 'cs.LG', 'cs.CV', 'cs.NI', 'cs.CR']

def fetch_papers(target_date):
    """특정 날짜의 모든 분야 논문 수집"""
    all_papers = {}
    
    for category in CATEGORIES:
        query = f'cat:{category}'
        url = 'http://export.arxiv.org/api/query'
        params = {
            'search_query': query,
            'start': 0,
            'max_results': 100,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            content = response.text
            
            entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
            
            papers = []
            for entry in entries:
                pub_match = re.search(r'<published>(\d{4}-\d{2}-\d{2})', entry)
                
                if pub_match and pub_match.group(1) == target_date:
                    title_match = re.search(r'<title>(.*?)</title>', entry)
                    id_match = re.search(r'<id>http://arxiv\.org/abs/(.*?)</id>', entry)
                    summary_match = re.search(r'<summary>\s*(.*?)\s*</summary>', entry, re.DOTALL)
                    authors = re.findall(r'<author>\s*<name>(.*?)</name>', entry)
                    
                    if title_match and id_match:
                        paper = {
                            'title': title_match.group(1).strip(),
                            'arxiv_id': id_match.group(1).strip(),
                            'authors': authors[:3],
                            'summary': summary_match.group(1).strip() if summary_match else '',
                            'date': target_date,
                            'category': category
                        }
                        papers.append(paper)
            
            all_papers[category] = papers
            print(f"  ✅ {category}: {len(papers)}편")
            time.sleep(0.6)  # Rate limit
            
        except Exception as e:
            print(f"  ❌ {category}: {str(e)[:40]}")
            all_papers[category] = []
    
    return all_papers

def translate_to_korean(text):
    """Claude API를 이용해 영문 요약을 한글로 번역"""
    if not text or len(text.strip()) == 0:
        return ""
    
    try:
        # OpenRouter API 사용 (Claude 3.5 Haiku)
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            print("⚠️ OPENROUTER_API_KEY 환경 변수 없음, 원문 그대로 사용")
            return text[:300] + "..." if len(text) > 300 else text
        
        url = 'https://openrouter.ai/api/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 텍스트 길이 제한 (번역 시간 단축)
        text_to_translate = text[:500] if len(text) > 500 else text
        
        payload = {
            'model': 'anthropic/claude-3.5-haiku',
            'messages': [{
                'role': 'user',
                'content': f'다음 영문 학술 논문 요약을 한글로 간결하게 번역해줘. 300자 이내로 요약해줘:\n\n{text_to_translate}'
            }],
            'temperature': 0.3,
            'max_tokens': 300
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            translated = result['choices'][0]['message']['content'].strip()
            return translated
        else:
            print(f"⚠️ Claude API 오류 (상태: {response.status_code}), 원문 사용")
            return text[:300] + "..." if len(text) > 300 else text
    
    except Exception as e:
        print(f"⚠️ 번역 오류: {str(e)[:50]}, 원문 사용")
        return text[:300] + "..." if len(text) > 300 else text

def score_paper(paper):
    """논문의 실무 적용 가능성과 주목도를 점수화"""
    score = 0
    
    title_lower = paper['title'].lower()
    summary_lower = paper['summary'].lower()
    full_text = (title_lower + ' ' + summary_lower).lower()
    
    # 실무 적용 관련 키워드 (높은 점수)
    practical_keywords = [
        'efficient', 'fast', 'optimization', 'scalable', 'production',
        'real-world', 'practical', 'robust', 'reliable', 'secure',
        'benchmark', 'sota', 'state-of-the-art', 'method', 'framework',
        'system', 'application', 'deployment', 'end-to-end', 'training'
    ]
    
    # 주목받는 분야 키워드 (중간 점수)
    trending_keywords = [
        'llm', 'multimodal', 'vision', 'language', 'transformer',
        'diffusion', 'reasoning', 'agent', 'retrieval', 'knowledge',
        '3d', 'video', 'image', 'text', 'speech'
    ]
    
    # 논문 점수 계산
    for keyword in practical_keywords:
        if keyword in full_text:
            score += 3
    
    for keyword in trending_keywords:
        if keyword in full_text:
            score += 1
    
    # 저자 수가 많으면 콜라보레이션 (가산점)
    if len(paper['authors']) >= 3:
        score += 1
    
    return score

def select_top_papers(all_papers, top_n=5):
    """모든 분야에서 TOP N 논문 선정"""
    all_scored = []
    
    for category, papers in all_papers.items():
        for paper in papers:
            paper['score'] = score_paper(paper)
            all_scored.append(paper)
    
    # 점수순으로 정렬 후 상위 N개 선정
    sorted_papers = sorted(all_scored, key=lambda x: x['score'], reverse=True)
    return sorted_papers[:top_n]

def generate_report(target_date, top_papers):
    """리포트 생성"""
    if not top_papers:
        return f"""# 📰 arXiv 엄선 리포트 - {target_date}

📊 **선정 기준**: 실무 적용 가능성 + 주목도  
🔗 **소스**: arXiv 공식 API | **업데이트**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

---

## ⚠️ 결과

해당 날짜에 게시된 논문이 없습니다.

---

*Generated by arXiv Curator | 엄선 논문 5편*
"""
    
    report = f"""# 📰 arXiv 엄선 리포트 - {target_date}

📊 **선정 기준**: 실무 적용 가능성 + 주목도  
🔗 **소스**: arXiv 공식 API | **업데이트**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC  
🎯 **선정 논문**: TOP 5 (점수 기반)

---

## 🏆 주목할 논문 TOP 5

"""
    
    emoji_map = {
        'cs.AI': '🤖',
        'cs.LG': '🧠',
        'cs.CV': '👁️',
        'cs.NI': '🌐',
        'cs.CR': '⛓️'
    }
    
    category_name_map = {
        'cs.AI': '인공지능',
        'cs.LG': '머신러닝',
        'cs.CV': '컴퓨터비전',
        'cs.NI': '네트워킹',
        'cs.CR': '보안/암호'
    }
    
    for i, paper in enumerate(top_papers, 1):
        cat = paper['category']
        authors_str = ', '.join(paper['authors'][:2]) if paper['authors'] else 'N/A'
        
        report += f"### {i}. {paper['title']}\n\n"
        report += f"{emoji_map[cat]} **분야**: {category_name_map[cat]} ({cat})\n"
        report += f"- **저자**: {authors_str}\n"
        report += f"- **arXiv ID**: {paper['arxiv_id']}\n"
        report += f"- **점수**: {paper['score']}점\n"
        
        if paper['summary']:
            # Claude를 이용해 한글로 번역
            print(f"   📝 {i}번 논문 요약 번역 중...")
            translated_summary = translate_to_korean(paper['summary'])
            report += f"- **요약 (한글)**: {translated_summary}\n"
        
        report += f"- **링크**: https://arxiv.org/abs/{paper['arxiv_id']}\n\n"
    
    report += """---

*Generated by arXiv Curator | 엄선 논문 5편*
"""
    
    return report

def commit_and_push(filepath, date_str):
    """Git 커밋 및 푸시"""
    try:
        subprocess.run(['git', 'add', filepath], cwd='/home/node/.openclaw/workspace', check=True)
        subprocess.run(
            ['git', 'commit', '-m', f'arxiv curator report: {date_str} (TOP 5 papers)'],
            cwd='/home/node/.openclaw/workspace',
            check=True
        )
        result = subprocess.run(
            ['git', 'push', 'origin', 'main'],
            cwd='/home/node/.openclaw/workspace',
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ GitHub 푸시 완료")
        else:
            print(f"⚠️ GitHub 푸시 실패 (토큰 문제)")
    except Exception as e:
        print(f"❌ Git 오류: {e}")

def main():
    # 전날 날짜 계산
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"🔍 {yesterday} 논문 수집 중...\n")
    
    # 논문 수집
    all_papers = fetch_papers(yesterday)
    total_papers = sum(len(papers) for papers in all_papers.values())
    
    print(f"\n📊 총 {total_papers}편 수집\n")
    
    # TOP 5 선정
    top_papers = select_top_papers(all_papers, top_n=5)
    
    if top_papers:
        print(f"🏆 TOP 5 선정:")
        for i, paper in enumerate(top_papers, 1):
            print(f"   {i}. [{paper['score']:2}점] {paper['title'][:60]}...")
    else:
        print(f"⚠️  선정된 논문이 없습니다.")
    
    # 리포트 생성
    report = generate_report(yesterday, top_papers)
    
    # 파일 저장
    filepath = f'/home/node/.openclaw/workspace/2026-04/2026-04-{yesterday.split("-")[2]}.md'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 리포트 생성: {filepath}")
    
    # Git 커밋 및 푸시
    print(f"📤 GitHub 업로드 중...")
    commit_and_push(filepath, yesterday)
    
    print(f"✅ 완료!")

if __name__ == '__main__':
    main()
