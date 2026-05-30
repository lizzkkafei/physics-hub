"""生成 AI 资讯网站：首页（无语音）+ 10个详情页（全文+语音）"""
import json, subprocess, os, re, html as html_mod
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
VOICES_DIR = os.path.join(BASE, "voices")
os.makedirs(VOICES_DIR, exist_ok=True)

TODAY = datetime.now()
DATE_ISO = TODAY.strftime("%Y-%m-%d")
WEEKDAYS_CN = ['日','一','二','三','四','五','六']
DATE_CN = f"{TODAY.year}年{TODAY.month}月{TODAY.day}日 星期{WEEKDAYS_CN[TODAY.weekday()]}"


def load_articles():
    """Load articles from JSON data file."""
    data_path = os.path.join(BASE, 'articles_data.json')
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        global DATE_CN
        DATE_CN = data.get('date_cn', DATE_CN)
        return data.get('articles', [])
    print("WARNING: articles_data.json not found, no articles to render")
    return []

ARTICLES = load_articles()


def esc(text):
    return html_mod.escape(text)

def build_index():
    """首页 — 无语音功能，纯列表展示"""
    items_html = []
    for a in ARTICLES:
        r = a['rank']
        rc = 'news-rank top3' if r <= 3 else 'news-rank'
        items_html.append(f"""
    <li class="news-item">
      <a href="detail-{r:02d}.html" class="news-link">
        <div class="news-head">
          <span class="{rc}">{r}</span>
          <div class="news-title-area">
            <div class="news-title">{esc(a['title'])}</div>
            <div class="news-desc">{esc(a['short'])}</div>
          </div>
          <span class="arrow-icon">→</span>
        </div>
      </a>
    </li>""")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>每日 AI 资讯 TOP10</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                   "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100vh;
      color: #1a1a2e;
      line-height: 1.6;
      padding: 24px 16px;
    }}
    .container {{ max-width: 820px; margin: 0 auto; }}

    .back-link {{
      display: inline-flex; align-items: center; gap: 4px;
      color: #667eea; text-decoration: none; font-size: 0.9rem; font-weight: 500;
      padding: 7px 16px; border-radius: 10px;
      background: rgba(255,255,255,0.5);
      transition: all 0.2s; margin-bottom: 16px;
    }}
    .back-link:hover {{ background: rgba(255,255,255,0.8); transform: translateX(-3px); }}

    .header {{
      text-align: center; padding: 42px 20px 22px;
      background: rgba(255,255,255,0.55);
      backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
      border-radius: 20px; margin-bottom: 28px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    }}
    .header h1 {{
      font-size: 2rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text; letter-spacing: 1px;
    }}
    .header .subtitle {{ margin-top: 8px; font-size: 0.95rem; color: #555; }}
    .header .source-area {{ margin-top: 8px; font-size: 0.82rem; color: #888; }}
    .header .source-area a {{ color: #667eea; text-decoration: none; }}
    .header .source-area a:hover {{ text-decoration: underline; }}
    .date-badge {{
      display: inline-block; margin-top: 12px;
      padding: 5px 20px; border-radius: 20px;
      background: #667eea; color: #fff;
      font-size: 0.85rem; font-weight: 500;
    }}

    .click-hint {{
      text-align: center; font-size: 0.82rem; color: #999;
      margin-bottom: 18px;
    }}

    .news-list {{ list-style: none; }}
    .news-item {{
      background: rgba(255,255,255,0.7);
      backdrop-filter: blur(8px);
      border-radius: 16px; margin-bottom: 14px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.04);
      transition: all 0.25s ease;
      border-left: 4px solid transparent;
      overflow: hidden;
    }}
    .news-item:hover {{
      box-shadow: 0 6px 24px rgba(0,0,0,0.12);
      border-left-color: #667eea;
      transform: translateX(4px);
    }}
    .news-item:active {{ transform: scale(0.98); }}
    .news-link {{
      display: block; padding: 22px 24px;
      text-decoration: none; color: inherit;
    }}
    .news-head {{ display: flex; align-items: flex-start; gap: 8px; }}
    .news-rank {{
      display: inline-flex; align-items: center; justify-content: center;
      width: 34px; height: 34px; border-radius: 10px;
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: #fff; font-weight: 700; font-size: 0.85rem; flex-shrink: 0;
    }}
    .news-rank.top3 {{ width: 38px; height: 38px; font-size: 1rem; }}
    .news-title-area {{ flex: 1; min-width: 0; }}
    .news-title {{ font-size: 1.08rem; font-weight: 600; color: #1a1a2e; line-height: 1.4; }}
    .news-desc {{
      margin-top: 6px; font-size: 0.9rem; color: #666; line-height: 1.6;
    }}
    .arrow-icon {{
      flex-shrink: 0; font-size: 1.3rem; color: #ccc;
      transition: all 0.2s; margin-left: 6px; margin-top: 6px;
    }}
    .news-item:hover .arrow-icon {{ color: #667eea; transform: translateX(4px); }}

    .footer {{
      text-align: center; padding: 28px 16px 10px; font-size: 0.82rem; color: #999;
    }}
    .footer a {{ color: #667eea; text-decoration: none; }}

    @media (max-width: 600px) {{
      body {{ padding: 12px 10px; }}
      .header h1 {{ font-size: 1.5rem; }}
      .news-link {{ padding: 16px; }}
      .news-title {{ font-size: 1rem; }}
    }}
  </style>
</head>
<body>
<div class="container">

  <a class="back-link" href="/">← 返回主站</a>

  <header class="header">
    <h1>🔥 每日 AI 资讯 TOP10</h1>
    <p class="subtitle">精选当日最热门人工智能资讯 · 点击条目阅读完整报道</p>
    <span class="date-badge">{DATE_CN}</span>
  </header>

  <div class="click-hint">💡 点击任意卡片查看完整报道与语音朗读</div>

  <ul class="news-list">
    {''.join(items_html)}
  </ul>

  <div class="footer">
  </div>

</div>

</body>
</html>"""

    path = os.path.join(BASE, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ index.html")

def build_detail(a):
    """详情页 — 含完整文章 + 语音播放"""
    r = a['rank']
    paras = [p.strip() for p in a['full'].strip().split('\n\n') if p.strip()]
    paras_html = '\n'.join(f'      <p>{esc(p)}</p>' for p in paras)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>#{r} {esc(a['title'])} — 每日 AI 资讯</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                   "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100vh;
      color: #1a1a2e;
      padding: 24px 16px;
    }}
    .container {{ max-width: 780px; margin: 0 auto; }}

    /* 导航栏 */
    .nav-bar {{
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 20px; flex-wrap: wrap; gap: 8px;
    }}
    .back-link {{
      display: inline-flex; align-items: center; gap: 4px;
      color: #667eea; text-decoration: none; font-size: 0.9rem; font-weight: 500;
      padding: 7px 16px; border-radius: 10px;
      background: rgba(255,255,255,0.5);
      transition: all 0.2s;
    }}
    .back-link:hover {{ background: rgba(255,255,255,0.8); transform: translateX(-3px); }}
    .rank-badge {{
      display: inline-flex; align-items: center; justify-content: center;
      width: 34px; height: 34px; border-radius: 10px;
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: #fff; font-weight: 700; font-size: 0.85rem;
    }}

    /* 语音控件 */
    .voice-bar {{
      display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
      padding: 16px 22px;
      background: rgba(255,255,255,0.7);
      backdrop-filter: blur(10px);
      border-radius: 14px; margin-bottom: 22px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }}
    .voice-bar .label {{ font-size: 0.85rem; color: #666; font-weight: 500; }}
    .voice-btn {{
      padding: 8px 18px; border: none; border-radius: 10px;
      font-size: 0.85rem; font-weight: 500; cursor: pointer;
      transition: all 0.2s; background: #eef0f7; color: #333;
    }}
    .voice-btn:hover {{ transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
    .voice-btn:active {{ transform: scale(0.96); }}
    .voice-btn.primary {{
      background: linear-gradient(135deg, #667eea, #764ba2); color: #fff;
    }}
    .voice-btn.primary:hover {{ box-shadow: 0 4px 16px rgba(102,126,234,0.4); }}
    .voice-btn.danger {{ background: #ff6b6b; color: #fff; }}
    .voice-btn:disabled {{ opacity: 0.4; cursor: not-allowed; transform: none !important; }}
    .voice-status {{
      font-size: 0.8rem; color: #888; text-align: center; padding: 4px 0 0;
    }}
    .progress-wrap {{
      width: 100%; height: 4px; background: #e0e0e0;
      border-radius: 2px; overflow: hidden;
    }}
    .progress-bar {{
      height: 100%; width: 0%;
      background: linear-gradient(90deg, #667eea, #764ba2);
      border-radius: 2px; transition: width 0.3s linear;
    }}

    /* 文章正文 */
    .article {{
      background: rgba(255,255,255,0.7);
      backdrop-filter: blur(8px);
      border-radius: 20px; padding: 36px 40px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    }}
    .article h1 {{
      font-size: 1.6rem; line-height: 1.4; color: #1a1a2e;
      margin-bottom: 8px;
    }}
    .article .meta {{
      font-size: 0.82rem; color: #999; margin-bottom: 24px;
      padding-bottom: 16px; border-bottom: 1px solid #e8e8e8;
    }}
    .article p {{
      font-size: 1rem; color: #333; line-height: 2;
      margin-bottom: 18px;
      text-indent: 2em;
    }}

    @media (max-width: 600px) {{
      body {{ padding: 12px 10px; }}
      .article {{ padding: 18px 16px; }}
      .article h1 {{ font-size: 1.2rem; }}
      .article p {{ font-size: 0.93rem; text-indent: 1.5em; }}
      .voice-bar {{ flex-direction: column; gap: 6px; }}
      .voice-btn {{ width: 100%; justify-content: center; }}
    }}
  </style>
</head>
<body>
<div class="container">

  <!-- 导航栏 -->
  <div class="nav-bar">
    <a class="back-link" href="/ai-news">← 返回全部资讯</a>
    <span class="rank-badge">#{r}</span>
  </div>

  <!-- 语音控件 -->
  <div class="voice-bar">
    <span class="label">🔊 语音</span>
    <button class="voice-btn primary" id="playBtn">▶ 朗读本文</button>
    <button class="voice-btn" id="pauseBtn">⏸ 暂停</button>
    <button class="voice-btn danger" id="stopBtn">⏹ 停止</button>
    <div class="progress-wrap">
      <div class="progress-bar" id="progressBar"></div>
    </div>
  </div>
  <div class="voice-status" id="voiceStatus">点击「朗读本文」收听全文</div>

  <!-- 正文 -->
  <div class="article">
    <h1>{esc(a['title'])}</h1>
    <div class="meta">{DATE_ISO}</div>
{paras_html}
  </div>

</div>

<script>
(function() {{
  var audio = new Audio();
  audio.src = 'voices/voice_{r:02d}.mp3';
  audio.preload = 'auto';

  var $ = function(id) {{ return document.getElementById(id); }};
  var playBtn = $('playBtn'), pauseBtn = $('pauseBtn'), stopBtn = $('stopBtn');
  var status = $('voiceStatus'), progressBar = $('progressBar');
  var timer = null;

  function setProgress() {{
    if (audio.duration && !isNaN(audio.duration))
      progressBar.style.width = Math.min((audio.currentTime / audio.duration) * 100, 100) + '%';
  }}
  function startTimer() {{ clearTimer(); timer = setInterval(setProgress, 200); }}
  function clearTimer() {{ if (timer) {{ clearInterval(timer); timer = null; }} }}

  audio.onplay = function() {{
    playBtn.textContent = '⏸ 播放中'; startTimer();
    status.textContent = '🔊 正在朗读全文...';
  }};
  audio.onpause = function() {{
    playBtn.textContent = '▶ 继续'; clearTimer();
    status.textContent = '⏸ 已暂停';
  }};
  audio.onended = function() {{
    playBtn.textContent = '▶ 重播'; clearTimer();
    progressBar.style.width = '0%';
    status.textContent = '✅ 播放完成';
  }};
  audio.onerror = function() {{
    playBtn.textContent = '▶ 朗读本文'; status.textContent = '⚠️ 音频加载失败';
    clearTimer(); progressBar.style.width = '0%';
  }};

  playBtn.onclick = function() {{
    if (!audio.paused) {{ audio.pause(); return; }}
    if (audio.ended) audio.currentTime = 0;
    audio.play().catch(function() {{ status.textContent = '⚠️ 请先点击页面激活音频'; }});
  }};
  pauseBtn.onclick = function() {{
    if (audio.paused) audio.play().catch(function(){{}}); else audio.pause();
  }};
  stopBtn.onclick = function() {{
    audio.pause(); audio.currentTime = 0;
    playBtn.textContent = '▶ 朗读本文'; status.textContent = '⏹ 已停止';
    clearTimer(); progressBar.style.width = '0%';
  }};
  document.addEventListener('keydown', function(e) {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.code === 'Space') {{
      e.preventDefault();
      if (audio.paused) audio.play().catch(function(){{}}); else audio.pause();
    }}
  }});
}})();
</script>
</body>
</html>"""

    path = os.path.join(BASE, f'detail-{r:02d}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ detail-{r:02d}.html")

def gen_voice(a):
    """为全文生成语音"""
    r = a['rank']
    mp3 = os.path.join(VOICES_DIR, f'voice_{r:02d}.mp3')
    if os.path.exists(mp3) and os.path.getsize(mp3) > 300000:
        return
    text = f"第{a['rank']}条：{a['title']}。" + a['full'].replace('\n\n', '。')
    cmd = ['edge-tts', '--voice', 'zh-CN-XiaoxiaoNeural', '--rate', '+0%', '--text', text, '--write-media', mp3]
    subprocess.run(cmd, capture_output=True, text=True)

def main():
    if not ARTICLES:
        print("No articles to render. Run generate_news.py first.")
        return

    print("🔊 Generating voice files (full articles)...")
    for a in ARTICLES:
        gen_voice(a)
        print(f"  ✓ voice_{a['rank']:02d}.mp3")

    print("\n📄 Generating index.html...")
    build_index()

    print("📄 Generating 10 detail pages...")
    for a in ARTICLES:
        build_detail(a)

    size = sum(os.path.getsize(os.path.join(BASE, f'detail-{a["rank"]:02d}.html')) for a in ARTICLES)
    print(f"\n✅ Done! {len(ARTICLES)} detail pages + index.html + voices/")
    print(f"   Total size: {size/1024:.0f}KB HTML + voices/")

if __name__ == '__main__':
    main()
