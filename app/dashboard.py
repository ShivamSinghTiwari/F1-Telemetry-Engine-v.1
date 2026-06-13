import streamlit as st
import fastf1
import fastf1.plotting
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="F1 Telemetry Engine",
    page_icon="🏎",
    layout="wide",
    initial_sidebar_state="expanded",
)

fastf1.Cache.enable_cache("cache")

_TC = {
    "VER_2021":"#1E41FF","VER_2022":"#3671C6","VER_2023":"#3671C6",
    "VER_2024":"#3671C6","VER_2025":"#3671C6","VER_2026":"#3671C6",
    "PER_2021":"#1E41FF","PER_2022":"#3671C6","PER_2023":"#3671C6","PER_2024":"#3671C6",
    "HAM_2021":"#00D2BE","HAM_2022":"#00D2BE","HAM_2023":"#00D2BE","HAM_2024":"#27F4D2",
    "HAM_2025":"#E8002D","HAM_2026":"#E8002D",
    "RUS_2021":"#00D2BE","RUS_2022":"#00D2BE","RUS_2023":"#00D2BE",
    "RUS_2024":"#27F4D2","RUS_2025":"#27F4D2","RUS_2026":"#27F4D2",
    "BOT_2021":"#00D2BE","BOT_2022":"#C92D4B","BOT_2023":"#C92D4B",
    "BOT_2024":"#C92D4B","BOT_2025":"#C92D4B",
    "ANT_2025":"#27F4D2","ANT_2026":"#27F4D2",
    "LEC_2021":"#DC0000","LEC_2022":"#E8002D","LEC_2023":"#E8002D",
    "LEC_2024":"#E8002D","LEC_2025":"#E8002D","LEC_2026":"#E8002D",
    "SAI_2021":"#DC0000","SAI_2022":"#E8002D","SAI_2023":"#E8002D","SAI_2024":"#E8002D",
    "SAI_2025":"#64C4FF","SAI_2026":"#64C4FF",
    "BEA_2024":"#B6BABD","BEA_2025":"#B6BABD","BEA_2026":"#E8002D",
    "NOR_2021":"#FF8700","NOR_2022":"#FF8000","NOR_2023":"#FF8000",
    "NOR_2024":"#FF8000","NOR_2025":"#FF8000","NOR_2026":"#FF8000",
    "PIA_2023":"#FF8000","PIA_2024":"#FF8000","PIA_2025":"#FF8000","PIA_2026":"#FF8000",
    "RIC_2021":"#FF8700","RIC_2022":"#FF8000","RIC_2023":"#FF8000",
    "ALO_2021":"#006F62","ALO_2022":"#006F62","ALO_2023":"#358C75","ALO_2024":"#358C75",
    "ALO_2025":"#358C75","ALO_2026":"#358C75",
    "STR_2021":"#006F62","STR_2022":"#006F62","STR_2023":"#358C75","STR_2024":"#358C75",
    "STR_2025":"#358C75","STR_2026":"#358C75",
    "VET_2022":"#006F62","VET_2023":"#358C75",
    "GAS_2021":"#0090FF","GAS_2022":"#0090FF","GAS_2023":"#2293D1",
    "GAS_2024":"#2293D1","GAS_2025":"#2293D1","GAS_2026":"#2293D1",
    "OCO_2021":"#0090FF","OCO_2022":"#0090FF","OCO_2023":"#2293D1","OCO_2024":"#2293D1",
    "OCO_2025":"#2293D1","OCO_2026":"#B6BABD",
    "DOO_2025":"#2293D1","DOO_2026":"#2293D1",
    "COL_2025":"#2293D1","COL_2026":"#2293D1",
    "TSU_2021":"#399BB3","TSU_2022":"#399BB3","TSU_2023":"#5E8FAA",
    "TSU_2024":"#5E8FAA","TSU_2025":"#5E8FAA","TSU_2026":"#5E8FAA",
    "LAW_2023":"#5E8FAA","LAW_2024":"#5E8FAA","LAW_2025":"#5E8FAA",
    "HAD_2025":"#5E8FAA","HAD_2026":"#5E8FAA",
    "BOR_2026":"#5E8FAA","LIN_2026":"#5E8FAA",
    "ZHO_2022":"#C92D4B","ZHO_2023":"#C92D4B","ZHO_2024":"#C92D4B","ZHO_2026":"#C92D4B",
    "HUL_2023":"#B6BABD","HUL_2024":"#B6BABD","HUL_2025":"#C92D4B","HUL_2026":"#C92D4B",
    "MAG_2022":"#B6BABD","MAG_2023":"#B6BABD","MAG_2024":"#B6BABD","MAG_2025":"#B6BABD",
    "MSC_2022":"#B6BABD","MSC_2023":"#B6BABD",
    "ALB_2022":"#64C4FF","ALB_2023":"#64C4FF","ALB_2024":"#64C4FF",
    "ALB_2025":"#64C4FF","ALB_2026":"#64C4FF",
    "SAR_2023":"#64C4FF","SAR_2024":"#64C4FF",
    "SAN_2025":"#64C4FF","SAN_2026":"#64C4FF",
    "LAT_2021":"#37BEDD","LAT_2022":"#37BEDD",
    "CRE_2026":"#64C4FF",
}

DEFAULT_DRIVER_COLOR = "#AAAAAA"

TEAM_COLORS = {
    "VER":"#3671C6","PER":"#3671C6",
    "HAM":"#E8002D","RUS":"#27F4D2","ANT":"#27F4D2",
    "LEC":"#E8002D","SAI":"#64C4FF","BEA":"#E8002D",
    "NOR":"#FF8000","PIA":"#FF8000",
    "ALO":"#358C75","STR":"#358C75",
    "GAS":"#2293D1","OCO":"#B6BABD","DOO":"#2293D1","COL":"#2293D1",
    "TSU":"#5E8FAA","LAW":"#5E8FAA","HAD":"#5E8FAA","BOR":"#5E8FAA",
    "BOT":"#C92D4B","ZHO":"#C92D4B","HUL":"#C92D4B",
    "MAG":"#B6BABD",
    "ALB":"#64C4FF","SAR":"#64C4FF","SAN":"#64C4FF","CRE":"#64C4FF",
    "LIN":"#5E8FAA",
}

DRIVERS_BY_YEAR = {
    2021: ["VER","HAM","BOT","PER","LEC","SAI","NOR","RIC","ALO","GAS",
           "STR","OCO","RAI","GIO","TSU","LAT","MAZ","MSC","VET","KUB"],
    2022: ["VER","PER","LEC","SAI","HAM","RUS","NOR","RIC","ALO","OCO",
           "BOT","ZHO","STR","VET","GAS","ALO","MAG","MSC","ALB","LAT"],
    2023: ["VER","PER","ALO","HAM","SAI","RUS","NOR","PIA","LEC","STR",
           "GAS","OCO","TSU","LAW","MAG","HUL","ALB","SAR","BOT","ZHO"],
    2024: ["VER","PER","NOR","PIA","LEC","SAI","HAM","RUS","ALO","STR",
           "GAS","OCO","TSU","LAW","MAG","HUL","ALB","SAR","BOT","ZHO"],
    2025: ["VER","NOR","PIA","LEC","HAM","RUS","ANT","SAI","ALO","STR",
           "GAS","DOO","TSU","HAD","MAG","BEA","ALB","SAR","BOT","HUL"],
    2026: ["VER","NOR","PIA","LEC","BEA","HAM","RUS","ANT","ALO","STR",
           "GAS","COL","TSU","HAD","OCO","BOR","ALB","SAN","HUL","ZHO"],
}

DEFAULT_COLOR = "#FFFFFF"


def driver_color(drv: str, yr: int = None) -> str:
    if yr is not None:
        key = f"{drv.upper()}_{yr}"
        if key in _TC:
            return _TC[key]
    return TEAM_COLORS.get(drv.upper(), DEFAULT_DRIVER_COLOR)


def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def lighten_color(hex_color: str, factor: float = 0.45) -> str:
    """Mix hex_color with white by factor (0=original, 1=white).
    Used to distinguish Driver B when both drivers share the same team colour."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r2 = int(r + (255 - r) * factor)
    g2 = int(g + (255 - g) * factor)
    b2 = int(b + (255 - b) * factor)
    return f"#{r2:02x}{g2:02x}{b2:02x}"


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:ital,wght@0,200;0,300;0,400;0,600;0,700;0,900;1,400&family=JetBrains+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Titillium Web', sans-serif; }

.stApp {
    background: #050508;
    background-image:
        linear-gradient(rgba(225,6,0,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(225,6,0,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}
.block-container { padding-top: 4rem !important; padding-bottom: 2rem !important; max-width: 1440px; }

/* Hide the Streamlit top toolbar (Deploy button etc) */
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }

[data-testid="stSidebar"] {
    background: #070709 !important;
    border-right: 1px solid #1a1a24 !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.6) !important;
}
[data-testid="stSidebar"] * { color: #b0b0c8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stNumberInput label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem !important; letter-spacing: 0.18em !important;
    text-transform: uppercase !important; color: #444458 !important;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #e10600 0%, #a00400 100%) !important;
    color: white !important; border: none !important; border-radius: 3px !important;
    font-family: 'Titillium Web', sans-serif !important; font-weight: 700 !important;
    font-size: 0.8rem !important; letter-spacing: 0.18em !important;
    text-transform: uppercase !important; padding: 0.65rem 1rem !important;
    box-shadow: 0 0 20px rgba(225,6,0,0.25) !important; transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #ff2010 0%, #c00500 100%) !important;
    box-shadow: 0 0 30px rgba(225,6,0,0.45) !important;
    transform: translateY(-1px) !important;
}
.stSelectbox > div > div, .stTextInput > div > div > input {
    background: #0c0c12 !important; border: 1px solid #1c1c28 !important;
    border-radius: 3px !important; color: #d0d0e8 !important;
    font-family: 'Titillium Web', sans-serif !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #e10600 !important;
    box-shadow: 0 0 0 1px rgba(225,6,0,0.3), 0 0 12px rgba(225,6,0,0.1) !important;
}
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0d0d16 0%, #0a0a10 100%) !important;
    border: 1px solid #1a1a26 !important; border-top: 2px solid #e10600 !important;
    border-radius: 4px !important; padding: 1rem 1.2rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03) !important;
}
[data-testid="metric-container"] label {
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.58rem !important;
    letter-spacing: 0.2em !important; text-transform: uppercase !important; color: #444458 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Titillium Web', sans-serif !important; font-size: 1.8rem !important;
    font-weight: 700 !important; color: #f0f0ff !important; line-height: 1.1 !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important; border-bottom: 1px solid #1a1a24 !important; gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Titillium Web', sans-serif !important; font-size: 0.72rem !important;
    font-weight: 700 !important; letter-spacing: 0.15em !important; text-transform: uppercase !important;
    color: #333344 !important; border-bottom: 2px solid transparent !important;
    padding: 0.7rem 1.4rem !important; background: transparent !important; transition: all 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #888898 !important; background: rgba(225,6,0,0.05) !important; }
.stTabs [aria-selected="true"] {
    color: #f0f0ff !important; border-bottom-color: #e10600 !important;
    background: linear-gradient(180deg, rgba(225,6,0,0.08) 0%, transparent 100%) !important;
}
.section-header {
    font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; font-weight: 500;
    letter-spacing: 0.25em; text-transform: uppercase; color: #333344;
    margin: 1.8rem 0 0.8rem; padding-bottom: 0.5rem; border-bottom: 1px solid #0f0f18;
    display: flex; align-items: center; gap: 8px;
}
.section-header::before {
    content: ''; display: inline-block; width: 16px; height: 1px;
    background: #e10600; flex-shrink: 0;
}
.page-title {
    font-family: 'Titillium Web', sans-serif; font-size: 2.8rem; font-weight: 900;
    letter-spacing: -0.02em; color: #f0f0ff; line-height: 0.95; margin-bottom: 0.15rem;
    text-shadow: 0 0 40px rgba(225,6,0,0.2);
}
.page-title span { color: #e10600; }
.page-subtitle {
    font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #2a2a38;
    margin-bottom: 1.5rem; letter-spacing: 0.2em; text-transform: uppercase;
}
.info-box {
    background: linear-gradient(90deg, rgba(225,6,0,0.06) 0%, rgba(0,0,0,0) 100%);
    border: 1px solid #1a1a26; border-left: 3px solid #e10600; border-radius: 3px;
    padding: 0.85rem 1.1rem; font-size: 0.8rem; color: #666678;
    margin: 0.5rem 0 1.2rem; font-family: 'Titillium Web', sans-serif;
}
.stSuccess {
    background: rgba(0,180,80,0.08) !important; border: 1px solid rgba(0,180,80,0.2) !important;
    border-left: 3px solid #00b450 !important; border-radius: 3px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important; color: #00b450 !important;
}
.stWarning {
    background: rgba(255,160,0,0.08) !important; border: 1px solid rgba(255,160,0,0.2) !important;
    border-left: 3px solid #ffa000 !important; border-radius: 3px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important;
}
.stError {
    background: rgba(225,6,0,0.08) !important; border: 1px solid rgba(225,6,0,0.25) !important;
    border-left: 3px solid #e10600 !important; border-radius: 3px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important;
}
.stSpinner > div { border-top-color: #e10600 !important; }
[data-testid="stDataFrame"] { border: 1px solid #1a1a24 !important; border-radius: 4px !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #050508; }
::-webkit-scrollbar-thumb { background: #1a1a28; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #e10600; }
.stRadio > label {
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.65rem !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important; color: #555570 !important;
}
hr { border-color: #0f0f18 !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)


PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#06060c",
    font=dict(family="'Titillium Web', sans-serif", color="#444458", size=11),
    title_font=dict(family="'Titillium Web', sans-serif", size=14, color="#c8c8d8"),
    legend=dict(
        bgcolor="rgba(6,6,12,0.9)", bordercolor="#141420", borderwidth=1,
        font=dict(size=11, family="'Titillium Web', sans-serif", color="#888898"),
        orientation="h", y=1.02, x=1, xanchor="right",
    ),
    xaxis=dict(
        gridcolor="#0c0c14", linecolor="#141420", tickcolor="#141420",
        tickfont=dict(size=10, color="#2a2a38", family="'JetBrains Mono', monospace"),
        zerolinecolor="#1a1a28", showgrid=True,
    ),
    yaxis=dict(
        gridcolor="#0c0c14", linecolor="#141420", tickcolor="#141420",
        tickfont=dict(size=10, color="#2a2a38", family="'JetBrains Mono', monospace"),
        zerolinecolor="#1a1a28", showgrid=True,
    ),
    margin=dict(l=55, r=20, t=50, b=50),
    hoverlabel=dict(
        bgcolor="#0d0d18", bordercolor="#1a1a28",
        font=dict(family="'JetBrains Mono', monospace", size=11, color="#c8c8d8"),
    ),
)


def apply_theme(fig, title=""):
    fig.update_layout(**PLOT_LAYOUT, title=title)
    return fig


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.2rem 0 1.4rem; border-bottom:1px solid #111118; margin-bottom:1.4rem;'>
        <div style='display:flex; align-items:flex-start; gap:10px;'>
            <div style='width:3px; height:48px; background:linear-gradient(180deg,#e10600,#600000);
                        border-radius:2px; flex-shrink:0; margin-top:2px;'></div>
            <div>
                <div style='font-family:"Titillium Web",sans-serif; font-size:1.5rem; font-weight:900;
                            color:#f0f0ff; letter-spacing:-0.01em; line-height:1;'>F1 TELEMETRY</div>
                <div style='font-family:"Titillium Web",sans-serif; font-size:1.5rem; font-weight:900;
                            color:#e10600; letter-spacing:-0.01em; line-height:1;'>ENGINE</div>
                <div style='font-family:"JetBrains Mono",monospace; font-size:0.55rem;
                            color:#252530; letter-spacing:0.22em; margin-top:5px; text-transform:uppercase;'>
                    POWERED BY FASTF1</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Session</div>', unsafe_allow_html=True)

    year = st.selectbox("Year", [2026, 2025, 2024, 2023, 2022, 2021], index=0)

    RACES = [
        "Bahrain", "Saudi Arabia", "Australia", "Japan", "China",
        "Miami", "Emilia Romagna", "Monaco", "Canada", "Spain",
        "Austria", "British", "Hungary", "Belgium", "Netherlands",
        "Italy", "Azerbaijan", "Singapore", "United States", "Mexico City",
        "São Paulo", "Las Vegas", "Qatar", "Abu Dhabi", "Madrid",
        # 2026 only — Barcelona uses a different FastF1 event name
        "Barcelona-Catalunya",
    ]
    race = st.selectbox("Grand Prix", RACES, index=0)
    session_type = st.selectbox(
        "Session", ["Q", "R", "FP1", "FP2", "FP3", "S", "SS"],
        format_func=lambda x: {"Q":"Qualifying","R":"Race","FP1":"Practice 1",
                                "FP2":"Practice 2","FP3":"Practice 3",
                                "S":"Sprint","SS":"Sprint Shootout"}.get(x, x)
    )

    st.markdown('<div class="section-header">Session A — Driver A</div>', unsafe_allow_html=True)
    DRIVERS = DRIVERS_BY_YEAR.get(year, DRIVERS_BY_YEAR[2025])
    driver1 = st.selectbox("Driver A", DRIVERS, index=0)

    st.markdown("<br>", unsafe_allow_html=True)
    load_btn = st.button("⬤  Load Session A", use_container_width=True)

    st.markdown('<div class="section-header">Session B — Driver B</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:"JetBrains Mono",monospace; font-size:0.58rem; color:#333344;
                letter-spacing:0.1em; margin-bottom:8px;'>
        Leave same as Session A to compare two drivers in one session.
        Change to compare across sessions.
    </div>
    """, unsafe_allow_html=True)

    year_b = st.selectbox("Year B", [2026, 2025, 2024, 2023, 2022, 2021],
                          index=[2026,2025,2024,2023,2022,2021].index(year), key="year_b")
    race_b = st.selectbox("Grand Prix B", RACES,
                          index=RACES.index(race) if race in RACES else 0, key="race_b")
    session_type_b = st.selectbox(
        "Session B", ["Q", "R", "FP1", "FP2", "FP3", "S", "SS"],
        format_func=lambda x: {"Q":"Qualifying","R":"Race","FP1":"Practice 1",
                                "FP2":"Practice 2","FP3":"Practice 3",
                                "S":"Sprint","SS":"Sprint Shootout"}.get(x, x),
        key="session_type_b",
    )
    DRIVERS_B = DRIVERS_BY_YEAR.get(year_b, DRIVERS_BY_YEAR[2025])
    driver2 = st.selectbox("Driver B", DRIVERS_B, index=min(1, len(DRIVERS_B)-1), key="driver2_b")

    load_btn_b = st.button("⬤  Load Session B", use_container_width=True)

    st.markdown("""
    <div style='margin-top:2rem; padding-top:1.2rem; border-top:1px solid #0f0f18;'>
        <div style='font-family:"JetBrains Mono",monospace; font-size:0.52rem;
                    color:#1c1c28; letter-spacing:0.12em; text-transform:uppercase; line-height:1.8;'>
            DATA © Formula One Management<br>Analysis via FastF1<br>─────────────────
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Page header ────────────────────────────────────────────────────────────────
current_key   = f"{year}_{race}_{session_type}"
current_key_b = f"{year_b}_{race_b}_{session_type_b}"
_cross_session = (current_key != current_key_b and st.session_state.session_b is not None)
_subtitle = (f"◈ &nbsp; {year} &nbsp;·&nbsp; {race.upper()} &nbsp;·&nbsp; {session_type}"
             + (f"  &nbsp;vs&nbsp;  {year_b} &nbsp;·&nbsp; {race_b.upper()} &nbsp;·&nbsp; {session_type_b}"
                if _cross_session else ""))

st.markdown(f"""
<div style='display:flex; align-items:flex-end; justify-content:space-between;
            border-bottom:1px solid #0f0f18; padding-bottom:1rem; margin-bottom:0.2rem;'>
    <div>
        <div class="page-title">TELEMETRY <span>ENGINE</span></div>
        <div class="page-subtitle">{_subtitle}</div>
    </div>
    <div style='text-align:right; padding-bottom:4px;'>
        <div style='font-family:"JetBrains Mono",monospace; font-size:0.6rem;
                    color:#1e1e2a; letter-spacing:0.15em; text-transform:uppercase;'>FastF1 v3</div>
        <div style='font-family:"JetBrains Mono",monospace; font-size:0.58rem;
                    color:#1a1a24; letter-spacing:0.1em; margin-top:2px;'>Real-time telemetry</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── State ──────────────────────────────────────────────────────────────────────
if "session" not in st.session_state:
    st.session_state.session = None
if "session_b" not in st.session_state:
    st.session_state.session_b = None
if "loaded_key" not in st.session_state:
    st.session_state.loaded_key = None
if "loaded_key_b" not in st.session_state:
    st.session_state.loaded_key_b = None

if load_btn:
    with st.spinner("Loading Session A…"):
        try:
            # 2026 Barcelona uses "Barcelona-Catalunya" in the dropdown
            # but FastF1 indexes it as "Spanish Grand Prix" or "Spain"
            _race_name = race
            if year == 2026 and race == "Barcelona-Catalunya":
                _race_name = "Spain"
            sess = fastf1.get_session(year, _race_name, session_type)
            sess.load()
            st.session_state.session = sess
            st.session_state.loaded_key = current_key
        except Exception as e:
            # Clear stale session so the landing page shows instead of crashing
            st.session_state.session = None
            st.error(f"Session A failed to load: {e}")

if load_btn_b:
    with st.spinner("Loading Session B…"):
        try:
            sess_b = fastf1.get_session(year_b, race_b, session_type_b)
            sess_b.load()
            st.session_state.session_b = sess_b
            st.session_state.loaded_key_b = current_key_b
        except Exception as e:
            st.session_state.session_b = None
            st.error(f"Session B failed to load: {e}")

session   = st.session_state.session
session_b = st.session_state.session_b if st.session_state.session_b is not None else session

# ── Landing page — shown whenever no session is loaded ────────────────────────
if session is None:
    # Status row showing what has/hasn't been loaded
    status_a = f"✓  {st.session_state.loaded_key.replace('_',' · ')}" if st.session_state.loaded_key else "Not loaded"
    status_b = f"✓  {st.session_state.loaded_key_b.replace('_',' · ')}" if st.session_state.loaded_key_b else "Same as A"

    st.markdown(f"""
    <div style='display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:1.5rem 0;'>
        <div style='background:#0a0a10; border:1px solid #141420; border-left:3px solid #e10600;
                    border-radius:3px; padding:1rem 1.2rem;'>
            <div style='font-family:"JetBrains Mono",monospace; font-size:0.58rem;
                        color:#444458; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:6px;'>
                Session A</div>
            <div style='font-family:"Titillium Web",sans-serif; font-size:0.95rem;
                        font-weight:700; color:#c8c8d8;'>{status_a}</div>
            <div style='font-family:"Titillium Web",sans-serif; font-size:0.75rem;
                        color:#333344; margin-top:4px;'>Select year, GP and session in the sidebar → Load Session A</div>
        </div>
        <div style='background:#0a0a10; border:1px solid #141420; border-left:3px solid #ffc906;
                    border-radius:3px; padding:1rem 1.2rem;'>
            <div style='font-family:"JetBrains Mono",monospace; font-size:0.58rem;
                        color:#444458; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:6px;'>
                Session B</div>
            <div style='font-family:"Titillium Web",sans-serif; font-size:0.95rem;
                        font-weight:700; color:#c8c8d8;'>{status_b}</div>
            <div style='font-family:"Titillium Web",sans-serif; font-size:0.75rem;
                        color:#333344; margin-top:4px;'>Optional — load a second session to compare across FP1/FP2/Q/R</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    tiles = [
        ("01", "Speed Trace", "Multi-channel telemetry overlay with throttle, brake & gear", "#3671C6"),
        ("02", "Delta Time", "Shaded gap chart with speed and throttle comparison", "#e10600"),
        ("03", "Race Tracker", "Animated GPS map of all drivers across the full race", "#FF8000"),
        ("04", "Track Maps", "Speed heatmap and racing line comparison", "#27F4D2"),
    ]
    for col, (num, title, desc, clr) in zip(cols, tiles):
        with col:
            st.markdown(f"""
            <div style='background:#0a0a10; border:1px solid #111118; border-top:2px solid {clr};
                        border-radius:3px; padding:1.2rem 1rem; height:130px; position:relative;
                        overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.3);'>
                <div style='position:absolute; top:0.8rem; right:0.8rem;
                            font-family:"JetBrains Mono",monospace; font-size:1.4rem;
                            font-weight:700; color:#0f0f18;'>{num}</div>
                <div style='font-family:"Titillium Web",sans-serif; font-size:0.85rem;
                            font-weight:700; color:{clr}; letter-spacing:0.08em;
                            text-transform:uppercase; margin-bottom:0.4rem;'>{title}</div>
                <div style='font-family:"Titillium Web",sans-serif; font-size:0.72rem;
                            color:#2a2a38; line-height:1.4;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    st.stop()

# Show a persistent status bar when a session is loaded
loaded_key_display = st.session_state.loaded_key.replace("_", " · ") if st.session_state.loaded_key else ""
loaded_key_b_display = st.session_state.loaded_key_b.replace("_", " · ") if st.session_state.loaded_key_b else ""
_b_badge = (f"  <span style='color:#ffc906;'>·  B: {loaded_key_b_display}</span>"
            if loaded_key_b_display and loaded_key_b_display != loaded_key_display else "")

st.markdown(f"""
<div style='display:flex; align-items:center; gap:10px; padding:6px 14px;
            background:#0a0a10; border:1px solid #141420; border-radius:3px;
            margin-bottom:1rem; font-family:"JetBrains Mono",monospace; font-size:0.65rem;'>
    <span style='color:#00b450;'>✓</span>
    <span style='color:#555570;'>A: {loaded_key_display}{_b_badge}</span>
</div>
""", unsafe_allow_html=True)

try:
    laps = session.laps
    if laps is None:
        raise ValueError("No laps data")
except Exception as _laps_err:
    st.error(f"Session data is incomplete or corrupted — please reload Session A. ({_laps_err})")
    st.session_state.session = None
    st.stop()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  Overview  ",
    "  Driver Comparison  ",
    "  Delta Time  ",
    "  Track Maps  ",
    "  Race Tracker  ",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Session Summary</div>', unsafe_allow_html=True)

    results = session.results if hasattr(session, "results") else None

    fastest = laps.pick_fastest()
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Fastest Driver", fastest["Driver"])
    with m2:
        lap_time = fastest["LapTime"]
        lap_str = str(lap_time).split(".")
        st.metric("Fastest Lap", f"{lap_str[0][-5:]}.{lap_str[1][:3]}" if "." in str(lap_time) else str(lap_time))
    with m3:
        st.metric("Total Laps", len(laps))
    with m4:
        st.metric("Drivers", laps["Driver"].nunique())

    st.markdown('<div class="section-header">Lap Time Distribution</div>', unsafe_allow_html=True)

    valid = laps.dropna(subset=["LapTime"])
    valid = valid[valid["LapTime"].dt.total_seconds() > 0].copy()
    valid["LapTimeSec"] = valid["LapTime"].dt.total_seconds()
    valid = valid[valid["LapTimeSec"] < valid["LapTimeSec"].quantile(0.95)]

    driver_medians = valid.groupby("Driver")["LapTimeSec"].median().sort_values(ascending=True)
    fig_dist = go.Figure()
    for drv in driver_medians.index:
        d = valid[valid["Driver"] == drv]["LapTimeSec"]
        fig_dist.add_trace(go.Box(
            y=d, name=drv,
            marker_color=driver_color(drv, year),
            line_color=driver_color(drv, year),
            fillcolor=hex_to_rgba(driver_color(drv, year), 0.13),
            boxpoints="outliers", marker_size=3,
        ))
    apply_theme(fig_dist, "Lap Time Distribution by Driver — sorted by median")
    fig_dist.update_layout(height=380, showlegend=False, yaxis_title="Lap Time (s)")
    st.plotly_chart(fig_dist, use_container_width=True)

    if results is not None and not results.empty:
        st.markdown('<div class="section-header">Session Results</div>', unsafe_allow_html=True)

        def fmt_laptime(val):
            try:
                if val is None or pd.isna(val): return "—"
                s = val.total_seconds() if hasattr(val, "total_seconds") else float(val)
                if s <= 0: return "—"
                m = int(s // 60)
                return f"{m}:{s % 60:06.3f}"
            except Exception:
                return "—"

        def fmt_gap(val):
            try:
                if val is None or pd.isna(val): return "DNF"
                s = val.total_seconds() if hasattr(val, "total_seconds") else float(val)
                if s <= 0: return "DNF"
                return f"+{s:.3f}" if s < 60 else f"+{int(s//60)}:{s%60:06.3f}"
            except Exception:
                return "DNF"

        def fmt_race_time(val):
            try:
                if val is None or pd.isna(val): return "DNF"
                s = val.total_seconds() if hasattr(val, "total_seconds") else float(val)
                if s <= 0: return "DNF"
                h = int(s // 3600); m = int((s % 3600) // 60); sec = s % 60
                return f"{h}:{m:02d}:{sec:06.3f}" if h > 0 else f"{m}:{sec:06.3f}"
            except Exception:
                return "DNF"

        is_race     = session_type in ("R", "S")
        is_quali    = session_type in ("Q", "SQ", "SS")
        is_practice = session_type in ("FP1", "FP2", "FP3")

        if is_race:
            cols_show = [c for c in ["Position","Abbreviation","FullName","TeamName","Time","Points"] if c in results.columns]
            display_results = results[cols_show].copy().reset_index(drop=True)
            if "Time" in display_results.columns and "Position" in display_results.columns:
                formatted_times = []
                for _, row in display_results.iterrows():
                    try:
                        pos_int = int(row["Position"])
                    except Exception:
                        formatted_times.append("DNF"); continue
                    formatted_times.append(fmt_race_time(row["Time"]) if pos_int == 1 else fmt_gap(row["Time"]))
                display_results["Time"] = formatted_times

        elif is_quali:
            q_cols = [c for c in ["Q1","Q2","Q3"] if c in results.columns]
            cols_show = [c for c in ["Position","Abbreviation","FullName","TeamName"] + q_cols if c in results.columns]
            display_results = results[cols_show].copy().reset_index(drop=True)
            if q_cols:
                for qc in q_cols:
                    display_results[qc] = display_results[qc].apply(fmt_laptime)
            else:
                drv_best = laps[laps["LapTime"].notna()].groupby("Driver")["LapTime"].min().reset_index()
                drv_best.columns = ["Abbreviation","Best Lap"]
                display_results = display_results.merge(drv_best, on="Abbreviation", how="left")
                display_results["Best Lap"] = display_results["Best Lap"].apply(fmt_laptime)
            try:
                p1_best = laps[laps["Driver"] == results.iloc[0]["Abbreviation"]]["LapTime"].min()
                p1_s = p1_best.total_seconds()
                def calc_gap(abbr):
                    drv_t = laps[laps["Driver"] == abbr]["LapTime"]
                    if drv_t.empty or drv_t.isna().all(): return "No time"
                    best_s = drv_t.min().total_seconds()
                    diff = best_s - p1_s
                    if diff <= 0.001: return fmt_laptime(p1_best)
                    return f"+{diff:.3f}" if diff < 60 else f"+{int(diff//60)}:{diff%60:06.3f}"
                display_results["Gap"] = display_results["Abbreviation"].apply(calc_gap)
            except Exception:
                pass

        elif is_practice:
            drv_best = laps[laps["LapTime"].notna()].groupby("Driver")["LapTime"].min().reset_index()
            drv_best.columns = ["Abbreviation","BestLapTime"]
            drv_best = drv_best.sort_values("BestLapTime").reset_index(drop=True)
            drv_best["Position"] = range(1, len(drv_best) + 1)
            meta_cols = [c for c in ["Abbreviation","FullName","TeamName"] if c in results.columns]
            display_results = drv_best.merge(results[meta_cols], on="Abbreviation", how="left")
            display_results = display_results[["Position","Abbreviation"] + [c for c in ["FullName","TeamName"] if c in display_results.columns] + ["BestLapTime"]].copy()
            display_results["Best Lap"] = display_results["BestLapTime"].apply(fmt_laptime)
            p1_s = display_results["BestLapTime"].iloc[0].total_seconds()
            def fp_gap(val):
                try:
                    s = val.total_seconds(); diff = s - p1_s
                    if diff <= 0.001: return "—"
                    return f"+{diff:.3f}" if diff < 60 else f"+{int(diff//60)}:{diff%60:06.3f}"
                except Exception: return "—"
            display_results["Gap"] = display_results["BestLapTime"].apply(fp_gap)
            display_results = display_results.drop(columns=["BestLapTime"])
        else:
            cols_show = [c for c in ["Position","Abbreviation","FullName","TeamName","Time","Points"] if c in results.columns]
            display_results = results[cols_show].copy().reset_index(drop=True)

        st.dataframe(display_results.reset_index(drop=True), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DRIVER COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Lap Selection</div>', unsafe_allow_html=True)

    def build_lap_options(driver: str, src_laps):
        """Build lap picker options from a given laps DataFrame (session A or B)."""
        drv_laps = src_laps.pick_drivers(driver).copy()
        drv_laps = drv_laps[drv_laps["LapTime"].notna()].reset_index(drop=True)
        options = {}
        for idx, row in drv_laps.iterrows():
            lap_num  = int(row["LapNumber"]) if pd.notna(row["LapNumber"]) else "?"
            lt       = row["LapTime"]
            lt_str   = f"{int(lt.total_seconds()//60)}:{lt.total_seconds()%60:06.3f}" if pd.notna(lt) else "N/A"
            compound = row.get("Compound", "?") or "?"
            stint    = int(row["Stint"]) if pd.notna(row.get("Stint")) else "?"
            label    = f"Lap {lap_num:>3}  ·  {lt_str}  ·  {compound}  ·  Stint {stint}"
            options[label] = idx
        return drv_laps, options

    # Session B status indicator
    _sess_b_loaded = st.session_state.session_b is not None
    _cross = (current_key != current_key_b and _sess_b_loaded)
    if _cross:
        st.markdown(f"""<div style='font-family:"JetBrains Mono",monospace; font-size:0.62rem;
            color:#ffc906; letter-spacing:0.12em; margin-bottom:8px;'>
            ◈  Cross-session mode  ·  A: {session_type} &nbsp;|&nbsp; B: {session_type_b}
        </div>""", unsafe_allow_html=True)

    laps_b_src = session_b.laps if _sess_b_loaded else laps

    try:
        drv_laps_a, opts_a = build_lap_options(driver1, laps)
        drv_laps_b, opts_b = build_lap_options(driver2, laps_b_src)
    except Exception as e:
        st.warning(f"Could not build lap list: {e}")
        drv_laps_a, opts_a, drv_laps_b, opts_b = None, {}, None, {}

    col_pick_a, col_pick_b = st.columns(2)

    if opts_a and opts_b:
        def fastest_label(drv_laps, opts):
            try:
                fl = drv_laps.loc[drv_laps["LapTime"].idxmin()]
                lap_num  = int(fl["LapNumber"]) if pd.notna(fl["LapNumber"]) else "?"
                lt       = fl["LapTime"]
                lt_str   = f"{int(lt.total_seconds()//60)}:{lt.total_seconds()%60:06.3f}"
                compound = fl.get("Compound", "?") or "?"
                stint    = int(fl["Stint"]) if pd.notna(fl.get("Stint")) else "?"
                return f"Lap {lap_num:>3}  ·  {lt_str}  ·  {compound}  ·  Stint {stint}"
            except Exception:
                return list(opts.keys())[0]

        label_list_a = list(opts_a.keys())
        label_list_b = list(opts_b.keys())
        default_a    = fastest_label(drv_laps_a, opts_a)
        default_b    = fastest_label(drv_laps_b, opts_b)
        def_idx_a    = label_list_a.index(default_a) if default_a in label_list_a else 0
        def_idx_b    = label_list_b.index(default_b) if default_b in label_list_b else 0

        with col_pick_a:
            st.markdown(f"""<div style='font-family:"JetBrains Mono",monospace; font-size:0.62rem;
                        color:{driver_color(driver1, year)}; letter-spacing:0.15em;
                        text-transform:uppercase; margin-bottom:4px;'>● {driver1}</div>""",
                        unsafe_allow_html=True)
            sel_a = st.selectbox("Lap A", label_list_a, index=def_idx_a,
                                  key="lap_sel_a", label_visibility="collapsed")

        with col_pick_b:
            st.markdown(f"""<div style='font-family:"JetBrains Mono",monospace; font-size:0.62rem;
                        color:{driver_color(driver2, year)}; letter-spacing:0.15em;
                        text-transform:uppercase; margin-bottom:4px;'>● {driver2}</div>""",
                        unsafe_allow_html=True)
            sel_b = st.selectbox("Lap B", label_list_b, index=def_idx_b,
                                  key="lap_sel_b", label_visibility="collapsed")

        try:
            lap_a = drv_laps_a.loc[opts_a[sel_a]]
            lap_b = drv_laps_b.loc[opts_b[sel_b]]
            tel_a = lap_a.get_telemetry().add_distance()
            tel_b = lap_b.get_telemetry().add_distance()

            st.markdown('<div class="section-header">Lap Summary</div>', unsafe_allow_html=True)
            m1, m2, m3, m4, m5, m6 = st.columns(6)
            def fmt_time(lt):
                if pd.isna(lt): return "N/A"
                s = lt.total_seconds()
                return f"{int(s//60)}:{s%60:06.3f}"

            with m1: st.metric(f"{driver1} · Lap Time", fmt_time(lap_a["LapTime"]))
            with m2: st.metric(f"{driver2} · Lap Time", fmt_time(lap_b["LapTime"]))
            with m3:
                gap = (lap_b["LapTime"] - lap_a["LapTime"]).total_seconds() if pd.notna(lap_a["LapTime"]) and pd.notna(lap_b["LapTime"]) else None
                st.metric("Gap", f"{gap:+.3f}s" if gap is not None else "N/A")
            with m4: st.metric(f"{driver1} · Compound", lap_a.get("Compound","?") or "?")
            with m5: st.metric(f"{driver2} · Compound", lap_b.get("Compound","?") or "?")
            with m6:
                lap_num_a = int(lap_a["LapNumber"]) if pd.notna(lap_a["LapNumber"]) else "?"
                lap_num_b = int(lap_b["LapNumber"]) if pd.notna(lap_b["LapNumber"]) else "?"
                st.metric("Laps", f"{lap_num_a}  vs  {lap_num_b}")

            st.markdown('<div class="section-header">Telemetry Channels</div>', unsafe_allow_html=True)
            channels = [("Speed","Speed (km/h)"),("Throttle","Throttle (%)"),("Brake","Brake"),("nGear","Gear")]
            fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.04,
                                subplot_titles=[c[1] for c in channels])
            color_a = driver_color(driver1, year)
            color_b = driver_color(driver2, year)
            lap_num_a = int(lap_a["LapNumber"]) if pd.notna(lap_a["LapNumber"]) else "?"
            lap_num_b = int(lap_b["LapNumber"]) if pd.notna(lap_b["LapNumber"]) else "?"

            same_color = (color_a.lower() == color_b.lower())
            # When teammates share a colour, use lightened version for Driver B
            # matching the official F1 telemetry overlay convention
            color_b_plot = lighten_color(color_b, 0.45) if same_color else color_b

            for i, (ch, label) in enumerate(channels, start=1):
                if ch not in tel_a.columns or ch not in tel_b.columns:
                    continue
                show_leg = (i == 1)
                fig.add_trace(go.Scatter(x=tel_a["Distance"], y=tel_a[ch],
                    name=f"{driver1} L{lap_num_a}",
                    line=dict(color=color_a, width=1.8),
                    showlegend=show_leg), row=i, col=1)
                fig.add_trace(go.Scatter(x=tel_b["Distance"], y=tel_b[ch],
                    name=f"{driver2} L{lap_num_b}",
                    line=dict(color=color_b_plot, width=1.8),
                    showlegend=show_leg), row=i, col=1)

            # ── Corner markers ─────────────────────────────────────────────
            # Fetch circuit corner distances from FastF1 circuit info
            corners = None
            try:
                ci = session.get_circuit_info()
                corners = ci.corners[["Number","Letter","Distance"]].copy()
            except Exception:
                corners = None

            if corners is not None and not corners.empty:
                # Get speed range for label placement (top of speed panel)
                spd_data = pd.concat([tel_a["Speed"], tel_b["Speed"]]).dropna()
                spd_max  = float(spd_data.quantile(0.99)) if not spd_data.empty else 350
                spd_min  = float(spd_data.quantile(0.01)) if not spd_data.empty else 60
                spd_range = spd_max - spd_min
                label_y  = spd_min + spd_range * 0.05   # just above the bottom

                for _, corner in corners.iterrows():
                    dist   = float(corner["Distance"])
                    num    = int(corner["Number"])
                    ltr    = str(corner.get("Letter") or "").strip()
                    label  = f"T{num}{ltr}"

                    # Faint vertical rule across all 4 panels
                    for row_i in range(1, 5):
                        fig.add_vline(
                            x=dist,
                            line_width=0.6,
                            line_color="rgba(255,255,255,0.07)",
                            row=row_i, col=1,
                        )

                    # Corner label on Speed panel only (row 1)
                    fig.add_annotation(
                        x=dist,
                        y=label_y,
                        text=label,
                        showarrow=False,
                        font=dict(
                            size=8,
                            color="rgba(180,180,200,0.45)",
                            family="JetBrains Mono, monospace",
                        ),
                        textangle=-90,
                        xref="x1",
                        yref="y1",
                        xanchor="center",
                        yanchor="bottom",
                    )

            fig.update_layout(**PLOT_LAYOUT, height=920,
                title=f"{driver1} Lap {lap_num_a}  vs  {driver2} Lap {lap_num_b}")
            for i in range(1, 5):
                fig.update_xaxes(gridcolor="#0c0c14", linecolor="#141420", row=i, col=1)
                fig.update_yaxes(gridcolor="#0c0c14", linecolor="#141420", row=i, col=1)
            fig.update_xaxes(title_text="Distance (m)", row=4, col=1)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div class="section-header">Sector Times</div>', unsafe_allow_html=True)
            def sec_to_s(val):
                try: return val.total_seconds()
                except Exception: return None

            data_rows = []
            for s_col, lbl in zip(["Sector1Time","Sector2Time","Sector3Time"], ["S1","S2","S3"]):
                data_rows.append({"Sector": lbl, "A": sec_to_s(lap_a.get(s_col)),
                                   "B": sec_to_s(lap_b.get(s_col))})
            df_sec = pd.DataFrame(data_rows).dropna(subset=["A","B"])
            if not df_sec.empty:
                fig_sec = go.Figure()
                fig_sec.add_trace(go.Bar(name=f"{driver1} L{lap_num_a}", x=df_sec["Sector"],
                    y=df_sec["A"], marker_color=color_a))
                fig_sec.add_trace(go.Bar(name=f"{driver2} L{lap_num_b}", x=df_sec["Sector"],
                    y=df_sec["B"], marker_color=color_b))
                apply_theme(fig_sec, "Sector Times (s)")
                fig_sec.update_layout(barmode="group", height=280, yaxis_title="Time (s)")
                st.plotly_chart(fig_sec, use_container_width=True)

        except Exception as e:
            st.warning(f"Could not load telemetry: {e}")
    else:
        st.info("No timed laps found for one or both drivers in this session.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — DELTA TIME
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Lap Selection</div>', unsafe_allow_html=True)

    try:
        _laps_a3, _opts_a3 = build_lap_options(driver1, laps)
        _laps_b3, _opts_b3 = build_lap_options(driver2, laps_b_src)
        _labels_a3 = list(_opts_a3.keys())
        _labels_b3 = list(_opts_b3.keys())

        _col_a3, _col_b3 = st.columns(2)
        with _col_a3:
            st.markdown(f"""<div style='font-family:"JetBrains Mono",monospace; font-size:0.62rem;
                color:{driver_color(driver1, year)}; letter-spacing:0.15em;
                text-transform:uppercase; margin-bottom:4px;'>● {driver1}</div>""",
                unsafe_allow_html=True)
            _sel_a3 = st.selectbox("Delta Lap A", _labels_a3,
                index=_labels_a3.index(fastest_label(_laps_a3, _opts_a3))
                      if fastest_label(_laps_a3, _opts_a3) in _labels_a3 else 0,
                key="delta_sel_a", label_visibility="collapsed")
        with _col_b3:
            st.markdown(f"""<div style='font-family:"JetBrains Mono",monospace; font-size:0.62rem;
                color:{driver_color(driver2, year)}; letter-spacing:0.15em;
                text-transform:uppercase; margin-bottom:4px;'>● {driver2}</div>""",
                unsafe_allow_html=True)
            _sel_b3 = st.selectbox("Delta Lap B", _labels_b3,
                index=_labels_b3.index(fastest_label(_laps_b3, _opts_b3))
                      if fastest_label(_laps_b3, _opts_b3) in _labels_b3 else 0,
                key="delta_sel_b", label_visibility="collapsed")

        lap_a = _laps_a3.loc[_opts_a3[_sel_a3]]
        lap_b = _laps_b3.loc[_opts_b3[_sel_b3]]
    except Exception as _e:
        st.warning(f"Could not build lap list for delta tab: {_e}")
        lap_a = laps.pick_drivers(driver1).pick_fastest()
        lap_b = laps.pick_drivers(driver2).pick_fastest()

    st.markdown('<div class="section-header">Delta Time Analysis</div>', unsafe_allow_html=True)

    if _cross and race != race_b:
        st.warning("⚠  Delta time works best when both sessions are from the same circuit. "
                   "Different circuits will produce meaningless gaps.")

    try:
        delta_time, ref_tel, compare_tel = fastf1.utils.delta_time(lap_a, lap_b)

        fig_d = go.Figure()
        pos_mask = delta_time >= 0
        fig_d.add_trace(go.Scatter(x=ref_tel["Distance"], y=np.where(pos_mask, delta_time, 0),
            fill="tozeroy", fillcolor=hex_to_rgba(driver_color(driver1, year), 0.19),
            line=dict(color="rgba(0,0,0,0)"), showlegend=False))
        fig_d.add_trace(go.Scatter(x=ref_tel["Distance"], y=np.where(~pos_mask, delta_time, 0),
            fill="tozeroy", fillcolor=hex_to_rgba(driver_color(driver2, year), 0.19),
            line=dict(color="rgba(0,0,0,0)"), showlegend=False))
        fig_d.add_trace(go.Scatter(x=ref_tel["Distance"], y=delta_time,
            line=dict(color="#ffffff", width=1.5), name=f"Δ {driver1} vs {driver2}"))
        fig_d.add_hline(y=0, line_dash="dot", line_color="#333348", line_width=1)
        apply_theme(fig_d, f"Delta Time  ·  {driver1} ahead when negative")
        fig_d.update_layout(height=350, yaxis_title="Delta (s)", xaxis_title="Distance (m)")
        net = float(delta_time.iloc[-1])
        winner = driver1 if net < 0 else driver2
        fig_d.add_annotation(x=ref_tel["Distance"].iloc[-1], y=net,
            text=f"  {winner} +{abs(net):.3f}s",
            font=dict(size=11, color="#f0f0ff"), showarrow=False, xanchor="right")
        st.plotly_chart(fig_d, use_container_width=True)

        st.markdown('<div class="section-header">Speed Overlay</div>', unsafe_allow_html=True)
        fig_spd = go.Figure()
        fig_spd.add_trace(go.Scatter(x=ref_tel["Distance"], y=ref_tel["Speed"],
            name=driver1, line=dict(color=driver_color(driver1, year), width=1.5)))
        fig_spd.add_trace(go.Scatter(x=compare_tel["Distance"], y=compare_tel["Speed"],
            name=driver2, line=dict(color=driver_color(driver2, year), width=1.5)))
        apply_theme(fig_spd, "Speed Trace")
        fig_spd.update_layout(height=280, yaxis_title="Speed (km/h)", xaxis_title="Distance (m)")
        st.plotly_chart(fig_spd, use_container_width=True)

    except Exception as e:
        st.warning(f"Delta time failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — TRACK MAPS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Track Maps</div>', unsafe_allow_html=True)
    map_type = st.radio("Map type", ["Speed heatmap", "Driver line comparison"],
                        horizontal=True, label_visibility="collapsed")
    try:
        if map_type == "Speed heatmap":
            fastest_lap = laps.pick_fastest()
            tel = fastest_lap.get_telemetry()
            drv = fastest_lap["Driver"]
            fig_map = px.scatter(tel, x="X", y="Y", color="Speed",
                color_continuous_scale=[[0.0,"#1a0a30"],[0.25,"#3671C6"],[0.5,"#27F4D2"],
                                         [0.75,"#FF8000"],[1.0,"#E8002D"]],
                title=f"Speed Heatmap · {drv} · Fastest Lap")
            fig_map.update_traces(marker=dict(size=3, opacity=0.9))
            fig_map.update_yaxes(scaleanchor="x", scaleratio=1)
            apply_theme(fig_map)
            fig_map.update_layout(height=520,
                coloraxis_colorbar=dict(
                    title=dict(text="km/h", font=dict(size=11, color="#888898")),
                    tickfont=dict(size=10, color="#888898")),
                xaxis=dict(visible=False), yaxis=dict(visible=False))
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            lap_a = laps.pick_drivers(driver1).pick_fastest()
            lap_b = laps.pick_drivers(driver2).pick_fastest()
            tel_a = lap_a.get_telemetry()
            tel_b = lap_b.get_telemetry()
            fig_lines = go.Figure()
            fig_lines.add_trace(go.Scatter(x=tel_a["X"], y=tel_a["Y"], mode="lines",
                name=driver1, line=dict(color=driver_color(driver1, year), width=2)))
            fig_lines.add_trace(go.Scatter(x=tel_b["X"], y=tel_b["Y"], mode="lines",
                name=driver2, line=dict(color=driver_color(driver2, year), width=2)))
            apply_theme(fig_lines, f"Racing Line · {driver1} vs {driver2}")
            fig_lines.update_yaxes(scaleanchor="x", scaleratio=1)
            fig_lines.update_layout(height=520, xaxis=dict(visible=False), yaxis=dict(visible=False))
            st.plotly_chart(fig_lines, use_container_width=True)
    except Exception as e:
        st.warning(f"Track map error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — ANIMATED RACE TRACKER
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Animated Race Position Tracker</div>', unsafe_allow_html=True)

    if session_type != "R":
        st.markdown("""<div class="info-box">
            ⚑  Switch session type to <strong>R (Race)</strong> in the sidebar and reload.
        </div>""", unsafe_allow_html=True)
        st.stop()

    try:
        pos_data = session.pos_data
        if pos_data is None or len(pos_data) == 0:
            st.error("No positional data available for this session.")
            st.stop()

        speed_opt = st.select_slider("Playback speed",
            options=["0.5×","1×","2×","5×","10×","20×"], value="5×")
        speed_map = {"0.5×":0.5,"1×":1,"2×":2,"5×":5,"10×":10,"20×":20}
        playback_speed = speed_map[speed_opt]

        num_to_abbr = {}
        try:
            results = session.results
            if results is not None and not results.empty:
                for _, row in results.iterrows():
                    num  = str(int(row["DriverNumber"])) if pd.notna(row.get("DriverNumber")) else None
                    abbr = str(row.get("Abbreviation","") or "").strip().upper()
                    if num and abbr:
                        num_to_abbr[num] = abbr
        except Exception:
            pass

        drivers_in_race = []
        frames_data     = {}

        for num, drv_pos in pos_data.items():
            if drv_pos is None or drv_pos.empty: continue
            if not {"X","Y","Time"}.issubset(drv_pos.columns): continue
            df = drv_pos[["X","Y","Time"]].dropna().copy()
            if len(df) < 10: continue
            key = num_to_abbr.get(str(num), str(num))
            drivers_in_race.append(key)
            frames_data[key] = df.reset_index(drop=True)

        if not drivers_in_race:
            st.error("No positional data could be loaded for any driver.")
            st.stop()

        def to_seconds(series):
            s = series.iloc[0]
            if hasattr(s, "total_seconds"):
                return series.apply(lambda x: x.total_seconds()).values.astype(float)
            return series.values.astype(np.int64) / 1e9

        for drv in drivers_in_race:
            frames_data[drv]["TimeSec"] = to_seconds(frames_data[drv]["Time"])
            frames_data[drv] = (frames_data[drv].sort_values("TimeSec")
                                .drop_duplicates(subset="TimeSec").reset_index(drop=True))

        drv_arrays = {}
        for drv in drivers_in_race:
            df = frames_data[drv]
            t = df["TimeSec"].values
            x = df["X"].values.astype(float)
            y = df["Y"].values.astype(float)
            dx = np.diff(x); dy = np.diff(y)
            dist = np.sqrt(dx**2 + dy**2)
            bad = np.where(dist > 500)[0] + 1
            for bi in bad:
                x[bi] = x[bi-1]; y[bi] = y[bi-1]
            drv_arrays[drv] = (t, x, y)

        def interp_pos(drv, t_target):
            t, x, y = drv_arrays[drv]
            t_clamped = float(np.clip(t_target, t[0], t[-1]))
            return float(np.interp(t_clamped, t, x)), float(np.interp(t_clamped, t, y))

        driver_lap_times = {}
        for drv in drivers_in_race:
            try:
                drv_laps = laps.pick_drivers(drv)[["LapNumber","LapStartTime"]].dropna().copy()
                if not drv_laps.empty:
                    drv_laps["StartSec"] = to_seconds(drv_laps["LapStartTime"])
                    driver_lap_times[drv] = drv_laps.sort_values("StartSec").reset_index(drop=True)
            except Exception:
                pass

        def get_lap_at(drv, t_sec):
            if drv not in driver_lap_times or driver_lap_times[drv].empty: return "—"
            rows = driver_lap_times[drv]
            past = rows[rows["StartSec"] <= t_sec]
            return int(past.iloc[-1]["LapNumber"]) if not past.empty else int(rows.iloc[0]["LapNumber"])

        t_min = max(drv_arrays[d][0][0] for d in drivers_in_race)
        t_max = min(drv_arrays[d][0][-1] for d in drivers_in_race)
        total_real_secs = t_max - t_min

        N_FRAMES    = 6400
        frame_ms    = max(50, int(total_real_secs / N_FRAMES / playback_speed * 1000))
        t_range     = np.linspace(t_min, t_max, N_FRAMES)
        total_mins  = total_real_secs / 60.0

        fastest_lap = laps.pick_fastest()
        track_tel   = fastest_lap.get_telemetry()
        track_x     = track_tel["X"].tolist()
        track_y     = track_tel["Y"].tolist()

        total_laps_est = int(laps["LapNumber"].max()) if "LapNumber" in laps.columns else "?"

        N_TRACK = 3
        driver_trace_indices = list(range(N_TRACK, N_TRACK + len(drivers_in_race)))

        init_traces = [
            go.Scatter(x=track_x, y=track_y, mode="lines",
                       line=dict(color="#2a2a3a", width=16), hoverinfo="skip", showlegend=False),
            go.Scatter(x=track_x, y=track_y, mode="lines",
                       line=dict(color="#18182a", width=10), hoverinfo="skip", showlegend=False),
            go.Scatter(x=track_x, y=track_y, mode="lines",
                       line=dict(color="rgba(255,255,255,0.03)", width=1, dash="dot"),
                       hoverinfo="skip", showlegend=False),
        ]

        for drv in drivers_in_race:
            x0, y0 = interp_pos(drv, t_range[0])
            clr = driver_color(drv, year)
            init_traces.append(go.Scatter(
                x=[x0], y=[y0], mode="markers+text", name=drv,
                marker=dict(size=14, color=clr, line=dict(color="#000000", width=2), symbol="circle"),
                text=[f"  {drv}"], textposition="middle right",
                textfont=dict(size=10, color=clr, family="Titillium Web, sans-serif"),
                hovertemplate=f"<b>{drv}</b><extra></extra>", showlegend=True,
            ))

        drv_colours = {drv: driver_color(drv, year) for drv in drivers_in_race}
        animation_frames = []

        for fi, t in enumerate(t_range):
            elapsed = t - t_min
            mins = int(elapsed // 60); secs = int(elapsed % 60)
            lap_num = get_lap_at(drivers_in_race[0], t)
            driver_stubs = []
            for drv in drivers_in_race:
                px, py = interp_pos(drv, t)
                clr = drv_colours[drv]
                driver_stubs.append(go.Scatter(
                    x=[px], y=[py], mode="markers+text",
                    marker=dict(color=clr, size=14, line=dict(color="#000000", width=2), symbol="circle"),
                    text=[f"  {drv}"], textposition="middle right",
                    textfont=dict(color=clr, size=10, family="Titillium Web, sans-serif"),
                ))
            animation_frames.append(go.Frame(
                data=driver_stubs, traces=driver_trace_indices, name=str(fi),
                layout=go.Layout(title=dict(
                    text=(f"<span style='color:#e10600;font-weight:900;'>LAP {lap_num}</span>"
                          f"<span style='color:#333344;'>  /  {total_laps_est}</span>"
                          f"<span style='color:#222230;font-size:12px;'>  ·  {mins:02d}:{secs:02d}</span>"),
                    font=dict(family="Titillium Web, sans-serif", size=20, color="#c8c8d8"),
                    x=0.01, xanchor="left")),
            ))

        slider_steps = []
        for i, t in enumerate(t_range):
            elapsed = t - t_min; m = int(elapsed//60); s = int(elapsed%60)
            label = f"{m}:{s:02d}" if i % max(1, N_FRAMES//20) == 0 else ""
            slider_steps.append(dict(method="animate", args=[[str(i)], dict(
                frame=dict(duration=frame_ms, redraw=True), mode="immediate",
                transition=dict(duration=0))], label=label))

        init_lap = get_lap_at(drivers_in_race[0], t_range[0])
        st.success(f"✓  {len(drivers_in_race)} drivers  ·  {N_FRAMES} frames  ·  "
                   f"{total_mins:.0f} min race  ·  frame {frame_ms}ms  ({speed_opt})")

        fig_race = go.Figure(
            data=init_traces, frames=animation_frames,
            layout=go.Layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#06060c",
                height=680, margin=dict(l=10, r=10, t=60, b=90),
                title=dict(
                    text=(f"<span style='color:#e10600;font-weight:900;'>LAP {init_lap}</span>"
                          f"<span style='color:#333344;'>  /  {total_laps_est}</span>"
                          f"<span style='color:#222230;font-size:12px;'>  ·  00:00</span>"),
                    font=dict(family="'Titillium Web', sans-serif", size=20, color="#c8c8d8"),
                    x=0.01, xanchor="left"),
                updatemenus=[dict(type="buttons", showactive=False,
                    y=-0.08, x=0.5, xanchor="center", yanchor="top",
                    buttons=[
                        dict(label="▶  PLAY", method="animate",
                             args=[None, dict(frame=dict(duration=frame_ms, redraw=True),
                                             fromcurrent=True, transition=dict(duration=0))]),
                        dict(label="⏸  PAUSE", method="animate",
                             args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
                    ], bgcolor="#0e0e18", bordercolor="#e10600", borderwidth=1,
                    font=dict(color="#f0f0ff", family="'Titillium Web', sans-serif", size=12))],
                sliders=[dict(steps=slider_steps, active=0,
                    x=0.0, y=-0.04, len=1.0, xanchor="left", yanchor="top",
                    pad=dict(b=10, t=50),
                    currentvalue=dict(prefix="⏱  ", visible=True, xanchor="center",
                        font=dict(color="#888898", family="'Titillium Web', sans-serif", size=12)),
                    transition=dict(duration=0), bgcolor="#0a0a12", bordercolor="#141420",
                    tickcolor="#141420", activebgcolor="#e10600", font=dict(color="#333344", size=8))],
                xaxis=dict(visible=False),
                yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
                legend=dict(orientation="v", x=1.01, y=1.0, yanchor="top",
                    bgcolor="rgba(6,6,12,0.9)", bordercolor="#141420", borderwidth=1,
                    font=dict(size=11, family="'Titillium Web', sans-serif", color="#c8c8d8"),
                    traceorder="normal"),
            ),
        )
        st.plotly_chart(fig_race, use_container_width=True)

        st.markdown('<div class="section-header">Driver Key</div>', unsafe_allow_html=True)
        key_cols = st.columns(min(len(drivers_in_race), 10))
        for i, drv in enumerate(drivers_in_race):
            with key_cols[i % len(key_cols)]:
                clr = driver_color(drv, year)
                st.markdown(f"""
                <div style='display:flex;align-items:center;gap:8px;padding:5px 0;'>
                    <div style='width:11px;height:11px;border-radius:50%;background:{clr};
                                flex-shrink:0;box-shadow:0 0 8px {clr}66;'></div>
                    <span style='font-family:"Titillium Web",sans-serif;font-size:0.78rem;
                                 font-weight:700;color:{clr};letter-spacing:0.06em;'>{drv}</span>
                </div>""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Race tracker error: {e}")
        st.info("Make sure you loaded a Race session (R). Some sessions may have limited positional data.")