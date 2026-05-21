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

# ============ 来源清单 ============
SOURCES = [
    "WWD", "Business of Fashion", "Vogue Business", "Ladymax",
    "Miss Tweed", "FashionNetwork", "Amy Odell / Back Row",
    "Style Zeitgeist", "1 Granary", "i-D", "GQ", "Vogue",
    "The Style Title", "Brenda Hashtag", "Retail Boss",
    "Puck News", "NYT / Vanessa Friedman", "Glitz Paris",
    "Baiguan News", "Rob Shuter", "Why You Should Care",
    "My Clothing Archive",
]

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
