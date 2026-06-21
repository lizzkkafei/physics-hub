// Knowledge Hub — Frontend Application

const App = {
  // State
  articles: [],
  currentArticle: null,
  currentPage: 'home',
  searchQuery: '',
  activeCategory: 'all',
  categories: [],
  authToken: localStorage.getItem('ph_token') || null,

  // API Base
  API: '',

  // Initialize
  init() {
    this.bindEvents();
    this.loadArticles();
  },

  // ============ Navigation ============
  bindEvents() {
    // Search input (desktop)
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      let debounce;
      searchInput.addEventListener('input', (e) => {
        clearTimeout(debounce);
        debounce = setTimeout(() => {
          this.searchQuery = e.target.value.trim();
          this.filterAndRender();
        }, 300);
      });
    }

    // Search clear button
    const searchClear = document.getElementById('search-clear');
    if (searchClear) {
      searchClear.addEventListener('click', () => {
        const input = document.getElementById('search-input');
        if (input) {
          input.value = '';
          this.searchQuery = '';
          this.filterAndRender();
          input.focus();
        }
      });
    }

    // Mobile search toggle
    const mobileToggle = document.getElementById('mobile-search-toggle');
    const searchOverlay = document.getElementById('search-overlay');
    const searchOverlayClose = document.getElementById('search-overlay-close');
    const searchInputMobile = document.getElementById('search-input-mobile');

    if (mobileToggle && searchOverlay) {
      mobileToggle.addEventListener('click', () => {
        searchOverlay.classList.add('open');
        setTimeout(() => {
          if (searchInputMobile) searchInputMobile.focus();
        }, 200);
      });
    }
    if (searchOverlayClose && searchOverlay) {
      searchOverlayClose.addEventListener('click', () => {
        searchOverlay.classList.remove('open');
      });
    }
    if (searchInputMobile) {
      let debounce;
      searchInputMobile.addEventListener('input', (e) => {
        clearTimeout(debounce);
        debounce = setTimeout(() => {
          this.searchQuery = e.target.value.trim();
          // Sync desktop search
          const desktopInput = document.getElementById('search-input');
          if (desktopInput) desktopInput.value = e.target.value;
          this.filterAndRender();
        }, 300);
      });
      // Close overlay on Escape
      searchInputMobile.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && searchOverlay) {
          searchOverlay.classList.remove('open');
        }
      });
    }

    // Close mobile search overlay on background click
    if (searchOverlay) {
      searchOverlay.addEventListener('click', (e) => {
        if (e.target === searchOverlay) {
          searchOverlay.classList.remove('open');
        }
      });
    }

    // Category tags
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('hero-tag')) {
        document.querySelectorAll('.hero-tag').forEach(t => t.classList.remove('active'));
        e.target.classList.add('active');
        this.activeCategory = e.target.dataset.category || 'all';
        this.filterAndRender();
      }
    });

    // Admin login form
    document.addEventListener('submit', (e) => {
      if (e.target.id === 'login-form') {
        e.preventDefault();
        this.handleLogin(e.target);
      }
    });

    // File upload
    document.addEventListener('click', (e) => {
      if (e.target.id === 'upload-zone' || e.target.closest('#upload-zone')) {
        const input = document.getElementById('file-input');
        if (input) input.click();
      }
    });

    // Drag and drop
    document.addEventListener('dragover', (e) => {
      e.preventDefault();
      const zone = document.getElementById('upload-zone');
      if (zone) zone.classList.add('dragover');
    });

    document.addEventListener('dragleave', (e) => {
      const zone = document.getElementById('upload-zone');
      if (zone && !zone.contains(e.relatedTarget)) {
        zone.classList.remove('dragover');
      }
    });

    document.addEventListener('drop', (e) => {
      e.preventDefault();
      const zone = document.getElementById('upload-zone');
      if (zone) {
        zone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) this.handleFileUpload(files);
      }
    });

    document.addEventListener('change', (e) => {
      if (e.target.id === 'file-input') {
        if (e.target.files.length > 0) this.handleFileUpload(e.target.files);
      }
    });

    // Back button
    document.addEventListener('click', (e) => {
      if (e.target.closest('.article-detail-back')) {
        this.showPage('home');
      }
    });
  },

  // ============ Data Loading ============
  async loadArticles() {
    try {
      const res = await fetch(`${this.API}/api/articles`);
      if (res.ok) {
        const data = await res.json();
        this.articles = data.articles || [];
      } else {
        this.articles = this.getSampleArticles();
      }
    } catch {
      this.articles = this.getSampleArticles();
    }
    this.extractCategories();
    this.renderHome();
  },

  getSampleArticles() {
    return [
      {
        id: '1',
        slug: 'rp-process-waiting-point-2026',
        title: 'rp-process等候点核⁶⁴Ge、⁶⁸Se、⁷²Kr的质量测量进展',
        date: '2026-05-08',
        category: '核天体物理',
        tags: ['rp-process', '等候点', '质量测量', 'HIAF'],
        description: '本文综述了rp-process中关键等候点核⁶⁴Ge、⁶⁸Se、⁷²Kr的质量测量最新进展，重点讨论了惠州HIAF装置2026年4月完成的首次终端实验结果，以及兰州CSRe Bρ-IMS方法的突破性贡献。',
        content: '## rp-process与等候点核\n\nrp-process（快速质子俘获过程）是X射线暴中重要的核合成路径。该过程的流量受制于若干等候点核——这些核素的质子俘获反应被其β⁺衰变所阻断，从而形成瓶颈。\n\n### 三个关键等候点\n\n| 等候点核 | 质子俘获阈值 | 影响范围 |\n|----------|-------------|----------|\n| ⁶⁴Ge | ⁶⁵As质子分离能极低 | A≈64质量区 |\n| ⁶⁸Se | ⁶⁹Br非束缚 | A≈68质量区 |\n| ⁷²Kr | ⁷³Rb质子分离能不确定 | A≈72质量区 |\n\n### HIAF突破性进展\n\n2026年4月8日，惠州HIAF装置完成首个终端实验，²⁰²Au质量精度达11 keV，创下国际最佳纪录。这一里程碑式的成果标志着中国重离子加速器在精密质量测量领域达到世界领先水平。\n\n### CSRe Bρ-IMS方法\n\n兰州CSRe采用的Bρ-IMS（磁刚度-等时性质谱仪）方法在Nature Physics 2023年发表的Zhou等人的工作中展示了卓越的质量分辨能力，为等候点核的精确质量确定提供了关键数据。\n\n$$S_p(^{65}\\text{As}) = M(^{64}\\text{Ge}) + m_p - M(^{65}\\text{As})$$\n\n上述质子分离能的精确测定直接决定了⁶⁴Ge等候点的突破效率。',
        published: true
      },
      {
        id: '2',
        slug: 'octupole-deformation-2026',
        title: '八极形变与梨形核：从²²⁴Ra到⁸⁰Zr的系统性研究',
        date: '2026-05-06',
        category: '核结构',
        tags: ['八极形变', '梨形核', '反射不对称', 'Parity双带'],
        description: '八极形变导致原子核呈现梨形空间对称性破缺，是核结构物理中反射不对称性的核心体现。本文系统梳理了从重核²²⁴Ra到轻核⁸⁰Zr区域八极形变的实验证据与理论进展。',
        content: '## 八极形变的物理起源\n\n原子核的八极形变（β₃ ≠ 0）导致空间反射对称性破缺，使核呈现"梨形"。这一现象最早在Ra-Th核区的低能谱中通过parity双带结构被识别。\n\n### 实验证据\n\n**重核区（A≈224）**：²²⁴Ra是八极形变的经典案例。其交替自旋宇称带Iπ = 0⁺, 1⁻, 2⁺, 3⁻, ...的低激发能级间隔极小，标志着重反射不对称性。\n\n**中重核区（A≈144-150）**：¹⁴⁴Ba和¹⁴⁸Ce等核素展示了增强的E3跃迁概率，B(E3)值比单粒子估计高出1-2个数量级。\n\n**轻核区（A≈80）**：⁸⁰Zr区域的理论预言和初步实验迹象表明，八极形变可能延伸至更轻的核区。\n\n### 理论框架\n\n相对论平均场（RMF）和Gogny DFT计算均成功再现了Ra-Th核区的八极形变极小值：\n\n$$E(\\beta_2, \\beta_3) = E_0 + \\frac{1}{2}C_2(\\beta_2 - \\beta_2^0)^2 + \\frac{1}{2}C_3(\\beta_3 - \\beta_3^0)^2$$\n\n其中β₃⁰ ≈ 0.15-0.20为Ra-Th核区的典型八极形变参量。',
        published: true
      },
      {
        id: '3',
        slug: 'hypernuclear-physics-kaon-2026',
        title: '超核物理与K介子核相互作用：从J-PARC到HIAF',
        date: '2026-05-03',
        category: '超核物理',
        tags: ['超核', 'K介子', '奇异物质', 'J-PARC'],
        description: '超核物理探索包含奇异夸克的重子系统，是连接核物理与粒子物理的桥梁。本文综述了Λ超核谱学、K⁻核相互作用势以及J-PARC和HIAF在奇异物质研究中的最新进展。',
        content: '## 超核物理的核心问题\n\n超核（Hypernucleus）是包含至少一个超子（Λ, Σ, Ξ等）的束缚核系统。研究超核的核心物理目标是理解超子-核子（YN）和超子-超子（YY）相互作用。\n\n### Λ超核谱学\n\n高分辨率γ射线谱学是研究Λ超核结构的黄金手段。J-PARC E13实验通过(K⁻, π⁻)反应产生了⁴_ΛHe和⁷_ΛLi，并利用Hyperball-J探测器测量了其γ射线能级：\n\n- ⁴_ΛHe的1⁺激发态能量：1.15 MeV\n- ⁷_ΛLi的自旋-轨道劈裂：ΔE_ls ≈ 50 keV\n\n### K⁻核相互作用\n\nK⁻核相互作用势的深度是长期争议的核心问题。FINUDA、AmaDEUS和J-PARC E62实验给出了不同的约束：\n\n| 实验 | 方法 | V_K⁻ 深度 |\n|------|------|----------|\n| FINUDA | K⁻原子位移 | ≈ -200 MeV |\n| AmaDEUS | K⁻⁴He吸收 | ≈ -50 MeV |\n| J-PARC E62 | K⁻³He发射 | 待发表 |\n\n### HIAF前瞻\n\n惠州HIAF即将开展的超核实验将利用高强度K⁻束流，系统测量中重超核的γ谱，有望为K⁻核势提供决定性约束。',
        published: true
      },
      {
        id: '4',
        slug: 's-process-intermediate-mass-stars-2026',
        title: '中等质量恒星中的s-process与i-process核合成',
        date: '2026-04-28',
        category: '核天体物理',
        tags: ['s-process', 'i-process', '中等质量恒星', '核合成'],
        description: '中等质量恒星（4-8 M☉）是银河系s-process的重要贡献者。近年来，i-process（中等中子密度过程）的发现重新定义了我们对非标准核合成路径的理解。本文讨论了这两类过程的核物理输入与天文观测约束。',
        content: '## s-process在中等质量恒星中的角色\n\n中等质量恒星（IMS，4-8 M☉）的热脉冲AGB阶段是s-process（慢中子俘获过程）的重要发生场所。与低质量AGB星不同，IMS中²²Ne(α,n)²⁵Mg反应是主要中子源。\n\n### ²²Ne中子源\n\n在IMS的TP-AGB阶段，第三次挖掘（3rd dredge-up）将s-process产物带入恒星包层：\n\n$$^{22}\\text{Ne}(\\alpha, n)^{25}\\text{Mg} \\quad T \\gtrsim 3 \\times 10^8 \\text{ K}$$\n\n该反应率的不确定性仍是s-process产量预测的主要误差来源。\n\n### i-process的发现\n\ni-process（intermediate process）的中子密度介于s-process和r-process之间（nn ≈ 10¹⁰-10¹⁵ cm⁻³），最初在CFB(pos)星和富锂碳星中被识别。其特征是：\n\n- 部分跨越s-process和r-process的核素区域\n- 对不稳定核素的截面不确定度极高\n- 可能与H-ingestion事件相关\n\n### 关键核物理输入\n\n| 核反应 | 作用 | 当前不确定度 |\n|--------|------|-------------|\n| ²²Ne(α,n)²⁵Mg | s-process中子源 | 2-3倍 |\n| ¹³C(α,n)¹⁶O | s-process中子源(i-process中次要) | 1.5倍 |\n| 各不稳定核(n,γ)截面 | i-process路径 | 可达10倍 |',
        published: true
      },
      {
        id: '5',
        slug: 'deep-sub-coulomb-transfer-2026',
        title: '深度亚库伦转移反应与对关联的探针',
        date: '2026-04-22',
        category: '核反应',
        tags: ['亚库伦转移', '对关联', '核子对转移', 'Fermi尺度'],
        description: '深度亚库伦转移反应发生在远低于库伦势垒的能量区域，对核结构中的对关联极为灵敏。本文综述了单核子转移与双核子转移在提取对关联信息方面的理论框架与实验进展。',
        content: '## 深度亚库伦转移的物理内涵\n\n深度亚库伦转移反应（Deep Sub-Coulomb Transfer, DSCT）是指入射能量远低于库伦势垒的核子转移反应。由于在该能量下核力仅作为微扰，转移截面直接反映了核表层区的单粒子和对关联结构。\n\n### 对关联探针\n\n双核子转移反应，特别是(t,p)和(p,t)反应，是研究对关联的传统工具：\n\n$$\\sigma_{(t,p)} \\propto |\\langle \\text{final}| \\sum_{k_1 k_2} P_{k_1 k_2}^\\dagger |\\text{initial}\\rangle|^2$$\n\n其中$P^\\dagger$为对产生算符。在深度亚库伦条件下，反应振幅与BCS对隙Δ直接相关。\n\n### 实验挑战\n\nDSCT的典型截面极小（μb至nb量级），对探测器灵敏度和束流强度提出极高要求：\n\n- 需要高流强束流（> 10 pnA）\n- 探测器需在强弹性散射背景下提取弱信号\n- 逆向运动学几何有助于提高探测效率\n\n### 近期进展\n\nFRIB和HIAF的高流强束流为DSCT实验开辟了新的可能性，特别是对丰中子核的对关联研究。',
        published: true
      }
    ];
  },

  extractCategories() {
    const cats = new Set();
    this.articles.forEach(a => {
      if (a.category) cats.add(a.category);
    });
    this.categories = ['all', ...Array.from(cats)];
  },

  // ============ Filtering ============
  filterAndRender() {
    let filtered = [...this.articles];

    // Category filter
    if (this.activeCategory !== 'all') {
      filtered = filtered.filter(a => a.category === this.activeCategory);
    }

    // Search filter
    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      filtered = filtered.filter(a =>
        a.title.toLowerCase().includes(q) ||
        a.description.toLowerCase().includes(q) ||
        (a.tags && a.tags.some(t => t.toLowerCase().includes(q)))
      );
    }

    // Sort by date descending
    filtered.sort((a, b) => new Date(b.date) - new Date(a.date));

    // Update article count
    const countEl = document.getElementById('article-count');
    if (countEl) {
      countEl.textContent = `${filtered.length} 篇`;
    }

    this.renderArticleList(filtered);
  },

  // ============ Rendering ============
  renderHome() {
    this.renderCategoryTags();
    this.filterAndRender();
  },

  renderCategoryTags() {
    const container = document.getElementById('category-tags');
    if (!container) return;
    const catLabels = { all: '全部' };
    container.innerHTML = this.categories.map(c => `
      <button class="hero-tag ${c === this.activeCategory ? 'active' : ''}" data-category="${c}" role="tab" ${c === this.activeCategory ? 'aria-selected="true"' : ''}>
        ${catLabels[c] || c}
      </button>
    `).join('');
  },

  renderArticleList(articles) {
    const container = document.getElementById('article-list');
    if (!container) return;

    if (articles.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="22" cy="22" r="14" opacity="0.3"/>
              <path d="M32 32L42 42" stroke-linecap="round" opacity="0.3"/>
              <path d="M16 22h12M22 16v12" opacity="0.5"/>
            </svg>
          </div>
          <h3>暂无文章</h3>
          <p>还没有相关的研究文章，请稍后再来查看</p>
        </div>`;
      return;
    }

    container.innerHTML = articles.map(a => {
      const desc = a.description && a.description !== a.title ? a.description : '';
      return `
      <div class="timeline-item">
        <article class="article-card" onclick="App.showArticle('${a.slug}')">
          <div class="article-meta">
            <span class="article-date">
              <svg width="13" height="13" viewBox="0 0 13 13" fill="none" stroke="currentColor" stroke-width="1.2" style="margin-right:2px">
                <rect x="1.5" y="2.5" width="10" height="9" rx="1.5"/>
                <path d="M1.5 5.5h10M4.5 1v3M8.5 1v3"/>
              </svg>
              ${this.formatDate(a.date)}
            </span>
            <span class="article-category">${a.category || '未分类'}</span>
          </div>
          <h2 class="article-title">
            <a href="#/article/${a.slug}" onclick="event.stopPropagation(); App.showArticle('${a.slug}')">${a.title}</a>
          </h2>
          ${desc ? `<p class="article-desc">${desc}</p>` : ''}
          ${a.tags && a.tags.length ? `
            <div class="article-tags">
              ${a.tags.map(t => `<span class="article-tag">${t}</span>`).join('')}
            </div>` : ''}
        </article>
      </div>`;
    }).join('');
  },

  renderArticleDetail(article) {
    const main = document.getElementById('main-content');
    if (!main) return;

    // Parse markdown content, stripping duplicate title and Org front matter
    let content = article.content || '';
    if (content) {
      // Strip Org-mode front matter (#+title:, #+date:, etc.) at the start
      content = content.replace(/^(#\+[^\n]*\n)+/, '');
      // Strip leading H1 heading that duplicates the display title
      content = content.replace(/^#\s+.*(\n{1,2})/, (match, newlines) => newlines);
    }
    let htmlContent = '';
    if (typeof marked !== 'undefined' && content) {
      htmlContent = marked.parse(content);
    } else if (content) {
      htmlContent = content.replace(/\n/g, '<br>');
    }

    main.innerHTML = `
      <div class="article-detail">
        <a class="article-detail-back" onclick="App.showPage('home')">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 3L5 7l4 4"/>
          </svg>
          返回文章列表
        </a>
        <div class="article-detail-header">
          <h1 class="article-detail-title">${article.title}</h1>
          <div class="article-detail-meta">
            <span>
              <svg width="14" height="14" viewBox="0 0 13 13" fill="none" stroke="currentColor" stroke-width="1.2" style="margin-right:4px;vertical-align:-2px">
                <rect x="1.5" y="2.5" width="10" height="9" rx="1.5"/>
                <path d="M1.5 5.5h10M4.5 1v3M8.5 1v3"/>
              </svg>
              ${this.formatDate(article.date)}
            </span>
            <span class="article-category">${article.category || '未分类'}</span>
            ${article.tags ? article.tags.map(t => `<span class="article-tag">${t}</span>`).join('') : ''}
          </div>
        </div>
        <div class="md-content">
          ${htmlContent}
        </div>
        <div class="article-nav">
          <div></div>
          <a class="article-detail-back" onclick="App.showPage('home')">
            返回列表
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 3l4 4-4 4"/>
            </svg>
          </a>
        </div>
      </div>`;

    // Render KaTeX if available
    if (typeof renderMathInElement !== 'undefined') {
      renderMathInElement(document.querySelector('.md-content'), {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false }
        ]
      });
    }
  },

  // ============ Page Navigation ============
  showArticle(slug) {
    const article = this.articles.find(a => a.slug === slug);
    if (!article) return;
    this.currentArticle = article;

    // Check if we're on admin page - redirect to main site for preview
    const adminContent = document.getElementById('admin-content');
    if (adminContent) {
      window.open(`/#/article/${slug}`, '_blank');
      return;
    }

    // If article has no content loaded, fetch from API
    if (!article.content) {
      this.fetchAndShowArticle(slug);
      return;
    }

    this.renderArticleDetail(article);
    window.scrollTo(0, 0);
    history.pushState({ page: 'article', slug }, '', `#/article/${slug}`);
  },

  async fetchAndShowArticle(slug) {
    try {
      const res = await fetch(`${this.API}/api/articles/${slug}`);
      if (res.ok) {
        const article = await res.json();
        this.currentArticle = article;
        this.renderArticleDetail(article);
        window.scrollTo(0, 0);
        history.pushState({ page: 'article', slug }, '', `#/article/${slug}`);
        return;
      }
    } catch {}
    // Fallback: show article with metadata only
    const article = this.articles.find(a => a.slug === slug);
    if (article) {
      article.content = article.description || '文章内容加载失败';
      this.renderArticleDetail(article);
      window.scrollTo(0, 0);
      history.pushState({ page: 'article', slug }, '', `#/article/${slug}`);
    }
  },

  showPage(page) {
    const main = document.getElementById('main-content');
    if (!main) return;

    if (page === 'home') {
      this.currentArticle = null;
      main.innerHTML = `
        <div class="section-header">
          <h2 class="section-title">
            <svg class="section-title-icon" width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <circle cx="10" cy="10" r="3" fill="#00D4AA"/>
              <circle cx="10" cy="10" r="7" stroke="#00D4AA" stroke-width="1.5" opacity="0.4"/>
            </svg>
            研究动态
            <span class="article-count" id="article-count"></span>
          </h2>
        </div>
        <div class="timeline" id="article-list"></div>`;
      this.renderHome();
      history.pushState({ page: 'home' }, '', '#/');
    }
  },

  // ============ Admin ============
  async handleLogin(form) {
    const username = form.querySelector('[name="username"]').value;
    const password = form.querySelector('[name="password"]').value;
    const errorEl = document.getElementById('login-error');

    try {
      const res = await fetch(`${this.API}/api/admin/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (res.ok) {
        const data = await res.json();
        this.authToken = data.token;
        localStorage.setItem('ph_token', data.token);
        window.location.href = '/admin/dashboard.html';
      } else {
        if (errorEl) {
          errorEl.textContent = '用户名或密码错误';
          errorEl.style.display = 'block';
        }
      }
    } catch {
      // Demo mode
      if (username === 'admin' && password === 'physics2026') {
        this.authToken = 'demo-token';
        localStorage.setItem('ph_token', 'demo-token');
        this.renderAdminDashboard();
      } else if (errorEl) {
        errorEl.textContent = '用户名或密码错误';
        errorEl.style.display = 'block';
      }
    }
  },

  async handleFileUpload(files) {
    const file = files[0];
    if (!file) return;
    if (!file.name.endsWith('.md')) {
      this.showToast('请上传 .md 格式的文件', 'error');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      this.showToast('文件大小不能超过 5MB', 'error');
      return;
    }

    // Read file
    const readFile = () => new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = reject;
      reader.readAsText(file);
    });
    const rawContent = await readFile();

    // Parse metadata from content/filename
    const parsed = this.parseMarkdown(rawContent, file.name);

    // Store for later upload
    this.uploadFileData = {
      fileName: file.name,
      rawContent,
      title: parsed.title,
      category: parsed.category,
      tags: parsed.tags,
      description: parsed.description
    };

    this.showUploadPreview();
  },

  showUploadPreview() {
    const content = document.getElementById('admin-content');
    if (!content || !this.uploadFileData) return;

    const d = this.uploadFileData;
    const tagsStr = d.tags ? d.tags.join(', ') : '';
    const catOptions = this.categories.filter(c => c !== 'all').map(c => `<option value="${c}">`).join('');

    content.innerHTML = `
      <div style="max-width:1000px">
        <div class="admin-header">
          <h2>上传文章</h2>
          <span style="font-size:13px;color:var(--text-muted);background:var(--card);padding:4px 12px;border-radius:999px;border:1px solid var(--border);">${d.fileName}</span>
        </div>

        <div class="edit-meta">
          <div class="form-group">
            <label>文章标题</label>
            <input type="text" id="upload-title" value="${this.escapeHtml(d.title)}" placeholder="文章标题">
          </div>
          <div class="form-group">
            <label>文章类别</label>
            <input type="text" id="upload-category" value="${this.escapeHtml(d.category)}" list="upload-cat-suggestions">
            <datalist id="upload-cat-suggestions">${catOptions}</datalist>
          </div>
          <div class="form-group" style="grid-column: 1 / -1;">
            <label>标签（逗号分隔）</label>
            <input type="text" id="upload-tags" value="${this.escapeHtml(tagsStr)}" placeholder="如：rp-process, 质量测量, HIAF">
          </div>
        </div>

        <div class="form-group">
          <label>Markdown 内容 <span style="font-weight:400;color:var(--text-dim);font-size:12px;">（可编辑）</span></label>
          <textarea id="upload-content" spellcheck="false">${this.escapeHtml(d.rawContent)}</textarea>
        </div>

        <div style="display:flex;gap:12px;align-items:center;margin-bottom:24px;">
          <button class="btn btn-primary" onclick="App.confirmUpload()">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:4px">
              <path d="M2 7l3.5 3.5L12 3"/>
            </svg>
            确认上传
          </button>
          <button class="btn btn-ghost" id="upload-preview-toggle" onclick="App.toggleUploadPreview()">预览</button>
          <button class="btn btn-ghost" onclick="App.showAdminTab('upload')">取消</button>
          <span id="upload-status" style="font-size:13px;color:var(--text-dim);"></span>
        </div>

        <div id="upload-preview" class="md-content" style="display:none;padding:24px;background:var(--bg-elevated);border:1px solid var(--border);border-radius:var(--radius);margin-top:8px;"></div>
      </div>`;
  },

  toggleUploadPreview() {
    const preview = document.getElementById('upload-preview');
    const btn = document.getElementById('upload-preview-toggle');
    if (!preview) return;

    if (preview.style.display === 'none' || !preview.style.display) {
      const textarea = document.getElementById('upload-content');
      const raw = textarea ? textarea.value : '';
      let html = '';
      if (typeof marked !== 'undefined') {
        html = marked.parse(raw);
      } else {
        html = raw.replace(/\n/g, '<br>');
      }
      preview.innerHTML = html;
      preview.style.display = 'block';
      if (btn) btn.textContent = '收起预览';
      if (typeof renderMathInElement !== 'undefined') {
        renderMathInElement(preview, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false }
          ]
        });
      }
    } else {
      preview.style.display = 'none';
      if (btn) btn.textContent = '预览';
    }
  },

  async confirmUpload() {
    const title = document.getElementById('upload-title')?.value.trim();
    const category = document.getElementById('upload-category')?.value.trim();
    const tagsStr = document.getElementById('upload-tags')?.value.trim();
    const content = document.getElementById('upload-content')?.value;

    if (!title || !content) {
      this.showToast('标题和内容不能为空', 'error');
      return;
    }

    const tags = tagsStr ? tagsStr.split(',').map(t => t.trim()).filter(t => t) : [];
    const fileName = this.uploadFileData?.fileName || 'article.md';

    // Inject front matter into content for upload
    const finalContent = this.injectFrontMatter(content, { title, category, tags });
    const modifiedFile = new File([finalContent], fileName, { type: 'text/markdown' });

    const formData = new FormData();
    formData.append('file', modifiedFile);

    const statusEl = document.getElementById('upload-status');
    if (statusEl) statusEl.textContent = '上传中...';

    try {
      const res = await fetch(`${this.API}/api/admin/upload`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${this.authToken}` },
        body: formData
      });

      if (res.ok) {
        this.showToast('文章上传成功！', 'success');
        this.uploadFileData = null;
        this.loadArticles();
      } else {
        const err = await res.json().catch(() => ({}));
        this.showToast(err.error || '上传失败，请重试', 'error');
        if (statusEl) statusEl.textContent = '上传失败';
      }
    } catch {
      // Fallback: add locally
      const article = {
        id: Date.now().toString(),
        slug: title.toLowerCase().replace(/[^a-z0-9一-鿿]+/g, '-').replace(/^-|-$/g, '') || 'article-' + Date.now(),
        title,
        date: new Date().toISOString().split('T')[0],
        category: category || '未分类',
        tags,
        description: content.replace(/[#*_`\[\]()!]/g, '').trim().substring(0, 200) + '...',
        content,
        published: true
      };
      this.articles.unshift(article);
      this.uploadFileData = null;
      this.showToast('文章上传成功！（本地预览模式）', 'success');
      this.showAdminTab('articles');
    }
  },

  injectFrontMatter(content, meta) {
    const fmMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
    if (fmMatch) {
      let fm = fmMatch[1];
      let body = fmMatch[2];
      if (meta.title) {
        if (fm.match(/^title:/m)) {
          fm = fm.replace(/^title:.*$/m, `title: "${meta.title}"`);
        } else {
          fm = `title: "${meta.title}"\n` + fm;
        }
      }
      if (meta.category) {
        if (fm.match(/^category:/m)) {
          fm = fm.replace(/^category:.*$/m, `category: ${meta.category}`);
        } else {
          fm = `category: ${meta.category}\n` + fm;
        }
      }
      if (meta.tags && meta.tags.length) {
        const tagsStr = meta.tags.map(t => `"${t}"`).join(', ');
        if (fm.match(/^tags:/m)) {
          fm = fm.replace(/^tags:.*$/m, `tags: [${tagsStr}]`);
        } else {
          fm = `tags: [${tagsStr}]\n` + fm;
        }
      }
      return `---\n${fm}\n---\n${body}`;
    } else {
      let fm = '---\n';
      if (meta.title) fm += `title: "${meta.title}"\n`;
      if (meta.category) fm += `category: ${meta.category}\n`;
      if (meta.tags && meta.tags.length) {
        const tagsStr = meta.tags.map(t => `"${t}"`).join(', ');
        fm += `tags: [${tagsStr}]\n`;
      }
      fm += `date: ${new Date().toISOString().split('T')[0]}\n`;
      fm += '---\n';
      return fm + content;
    }
  },

  parseMarkdown(content, filename) {
    let title = filename.replace('.md', '');
    let date = new Date().toISOString().split('T')[0];
    let category = '未分类';
    let tags = [];
    let description = '';
    let bodyContent = content;

    const fmMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
    if (fmMatch) {
      const fm = fmMatch[1];
      bodyContent = fmMatch[2];
      const titleMatch = fm.match(/title:\s*["']?(.+?)["']?\s*$/m);
      if (titleMatch) title = titleMatch[1];
      const dateMatch = fm.match(/date:\s*(.+)\s*$/m);
      if (dateMatch) date = dateMatch[1];
      const catMatch = fm.match(/category:\s*(.+)\s*$/m);
      if (catMatch) category = catMatch[1];
      const tagsMatch = fm.match(/tags:\s*\[(.+)\]\s*$/m);
      if (tagsMatch) tags = tagsMatch[1].split(',').map(t => t.trim().replace(/["']/g, ''));
      const descMatch = fm.match(/description:\s*["'](.+?)["']\s*$/m);
      if (descMatch) description = descMatch[1];
    }

    if (!description) {
      description = bodyContent.replace(/[#*_`\[\]()!]/g, '').trim().substring(0, 200) + '...';
    }

    const slug = title.toLowerCase().replace(/[^a-z0-9一-鿿]+/g, '-').replace(/^-|-$/g, '');

    return {
      id: Date.now().toString(),
      slug: slug || 'article-' + Date.now(),
      title,
      date,
      category,
      tags,
      description,
      content: bodyContent,
      published: true
    };
  },

  renderAdminDashboard() {
    document.getElementById('app').innerHTML = `
      <nav class="navbar">
        <div class="navbar-inner">
          <a class="navbar-brand" href="#/">
            <svg class="brand-icon" width="28" height="28" viewBox="0 0 28 28" fill="none" aria-hidden="true">
              <circle cx="14" cy="14" r="13" stroke="url(#brand-grad)" stroke-width="1.5" opacity="0.3"/>
              <ellipse cx="14" cy="14" rx="7" ry="13" stroke="url(#brand-grad)" stroke-width="1.2" opacity="0.7" transform="rotate(30 14 14)"/>
              <ellipse cx="14" cy="14" rx="7" ry="13" stroke="url(#brand-grad)" stroke-width="1.2" opacity="0.7" transform="rotate(-30 14 14)"/>
              <circle cx="14" cy="14" r="2" fill="#00D4AA"/>
              <defs>
                <linearGradient id="brand-grad2" x1="0" y1="0" x2="28" y2="28">
                  <stop stop-color="#00D4AA"/>
                  <stop offset="1" stop-color="#6366F1"/>
                </linearGradient>
              </defs>
            </svg>
            Knowledge Hub
          </a>
          <div class="navbar-actions">
            <a href="/" class="btn btn-ghost btn-nav">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.3">
                <path d="M2 7h10M6 3l-4 4 4 4"/>
              </svg>
              <span>返回首页</span>
            </a>
            <button class="btn btn-ghost btn-sm" onclick="App.logout()">退出登录</button>
          </div>
        </div>
      </nav>
      <div class="admin-layout">
        <aside class="admin-sidebar">
          <div class="sidebar-section">
            <div class="sidebar-section-title">管理</div>
            <div class="sidebar-item active" onclick="App.showAdminTab('articles')">
              <span class="item-icon">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3">
                  <path d="M3 2h10a1 1 0 011 1v10a1 1 0 01-1 1H3a1 1 0 01-1-1V3a1 1 0 011-1z"/>
                  <path d="M6 5h4M6 8h4M6 11h2"/>
                </svg>
              </span> 文章管理
            </div>
            <div class="sidebar-item" onclick="App.showAdminTab('upload')">
              <span class="item-icon">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3">
                  <path d="M8 2v10M3 7l5-5 5 5M2 12v2h12v-2"/>
                </svg>
              </span> 上传文章
            </div>
            <div class="sidebar-item" onclick="App.showAdminTab('settings')">
              <span class="item-icon">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3">
                  <circle cx="8" cy="8" r="2.5"/>
                  <path d="M8 1v2M8 13v2M1 8h2M13 8h2M3.05 3.05l1.41 1.41M11.54 11.54l1.41 1.41M3.05 12.95l1.41-1.41M11.54 4.46l1.41-1.41"/>
                </svg>
              </span> 系统设置
            </div>
            <div class="sidebar-item" onclick="window.open('/finagent/', '_blank')">
              <span class="item-icon">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3">
                  <rect x="2" y="3" width="12" height="10" rx="1.5"/>
                  <path d="M5 7l2 2 4-4"/>
                </svg>
              </span> 至真AI股票分析
            </div>
          </div>
        </aside>
        <main class="admin-content" id="admin-content">
        </main>
      </div>`;
    this.showAdminTab('articles');
  },

  showAdminTab(tab) {
    const content = document.getElementById('admin-content');
    if (!content) return;

    document.querySelectorAll('.sidebar-item').forEach(item => item.classList.remove('active'));
    const items = document.querySelectorAll('.sidebar-item');
    if (tab === 'edit') {
      // Keep articles tab active when editing
      if (items[0]) items[0].classList.add('active');
      this.renderEditView();
      return;
    }
    if (tab === 'articles' && items[0]) items[0].classList.add('active');
    if (tab === 'upload' && items[1]) items[1].classList.add('active');
    if (tab === 'settings' && items[2]) items[2].classList.add('active');

    if (tab === 'articles') {
      content.innerHTML = `
        <div class="admin-header">
          <h2>文章管理</h2>
          <button class="btn btn-primary" onclick="App.showAdminTab('upload')">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:2px">
              <path d="M7 2v10M2 7h10"/>
            </svg>
            上传新文章
          </button>
        </div>
        <div class="admin-article-list">
          ${this.articles.map(a => `
            <div class="admin-article-item">
              <div class="admin-article-info">
                <h4>${a.title}</h4>
                <span>${this.formatDate(a.date)} · ${a.category}</span>
              </div>
              <div class="admin-article-actions">
                <button class="btn btn-sm btn-secondary" onclick="App.editArticle('${a.slug}')">编辑</button>
                <button class="btn btn-sm btn-danger" onclick="App.deleteArticle('${a.slug}')">删除</button>
              </div>
            </div>
          `).join('')}
        </div>`;
    } else if (tab === 'upload') {
      content.innerHTML = `
        <div class="admin-header">
          <h2>上传文章</h2>
        </div>
        <div class="upload-zone" id="upload-zone">
          <div class="upload-icon">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5">
              <path d="M24 14v20M14 24l10-10 10 10M10 36h28" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h3>拖拽 Markdown 文件到此处</h3>
          <p>或点击选择文件上传</p>
          <div class="upload-hint">支持 .md 格式，最大 5MB</div>
          <div class="upload-hint" style="margin-top:8px; background: var(--primary-dim); color: var(--primary);">选择文件后可预览和编辑内容，确认后才上传</div>
        </div>
        <input type="file" id="file-input" accept=".md" style="display:none">`;
    } else if (tab === 'settings') {
      content.innerHTML = `
        <div class="admin-header">
          <h2>系统设置</h2>
        </div>
        <div style="max-width: 500px;">
          <div class="form-group">
            <label>站点名称</label>
            <input type="text" id="settings-site-name" value="Knowledge Hub" placeholder="站点名称">
          </div>
          <div class="form-group">
            <label>站点副标题</label>
            <input type="text" id="settings-subtitle" value="物理研究前沿" placeholder="站点副标题">
          </div>
          <div class="form-group">
            <label>管理员用户名</label>
            <input type="text" id="settings-username" value="admin" placeholder="用户名" disabled style="opacity:0.5">
          </div>
          <hr style="border:none;border-top:1px solid var(--border);margin:24px 0;">
          <div class="form-group">
            <label>旧密码</label>
            <input type="password" id="settings-old-password" placeholder="输入旧密码">
          </div>
          <div class="form-group">
            <label>新密码</label>
            <input type="password" id="settings-new-password" placeholder="留空则不修改">
          </div>
          <div style="display:flex;gap:12px;align-items:center;">
            <button class="btn btn-primary" onclick="App.saveSettings()">保存设置</button>
            <span id="settings-status" style="font-size:13px;color:var(--text-dim);"></span>
          </div>
        </div>`;
    }
  },

  async deleteArticle(slug) {
    if (!confirm('确定要删除这篇文章吗？')) return;

    try {
      const res = await fetch(`${this.API}/api/admin/articles/${slug}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${this.authToken}`}
      });
      if (res.ok) {
        this.showToast('文章已删除', 'success');
        this.articles = this.articles.filter(a => a.slug !== slug);
        this.showAdminTab('articles');
      } else {
        const data = await res.json().catch(() => ({}));
        this.showToast(data.error || '删除失败', 'error');
      }
    } catch {
      this.articles = this.articles.filter(a => a.slug !== slug);
      this.showToast('文章已删除（本地）', 'success');
      this.showAdminTab('articles');
    }
  },

  // ============ Article Edit ============
  async editArticle(slug) {
    const article = this.articles.find(a => a.slug === slug);
    if (!article) return;

    // Fetch full content if not already loaded
    if (!article.content) {
      try {
        const res = await fetch(`${this.API}/api/articles/${slug}`);
        if (res.ok) {
          const data = await res.json();
          article.content = data.content || '';
        }
      } catch { /* use fallback */ }
    }

    if (!article.content) {
      article.content = article.description || '';
    }

    this.editingArticle = article;
    this.showAdminTab('edit');
  },

  renderEditView() {
    const content = document.getElementById('admin-content');
    if (!content || !this.editingArticle) return;

    const a = this.editingArticle;
    const tagsStr = a.tags ? a.tags.join(', ') : '';

    content.innerHTML = `
      <div style="max-width:1000px">
        <div class="admin-header">
          <h2>编辑文章</h2>
          <button class="btn btn-ghost" onclick="App.showAdminTab('articles')">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.3" style="margin-right:4px;vertical-align:-2px">
              <path d="M9 3L5 7l4 4"/>
            </svg>
            返回文章列表
          </button>
        </div>

        <div class="edit-meta" style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-bottom:20px;">
          <div class="form-group">
            <label>文章标题</label>
            <input type="text" id="edit-title" value="${this.escapeHtml(a.title)}">
          </div>
          <div class="form-group">
            <label>文章类别</label>
            <input type="text" id="edit-category" value="${this.escapeHtml(a.category || '')}" list="category-suggestions">
            <datalist id="category-suggestions">
              ${this.categories.filter(c => c !== 'all').map(c => `<option value="${c}">`).join('')}
              <option value="核天体物理">
              <option value="核结构">
              <option value="超核物理">
              <option value="核反应">
              <option value="核谱学">
              <option value="核合成">
            </datalist>
          </div>
          <div class="form-group" style="grid-column: 1 / -1;">
            <label>标签（逗号分隔）</label>
            <input type="text" id="edit-tags" value="${this.escapeHtml(tagsStr)}">
          </div>
        </div>

        <div class="form-group">
          <label>Markdown 内容</label>
          <textarea id="edit-content" spellcheck="false" style="width:100%; min-height:400px; padding:16px; background:var(--bg); border:1px solid var(--border); border-radius:var(--radius-sm); color:var(--text); font-family:'JetBrains Mono','Fira Code',monospace; font-size:14px; line-height:1.6; resize:vertical; outline:none;">${this.escapeHtml(a.content || '')}</textarea>
        </div>

        <div style="display:flex; gap:12px; align-items:center; margin-bottom:24px;">
          <button class="btn btn-primary" onclick="App.saveArticleEdit()">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:4px">
              <path d="M2 7l3.5 3.5L12 3"/>
            </svg>
            保存修改
          </button>
          <button class="btn btn-ghost" id="preview-toggle" onclick="App.toggleEditPreview()">预览</button>
          <button class="btn btn-ghost" onclick="App.showAdminTab('articles')">取消</button>
          <span id="edit-status" style="font-size:13px; color:var(--text-dim);"></span>
        </div>

        <div id="edit-preview" class="md-content" style="display:none; padding:24px; background:var(--bg-elevated); border:1px solid var(--border); border-radius:var(--radius); margin-top:8px;"></div>
      </div>`;
  },

  toggleEditPreview() {
    const preview = document.getElementById('edit-preview');
    const btn = document.getElementById('preview-toggle');
    if (!preview) return;

    if (preview.style.display === 'none' || !preview.style.display) {
      const textarea = document.getElementById('edit-content');
      const raw = textarea ? textarea.value : '';
      let html = '';
      if (typeof marked !== 'undefined') {
        html = marked.parse(raw);
      } else {
        html = raw.replace(/\n/g, '<br>');
      }
      preview.innerHTML = html;
      preview.style.display = 'block';
      if (btn) btn.textContent = '收起预览';
      if (typeof renderMathInElement !== 'undefined') {
        renderMathInElement(preview, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false }
          ]
        });
      }
    } else {
      preview.style.display = 'none';
      if (btn) btn.textContent = '预览';
    }
  },

  async saveArticleEdit() {
    const a = this.editingArticle;
    if (!a) return;

    const title = document.getElementById('edit-title')?.value.trim();
    const category = document.getElementById('edit-category')?.value.trim();
    const tagsStr = document.getElementById('edit-tags')?.value.trim();
    const content = document.getElementById('edit-content')?.value;

    if (!title || !content) {
      this.showToast('标题和内容不能为空', 'error');
      return;
    }

    const statusEl = document.getElementById('edit-status');
    if (statusEl) statusEl.textContent = '保存中...';

    const tags = tagsStr ? tagsStr.split(',').map(t => t.trim()).filter(t => t) : [];

    try {
      const res = await fetch(`${this.API}/api/admin/articles/${a.slug}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.authToken}`
        },
        body: JSON.stringify({ title, category, tags, content })
      });

      if (res.ok) {
        a.title = title;
        a.category = category;
        a.tags = tags;
        a.content = content;
        this.showToast('文章已保存', 'success');
        this.showAdminTab('articles');
      } else {
        const err = await res.json().catch(() => ({}));
        this.showToast(err.error || '保存失败', 'error');
        if (statusEl) statusEl.textContent = '保存失败';
      }
    } catch {
      a.title = title;
      a.category = category;
      a.tags = tags;
      a.content = content;
      this.showToast('文章已保存（本地模式）', 'success');
      this.showAdminTab('articles');
    }
  },

  escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  },

  async saveSettings() {
    const oldPassword = document.getElementById('settings-old-password')?.value;
    const newPassword = document.getElementById('settings-new-password')?.value;
    const statusEl = document.getElementById('settings-status');
    if (!statusEl) return;

    if (!oldPassword && !newPassword) {
      this.showToast('没有需要保存的修改', 'error');
      return;
    }

    if (newPassword && !oldPassword) {
      this.showToast('修改密码需要输入旧密码', 'error');
      return;
    }

    statusEl.textContent = '保存中...';

    try {
      const res = await fetch(`${this.API}/api/admin/change-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.authToken}`
        },
        body: JSON.stringify({
          old_password: oldPassword,
          new_password: newPassword
        })
      });

      const data = await res.json();
      if (res.ok) {
        this.showToast('密码已修改', 'success');
        statusEl.textContent = '✓ 已保存';
        document.getElementById('settings-old-password').value = '';
        document.getElementById('settings-new-password').value = '';
      } else {
        this.showToast(data.error || '保存失败', 'error');
        statusEl.textContent = '保存失败';
      }
    } catch {
      this.showToast('无法连接服务器', 'error');
      statusEl.textContent = '';
    }
  },

  logout() {
    this.authToken = null;
    localStorage.removeItem('ph_token');
    window.location.href = '/';
  },

  // ============ Utilities ============
  formatDate(dateStr) {
    const d = new Date(dateStr);
    return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
  },

  showToast(message, type = 'success') {
    const container = document.getElementById('toast-container') || (() => {
      const c = document.createElement('div');
      c.id = 'toast-container';
      c.className = 'toast-container';
      document.body.appendChild(c);
      return c;
    })();

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
};

// Boot
document.addEventListener('DOMContentLoaded', () => App.init());
