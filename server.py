"""
Knowledge Hub — Backend Server
Flask-based API server for article management
"""

import os
import json
import re
import hashlib
import secrets
from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import jwt

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Prevent caching of static files so updates reflect immediately
@app.after_request
def add_no_cache(response):
    if response.content_type and 'text/html' in response.content_type:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    elif response.content_type and ('javascript' in response.content_type or 'css' in response.content_type):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

# Configuration
SECRET_KEY = os.environ.get('KH_SECRET_KEY', 'knowledge-hub-secret-key-change-in-production')
ARTICLES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'articles')
INDEX_FILE = os.path.join(os.path.dirname(__file__), 'articles_index.json')
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

# Ensure directories exist
os.makedirs(ARTICLES_DIR, exist_ok=True)


# ============ Utility Functions ============

def load_config():
    """Load or create default config"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    config = {
        'admin': {
            'username': 'admin',
            'password_hash': hashlib.sha256('physics2026'.encode()).hexdigest()
        },
        'site': {
            'name': 'Knowledge Hub',
            'subtitle': '物理研究前沿',
            'description': '核物理·核天体物理·超核物理 研究动态'
        }
    }
    save_config(config)
    return config


def save_config(config):
    """Save config to file"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_index():
    """Load or create articles index"""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    index = {'articles': []}
    save_index(index)
    return index


def save_index(index):
    """Save articles index"""
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def parse_front_matter(content):
    """Parse YAML-like front matter from markdown content"""
    meta = {
        'title': '',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'category': '未分类',
        'tags': [],
        'description': ''
    }
    body = content

    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        body = fm_match.group(2)

        for line in fm.split('\n'):
            line = line.strip()
            if line.startswith('title:'):
                val = line.replace('title:', '').strip().strip('"\'')
                meta['title'] = val
            elif line.startswith('date:'):
                val = line.replace('date:', '').strip()
                meta['date'] = val
            elif line.startswith('category:'):
                val = line.replace('category:', '').strip()
                meta['category'] = val
            elif line.startswith('tags:'):
                tags_match = re.match(r'tags:\s*\[(.+)\]', line)
                if tags_match:
                    meta['tags'] = [t.strip().strip('"\'') for t in tags_match.group(1).split(',')]
            elif line.startswith('description:'):
                val = line.replace('description:', '').strip().strip('"\'')
                meta['description'] = val

    return meta, body


def generate_slug(title):
    """Generate URL-friendly slug from title"""
    slug = re.sub(r'[^\w\u4e00-\u9fff-]', '-', title.lower())
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug or f'article-{int(datetime.now().timestamp())}'


def token_required(f):
    """JWT token verification decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': '未提供认证令牌'}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': '令牌已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': '无效令牌'}), 401

        return f(*args, **kwargs)
    return decorated


# ============ Static File Routes ============

@app.route('/')
def index():
    return send_file('index.html')


@app.route('/ai-news')
def ai_news():
    return send_file('daily-ai-news.html')


@app.route('/admin/<path:filename>')
def admin_pages(filename):
    return send_from_directory('admin', filename)


# ============ Public API Routes ============

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Get all published articles (list only)"""
    index = load_index()
    articles = [a for a in index['articles'] if a.get('published', True)]
    articles.sort(key=lambda x: x.get('date', ''), reverse=True)
    return jsonify({'articles': articles})


@app.route('/api/articles/<slug>', methods=['GET'])
def get_article(slug):
    """Get article detail by slug"""
    index = load_index()
    article_meta = None
    for a in index['articles']:
        if a['slug'] == slug:
            article_meta = a
            break

    if not article_meta:
        return jsonify({'error': '文章未找到'}), 404

    # Read markdown content
    filename = article_meta.get('filename', '')
    filepath = os.path.join(ARTICLES_DIR, filename)
    content = ''
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            raw = f.read()
            _, content = parse_front_matter(raw)

    article = {**article_meta, 'content': content}
    return jsonify(article)


@app.route('/api/search', methods=['GET'])
def search_articles():
    """Search articles by keyword"""
    q = request.args.get('q', '').lower()
    category = request.args.get('category', '')

    index = load_index()
    articles = [a for a in index['articles'] if a.get('published', True)]

    if q:
        articles = [a for a in articles if
                    q in a.get('title', '').lower() or
                    q in a.get('description', '').lower() or
                    any(q in t.lower() for t in a.get('tags', []))]

    if category:
        articles = [a for a in articles if a.get('category') == category]

    articles.sort(key=lambda x: x.get('date', ''), reverse=True)
    return jsonify({'articles': articles})


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    index = load_index()
    categories = list(set(a.get('category', '未分类') for a in index['articles']))
    return jsonify({'categories': categories})


# ============ Admin API Routes ============

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login"""
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    config = load_config()
    admin = config['admin']

    if username != admin['username']:
        return jsonify({'error': '用户名或密码错误'}), 401

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if password_hash != admin['password_hash']:
        return jsonify({'error': '用户名或密码错误'}), 401

    token = jwt.encode({
        'username': username,
        'exp': datetime.utcnow().timestamp() + 86400  # 24h
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token, 'username': username})


@app.route('/api/admin/upload', methods=['POST'])
@token_required
def upload_article():
    """Upload markdown article"""
    if 'file' not in request.files:
        return jsonify({'error': '未找到文件'}), 400

    file = request.files['file']
    if not file.filename.endswith('.md'):
        return jsonify({'error': '仅支持 .md 格式文件'}), 400

    content = file.read().decode('utf-8')
    if len(content) > 5 * 1024 * 1024:
        return jsonify({'error': '文件大小超过 5MB 限制'}), 400

    meta, body = parse_front_matter(content)

    # Override with form fields if provided (takes priority over front matter)
    form_title = request.form.get('title', '').strip()
    form_category = request.form.get('category', '').strip()
    form_tags = request.form.get('tags', '').strip()

    if form_title:
        meta['title'] = form_title
    if form_category:
        meta['category'] = form_category
    if form_tags:
        meta['tags'] = [t.strip().strip('"\'') for t in form_tags.split(',') if t.strip()]

    # Auto-infer missing fields
    if not meta['title']:
        name = os.path.splitext(file.filename)[0]
        # Remove date prefix if present
        name = re.sub(r'^\d{4}-\d{2}-\d{2}[-_]?', '', name)
        # Remove plain- prefix and __plain suffix
        name = re.sub(r'^plain-', '', name)
        name = re.sub(r'__plain$', '', name)
        # Remove timestamp prefix like 20260509T085550--
        name = re.sub(r'^\d{8}T\d{6}[-]{1,2}', '', name)
        meta['title'] = name

    slug = generate_slug(meta['title'])
    filename = f"{meta['date']}-{slug}.md"

    # Save markdown file
    filepath = os.path.join(ARTICLES_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Auto-generate description if missing
    if not meta['description']:
        clean_body = re.sub(r'[#*_`\[\]()!]', '', body).strip()
        meta['description'] = clean_body[:200] + '...' if len(clean_body) > 200 else clean_body

    # Update index
    index = load_index()
    article_entry = {
        'id': str(int(datetime.now().timestamp() * 1000)),
        'slug': slug,
        'title': meta['title'],
        'date': meta['date'],
        'category': meta['category'],
        'tags': meta['tags'],
        'description': meta['description'],
        'filename': filename,
        'published': True
    }
    index['articles'].append(article_entry)
    save_index(index)

    return jsonify({'message': '文章上传成功', 'article': article_entry}), 201


@app.route('/api/admin/articles/<slug>', methods=['DELETE'])
@token_required
def delete_article(slug):
    """Delete article by slug"""
    index = load_index()
    article = None
    for i, a in enumerate(index['articles']):
        if a['slug'] == slug:
            article = index['articles'].pop(i)
            break

    if not article:
        return jsonify({'error': '文章未找到'}), 404

    # Remove markdown file
    filename = article.get('filename', '')
    filepath = os.path.join(ARTICLES_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    save_index(index)
    return jsonify({'message': '文章已删除'})


@app.route('/api/admin/articles/<slug>', methods=['PUT'])
@token_required
def update_article(slug):
    """Update article metadata and/or content"""
    data = request.get_json()
    index = load_index()

    for a in index['articles']:
        if a['slug'] == slug:
            if 'title' in data:
                a['title'] = data['title']
            if 'category' in data:
                a['category'] = data['category']
            if 'tags' in data:
                a['tags'] = data['tags']
            if 'description' in data:
                a['description'] = data['description']
            if 'published' in data:
                a['published'] = data['published']
            # If content is provided, rewrite the markdown file
            if 'content' in data:
                filename = a.get('filename', '')
                if filename:
                    filepath = os.path.join(ARTICLES_DIR, filename)
                    # Preserve original front matter, replace body
                    raw = ''
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            raw = f.read()
                    except FileNotFoundError:
                        pass
                    # Check for YAML front matter
                    fm_match = re.match(r'^(---\s*\n.*?\n---\s*\n)(.*)$', raw, re.DOTALL)
                    if fm_match:
                        # Keep existing front matter, replace body
                        new_content = fm_match.group(1) + data['content']
                    else:
                        new_content = data['content']
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            save_index(index)
            return jsonify({'message': '文章已更新', 'article': a})

    return jsonify({'error': '文章未找到'}), 404


@app.route('/api/admin/change-password', methods=['POST'])
@token_required
def change_password():
    """Change admin password"""
    data = request.get_json()
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')

    config = load_config()
    old_hash = hashlib.sha256(old_password.encode()).hexdigest()
    if old_hash != config['admin']['password_hash']:
        return jsonify({'error': '旧密码不正确'}), 400

    config['admin']['password_hash'] = hashlib.sha256(new_password.encode()).hexdigest()
    save_config(config)
    return jsonify({'message': '密码已修改'})


# ============ Run Server ============

if __name__ == '__main__':
    # Initialize default config and sample articles if needed
    load_config()
    load_index()

    print('\n' + '=' * 50)
    print('  Knowledge Hub Server Starting...')
    print('=' * 50)
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    print(f'  URL: http://0.0.0.0:{port}')
    print(f'  Admin: http://0.0.0.0:{port}/admin/login.html')
    print(f'  Default: admin / physics2026')
    print(f'  Debug: {debug}')
    print('=' * 50 + '\n')

    app.run(host='0.0.0.0', port=port, debug=debug)
