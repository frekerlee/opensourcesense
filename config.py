"""Fashion Dashboard — 配置：来源、品牌、配色、分类"""

# ============ 配色方案（深色时尚主题）============
COLORS = {
    "bg_primary": "#0E1116",
    "bg_secondary": "#1A1D23",
    "bg_sidebar": "#16181D",
    "bg_card": "#1E2127",
    "text_primary": "#E8E6E3",
    "text_secondary": "#9B9B9B",
    "accent_red": "#FF4757",
    "accent_gold": "#D4AF37",
    "accent_green": "#2ED573",
    "accent_orange": "#FFA502",
    "accent_pink": "#FF6B81",
    "score_gradient": ["#FF4757", "#FF6B81", "#FFA502", "#2ED573"],
}

# ============ CSS 样式 ============
CUSTOM_CSS = """
<style>
    /* 全局背景 */
    .stApp {
        background-color: #0E1116;
    }
    header[data-testid="stHeader"] {
        background-color: #0E1116;
    }
    section[data-testid="stSidebar"] {
        background-color: #16181D;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label {
        color: #E8E6E3 !important;
    }

    /* 卡片容器 */
    .article-card {
        background: #1E2127;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #2A2D33;
        transition: border-color 0.2s;
    }
    .article-card:hover {
        border-color: #FF4757;
    }

    /* 标题 */
    .card-title-en {
        color: #E8E6E3;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 2px;
        line-height: 1.3;
    }
    .card-title-cn {
        color: #9B9B9B;
        font-size: 12px;
        margin-bottom: 8px;
        line-height: 1.3;
    }

    /* 来源和日期 */
    .card-meta {
        color: #6B6B6B;
        font-size: 11px;
        margin-bottom: 8px;
    }
    .card-meta .source {
        color: #D4AF37;
        font-weight: 500;
    }

    /* 评分条 */
    .score-bar-container {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }
    .score-label {
        color: #FF4757;
        font-size: 11px;
        font-weight: 700;
        min-width: 28px;
    }
    .score-bar-bg {
        flex: 1;
        height: 4px;
        background: #2A2D33;
        border-radius: 2px;
        overflow: hidden;
    }
    .score-bar-fill {
        height: 100%;
        border-radius: 2px;
        background: linear-gradient(90deg, #FF4757, #FF6B81, #FFA502, #2ED573);
    }
    .score-value {
        color: #E8E6E3;
        font-size: 11px;
        font-weight: 700;
        min-width: 30px;
        text-align: right;
    }

    /* 子指标 */
    .sub-metrics {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        font-size: 10px;
        color: #9B9B9B;
        margin-bottom: 8px;
    }
    .sub-metric {
        display: flex;
        align-items: center;
        gap: 3px;
    }
    .sub-metric .val {
        color: #E8E6E3;
        font-weight: 600;
    }
    .trend-up { color: #2ED573; }
    .trend-down { color: #FF4757; }
    .trend-stable { color: #9B9B9B; }

    /* 标签 */
    .tags {
        display: flex;
        gap: 4px;
        flex-wrap: wrap;
    }
    .tag {
        background: #2A2D33;
        color: #9B9B9B;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 10px;
    }
    .tag.brand {
        background: rgba(212, 175, 55, 0.15);
        color: #D4AF37;
    }
    .tag.trending {
        background: rgba(255, 71, 87, 0.15);
        color: #FF4757;
    }

    /* Gallery 卡片 */
    .gallery-card {
        background: #1E2127;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #2A2D33;
        transition: border-color 0.2s;
        cursor: pointer;
    }
    .gallery-card:hover {
        border-color: #FF4757;
    }
    .gallery-card img {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    .gallery-card-info {
        padding: 8px 10px;
    }
    .gallery-card-info .title {
        color: #E8E6E3;
        font-size: 12px;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .gallery-card-info .score {
        color: #FF4757;
        font-size: 11px;
        font-weight: 700;
    }

    /* 顶部导航模拟 */
    .top-nav {
        display: flex;
        align-items: center;
        gap: 24px;
        padding: 12px 0;
        border-bottom: 1px solid #2A2D33;
        margin-bottom: 4px;
    }
    .top-nav .logo {
        color: #D4AF37;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .top-nav a {
        color: #9B9B9B;
        text-decoration: none;
        font-size: 13px;
    }
    .top-nav a.active {
        color: #FF4757;
    }

    /* 隐藏 Streamlit 默认元素 */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
"""

# ============ 内容分类 ============
CATEGORIES = [
    "产业新闻",
    "趋势分析",
    "深度评论",
    "数据报告",
    "品牌动态",
    "时装周",
    "小红书",
    "公众号",
    "博主观点",
]

# ============ 品牌列表 ============
BRANDS = [
    "Gucci", "Prada", "Louis Vuitton", "Balenciaga", "Chanel",
    "Dior", "Hermès", "Bottega Veneta", "Loewe", "Miu Miu",
    "Saint Laurent", "Burberry", "Versace", "Fendi", "Givenchy",
    "Jacquemus", "The Row", "Khaite", "Schiaparelli", "Valentino",
    "Moncler", "Rick Owens", "Maison Margiela", "Loro Piana", "Zara",
]

# ============ 风格 / 品类标签 ============
STYLE_TAGS = [
    "Quiet Luxury", "Gorpcore", "Y2K Revival", "Minimalism",
    "Avant-Garde", "Streetwear", "Couture", "Resort", "Menswear",
    "Sustainability", "Metaverse Fashion", "Genderless", "Vintage",
    "Athleisure", "Craftsmanship", "Resale",
]

# ============ 来源清单（22个 + 博主平台）============
# access: "open" = 可直接抓取, "paywall" = 付费墙, "blogger" = 博主内容
SOURCES = [
    # 可直接访问（16个）
    {"name": "WWD", "access": "open", "url": "https://wwd.com/", "desc": "时尚产业综合"},
    {"name": "Miss Tweed", "access": "open", "url": "https://misstweed.com/", "desc": "奢侈品深度"},
    {"name": "Ladymax", "access": "open", "url": "https://www.ladymax.cn/", "desc": "中文时尚商业"},
    {"name": "FashionNetwork", "access": "open", "url": "https://ww.fashionnetwork.com/", "desc": "时尚产业新闻"},
    {"name": "Rob Shuter", "access": "open", "url": "https://robshuter.substack.com/", "desc": "名人娱乐"},
    {"name": "The Style Title", "access": "open", "url": "https://thestyletitle.substack.com/", "desc": "时尚文化批评"},
    {"name": "Why You Should Care", "access": "open", "url": "https://whyyoushouldcare.substack.com/", "desc": "时尚/奢侈品牌分析"},
    {"name": "Baiguan News", "access": "open", "url": "https://www.baiguan.news/", "desc": "中国市场数据"},
    {"name": "Amy Odell / Back Row", "access": "open", "url": "https://amyodell.substack.com/", "desc": "时尚产业评论"},
    {"name": "i-D", "access": "open", "url": "https://substack.i-d.co/", "desc": "青年文化/时尚"},
    {"name": "Retail Boss", "access": "open", "url": "https://retailboss.substack.com/", "desc": "零售产业"},
    {"name": "Style Zeitgeist", "access": "open", "url": "https://stylezeitgeist.substack.com/", "desc": "时尚文化评论"},
    {"name": "Brenda Hashtag", "access": "open", "url": "https://brendahashtag.substack.com/", "desc": "时尚生活方式"},
    {"name": "My Clothing Archive", "access": "open", "url": "https://myclothingarchive.substack.com/", "desc": "时尚档案/历史"},
    {"name": "Climax Books", "access": "open", "url": "https://climaxbooks.substack.com/", "desc": "时尚书籍/文化"},
    {"name": "1 Granary", "access": "open", "url": "https://1granary.substack.com/", "desc": "时装教育/新锐"},
    # 付费墙 / 受限（6个）
    {"name": "Puck News", "access": "paywall", "url": "https://puck.news/", "desc": "时尚/媒体 insider"},
    {"name": "NYT / Vanessa Friedman", "access": "paywall", "url": "https://www.nytimes.com/", "desc": "时尚评论"},
    {"name": "Business of Fashion", "access": "paywall", "url": "https://www.businessoffashion.com/", "desc": "时尚商业权威"},
    {"name": "Glitz Paris", "access": "paywall", "url": "https://glitz.paris/", "desc": "巴黎时尚"},
    {"name": "Vogue Business", "access": "paywall", "url": "https://www.voguebusiness.com/", "desc": "时尚商业数据"},
    {"name": "GQ", "access": "paywall", "url": "https://www.gq.com/", "desc": "男装/文化"},
    # 博主 / 平台内容
    {"name": "小红书时尚博主", "access": "blogger", "url": "https://www.xiaohongshu.com/", "desc": "小红书平台时尚内容"},
    # B站时尚博主
    {"name": "AHALOLO (B站)", "access": "blogger", "url": "https://space.bilibili.com/353368172", "desc": "B站时尚评论/吐槽 · 深度解析"},
    {"name": "午夜飞行鼠 (B站)", "access": "blogger", "url": "https://space.bilibili.com/14359467", "desc": "B站时尚内容创作 · 穿搭测评"},
    # 微信公众号
    {"name": "LADYMAX (公众号)", "access": "blogger", "url": "https://mp.weixin.qq.com/", "desc": "中文时尚商业深度 · 公众号"},
    {"name": "Numero中文版 (公众号)", "access": "blogger", "url": "https://mp.weixin.qq.com/", "desc": "Numero大都市中文版 · 公众号"},
    {"name": "Vogue Business (公众号)", "access": "blogger", "url": "https://mp.weixin.qq.com/", "desc": "Vogue商业洞察中文版 · 公众号"},
    {"name": "1stRow (公众号)", "access": "blogger", "url": "https://mp.weixin.qq.com/", "desc": "秀场前排 · 时装周深度报道"},
    {"name": "InsideFashion (公众号)", "access": "blogger", "url": "https://mp.weixin.qq.com/", "desc": "时尚圈内幕 · 产业深度"},
]

# 提取纯名称列表（兼容旧代码）
SOURCE_NAMES = [s["name"] for s in SOURCES]

# ============ 评分权重 ============
SCORE_WEIGHTS = {
    "social_heat": 0.30,
    "industry_impact": 0.25,
    "content_quality": 0.20,
    "trend_velocity": 0.15,
    "exclusivity": 0.10,
}

# ============ 页面标题 ============
SITE_NAME = "OPEN SOURCESENSE"
SITE_SUBTITLE = "时尚内容开源情报平台"
