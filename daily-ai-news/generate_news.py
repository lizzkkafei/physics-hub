"""
Daily AI News Generator
1. Search today's AI news via Tavily API
2. Summarize into 10 structured Chinese articles via DeepSeek API
3. Write articles_data.json
4. Call build_page.py to generate static HTML + TTS voices
"""
import json, os, re, sys, time
from datetime import datetime
from dotenv import load_dotenv

BASE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE, '..', '.env'))

DEEPSEEK_KEY = os.environ.get('DEEPSEEK_API_KEY')
TAVILY_KEY = os.environ.get('TAVILY_API_KEY')

NOW = datetime.now()
DATE_ISO = NOW.strftime('%Y-%m-%d')
WEEKDAYS_CN = ['一', '二', '三', '四', '五', '六', '日']
DATE_CN = f"{NOW.year}年{NOW.month}月{NOW.day}日 星期{WEEKDAYS_CN[NOW.weekday()]}"

DATA_FILE = os.path.join(BASE, 'articles_data.json')

SEARCH_QUERIES = [
    "AI artificial intelligence news today",
    "大模型 人工智能 最新新闻 今天",
    "OpenAI Anthropic Google AI breakthrough news today",
    "AI agent LLM latest news 2026",
]


def is_already_generated():
    if not os.path.exists(DATA_FILE):
        return False
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('generated_date') == DATE_ISO


def search_news():
    """Search for today's AI news using Tavily API."""
    from tavily import TavilyClient
    client = TavilyClient(api_key=TAVILY_KEY)

    all_results = []
    seen_urls = set()

    for query in SEARCH_QUERIES:
        try:
            resp = client.search(query, search_depth="advanced", max_results=8)
            for r in resp.get('results', []):
                url = r.get('url', '')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append({
                        'title': r.get('title', ''),
                        'url': url,
                        'content': r.get('content', ''),
                    })
        except Exception as e:
            print(f"  [WARN] Tavily search failed for '{query}': {e}")
            continue

    print(f"  Tavily search: {len(all_results)} unique results from {len(SEARCH_QUERIES)} queries")
    return all_results


def build_search_context(results):
    """Format search results as text for DeepSeek prompt."""
    lines = []
    for i, r in enumerate(results[:40], 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    URL: {r['url']}")
        lines.append(f"    Summary: {r['content'][:300]}")
        lines.append("")
    return '\n'.join(lines)


def summarize_with_deepseek(search_context):
    """Call DeepSeek API to generate 10 structured Chinese news articles."""
    from openai import OpenAI

    system_prompt = """你是一个专业的AI科技新闻编辑。根据提供的搜索结果，生成今日最重要的10条AI/人工智能中文新闻。

要求：
1. 每条新闻包含：title(标题)、short(简短摘要, 80-150字)、full(完整报道, 3-6段详细分析)
2. 完整报道要有深度分析，包含背景、影响和行业观点，不是简单翻译
3. 按重要性排序，第1条是最重要的新闻
4. 如果搜索结果不够10条，根据你对AI行业的了解补充相关新闻
5. 所有内容使用简体中文
6. 输出必须是合法的JSON格式，不要包含任何markdown代码块标记

输出格式：
{"articles":[{"rank":1,"title":"新闻标题","short":"简要概述...","full":"详细报道第一段...\\n\\n详细报道第二段...","sources":["https://..."],"source_titles":["原始来源标题"]}]}"""

    user_prompt = f"""今天是{DATE_CN}。以下是搜索到的AI领域最新信息：

{search_context}

请根据以上信息，生成今日最重要的10条AI新闻。直接输出JSON。"""

    for attempt in range(3):
        try:
            client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")
            resp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=8000,
            )
            content = resp.choices[0].message.content
            return _parse_json(content)
        except Exception as e:
            print(f"  [WARN] DeepSeek API attempt {attempt + 1}/3 failed: {e}")
            if attempt < 2:
                time.sleep(5)
    raise RuntimeError("DeepSeek API failed after 3 attempts")


def _parse_json(content):
    """Parse JSON from DeepSeek response, with markdown code block fallback."""
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        m = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
        if m:
            data = json.loads(m.group(1))
        else:
            raise ValueError(f"Cannot parse JSON from: {content[:500]}")
    return data


def main():
    print(f"[{NOW.strftime('%Y-%m-%d %H:%M:%S')}] Starting daily AI news generation...")

    if not DEEPSEEK_KEY or not TAVILY_KEY:
        print("ERROR: Missing API keys. Check .env file.")
        sys.exit(1)

    if is_already_generated():
        print(f"  Already generated for {DATE_ISO}, skipping.")
        return

    # Step 1: Search
    print("[1/4] Searching AI news via Tavily...")
    for attempt in range(3):
        try:
            results = search_news()
            if results:
                break
        except Exception as e:
            print(f"  [WARN] Search attempt {attempt + 1}/3: {e}")
            time.sleep(5)
    else:
        print("ERROR: Tavily search failed after 3 attempts. Exiting.")
        sys.exit(1)

    # Step 2: Summarize with DeepSeek
    print("[2/4] Summarizing with DeepSeek...")
    context = build_search_context(results)
    data = summarize_with_deepseek(context)

    articles = data.get('articles', [])
    print(f"  DeepSeek returned {len(articles)} articles")

    # Step 3: Write data file
    print("[3/4] Writing articles_data.json...")
    output = {
        'generated_at': NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
        'generated_date': DATE_ISO,
        'date_cn': DATE_CN,
        'articles': articles,
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"  ✓ articles_data.json ({len(articles)} articles)")

    # Step 4: Generate static pages + voices
    print("[4/4] Generating HTML pages and voice files...")
    import build_page
    build_page.main()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Done! "
          f"{len(articles)} articles, index.html, voices/ updated.")


if __name__ == '__main__':
    main()
