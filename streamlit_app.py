"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SOAL 7 — Dashboard Dinamis (Streamlit) · ULTIMATE PREMIUM Edition         ║
║  Business Intelligence Remidi — Universitas Islam Indonesia                ║
║  Februari 2026                                                              ║
║                                                                             ║
║  Features:                                                                  ║
║    · Glassmorphism UI with animated gradient accents & particles            ║
║    · Collapsible sidebar with premium filters                               ║
║    · Dark / Light mode toggle with smooth CSS transitions                  ║
║    · Sparkline KPI cards with comparison badges (↑↓%) & shimmer effect     ║
║    · Premium tab navigation (Trend / Segmentasi / Geographic)               ║
║    · RFM Radar chart, Revenue Treemap, RFM Scatter plot                    ║
║    · Customer Funnel, Business Health Gauge                                 ║
║    · Cross-segment heatmap analysis (Soal 5)                                ║
║    · Animated number counters, dot-grid, floating particles                ║
║    · Styled data table with gradient header                                ║
║    · Filter info summary & animated header gradient border                 ║
║                                                                             ║
║  Run:  streamlit run streamlit_app.py                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import base64
import warnings

warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Sales Analytics Dashboard · BI UII",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ═══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

PRIMARY       = "#6366f1"
PRIMARY_LIGHT = "#818cf8"
PRIMARY_DARK  = "#4338ca"
ACCENT        = "#8b5cf6"
SUCCESS       = "#10b981"
WARNING       = "#f59e0b"
DANGER        = "#ef4444"
INFO          = "#3b82f6"
CYAN          = "#06b6d4"
PINK          = "#ec4899"
ORANGE        = "#f97316"

GRAD_PRIMARY = "linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%)"
GRAD_ACCENT  = "linear-gradient(135deg, #3b82f6 0%, #6366f1 50%, #8b5cf6 100%)"

FONT      = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif"
FONT_MONO = "'JetBrains Mono', 'Cascadia Code', 'Fira Code', monospace"
CHART_H   = 380

COLORS_PROD = {
    "Very Frequently Purchased": "#059669",
    "Frequently Purchased":      "#34d399",
    "Moderately Purchased":      "#fbbf24",
    "Rarely Purchased":          "#f97316",
    "Very Rarely Purchased":     "#ef4444",
}
COLORS_CUST = {
    "Loyal Customer":      "#059669",
    "Active Customer":     "#3b82f6",
    "Occasional Customer": "#f59e0b",
    "Inactive Customer":   "#ef4444",
}

PRODUCT_SEGMENTS = [
    "Very Rarely Purchased", "Rarely Purchased",
    "Moderately Purchased", "Frequently Purchased",
    "Very Frequently Purchased",
]
CUSTOMER_SEGMENTS = [
    "Loyal Customer", "Active Customer",
    "Occasional Customer", "Inactive Customer",
]

COUNTRY_ISO3 = {
    "Australia": "AUS", "Austria": "AUT", "Bahrain": "BHR", "Belgium": "BEL",
    "Brazil": "BRA", "Canada": "CAN", "Channel Islands": "GBR", "Cyprus": "CYP",
    "Czech Republic": "CZE", "Denmark": "DNK", "EIRE": "IRL",
    "European Community": "EUR", "Finland": "FIN", "France": "FRA",
    "Germany": "DEU", "Greece": "GRC", "Hong Kong": "HKG", "Iceland": "ISL",
    "Israel": "ISR", "Italy": "ITA", "Japan": "JPN", "Lebanon": "LBN",
    "Lithuania": "LTU", "Malta": "MLT", "Netherlands": "NLD", "Norway": "NOR",
    "Poland": "POL", "Portugal": "PRT", "RSA": "ZAF", "Saudi Arabia": "SAU",
    "Singapore": "SGP", "Spain": "ESP", "Sweden": "SWE", "Switzerland": "CHE",
    "USA": "USA", "United Arab Emirates": "ARE", "United Kingdom": "GBR",
    "Unspecified": None,
}

# ── Theme dictionaries ──

LIGHT = {
    "bg_page":      "#eef1f8",
    "bg_card":      "rgba(255,255,255,0.78)",
    "bg_card_solid": "#ffffff",
    "bg_sidebar":   "rgba(255,255,255,0.6)",
    "bg_header":    "rgba(255,255,255,0.78)",
    "text_primary": "#0f172a",
    "text_sec":     "#475569",
    "text_muted":   "#94a3b8",
    "border":       "rgba(226,232,240,0.8)",
    "shadow":       "0 4px 30px rgba(0,0,0,0.06)",
    "shadow_hover": "0 20px 60px rgba(99,102,241,0.12)",
    "plotly_tpl":   "plotly_white",
    "plot_bg":      "rgba(255,255,255,0)",
    "plot_paper":   "rgba(255,255,255,0)",
    "plot_grid":    "rgba(226,232,240,0.5)",
    "plot_text":    "#334155",
    "geo_land":     "#eef2ff",
    "geo_coast":    "#c7d2fe",
    "table_odd":    "rgba(248,250,252,0.8)",
    "kpi_bg":       "rgba(255,255,255,0.78)",
    "kpi_border":   "rgba(226,232,240,0.6)",
    "glow":         "0 0 20px rgba(99,102,241,0.15)",
    "orb_opacity":  "0.06",
    "dot_opacity":  "0.025",
    "card_border_c": "rgba(255,255,255,0.6)",
    "shine":        "rgba(255,255,255,0.45)",
    "particle1":    "rgba(99,102,241,0.06)",
    "particle2":    "rgba(139,92,246,0.05)",
    "hover_bg":     "rgba(255,255,255,0.95)",
    "hover_text":   "#0f172a",
    # Aurora / mesh gradient colors
    "aurora1":      "rgba(99,102,241,0.06)",
    "aurora2":      "rgba(139,92,246,0.05)",
    "aurora3":      "rgba(59,130,246,0.04)",
    "aurora4":      "rgba(16,185,129,0.03)",
    "mesh1":        "rgba(99,102,241,0.04)",
    "mesh2":        "rgba(139,92,246,0.03)",
    "mesh3":        "rgba(236,72,153,0.02)",
}

DARK = {
    "bg_page":      "#080c16",
    "bg_card":      "rgba(30,41,59,0.55)",
    "bg_card_solid": "#1e293b",
    "bg_sidebar":   "rgba(12,18,32,0.85)",
    "bg_header":    "rgba(30,41,59,0.55)",
    "text_primary": "#f1f5f9",
    "text_sec":     "#94a3b8",
    "text_muted":   "#64748b",
    "border":       "rgba(51,65,85,0.5)",
    "shadow":       "0 4px 30px rgba(0,0,0,0.35)",
    "shadow_hover": "0 20px 60px rgba(99,102,241,0.2)",
    "plotly_tpl":   "plotly_dark",
    "plot_bg":      "rgba(0,0,0,0)",
    "plot_paper":   "rgba(0,0,0,0)",
    "plot_grid":    "rgba(71,85,105,0.25)",
    "plot_text":    "#e2e8f0",
    "geo_land":     "#1e293b",
    "geo_coast":    "#475569",
    "table_odd":    "rgba(30,41,59,0.8)",
    "kpi_bg":       "rgba(30,41,59,0.55)",
    "kpi_border":   "rgba(71,85,105,0.25)",
    "glow":         "0 0 30px rgba(99,102,241,0.25)",
    "orb_opacity":  "0.08",
    "dot_opacity":  "0.04",
    "card_border_c": "rgba(71,85,105,0.25)",
    "shine":        "rgba(255,255,255,0.06)",
    "particle1":    "rgba(99,102,241,0.10)",
    "particle2":    "rgba(139,92,246,0.08)",
    "hover_bg":     "rgba(15,23,42,0.9)",
    "hover_text":   "#f1f5f9",
    # Aurora / mesh gradient colors — more vivid in dark
    "aurora1":      "rgba(99,102,241,0.12)",
    "aurora2":      "rgba(139,92,246,0.10)",
    "aurora3":      "rgba(59,130,246,0.08)",
    "aurora4":      "rgba(16,185,129,0.06)",
    "mesh1":        "rgba(99,102,241,0.08)",
    "mesh2":        "rgba(139,92,246,0.06)",
    "mesh3":        "rgba(236,72,153,0.04)",
}


# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS — ULTIMATE PREMIUM (matching Dash version 1:1)
# ═══════════════════════════════════════════════════════════════════════════════

def inject_custom_css(is_dark=False):
    t = DARK if is_dark else LIGHT

    # Build dark-mode overrides as a plain string (not f-string)
    # so CSS braces stay as single { } instead of doubled {{ }}
    dark_mode_css = ""
    if is_dark:
        dark_mode_css = """
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border-color: #334155 !important;
    }

    [data-testid="stSidebar"] .stDateInput input {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border-color: #334155 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(51,65,85,0.4) !important;
    }

    .stApp .main .block-container p,
    .stApp .main .block-container span,
    .stApp .main .block-container h1,
    .stApp .main .block-container h2,
    .stApp .main .block-container h3,
    .stApp .main .block-container h4 {
        color: #f1f5f9 !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
    }

    .stDataFrame {
        background-color: #1e293b !important;
    }

    .stDataFrame [data-testid="stDataFrameResizable"] {
        background-color: #1e293b !important;
    }
        """

    st.markdown(f"""
    <style>
    /* ═══ Google Fonts ═══ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* ═══ CSS Custom Properties ═══ */
    :root {{
        --primary: #6366f1;
        --primary-light: #818cf8;
        --accent: #8b5cf6;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-page: {t["bg_page"]};
        --bg-card: {t["bg_card"]};
        --bg-card-solid: {t["bg_card_solid"]};
        --text-primary: {t["text_primary"]};
        --text-secondary: {t["text_sec"]};
        --text-muted: {t["text_muted"]};
        --border-color: {t["border"]};
        --card-shadow: {t["shadow"]};
        --card-shadow-hover: {t["shadow_hover"]};
        --glow-primary: {t["glow"]};
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%);
        --gradient-accent: linear-gradient(135deg, #3b82f6 0%, #6366f1 50%, #8b5cf6 100%);
        --blur-amount: 20px;
        --radius: 16px;
        --radius-sm: 10px;
        --radius-lg: 24px;
    }}

    /* ═══ Global Overrides ═══ */
    .stApp {{
        font-family: {FONT};
        background-color: {t["bg_page"]} !important;
        color: {t["text_primary"]} !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    /* Hide top bar completely */
    .stApp > header {{
        display: none !important;
    }}

    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    /* Sidebar collapsed control — reparented outside header so still visible */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"] {{
        z-index: 99999 !important;
        pointer-events: all !important;
        position: fixed !important;
        top: 12px !important;
        left: 12px !important;
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }}

    .stApp .main .block-container {{
        color: {t["text_primary"]};
    }}

    /* ═══ Aurora Animated Background ═══ */
    .stApp::before {{
        content: '';
        position: fixed;
        top: -60%; left: -60%;
        width: 220%; height: 220%;
        background:
            radial-gradient(ellipse 600px 400px at 15% 85%, {t["aurora1"]} 0%, transparent 70%),
            radial-gradient(ellipse 500px 500px at 85% 15%, {t["aurora2"]} 0%, transparent 70%),
            radial-gradient(ellipse 450px 350px at 50% 50%, {t["aurora3"]} 0%, transparent 70%),
            radial-gradient(ellipse 400px 300px at 70% 70%, {t["aurora4"]} 0%, transparent 70%);
        animation: auroraFlow 30s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }}

    @keyframes auroraFlow {{
        0%   {{ transform: translate(0, 0) rotate(0deg) scale(1); }}
        25%  {{ transform: translate(40px, -60px) rotate(3deg) scale(1.02); }}
        50%  {{ transform: translate(-30px, 30px) rotate(-2deg) scale(0.98); }}
        75%  {{ transform: translate(20px, -40px) rotate(4deg) scale(1.01); }}
        100% {{ transform: translate(-15px, 50px) rotate(-1deg) scale(1); }}
    }}

    /* ═══ Subtle Dot-Grid Pattern ═══ */
    .stApp::after {{
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image: radial-gradient(circle, rgba(99,102,241,{t["dot_opacity"]}) 0.8px, transparent 0.8px);
        background-size: 32px 32px;
        pointer-events: none;
        z-index: 0;
        opacity: 0.8;
    }}

    /* ═══ Floating Particles ═══ */
    @keyframes floatParticle1 {{
        0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
        25%  {{ transform: translate(30px, -25px) rotate(90deg); }}
        50%  {{ transform: translate(-15px, -50px) rotate(180deg); }}
        75%  {{ transform: translate(20px, -30px) rotate(270deg); }}
    }}

    @keyframes floatParticle2 {{
        0%, 100% {{ transform: translate(0, 0); }}
        33%  {{ transform: translate(-20px, 30px); }}
        66%  {{ transform: translate(25px, -20px); }}
    }}

    /* ═══ Multi-layer Gradient Mesh Overlay ═══ */
    .stApp .main::before {{
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background:
            conic-gradient(from 45deg at 25% 35%,
                {t["mesh1"]} 0deg, transparent 90deg,
                {t["mesh2"]} 180deg, transparent 270deg),
            conic-gradient(from 200deg at 75% 65%,
                {t["mesh3"]} 0deg, transparent 120deg,
                {t["mesh1"]} 240deg, transparent 360deg),
            radial-gradient(ellipse at 50% 0%, {t["aurora3"]} 0%, transparent 60%);
        pointer-events: none;
        z-index: -1;
        animation: meshShift 40s ease-in-out infinite alternate;
    }}

    @keyframes meshShift {{
        0%   {{ opacity: 0.7; }}
        50%  {{ opacity: 1; }}
        100% {{ opacity: 0.8; }}
    }}

    /* ═══ Custom Scrollbar ═══ */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, #6366f1, #8b5cf6);
        border-radius: 10px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, #4f46e5, #7c3aed);
    }}

    /* ═══ Header — Animated Gradient Border ═══ */
    .header-bar {{
        position: relative;
        overflow: hidden;
        padding: 14px 0 16px;
        margin-bottom: 0;
    }}

    .header-bar::after {{
        content: '';
        position: absolute;
        bottom: 0; left: 0;
        width: 100%; height: 2px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #3b82f6, #6366f1);
        background-size: 300% 100%;
        animation: gradientSlide 6s ease infinite;
    }}

    @keyframes gradientSlide {{
        0%   {{ background-position: 0% 50%; }}
        50%  {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .gradient-title {{
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        line-height: 1.2;
    }}

    .header-subtitle {{
        font-size: 12px;
        color: {t["text_muted"]};
        font-weight: 500;
        letter-spacing: 0.3px;
        margin-top: 2px;
    }}

    /* ═══ KPI Cards — Premium with Shimmer ═══ */
    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        padding: 10px 0;
    }}

    .kpi-card {{
        background: {t["kpi_bg"]};
        border-radius: var(--radius);
        padding: 20px 16px 14px;
        text-align: center;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {t["kpi_border"]};
        box-shadow: {t["shadow"]};
        cursor: default;
        transition: all 0.35s cubic-bezier(0.25,0.8,0.25,1);
        animation: fadeInUp 0.4s cubic-bezier(0.16,1,0.3,1) both;
    }}

    /* Shimmer sweep on hover */
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 200%; height: 100%;
        background: linear-gradient(90deg, transparent, {t["shine"]}, transparent);
        transition: left 0.7s ease;
        z-index: 1;
    }}

    .kpi-card:hover::before {{
        left: 100%;
    }}

    /* Bottom gradient accent on hover */
    .kpi-card::after {{
        content: '';
        position: absolute;
        bottom: 0; left: 0;
        width: 100%; height: 3px;
        background: var(--gradient-primary);
        opacity: 0;
        transition: opacity 0.35s ease;
    }}

    .kpi-card:hover::after {{
        opacity: 1;
    }}

    .kpi-card:hover {{
        transform: translateY(-6px) scale(1.02);
        box-shadow: {t["shadow_hover"]}, {t["glow"]};
    }}

    /* Staggered entrance */
    .kpi-card:nth-child(1) {{ animation-delay: 0.05s; }}
    .kpi-card:nth-child(2) {{ animation-delay: 0.10s; }}
    .kpi-card:nth-child(3) {{ animation-delay: 0.15s; }}
    .kpi-card:nth-child(4) {{ animation-delay: 0.20s; }}
    .kpi-card:nth-child(5) {{ animation-delay: 0.25s; }}
    .kpi-card:nth-child(6) {{ animation-delay: 0.30s; }}
    .kpi-card:nth-child(7) {{ animation-delay: 0.35s; }}
    .kpi-card:nth-child(8) {{ animation-delay: 0.40s; }}

    .kpi-icon {{ font-size: 22px; margin-bottom: 8px; }}

    .kpi-label {{
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 6px;
        color: {t["text_muted"]};
    }}

    .kpi-value {{
        font-size: 22px;
        font-weight: 800;
        font-family: {FONT_MONO};
        letter-spacing: -0.5px;
        line-height: 1.2;
        color: {t["text_primary"]};
        animation: counterPop 0.6s cubic-bezier(0.25,0.8,0.25,1) both;
    }}

    .kpi-badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 11px;
        font-weight: 700;
        font-family: {FONT_MONO};
        padding: 2px 8px;
        border-radius: 12px;
        transition: transform 0.2s ease;
    }}

    .kpi-badge:hover {{ transform: scale(1.1); }}

    .kpi-badge.up {{ color: #10b981; background: rgba(16,185,129,0.1); }}
    .kpi-badge.down {{ color: #ef4444; background: rgba(239,68,68,0.1); }}

    /* Sparkline opacity transition */
    .kpi-card .kpi-sparkline {{
        opacity: 0.85;
        transition: opacity 0.3s ease;
    }}
    .kpi-card:hover .kpi-sparkline {{
        opacity: 1;
    }}

    /* ═══ Section Headers — Expanding Underline ═══ */
    .section-header {{
        display: inline-flex;
        align-items: center;
        gap: 12px;
        padding: 24px 0 12px;
        position: relative;
    }}

    .section-header::after {{
        content: '';
        position: absolute;
        bottom: 4px; left: 0;
        width: 40px; height: 3px;
        background: var(--gradient-primary);
        border-radius: 2px;
        transition: width 0.35s ease;
    }}

    .section-header:hover::after {{
        width: 100%;
    }}

    .section-icon {{ font-size: 22px; }}

    .section-title {{
        margin: 0;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.4px;
        color: {t["text_primary"]};
    }}

    .section-subtitle {{
        margin: 2px 0 0 34px;
        font-size: 12px;
        color: {t["text_muted"]};
        letter-spacing: 0.2px;
    }}

    /* ═══ Chart Cards — Glassmorphism ═══ */
    .chart-card {{
        background: {t["bg_card"]};
        border-radius: var(--radius);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {t["card_border_c"]};
        box-shadow: {t["shadow"]};
        padding: 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.25,0.8,0.25,1);
        animation: fadeInScale 0.5s cubic-bezier(0.25,0.8,0.25,1) both;
    }}

    /* Top shine line */
    .chart-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 10%, {t["shine"]} 50%, transparent 90%);
        z-index: 1;
    }}

    .chart-card:hover {{
        transform: translateY(-4px);
        box-shadow: {t["shadow_hover"]};
        border-color: rgba(99,102,241,0.2);
    }}

    /* Staggered chart entrance */
    .chart-card:nth-child(1) {{ animation-delay: 0.1s; }}
    .chart-card:nth-child(2) {{ animation-delay: 0.2s; }}
    .chart-card:nth-child(3) {{ animation-delay: 0.3s; }}
    .chart-card:nth-child(4) {{ animation-delay: 0.4s; }}

    /* ═══ Insight Panel ═══ */
    .insight-panel {{
        background: {t["bg_card"]};
        border-radius: var(--radius);
        padding: 22px 28px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {t["border"]};
        box-shadow: {t["shadow"]};
        margin-bottom: 12px;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.5s ease both;
    }}

    /* Gradient left accent bar */
    .insight-panel::before {{
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
        background: var(--gradient-primary);
        border-radius: 4px 0 0 4px;
    }}

    .insight-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
    }}

    .insight-title {{
        font-size: 14px;
        font-weight: 800;
        letter-spacing: -0.2px;
        color: {t["text_primary"]};
    }}

    .insight-count {{
        font-size: 10px;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 12px;
        background: rgba(99,102,241,0.08);
        color: var(--primary);
        margin-left: auto;
    }}

    .insight-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4px 24px;
    }}

    .insight-bullet {{
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 4px 0;
        font-size: 12px;
        line-height: 1.6;
        color: {t["text_sec"]};
    }}

    .insight-dot {{
        color: var(--primary);
        font-size: 16px;
        font-weight: 700;
    }}

    /* ═══ Business Interpretation Card ═══ */
    .biz-card {{
        background: {t["bg_card"]};
        border-radius: var(--radius);
        padding: 28px 30px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {t["border"]};
        box-shadow: {t["shadow"]};
        border-left: 4px solid #8b5cf6;
        animation: fadeInUp 0.5s ease both;
    }}

    .biz-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }}

    .biz-item {{
        padding: 16px 18px;
        border-radius: var(--radius-sm);
        border: 1px solid;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}

    .biz-item:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }}

    .biz-item-title {{
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .biz-item-text {{
        margin: 0;
        line-height: 1.7;
        font-size: 13px;
        color: {t["text_sec"]};
    }}

    /* ═══ Sidebar — Premium Glassmorphism ═══ */
    [data-testid="stSidebar"] {{
        background-color: {t["bg_sidebar"]} !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
    }}

    [data-testid="stSidebar"] > div:first-child {{
        background-color: transparent !important;
    }}

    /* Sidebar glow line on right edge */
    [data-testid="stSidebar"]::after {{
        content: '';
        position: absolute;
        top: 10%; right: 0;
        width: 1px; height: 80%;
        background: linear-gradient(180deg, transparent, rgba(99,102,241,0.2), transparent);
        pointer-events: none;
    }}

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stDateInput label {{
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        color: {t["text_muted"]} !important;
    }}

    /* ═══ Dark Mode — Sidebar Widget Overrides ═══ */
    {dark_mode_css}

    /* ═══ Tab Styling — Premium Pill Tabs ═══ */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        padding: 4px;
        border-radius: 14px;
        background: {'rgba(99,102,241,0.04)' if not is_dark else 'rgba(99,102,241,0.08)'};
        border: 1px solid {'rgba(99,102,241,0.08)' if not is_dark else 'rgba(99,102,241,0.15)'};
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 13px;
        letter-spacing: -0.2px;
        transition: all 0.3s ease;
        color: {t["text_muted"]};
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: {t["text_primary"]};
        background: rgba(99,102,241,0.04);
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.3);
        font-weight: 700;
    }}

    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* ═══ Data Table — Gradient Header ═══ */
    .styled-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: var(--radius-sm);
        overflow: hidden;
        font-family: {FONT};
        font-size: 12px;
    }}

    .styled-table thead th {{
        background: {'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%)' if not is_dark else 'linear-gradient(135deg, #3b82f6 0%, #6366f1 50%, #8b5cf6 100%)'};
        color: white;
        font-weight: 700;
        font-size: 11px;
        text-align: center;
        padding: 12px 10px;
        letter-spacing: 0.3px;
        border: none;
    }}

    .styled-table tbody td {{
        text-align: center;
        padding: 10px 12px;
        color: {t["text_primary"]};
        border: 1px solid {t["border"]};
        background: {t["bg_card_solid"]};
    }}

    .styled-table tbody tr:nth-child(odd) td {{
        background: {t["table_odd"]};
    }}

    .styled-table tbody tr:hover td {{
        background: rgba(99,102,241,0.08);
    }}

    /* ═══ Filter Info Box ═══ */
    .filter-info {{
        font-size: 11px;
        color: {t["text_muted"]};
        line-height: 1.7;
        padding: 12px 14px;
        border-radius: var(--radius-sm);
        border: 1px solid rgba(99,102,241,0.08);
        background: rgba(99,102,241,0.02);
        margin-top: 8px;
    }}

    /* ═══ Animations ═══ */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes fadeInLeft {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to   {{ opacity: 1; transform: translateX(0); }}
    }}

    @keyframes fadeInScale {{
        from {{ opacity: 0; transform: scale(0.95); }}
        to   {{ opacity: 1; transform: scale(1); }}
    }}

    @keyframes counterPop {{
        0%   {{ transform: scale(0.8); opacity: 0; }}
        60%  {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}

    @keyframes pulse-glow {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(16,185,129,0.4); }}
        50%      {{ box-shadow: 0 0 0 6px rgba(16,185,129,0); }}
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50%      {{ transform: translateY(-6px); }}
    }}

    @keyframes spin-slow {{
        from {{ transform: rotate(0deg); }}
        to   {{ transform: rotate(360deg); }}
    }}

    /* ═══ Live Dot ═══ */
    .live-dot {{
        width: 8px; height: 8px;
        background: #10b981;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-glow 2s infinite;
        box-shadow: 0 0 6px rgba(16,185,129,0.4);
    }}

    /* ═══ Brand Icon Float ═══ */
    .brand-icon {{
        font-size: 28px;
        filter: drop-shadow(0 0 8px rgba(99,102,241,0.3));
        animation: float 3s ease-in-out infinite;
    }}

    /* ═══ Footer ═══ */
    .footer {{
        text-align: center;
        padding: 40px 0 12px;
        font-size: 11px;
        color: {t["text_muted"]};
        position: relative;
    }}

    .footer::before {{
        content: '';
        position: absolute;
        top: 0; left: 10%;
        width: 80%; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
    }}

    .footer-brand {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }}

    /* ═══ Badge / Pill ═══ */
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }}

    .badge-primary {{
        background: rgba(99,102,241,0.1);
        color: #6366f1;
    }}

    /* ═══ Theme Toggle Button (replaces box + toggle) ═══ */
    .theme-toggle-btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        width: 100%;
        padding: 12px 16px;
        border-radius: var(--radius-sm);
        border: 1px solid rgba(99,102,241,0.2);
        background: {'rgba(99,102,241,0.06)' if not is_dark else 'rgba(99,102,241,0.12)'};
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: {FONT};
        font-size: 13px;
        font-weight: 600;
        color: {'#0f172a' if not is_dark else '#e2e8f0'};
        letter-spacing: -0.2px;
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
    }}

    .theme-toggle-btn::before {{
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.08), transparent);
        transition: left 0.5s ease;
    }}

    .theme-toggle-btn:hover {{
        border-color: rgba(99,102,241,0.4);
        background: {'rgba(99,102,241,0.10)' if not is_dark else 'rgba(99,102,241,0.18)'};
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99,102,241,0.15);
    }}

    .theme-toggle-btn:hover::before {{
        left: 100%;
    }}

    .theme-toggle-btn:active {{
        transform: translateY(0);
        box-shadow: none;
    }}

    /* Hide the Streamlit button container styling */
    div[data-testid="stButton"] .theme-toggle-btn {{
        all: unset;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        width: 100%;
        padding: 12px 16px;
        border-radius: var(--radius-sm);
        border: 1px solid rgba(99,102,241,0.2);
        background: {'rgba(99,102,241,0.06)' if not is_dark else 'rgba(99,102,241,0.12)'};
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: {FONT};
        font-size: 13px;
        font-weight: 600;
        color: {'#0f172a' if not is_dark else '#e2e8f0'};
        letter-spacing: -0.2px;
        box-sizing: border-box;
    }}

    /* Style the st.button used for theme toggle */
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {{
        width: 100%;
        padding: 12px 16px;
        border-radius: 10px !important;
        border: 1px solid rgba(99,102,241,0.2) !important;
        background: {'rgba(99,102,241,0.06)' if not is_dark else 'rgba(99,102,241,0.12)'} !important;
        color: {'#0f172a' if not is_dark else '#e2e8f0'} !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.3s ease !important;
        letter-spacing: -0.2px;
    }}

    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {{
        border-color: rgba(99,102,241,0.4) !important;
        background: {'rgba(99,102,241,0.12)' if not is_dark else 'rgba(99,102,241,0.20)'} !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99,102,241,0.15) !important;
    }}

    /* ═══ Plotly Chart Rounding ═══ */
    .js-plotly-plot .plotly .main-svg {{
        border-radius: var(--radius);
    }}

    /* ═══ DataFrame / Table Rounding ═══ */
    .stDataFrame {{
        border-radius: var(--radius-sm);
        overflow: hidden;
    }}

    /* ═══ Smooth Transitions ═══ */
    .chart-card,
    .kpi-card,
    .biz-item {{
        transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }}

    /* ═══ Responsive ═══ */
    @media (max-width: 768px) {{
        .kpi-container {{ grid-template-columns: repeat(2, 1fr); }}
        .insight-grid {{ grid-template-columns: 1fr; }}
        .biz-grid {{ grid-template-columns: 1fr; }}
        .header-bar h1 {{ font-size: 20px; }}
    }}

    @media (max-width: 480px) {{
        .kpi-container {{ grid-template-columns: 1fr; }}
    }}
    </style>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING & PREPROCESSING
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_and_clean(path="Sales Transaction v.4a.csv.gz"):
    df = pd.read_csv(path)
    df = df.dropna(subset=["CustomerNo", "ProductName"])
    df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=False)
    df = df[(df["Price"] > 0) & df["Price"].notna() & (df["Quantity"] != 0)]
    df["IsCancelled"] = df["Quantity"] < 0
    df["TotalAmount"] = df["Quantity"] * df["Price"]
    df["Year"]      = df["Date"].dt.year
    df["Month"]     = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.month_name()
    df["Quarter"]   = df["Date"].dt.quarter
    return df[~df["IsCancelled"]].copy()


@st.cache_data
def segment_products(df):
    pq = df.groupby("ProductName")["Quantity"].sum()
    q = pq.quantile([0.2, 0.4, 0.6, 0.8])
    def _seg(v):
        if v <= q[0.2]: return "Very Rarely Purchased"
        if v <= q[0.4]: return "Rarely Purchased"
        if v <= q[0.6]: return "Moderately Purchased"
        if v <= q[0.8]: return "Frequently Purchased"
        return "Very Frequently Purchased"
    return pq.apply(_seg)


@st.cache_data
def segment_customers(df):
    ref = df["Date"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("CustomerNo").agg(
        Recency   = ("Date", lambda x: (ref - x.max()).days),
        Frequency = ("TransactionNo", "nunique"),
        Monetary  = ("TotalAmount", "sum"),
    ).reset_index()
    rfm["R"] = pd.qcut(rfm["Recency"], 4, labels=[4, 3, 2, 1]).astype(int)
    rfm["F"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4,
                        labels=[1, 2, 3, 4]).astype(int)
    rfm["M"] = pd.qcut(rfm["Monetary"].rank(method="first"), 4,
                        labels=[1, 2, 3, 4]).astype(int)
    def _seg(r):
        if r.R >= 3 and r.F >= 4 and r.M >= 3: return "Loyal Customer"
        if r.R >= 3 and r.F >= 3:               return "Active Customer"
        if r.R >= 2 and r.F >= 2:               return "Occasional Customer"
        return "Inactive Customer"
    rfm["Segment"] = rfm.apply(_seg, axis=1)
    return rfm


@st.cache_data
def build_dashboard_df(df, prod_map, rfm):
    out = df.copy()
    out["Product_Segment"]  = out["ProductName"].map(prod_map)
    out["Customer_Segment"] = out["CustomerNo"].map(
        rfm.set_index("CustomerNo")["Segment"])
    out["YearMonth"] = out["Date"].dt.to_period("M").dt.to_timestamp()
    return out.dropna(subset=["Product_Segment", "Customer_Segment"])


# ═══════════════════════════════════════════════════════════════════════════════
# CHART BUILDERS (all theme-aware)
# ═══════════════════════════════════════════════════════════════════════════════

def _fig_layout(fig, height=CHART_H, is_dark=False, **extra):
    t = DARK if is_dark else LIGHT
    defaults = dict(
        template=t["plotly_tpl"], height=height,
        font=dict(family=FONT, color=t["plot_text"], size=12),
        title_font_color=t["text_primary"],
        paper_bgcolor=t["plot_paper"],
        plot_bgcolor=t["plot_bg"],
        margin=dict(t=60, b=45, l=65, r=35),
        hoverlabel=dict(
            bgcolor=t["hover_bg"],
            font=dict(family=FONT, size=12, color=t["hover_text"]),
            bordercolor="rgba(99,102,241,0.3)",
        ),
    )
    defaults.update(extra)
    # Ensure title font color always follows theme even when overridden
    if "title" in defaults and isinstance(defaults["title"], dict):
        tf = defaults["title"].get("font", {})
        if isinstance(tf, dict) and "color" not in tf:
            tf["color"] = t["text_primary"]
            defaults["title"]["font"] = tf
    fig.update_layout(**defaults)
    fig.update_xaxes(
        gridcolor=t["plot_grid"], gridwidth=1,
        zeroline=False, showline=False,
        tickfont=dict(size=11, color=t["plot_text"]),
        title_font_color=t["plot_text"],
    )
    fig.update_yaxes(
        gridcolor=t["plot_grid"], gridwidth=1,
        zeroline=False, showline=False,
        tickfont=dict(size=11, color=t["plot_text"]),
        title_font_color=t["plot_text"],
    )
    return fig


def _empty_fig(is_dark=False):
    t = DARK if is_dark else LIGHT
    fig = go.Figure()
    fig.add_annotation(
        text="<b>Tidak ada data</b><br>untuk filter ini",
        showarrow=False,
        font=dict(size=15, color=t["text_muted"]),
        align="center",
    )
    return _fig_layout(fig, is_dark=is_dark)


def _hex_to_rgba(hex_color, alpha=0.08):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _svg_sparkline_html(values, color="#6366f1", width=110, height=28):
    vals = list(values)
    if len(vals) < 2:
        return ""
    mn, mx = min(vals), max(vals)
    vr = mx - mn or 1
    hc = color.lstrip('#')
    pts = []
    for i, v in enumerate(vals):
        x = round(i / (len(vals) - 1) * width, 1)
        y = round(height - 3 - ((v - mn) / vr) * (height - 8), 1)
        pts.append(f"{x},{y}")
    polyline = " ".join(pts)
    last_x, last_y = pts[-1].split(",")
    area = polyline + f" {width},{height} 0,{height}"
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" class="kpi-sparkline">'
        f'<defs><linearGradient id="sg{hc[:3]}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="#{hc}" stop-opacity="0.25"/>'
        f'<stop offset="100%" stop-color="#{hc}" stop-opacity="0.02"/>'
        f'</linearGradient></defs>'
        f'<polygon points="{area}" fill="url(#sg{hc[:3]})"/>'
        f'<polyline points="{polyline}" fill="none" stroke="#{hc}" '
        f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="{last_x}" cy="{last_y}" r="2.5" fill="#{hc}"/>'
        f'</svg>'
    )
    b64 = base64.b64encode(svg.encode()).decode()
    return f'<img src="data:image/svg+xml;base64,{b64}" style="width:{width}px;height:{height}px;display:block;margin:6px auto 0;">'


# ── Trend ──

def build_trend_chart(filtered, is_dark=False):
    monthly = (
        filtered.groupby("YearMonth")
        .agg(Revenue=("TotalAmount", "sum"),
             Transactions=("TransactionNo", "nunique"))
        .reset_index().sort_values("YearMonth")
    )
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    n = len(monthly)
    bar_colors = [f"rgba(99,102,241,{0.4 + 0.5*i/max(n-1,1):.2f})" for i in range(n)]
    fig.add_trace(go.Bar(
        x=monthly["YearMonth"], y=monthly["Revenue"], name="Revenue",
        marker=dict(color=bar_colors, line=dict(width=0)),
        hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: £%{y:,.0f}<extra></extra>",
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=monthly["YearMonth"], y=monthly["Transactions"], name="Transaksi",
        mode="lines+markers",
        line=dict(color=DANGER, width=3, shape="spline"),
        marker=dict(size=6, color=DANGER, line=dict(color="white", width=1.5)),
        hovertemplate="<b>%{x|%b %Y}</b><br>Transaksi: %{y:,}<extra></extra>",
    ), secondary_y=True)
    _fig_layout(fig, is_dark=is_dark,
                title=dict(text="<b>Tren Penjualan Bulanan</b>", font=dict(size=16), x=0.02),
                legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center",
                            bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
                hovermode="x unified", bargap=0.3)
    fig.update_yaxes(title_text="Revenue (£)", tickprefix="£", tickformat=",", secondary_y=False)
    fig.update_yaxes(title_text="Transaksi", tickformat=",", secondary_y=True)
    return fig


def build_distribution_chart(filtered, is_dark=False):
    txn_qty  = filtered.groupby("TransactionNo")["Quantity"].sum()
    cap      = txn_qty.quantile(0.99)
    clipped  = txn_qty[txn_qty <= cap]
    mean_q, median_q = txn_qty.mean(), txn_qty.median()
    fig = go.Figure(go.Histogram(
        x=clipped, nbinsx=50,
        marker=dict(color="rgba(99,102,241,0.6)",
                    line=dict(color=PRIMARY, width=0.5)),
        hovertemplate="Qty: %{x}<br>Frekuensi: %{y:,}<extra></extra>",
    ))
    fig.add_vline(x=mean_q, line_dash="dash", line_color=DANGER, line_width=2,
                  annotation_text=f"Mean: {mean_q:.1f}",
                  annotation_font=dict(size=11, color=DANGER),
                  annotation_position="top right")
    fig.add_vline(x=median_q, line_dash="dash", line_color=SUCCESS, line_width=2,
                  annotation_text=f"Median: {median_q:.0f}",
                  annotation_font=dict(size=11, color=SUCCESS),
                  annotation_position="top left")
    _fig_layout(fig, is_dark=is_dark,
                title=dict(text="<b>Distribusi Produk per Transaksi</b>", font=dict(size=16), x=0.02),
                xaxis_title="Qty per Transaksi", yaxis_title="Frekuensi", bargap=0.08)
    return fig


def build_revenue_line(filtered, is_dark=False):
    monthly = (
        filtered.groupby("YearMonth")["TotalAmount"].sum()
        .reset_index().sort_values("YearMonth")
    )
    monthly.columns = ["YearMonth", "Revenue"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["YearMonth"], y=monthly["Revenue"],
        mode="lines", fill="tozeroy", name="Revenue",
        line=dict(color=PRIMARY, width=3, shape="spline"),
        fillcolor="rgba(99,102,241,0.06)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: £%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=monthly["YearMonth"], y=monthly["Revenue"],
        mode="markers", name="",
        marker=dict(size=7, color=PRIMARY, line=dict(color="white", width=2)),
        showlegend=False, hoverinfo="skip",
    ))
    _fig_layout(fig, is_dark=is_dark,
                title=dict(text="<b>Revenue Bulanan</b>", font=dict(size=16), x=0.02),
                yaxis_tickprefix="£", yaxis_tickformat=",", showlegend=False)
    return fig


def build_day_of_week_chart(filtered, is_dark=False):
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    daily = filtered.copy()
    daily["DayName"] = daily["Date"].dt.day_name()
    agg = daily.groupby("DayName")["TotalAmount"].sum().reindex(day_order).fillna(0)
    colors = ["rgba(99,102,241,0.7)"] * 7
    max_idx = agg.values.argmax()
    colors[max_idx] = PRIMARY
    fig = go.Figure(go.Bar(
        x=agg.index, y=agg.values,
        marker=dict(color=colors, line=dict(width=0), cornerradius=6),
        text=[f"£{v:,.0f}" for v in agg.values],
        textposition="outside",
        textfont=dict(size=10, family=FONT_MONO),
        hovertemplate="<b>%{x}</b><br>Revenue: £%{y:,.0f}<extra></extra>",
    ))
    _fig_layout(fig, is_dark=is_dark,
                title=dict(text="<b>Revenue per Hari</b>", font=dict(size=16), x=0.02),
                yaxis_tickprefix="£", yaxis_tickformat=",")
    return fig


# ── Segmentasi ──

def build_prod_pie(filtered, is_dark=False):
    t = DARK if is_dark else LIGHT
    agg = (
        filtered.groupby("Product_Segment")["TotalAmount"].sum()
        .reindex(PRODUCT_SEGMENTS).dropna().reset_index()
    )
    agg.columns = ["Segment", "Revenue"]
    fig = go.Figure(go.Pie(
        labels=agg["Segment"], values=agg["Revenue"],
        marker=dict(colors=[COLORS_PROD[s] for s in agg["Segment"]],
                    line=dict(color="white", width=2)),
        textinfo="percent+label", textposition="inside",
        textfont=dict(size=11, family=FONT),
        hole=0.48,
        hovertemplate="<b>%{label}</b><br>Revenue: £%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig.add_annotation(
        text=f"<b>£{agg['Revenue'].sum():,.0f}</b><br><span style='font-size:10px;color:{t['text_muted']}'>Total</span>",
        showarrow=False, font=dict(size=14, color=t["text_primary"]),
    )
    _fig_layout(fig, is_dark=is_dark,
                title=dict(text="<b>Revenue per Segment Produk</b>", font=dict(size=16), x=0.02),
                showlegend=False)
    return fig


def build_cust_bar(filtered, is_dark=False):
    agg = (
        filtered.groupby("Customer_Segment")["TotalAmount"].sum()
        .reindex(CUSTOMER_SEGMENTS).dropna().reset_index()
    )
    agg.columns = ["Segment", "Revenue"]
    total = agg["Revenue"].sum()
    fig = go.Figure(go.Bar(
        x=agg["Segment"], y=agg["Revenue"],
        marker=dict(
            color=[COLORS_CUST[s] for s in agg["Segment"]],
            line=dict(width=0), cornerradius=6,
        ),
        text=[f"£{v:,.0f}<br><span style='font-size:10px'>({v/total*100:.1f}%)</span>"
              for v in agg["Revenue"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Revenue: £%{y:,.0f}<extra></extra>",
    ))
    _fig_layout(fig, is_dark=is_dark,
                title=dict(text="<b>Revenue per Segment Pelanggan</b>", font=dict(size=16), x=0.02),
                yaxis_tickprefix="£", yaxis_tickformat=",")
    return fig


def build_top_products(filtered, is_dark=False, n=10):
    top = (
        filtered.groupby("ProductName")["Quantity"].sum()
        .nlargest(n).reset_index().sort_values("Quantity")
    )
    n_bars = len(top)
    colors = [f"rgba(99,102,241,{0.35 + 0.6*i/max(n_bars-1,1):.2f})" for i in range(n_bars)]
    fig = go.Figure(go.Bar(
        y=top["ProductName"], x=top["Quantity"], orientation="h",
        marker=dict(color=colors, line=dict(width=0), cornerradius=4),
        text=[f"  {v:,.0f}" for v in top["Quantity"]], textposition="outside",
        textfont=dict(size=11, family=FONT_MONO),
        hovertemplate="<b>%{y}</b><br>Quantity: %{x:,}<extra></extra>",
    ))
    _fig_layout(fig, is_dark=is_dark, height=420,
                title=dict(text=f"<b>Top {n} Produk (Quantity)</b>", font=dict(size=16), x=0.02),
                margin=dict(t=60, b=45, l=260, r=70),
                xaxis_title="Total Quantity")
    return fig


def build_top_countries(filtered, is_dark=False, n=10):
    top = (
        filtered.groupby("Country")["TransactionNo"].nunique()
        .nlargest(n).reset_index()
    )
    top.columns = ["Country", "Transactions"]
    top = top.sort_values("Transactions")
    n_bars = len(top)
    colors = [f"rgba(16,185,129,{0.35 + 0.6*i/max(n_bars-1,1):.2f})" for i in range(n_bars)]
    fig = go.Figure(go.Bar(
        y=top["Country"], x=top["Transactions"], orientation="h",
        marker=dict(color=colors, line=dict(width=0), cornerradius=4),
        text=[f"  {v:,}" for v in top["Transactions"]], textposition="outside",
        textfont=dict(size=11, family=FONT_MONO),
        hovertemplate="<b>%{y}</b><br>Transaksi: %{x:,}<extra></extra>",
    ))
    _fig_layout(fig, is_dark=is_dark, height=420,
                title=dict(text=f"<b>Top {n} Negara (Transaksi)</b>", font=dict(size=16), x=0.02),
                margin=dict(t=60, b=45, l=155, r=70),
                xaxis_title="Jumlah Transaksi")
    return fig


# ── Geographic ──

def build_choropleth(filtered, is_dark=False):
    t = DARK if is_dark else LIGHT
    geo = (
        filtered.groupby("Country")
        .agg(Revenue=("TotalAmount", "sum"),
             Transactions=("TransactionNo", "nunique"),
             Customers=("CustomerNo", "nunique"))
        .reset_index()
    )
    geo["ISO3"] = geo["Country"].map(COUNTRY_ISO3)
    geo = geo.dropna(subset=["ISO3"])
    geo["Hover"] = (
        "<b>" + geo["Country"] + "</b><br>"
        + "Revenue: £" + geo["Revenue"].apply(lambda v: f"{v:,.0f}") + "<br>"
        + "Transaksi: " + geo["Transactions"].apply(lambda v: f"{v:,}") + "<br>"
        + "Pelanggan: " + geo["Customers"].apply(lambda v: f"{v:,}")
    )
    fig = go.Figure(go.Choropleth(
        locations=geo["ISO3"], z=geo["Revenue"],
        text=geo["Hover"], hoverinfo="text",
        colorscale=[[0,"#eef2ff"],[0.15,"#c7d2fe"],[0.35,"#a5b4fc"],
                     [0.55,"#818cf8"],[0.75,"#6366f1"],[1,"#4338ca"]],
        colorbar=dict(title=dict(text="Revenue (£)", font=dict(size=11, color=t["plot_text"])),
                      tickprefix="£", tickformat=",.0f",
                      len=0.55, thickness=14, x=1.01,
                      tickfont=dict(color=t["plot_text"]),
                      bgcolor="rgba(0,0,0,0)", outlinewidth=0),
        marker_line_color="rgba(255,255,255,0.5)", marker_line_width=0.8,
    ))
    _fig_layout(fig, is_dark=is_dark, height=440,
                title=dict(text="<b>Distribusi Revenue Geografis</b>", font=dict(size=16), x=0.02),
                margin=dict(t=60, b=10, l=10, r=10),
                geo=dict(showframe=False, showcoastlines=True,
                         coastlinecolor=t["geo_coast"], coastlinewidth=0.5,
                         projection_type="natural earth",
                         bgcolor="rgba(0,0,0,0)",
                         landcolor=t["geo_land"], showlakes=False))
    return fig


def build_top_countries_rev(filtered, is_dark=False, n=10):
    top = (
        filtered.groupby("Country")["TotalAmount"].sum()
        .nlargest(n).reset_index()
    )
    top.columns = ["Country", "Revenue"]
    top = top.sort_values("Revenue")
    n_bars = len(top)
    colors = [f"rgba(99,102,241,{0.3 + 0.65*i/max(n_bars-1,1):.2f})" for i in range(n_bars)]
    fig = go.Figure(go.Bar(
        y=top["Country"], x=top["Revenue"], orientation="h",
        marker=dict(color=colors, line=dict(width=0), cornerradius=4),
        text=[f"  £{v:,.0f}" for v in top["Revenue"]], textposition="outside",
        textfont=dict(size=11, family=FONT_MONO),
        hovertemplate="<b>%{y}</b><br>Revenue: £%{x:,.0f}<extra></extra>",
    ))
    _fig_layout(fig, is_dark=is_dark, height=440,
                title=dict(text=f"<b>Top {n} Negara (Revenue)</b>", font=dict(size=16), x=0.02),
                margin=dict(t=60, b=45, l=145, r=90),
                xaxis_title="Revenue (£)", xaxis_tickprefix="£", xaxis_tickformat=",")
    return fig


# ── Cross-Segment Heatmap (Soal 5) ──

def build_cross_segment_heatmap(filtered, is_dark=False):
    t = DARK if is_dark else LIGHT
    cross = (
        filtered.groupby(["Customer_Segment", "Product_Segment"])["TotalAmount"]
        .sum().unstack(fill_value=0)
    )
    cross = cross.reindex(index=CUSTOMER_SEGMENTS, columns=PRODUCT_SEGMENTS).fillna(0)
    cross_pct = cross.div(cross.sum(axis=1), axis=0) * 100
    short_prod = [s.replace("Purchased", "Purch.").replace("Very ", "V.") for s in cross_pct.columns]
    short_cust = [s.replace("Customer", "").strip() for s in cross_pct.index]
    text = [[f"{cross_pct.iloc[i,j]:.1f}%<br>£{cross.iloc[i,j]:,.0f}"
             for j in range(len(cross_pct.columns))]
            for i in range(len(cross_pct.index))]
    fig = go.Figure(go.Heatmap(
        z=cross_pct.values,
        x=short_prod, y=short_cust,
        text=text, texttemplate="%{text}",
        textfont=dict(size=10, family=FONT, color=t["plot_text"] if not is_dark else "#e2e8f0"),
        colorscale=[[0,"#eef2ff"],[0.3,"#a5b4fc"],[0.6,"#6366f1"],[1,"#312e81"]],
        colorbar=dict(title=dict(text="% Revenue", font=dict(size=11, color=t["plot_text"])),
                      len=0.8, thickness=12, outlinewidth=0,
                      tickfont=dict(color=t["plot_text"])),
        hovertemplate="<b>%{y} × %{x}</b><br>%{text}<extra></extra>",
        xgap=3, ygap=3,
    ))
    _fig_layout(fig, is_dark=is_dark, height=380,
                title=dict(text="<b>Cross-Segment: Pelanggan × Produk (% Revenue)</b>",
                           font=dict(size=16), x=0.02),
                margin=dict(t=60, b=80, l=100, r=30))
    return fig


# ── RFM Deep Dive ──

def build_rfm_radar(rfm_df, filtered_cust_ids, is_dark=False):
    t = DARK if is_dark else LIGHT
    sub = rfm_df[rfm_df["CustomerNo"].isin(filtered_cust_ids)]
    seg_avg = sub.groupby("Segment")[["R", "F", "M"]].mean().reindex(CUSTOMER_SEGMENTS).dropna()
    if seg_avg.empty:
        return _empty_fig(is_dark)
    fig = go.Figure()
    for seg in seg_avg.index:
        row = seg_avg.loc[seg]
        fig.add_trace(go.Scatterpolar(
            r=[row["R"], row["F"], row["M"], row["R"]],
            theta=["Recency", "Frequency", "Monetary", "Recency"],
            fill='toself', name=seg,
            line=dict(color=COLORS_CUST[seg], width=2.5),
            fillcolor=_hex_to_rgba(COLORS_CUST[seg], 0.12),
            marker=dict(size=5),
        ))
    _fig_layout(fig, is_dark=is_dark, height=400,
                title=dict(text="<b>RFM Radar per Segment</b>", font=dict(size=16), x=0.02),
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 4.5],
                                    tickfont=dict(size=10), gridcolor=t["plot_grid"]),
                    angularaxis=dict(tickfont=dict(size=12, weight="bold")),
                    bgcolor="rgba(0,0,0,0)",
                ),
                showlegend=True,
                legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center",
                            font=dict(size=11)))
    return fig


def build_revenue_treemap(filtered, is_dark=False):
    agg = filtered.groupby(["Product_Segment", "ProductName"])["TotalAmount"].sum().reset_index()
    agg = agg.nlargest(60, "TotalAmount")
    if agg.empty:
        return _empty_fig(is_dark)
    fig = px.treemap(
        agg, path=["Product_Segment", "ProductName"], values="TotalAmount",
        color="TotalAmount",
        color_continuous_scale=[[0,"#c7d2fe"],[0.3,"#a5b4fc"],[0.6,"#6366f1"],[1,"#312e81"]],
    )
    fig.update_traces(
        textfont=dict(family=FONT, size=11),
        hovertemplate="<b>%{label}</b><br>Revenue: £%{value:,.0f}<br>%{percentRoot:.1%} of total<extra></extra>",
        marker=dict(cornerradius=4),
    )
    _fig_layout(fig, is_dark=is_dark, height=480,
                title=dict(text="<b>Revenue Treemap — Produk per Segment</b>", font=dict(size=16), x=0.02),
                margin=dict(t=60, b=10, l=10, r=10),
                coloraxis_showscale=False)
    return fig


def build_rfm_scatter(rfm_df, filtered_cust_ids, is_dark=False):
    sub = rfm_df[rfm_df["CustomerNo"].isin(filtered_cust_ids)].copy()
    if sub.empty:
        return _empty_fig(is_dark)
    fig = go.Figure()
    for seg in CUSTOMER_SEGMENTS:
        seg_data = sub[sub["Segment"] == seg]
        if seg_data.empty:
            continue
        fig.add_trace(go.Scatter(
            x=seg_data["Frequency"], y=seg_data["Monetary"],
            mode="markers", name=seg,
            marker=dict(
                color=COLORS_CUST[seg], size=7, opacity=0.7,
                line=dict(color="white", width=0.5),
            ),
            hovertemplate=(
                f"<b>{seg}</b><br>"
                "Frequency: %{x}<br>Monetary: £%{y:,.0f}<br>"
                "<extra></extra>"
            ),
        ))
    _fig_layout(fig, is_dark=is_dark, height=420,
                title=dict(text="<b>RFM Scatter — Frequency vs Monetary</b>", font=dict(size=16), x=0.02),
                xaxis_title="Frequency (Transaksi Unik)",
                yaxis_title="Monetary (£)", yaxis_tickprefix="£", yaxis_tickformat=",",
                legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center",
                            font=dict(size=11)))
    return fig


def build_customer_funnel(filtered, rfm_df, is_dark=False):
    cust_ids = filtered["CustomerNo"].unique()
    sub = rfm_df[rfm_df["CustomerNo"].isin(cust_ids)]
    seg_counts = sub["Segment"].value_counts().reindex(CUSTOMER_SEGMENTS).fillna(0)
    if seg_counts.sum() == 0:
        return _empty_fig(is_dark)
    fig = go.Figure(go.Funnel(
        y=seg_counts.index, x=seg_counts.values,
        textinfo="value+percent initial",
        textfont=dict(family=FONT_MONO, size=13),
        marker=dict(color=[COLORS_CUST[s] for s in seg_counts.index],
                    line=dict(width=1, color="white")),
        connector=dict(line=dict(color="rgba(99,102,241,0.2)", width=1)),
    ))
    _fig_layout(fig, is_dark=is_dark, height=350,
                title=dict(text="<b>Customer Funnel — Segment</b>", font=dict(size=16), x=0.02),
                margin=dict(t=60, b=30, l=180, r=30))
    return fig


def build_health_gauge(filtered, rfm_df, is_dark=False):
    t = DARK if is_dark else LIGHT
    cust_ids = filtered["CustomerNo"].unique()
    sub = rfm_df[rfm_df["CustomerNo"].isin(cust_ids)]
    seg_counts = sub["Segment"].value_counts()
    total = seg_counts.sum()
    loyal_active = seg_counts.get("Loyal Customer", 0) + seg_counts.get("Active Customer", 0)
    loyalty_rate = (loyal_active / total * 100) if total > 0 else 0
    rev_by_prod = filtered.groupby("ProductName")["TotalAmount"].sum()
    if rev_by_prod.sum() > 0:
        shares = rev_by_prod / rev_by_prod.sum()
        hhi = (shares ** 2).sum()
        diversity = (1 - hhi) * 100
    else:
        diversity = 0
    score = round(loyalty_rate * 0.6 + diversity * 0.4, 1)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(suffix="%", font=dict(size=42, family=FONT_MONO, color=t["text_primary"])),
        title=dict(text="Business Health Score",
                   font=dict(size=14, family=FONT, color=t["text_sec"])),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1, tickcolor=t["text_muted"],
                      tickfont=dict(size=10)),
            bgcolor="rgba(0,0,0,0)",
            bar=dict(color=PRIMARY, thickness=0.75),
            steps=[
                dict(range=[0, 35], color="rgba(239,68,68,0.1)"),
                dict(range=[35, 65], color="rgba(245,158,11,0.1)"),
                dict(range=[65, 100], color="rgba(16,185,129,0.1)"),
            ],
            threshold=dict(line=dict(color=SUCCESS, width=3), thickness=0.8, value=score),
        ),
    ))
    _fig_layout(fig, is_dark=is_dark, height=260, margin=dict(t=70, b=10, l=40, r=40))
    return fig


# ── Insight & Table helpers ──

def build_insight_bullets(filtered):
    best_m = filtered.groupby(filtered["Date"].dt.to_period("M"))["TotalAmount"].sum()
    best_month_str = best_m.idxmax().strftime("%B %Y")
    best_month_rev = best_m.max()
    top_cseg = filtered.groupby("Customer_Segment")["TotalAmount"].sum()
    top_cseg_name = top_cseg.idxmax()
    top_cseg_pct = top_cseg.max() / filtered["TotalAmount"].sum() * 100
    top_pseg = filtered.groupby("Product_Segment")["TotalAmount"].sum().idxmax()
    avg_qty = filtered.groupby("TransactionNo")["Quantity"].sum().mean()
    top_prod = filtered.groupby("ProductName")["Quantity"].sum()
    top_prod_name, top_prod_qty = top_prod.idxmax(), top_prod.max()
    top_cntry = filtered.groupby("Country")["TransactionNo"].nunique()
    top_cntry_name, top_cntry_txn = top_cntry.idxmax(), top_cntry.max()
    total_cust = filtered["CustomerNo"].nunique()
    return [
        f"Bulan revenue tertinggi: <b>{best_month_str}</b> (£{best_month_rev:,.0f})",
        f"Produk paling laku: <b>{top_prod_name}</b> ({top_prod_qty:,.0f} unit)",
        f"Segment pelanggan terbesar: <b>{top_cseg_name}</b> ({top_cseg_pct:.1f}% revenue)",
        f"Segment produk dominan: <b>{top_pseg}</b>",
        f"Rata-rata produk per transaksi: <b>{avg_qty:.1f}</b> item",
        f"Negara transaksi tertinggi: <b>{top_cntry_name}</b> ({top_cntry_txn:,} transaksi)",
        f"Total pelanggan aktif: <b>{total_cust:,}</b>",
    ]


def build_customer_table(filtered, rfm_df):
    cust_ids = filtered["CustomerNo"].unique()
    sub = rfm_df[rfm_df["CustomerNo"].isin(cust_ids)]
    tbl = (
        sub.groupby("Segment")
        .agg(Customers=("CustomerNo","count"), Avg_Recency=("Recency","mean"),
             Avg_Frequency=("Frequency","mean"), Avg_Monetary=("Monetary","mean"))
        .reindex(CUSTOMER_SEGMENTS).dropna().reset_index()
    )
    tbl["Avg_Recency"]   = tbl["Avg_Recency"].round(0).astype(int)
    tbl["Avg_Frequency"] = tbl["Avg_Frequency"].round(1)
    tbl["Avg_Monetary"]  = tbl["Avg_Monetary"].apply(lambda v: f"£{v:,.0f}")
    tbl.columns = ["Segment", "Jumlah", "Avg Recency (hari)", "Avg Frequency", "Avg Monetary"]
    return tbl


# ═══════════════════════════════════════════════════════════════════════════════
# RENDER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def render_kpi_cards(filtered, monthly_agg, d_min, d_max, is_dark=False):
    t = DARK if is_dark else LIGHT
    total_rev  = filtered["TotalAmount"].sum()
    total_txn  = filtered["TransactionNo"].nunique()
    total_prod = filtered["ProductName"].nunique()
    total_cust = filtered["CustomerNo"].nunique()
    aov        = total_rev / total_txn if total_txn else 0
    avg_txn_c  = total_txn / total_cust if total_cust else 0
    median_qty = filtered.groupby("TransactionNo")["Quantity"].sum().median()
    clv_avg    = total_rev / total_cust if total_cust else 0

    date_range_days = (d_max - d_min).days
    def _pct_chg(cur, prev):
        return ((cur - prev) / prev * 100) if prev != 0 else 0.0

    chg_rev = chg_txn = chg_prod = chg_cust = None
    if date_range_days > 30 and len(filtered) > 10:
        mid = d_min + pd.Timedelta(days=date_range_days // 2)
        h1 = filtered[filtered["Date"] < mid]
        h2 = filtered[filtered["Date"] >= mid]
        if len(h1) > 0 and len(h2) > 0:
            chg_rev  = _pct_chg(h2["TotalAmount"].sum(), h1["TotalAmount"].sum())
            chg_txn  = _pct_chg(h2["TransactionNo"].nunique(), h1["TransactionNo"].nunique())
            chg_prod = _pct_chg(h2["ProductName"].nunique(), h1["ProductName"].nunique())
            chg_cust = _pct_chg(h2["CustomerNo"].nunique(), h1["CustomerNo"].nunique())

    kpi_data = [
        ("Total Revenue",      f"£{total_rev:,.0f}",  "💰", PRIMARY, monthly_agg["sp_rev"].values if "sp_rev" in monthly_agg else [],  chg_rev),
        ("Total Transaksi",    f"{total_txn:,}",       "🛒", ACCENT,  monthly_agg["sp_txn"].values if "sp_txn" in monthly_agg else [],  chg_txn),
        ("Produk Unik",        f"{total_prod:,}",      "📦", INFO,    monthly_agg["sp_prod"].values if "sp_prod" in monthly_agg else [], chg_prod),
        ("Pelanggan",          f"{total_cust:,}",      "👥", SUCCESS, monthly_agg["sp_cust"].values if "sp_cust" in monthly_agg else [], chg_cust),
        ("Avg Order Value",    f"£{aov:,.0f}",         "📊", WARNING, monthly_agg["sp_aov"].values if "sp_aov" in monthly_agg else [],  None),
        ("Avg Txn / Customer", f"{avg_txn_c:,.1f}",    "🔄", ACCENT,  [],                            None),
        ("Median Qty / Txn",   f"{median_qty:,.0f}",   "📐", PINK,    [],                            None),
        ("Avg CLV",            f"£{clv_avg:,.0f}",     "💎", ORANGE,  [],                            None),
    ]

    cards_html = ""
    for i, (label, value, icon, accent, spark_vals, change) in enumerate(kpi_data):
        badge_html = ""
        if change is not None:
            is_up = change >= 0
            badge_cls = "up" if is_up else "down"
            badge_icon = "↑" if is_up else "↓"
            badge_html = (f'<div style="margin-top:6px;display:flex;justify-content:center;'
                          f'align-items:center;gap:4px;">'
                          f'<span class="kpi-badge {badge_cls}">{badge_icon} {abs(change):.1f}%</span>'
                          f'<span style="font-size:9px;color:{t["text_muted"]};">vs prev</span>'
                          f'</div>')

        sparkline_html = ""
        if len(spark_vals) > 1:
            sparkline_html = _svg_sparkline_html(list(spark_vals), accent)

        cards_html += (f'<div class="kpi-card" style="border-top:3px solid {accent};">'
                       f'<div class="kpi-icon" style="filter:drop-shadow(0 0 6px {_hex_to_rgba(accent, 0.4)})">{icon}</div>'
                       f'<div class="kpi-label">{label}</div>'
                       f'<div class="kpi-value">{value}</div>'
                       f'{badge_html}'
                       f'{sparkline_html}'
                       f'</div>')

    st.markdown(f'<div class="kpi-container">{cards_html}</div>', unsafe_allow_html=True)


def render_insight_panel(filtered, is_dark=False):
    t = DARK if is_dark else LIGHT
    bullets = build_insight_bullets(filtered)
    bullets_html = ""
    for b in bullets:
        bullets_html += (f'<div class="insight-bullet">'
                         f'<span class="insight-dot">•</span>'
                         f'<span>{b}</span>'
                         f'</div>')

    html = (f'<div class="insight-panel">'
            f'<div class="insight-header">'
            f'<span style="font-size:18px">💡</span>'
            f'<span class="insight-title">Insight Utama</span>'
            f'<span class="insight-count">{len(filtered):,} transaksi</span>'
            f'</div>'
            f'<div class="insight-grid">{bullets_html}</div>'
            f'</div>')
    st.markdown(html, unsafe_allow_html=True)


def render_business_interpretation(is_dark=False):
    t = DARK if is_dark else LIGHT
    html = (f'<div class="biz-card">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">'
            f'<span style="font-size:20px">💡</span>'
            f'<h4 style="margin:0;font-size:17px;font-weight:700;color:{t["text_primary"]};">Business Interpretation</h4>'
            f'</div>'
            f'<div class="biz-grid">'
            f'<div class="biz-item" style="background:rgba(99,102,241,0.04);border-color:rgba(99,102,241,0.1);">'
            f'<div class="biz-item-title" style="color:#6366f1;">📊 Strategi Revenue</div>'
            f'<p class="biz-item-text">Fokuskan promosi pada bulan-bulan dengan revenue rendah untuk meratakan pendapatan. Prioritaskan produk Frequently Purchased dan pelanggan Loyal untuk memaksimalkan ROI kampanye.</p>'
            f'</div>'
            f'<div class="biz-item" style="background:rgba(16,185,129,0.04);border-color:rgba(16,185,129,0.1);">'
            f'<div class="biz-item-title" style="color:#10b981;">👥 Retensi Pelanggan</div>'
            f'<p class="biz-item-text">Pelanggan Inactive dan Occasional membutuhkan program retensi khusus. Gunakan analisis RFM untuk personalisasi penawaran. Cross-segment analysis menunjukkan peluang cross-selling.</p>'
            f'</div>'
            f'<div class="biz-item" style="background:rgba(245,158,11,0.04);border-color:rgba(245,158,11,0.1);">'
            f'<div class="biz-item-title" style="color:#f59e0b;">🌍 Ekspansi Pasar</div>'
            f'<p class="biz-item-text">United Kingdom mendominasi pasar. Identifikasi negara potensial dengan AOV tinggi tetapi volume rendah untuk ekspansi. Perkuat distribusi di pasar inti Eropa.</p>'
            f'</div>'
            f'<div class="biz-item" style="background:rgba(236,72,153,0.04);border-color:rgba(236,72,153,0.1);">'
            f'<div class="biz-item-title" style="color:#ec4899;">📦 Optimasi Produk</div>'
            f'<p class="biz-item-text">Produk Very Rarely Purchased perlu evaluasi — pertimbangkan bundling atau discontinue. Produk unggulan dapat digunakan sebagai anchor untuk strategi upselling dan product recommendation.</p>'
            f'</div>'
            f'</div>'
            f'</div>')
    st.markdown(html, unsafe_allow_html=True)


def render_customer_table_html(tbl_df, is_dark=False):
    """Styled HTML table with gradient header — matching Dash version."""
    header = "".join(f"<th>{c}</th>" for c in tbl_df.columns)
    rows = ""
    for _, row in tbl_df.iterrows():
        cells = "".join(f"<td>{v}</td>" for v in row.values)
        rows += f"<tr>{cells}</tr>"
    html = f'<table class="styled-table"><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table>'
    st.markdown(html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # ── Session state init ──
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    is_dark = st.session_state.dark_mode

    # ── Inject all CSS ──
    inject_custom_css(is_dark)

    # ── Load data ──
    df_valid     = load_and_clean()
    prod_seg_map = segment_products(df_valid)
    rfm_data     = segment_customers(df_valid)
    df_dash      = build_dashboard_df(df_valid, prod_seg_map, rfm_data)

    DATE_MIN = df_dash["Date"].min()
    DATE_MAX = df_dash["Date"].max()
    ALL_COUNTRIES = sorted(df_dash["Country"].dropna().unique().tolist())

    # ═══════════════════════════════════════════════════════════════════
    # SIDEBAR
    # ═══════════════════════════════════════════════════════════════════

    with st.sidebar:
        # Brand with floating icon
        st.markdown(f'''
            <div style="margin-bottom:28px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="brand-icon">📊</div>
                    <div>
                        <div style="font-size:17px;font-weight:800;letter-spacing:-0.4px;
                                    color:{'#f1f5f9' if is_dark else '#0f172a'};">Sales Analytics</div>
                        <div style="display:flex;align-items:center;gap:6px;margin-top:2px;">
                            <span class="live-dot"></span>
                            <span style="font-size:11px;opacity:0.5;font-weight:500;
                                        color:{'#94a3b8' if is_dark else '#64748b'};">BI Dashboard</span>
                        </div>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

        # Dark/Light mode — single button click to toggle
        toggle_label = "☀️  Switch to Light Mode" if is_dark else "🌙  Switch to Dark Mode"
        if st.button(toggle_label, key="theme_toggle", use_container_width=True):
            st.session_state.dark_mode = not is_dark
            st.rerun()

        st.markdown("---")

        # Filters header
        st.markdown(f"""
            <div style="font-size:10px;font-weight:700;letter-spacing:1.2px;
                        text-transform:uppercase;opacity:0.35;display:flex;
                        align-items:center;gap:6px;margin-bottom:8px;
                        color:{'#94a3b8' if is_dark else '#64748b'};">
                <span style="font-size:12px">⚙</span> FILTERS
            </div>
        """, unsafe_allow_html=True)

        # Date range
        st.markdown("##### 📅 Rentang Tanggal")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Dari", value=DATE_MIN.date(),
                                        min_value=DATE_MIN.date(),
                                        max_value=DATE_MAX.date(),
                                        label_visibility="collapsed")
        with col2:
            end_date = st.date_input("Sampai", value=DATE_MAX.date(),
                                      min_value=DATE_MIN.date(),
                                      max_value=DATE_MAX.date(),
                                      label_visibility="collapsed")

        # Product segment
        prod_filter = st.selectbox(
            "📦 Segment Produk",
            options=["✦ Semua Segment"] + PRODUCT_SEGMENTS,
            index=0,
        )

        # Customer segment
        cust_filter = st.selectbox(
            "👥 Segment Pelanggan",
            options=["✦ Semua Segment"] + CUSTOMER_SEGMENTS,
            index=0,
        )

        # Country
        country_filter = st.selectbox(
            "🌍 Negara",
            options=["✦ Semua Negara"] + ALL_COUNTRIES,
            index=0,
        )

        st.markdown("---")

        # ── Filter info box (matching Dash version) ──
        d_min_disp = pd.Timestamp(start_date)
        d_max_disp = pd.Timestamp(end_date)
        p_lbl = prod_filter if prod_filter != "✦ Semua Segment" else "Semua"
        c_lbl = cust_filter if cust_filter != "✦ Semua Segment" else "Semua"
        g_lbl = country_filter if country_filter != "✦ Semua Negara" else "Semua"
        d_lbl = f"{d_min_disp:%d/%m/%Y} – {d_max_disp:%d/%m/%Y}"

        st.markdown(f'''
            <div class="filter-info">
                📦 {p_lbl}  ·  👥 {c_lbl}  ·  🌍 {g_lbl}<br>
                📅 {d_lbl}<br>
                📋 Filter aktif
            </div>
        ''', unsafe_allow_html=True)

        st.markdown("---")

        # Sidebar footer
        st.markdown(f"""
            <div style="font-size:10px;opacity:0.3;line-height:1.7;text-align:center;
                        color:{'#94a3b8' if is_dark else '#64748b'};">
                <div>Business Intelligence</div>
                <div>Universitas Islam Indonesia</div>
                <div>Februari 2026</div>
                <div style="margin-top:8px;">
                    <span style="font-size:9px;">Powered by </span>
                    <span style="font-size:9px;font-weight:700;">Streamlit + Plotly</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════
    # FILTERS
    # ═══════════════════════════════════════════════════════════════════

    d_min = pd.Timestamp(start_date)
    d_max = pd.Timestamp(end_date)
    filtered = df_dash[(df_dash["Date"] >= d_min) & (df_dash["Date"] <= d_max)]

    if prod_filter != "✦ Semua Segment":
        filtered = filtered[filtered["Product_Segment"] == prod_filter]
    if cust_filter != "✦ Semua Segment":
        filtered = filtered[filtered["Customer_Segment"] == cust_filter]
    if country_filter != "✦ Semua Negara":
        filtered = filtered[filtered["Country"] == country_filter]

    # ═══════════════════════════════════════════════════════════════════
    # HEADER — Animated gradient border
    # ═══════════════════════════════════════════════════════════════════

    st.markdown(f'''
        <div class="header-bar">
            <h1 class="gradient-title">Dashboard Sales Analytics</h1>
            <p class="header-subtitle">Business Intelligence  ·  Universitas Islam Indonesia</p>
        </div>
    ''', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════
    # EMPTY GUARD
    # ═══════════════════════════════════════════════════════════════════

    if len(filtered) == 0:
        st.markdown(f"""
            <div style="text-align:center;padding:60px 0;">
                <div style="font-size:48px;margin-bottom:12px;">🔍</div>
                <div style="font-size:18px;font-weight:700;color:#ef4444;">
                    Tidak ada data untuk filter ini.
                </div>
            </div>
        """, unsafe_allow_html=True)
        return

    # ═══════════════════════════════════════════════════════════════════
    # OVERVIEW SECTION
    # ═══════════════════════════════════════════════════════════════════

    st.markdown(f'''
        <div class="section-header">
            <span class="section-icon">📈</span>
            <h3 class="section-title">Overview</h3>
        </div>
        <p class="section-subtitle">Ringkasan metrik utama berdasarkan filter aktif</p>
    ''', unsafe_allow_html=True)

    # Insight panel
    render_insight_panel(filtered, is_dark)

    # KPI Cards
    monthly_agg = filtered.groupby("YearMonth").agg(
        sp_rev=("TotalAmount", "sum"),
        sp_txn=("TransactionNo", "nunique"),
        sp_prod=("ProductName", "nunique"),
        sp_cust=("CustomerNo", "nunique"),
    ).sort_index()
    monthly_agg["sp_aov"] = monthly_agg["sp_rev"] / monthly_agg["sp_txn"].replace(0, 1)

    render_kpi_cards(filtered, monthly_agg, d_min, d_max, is_dark)

    # ═══════════════════════════════════════════════════════════════════
    # TABS
    # ═══════════════════════════════════════════════════════════════════

    tab1, tab2, tab3 = st.tabs([
        "📊  Trend & Revenue",
        "🔍  Segmentasi & RFM",
        "🌍  Geographic & Strategy",
    ])

    plotly_cfg = {"displayModeBar": True, "displaylogo": False,
                  "toImageButtonOptions": {"format": "png", "scale": 2},
                  "modeBarButtonsToRemove": ["lasso2d", "select2d"]}

    # ── Tab 1: Trend & Revenue ──
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_trend_chart(filtered, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_distribution_chart(filtered, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_revenue_line(filtered, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_day_of_week_chart(filtered, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 2: Segmentasi & RFM ──
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_prod_pie(filtered, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_cust_bar(filtered, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_top_products(filtered, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:16px 20px 10px;font-size:16px;font-weight:700;color:{LIGHT['text_primary'] if not is_dark else DARK['text_primary']};'>Ringkasan Segment Pelanggan</h4>", unsafe_allow_html=True)
            tbl_df = build_customer_table(filtered, rfm_data)
            render_customer_table_html(tbl_df, is_dark)
            st.markdown('</div>', unsafe_allow_html=True)

        # Cross-segment heatmap
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(build_cross_segment_heatmap(filtered, is_dark), width='stretch', config=plotly_cfg)
        st.markdown('</div>', unsafe_allow_html=True)

        # RFM Deep Dive section
        st.markdown(f'''
            <div class="section-header">
                <span class="section-icon">🎯</span>
                <h3 class="section-title">RFM Deep Dive</h3>
            </div>
            <p class="section-subtitle">Analisis mendalam Recency, Frequency, Monetary</p>
        ''', unsafe_allow_html=True)

        cust_ids = filtered["CustomerNo"].unique()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_rfm_radar(rfm_data, cust_ids, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_rfm_scatter(rfm_data, cust_ids, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)

        # Customer Funnel + Revenue Treemap
        col1, col2 = st.columns([2, 3])
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_customer_funnel(filtered, rfm_data, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_revenue_treemap(filtered, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 3: Geographic & Strategy ──
    with tab3:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_choropleth(filtered, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(build_top_countries_rev(filtered, is_dark), width='stretch', config=plotly_cfg)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(build_top_countries(filtered, is_dark), width='stretch', config=plotly_cfg)
        st.markdown('</div>', unsafe_allow_html=True)

        # Business Strategy
        st.markdown(f'''
            <div class="section-header">
                <span class="section-icon">💡</span>
                <h3 class="section-title">Business Strategy</h3>
            </div>
            <p class="section-subtitle">Skor kesehatan bisnis & rekomendasi strategis</p>
        ''', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown('<div class="chart-card" style="display:flex;align-items:center;justify-content:center;">', unsafe_allow_html=True)
            st.plotly_chart(build_health_gauge(filtered, rfm_data, is_dark), width='stretch',
                          config={**plotly_cfg, "displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            render_business_interpretation(is_dark)

    # ═══════════════════════════════════════════════════════════════════
    # FOOTER
    # ═══════════════════════════════════════════════════════════════════

    st.markdown(f"""
        <div class="footer">
            <div class="footer-brand">
                <span style="font-size:14px;">📊</span>
                <span>Data: Sales Transaction v.4a.csv.gz</span>
            </div>
            <div style="font-weight:600;">
                Business Intelligence REMIDI — Universitas Islam Indonesia — Februari 2026
            </div>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
