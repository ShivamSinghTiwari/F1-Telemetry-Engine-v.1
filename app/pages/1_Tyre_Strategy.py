import streamlit as st
import fastf1
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tyre Strategy · F1 Telemetry Engine",
    page_icon="🏎",
    layout="wide",
    initial_sidebar_state="expanded",
)

fastf1.Cache.enable_cache("cache")

# ── Design tokens (mirrored from dashboard.py) ─────────────────────────────────
# Shared year-aware colour lookup (same as dashboard.py)
_TC = {
    "VER_2021":"#1E41FF","VER_2022":"#3671C6","VER_2023":"#3671C6","VER_2024":"#3671C6","VER_2025":"#3671C6","VER_2026":"#3671C6",
    "HAM_2021":"#00D2BE","HAM_2022":"#00D2BE","HAM_2023":"#00D2BE","HAM_2024":"#27F4D2","HAM_2025":"#E8002D","HAM_2026":"#E8002D",
    "RUS_2022":"#00D2BE","RUS_2023":"#00D2BE","RUS_2024":"#27F4D2","RUS_2025":"#27F4D2","RUS_2026":"#27F4D2",
    "ANT_2025":"#27F4D2","ANT_2026":"#27F4D2",
    "LEC_2022":"#E8002D","LEC_2023":"#E8002D","LEC_2024":"#E8002D","LEC_2025":"#E8002D","LEC_2026":"#E8002D",
    "SAI_2022":"#E8002D","SAI_2023":"#E8002D","SAI_2024":"#E8002D","SAI_2025":"#64C4FF","SAI_2026":"#64C4FF",
    "BEA_2024":"#B6BABD","BEA_2025":"#B6BABD","BEA_2026":"#E8002D",
    "NOR_2022":"#FF8000","NOR_2023":"#FF8000","NOR_2024":"#FF8000","NOR_2025":"#FF8000","NOR_2026":"#FF8000",
    "PIA_2023":"#FF8000","PIA_2024":"#FF8000","PIA_2025":"#FF8000","PIA_2026":"#FF8000",
    "ALO_2023":"#358C75","ALO_2024":"#358C75","ALO_2025":"#358C75","ALO_2026":"#358C75",
    "STR_2022":"#006F62","STR_2023":"#358C75","STR_2024":"#358C75","STR_2025":"#358C75","STR_2026":"#358C75",
    "GAS_2022":"#0090FF","GAS_2023":"#2293D1","GAS_2024":"#2293D1","GAS_2025":"#2293D1","GAS_2026":"#2293D1",
    "OCO_2022":"#0090FF","OCO_2023":"#2293D1","OCO_2024":"#2293D1","OCO_2025":"#2293D1","OCO_2026":"#B6BABD",
    "DOO_2025":"#2293D1","DOO_2026":"#2293D1","COL_2025":"#2293D1","COL_2026":"#2293D1",
    "TSU_2022":"#399BB3","TSU_2023":"#5E8FAA","TSU_2024":"#5E8FAA","TSU_2025":"#5E8FAA","TSU_2026":"#5E8FAA",
    "LAW_2024":"#5E8FAA","LAW_2025":"#5E8FAA","HAD_2025":"#5E8FAA","HAD_2026":"#5E8FAA","BOR_2026":"#5E8FAA",
    "BOT_2022":"#C92D4B","BOT_2023":"#C92D4B","BOT_2024":"#C92D4B","BOT_2025":"#C92D4B",
    "ZHO_2022":"#C92D4B","ZHO_2023":"#C92D4B","ZHO_2024":"#C92D4B","ZHO_2026":"#C92D4B",
    "HUL_2023":"#B6BABD","HUL_2024":"#B6BABD","HUL_2025":"#C92D4B","HUL_2026":"#C92D4B",
    "MAG_2022":"#B6BABD","MAG_2023":"#B6BABD","MAG_2024":"#B6BABD","MAG_2025":"#B6BABD",
    "ALB_2022":"#64C4FF","ALB_2023":"#64C4FF","ALB_2024":"#64C4FF","ALB_2025":"#64C4FF","ALB_2026":"#64C4FF",
    "SAR_2023":"#64C4FF","SAR_2024":"#64C4FF","SAN_2025":"#64C4FF","SAN_2026":"#64C4FF",
    "PER_2021":"#1E41FF","PER_2022":"#3671C6","PER_2023":"#3671C6","PER_2024":"#3671C6",
}
TEAM_COLORS = {
    "VER":"#3671C6","PER":"#3671C6","HAM":"#E8002D","RUS":"#27F4D2","ANT":"#27F4D2",
    "LEC":"#E8002D","SAI":"#64C4FF","BEA":"#E8002D","NOR":"#FF8000","PIA":"#FF8000",
    "ALO":"#358C75","STR":"#358C75","GAS":"#2293D1","OCO":"#B6BABD","DOO":"#2293D1","COL":"#2293D1",
    "TSU":"#5E8FAA","LAW":"#5E8FAA","HAD":"#5E8FAA","BOR":"#5E8FAA",
    "BOT":"#C92D4B","ZHO":"#C92D4B","HUL":"#C92D4B","MAG":"#B6BABD",
    "ALB":"#64C4FF","SAR":"#64C4FF","SAN":"#64C4FF",
}
DEFAULT_COLOR = "#AAAAAA"

COMPOUND_COLORS = {
    "SOFT":   "#E8002D",
    "MEDIUM": "#FFF200",
    "HARD":   "#FFFFFF",
    "INTER":  "#39B54A",
    "WET":    "#0067FF",
    "TEST":   "#999999",
    "UNKNOWN":"#666666",
}

COMPOUND_SHORT = {
    "SOFT": "S", "MEDIUM": "M", "HARD": "H",
    "INTER": "I", "WET": "W",
}

DRIVERS_BY_YEAR = {
    2021: ["VER","HAM","BOT","PER","LEC","SAI","NOR","RIC","ALO","GAS",
           "STR","OCO","RAI","GIO","TSU","LAT","MAZ","MSC","VET","KUB"],
    2022: ["VER","PER","LEC","SAI","HAM","RUS","NOR","RIC","ALO","OCO",
           "BOT","ZHO","STR","VET","GAS","MAG","MSC","ALB","LAT","TSU"],
    2023: ["VER","PER","ALO","HAM","SAI","RUS","NOR","PIA","LEC","STR",
           "GAS","OCO","TSU","LAW","MAG","HUL","ALB","SAR","BOT","ZHO"],
    2024: ["VER","PER","NOR","PIA","LEC","SAI","HAM","RUS","ALO","STR",
           "GAS","OCO","TSU","LAW","MAG","HUL","ALB","SAR","BOT","ZHO"],
    2025: ["VER","NOR","PIA","LEC","HAM","RUS","ANT","SAI","ALO","STR",
           "GAS","DOO","TSU","HAD","MAG","BEA","ALB","SAR","BOT","HUL"],
    2026: ["VER","NOR","PIA","LEC","BEA","HAM","RUS","ANT","ALO","STR",
           "GAS","COL","TSU","HAD","OCO","BOR","ALB","SAN","HUL","ZHO"],
}

RACES = [
    "Australian Grand Prix",
    "Chinese Grand Prix",
    "Japanese Grand Prix",
    "Bahrain Grand Prix",
    "Saudi Arabian Grand Prix",
    "Miami Grand Prix",
    "Emilia Romagna Grand Prix",
    "Monaco Grand Prix",
    "Canadian Grand Prix",
    "Barcelona Grand Prix",
    "Spanish Grand Prix",
    "Austrian Grand Prix",
    "British Grand Prix",
    "Hungarian Grand Prix",
    "Belgian Grand Prix",
    "Dutch Grand Prix",
    "Italian Grand Prix",
    "Azerbaijan Grand Prix",
    "Singapore Grand Prix",
    "United States Grand Prix",
    "Mexico City Grand Prix",
    "São Paulo Grand Prix",
    "Las Vegas Grand Prix",
    "Qatar Grand Prix",
    "Abu Dhabi Grand Prix",
]


def driver_color(drv: str, yr: int = None) -> str:
    if yr is not None:
        key = f"{drv.upper()}_{yr}"
        if key in _TC:
            return _TC[key]
    return TEAM_COLORS.get(drv.upper(), DEFAULT_COLOR)


def compound_color(c: str) -> str:
    return COMPOUND_COLORS.get((c or "UNKNOWN").upper(), COMPOUND_COLORS["UNKNOWN"])


def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


PLOT_BG   = "#06060c"
PAPER_BG  = "rgba(0,0,0,0)"
GRID_CLR  = "#0c0c14"
LINE_CLR  = "#141420"
TEXT_CLR  = "#444458"
FONT_MONO = "JetBrains Mono, monospace"
FONT_MAIN = "Titillium Web, sans-serif"

PLOT_LAYOUT = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=PLOT_BG,
    font=dict(family=FONT_MAIN, color=TEXT_CLR, size=11),
    title_font=dict(family=FONT_MAIN, size=14, color="#c8c8d8"),
    margin=dict(l=55, r=20, t=50, b=50),
    hoverlabel=dict(bgcolor="#0d0d18", bordercolor=LINE_CLR,
                    font=dict(family=FONT_MONO, size=11, color="#c8c8d8")),
)

# Reusable legend style — pass explicitly at each call site
LEGEND_STYLE = dict(bgcolor="rgba(6,6,12,0.9)", bordercolor=LINE_CLR,
                    borderwidth=1, font=dict(size=11, family=FONT_MAIN,
                    color="#888898"))

# Reusable axis style dicts — pass explicitly at each call site
AXIS_STYLE = dict(gridcolor=GRID_CLR, linecolor=LINE_CLR,
                  tickcolor=LINE_CLR, zerolinecolor=LINE_CLR,
                  tickfont=dict(size=10, color="#2a2a38", family=FONT_MONO))

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@200;300;400;600;700;900&family=JetBrains+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Titillium Web', sans-serif; }

.stApp {
    background: #050508;
    background-image:
        linear-gradient(rgba(255,200,0,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,200,0,0.02) 1px, transparent 1px);
    background-size: 40px 40px;
}
.block-container { padding-top:1.2rem !important; max-width:1440px; }

[data-testid="stSidebar"] {
    background: #070709 !important;
    border-right: 1px solid #111118 !important;
}
[data-testid="stSidebar"] * { color: #b0b0c8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label {
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
    box-shadow: 0 0 20px rgba(225,6,0,0.25) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    box-shadow: 0 0 30px rgba(225,6,0,0.45) !important;
    transform: translateY(-1px) !important;
}
.stSelectbox > div > div {
    background: #0c0c12 !important; border: 1px solid #1c1c28 !important;
    border-radius: 3px !important; color: #d0d0e8 !important;
}
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0d0d16 0%, #0a0a10 100%) !important;
    border: 1px solid #1a1a26 !important; border-top: 2px solid #ffc906 !important;
    border-radius: 4px !important; padding: 1rem 1.2rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
}
[data-testid="metric-container"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.58rem !important; letter-spacing: 0.2em !important;
    text-transform: uppercase !important; color: #444458 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Titillium Web', sans-serif !important;
    font-size: 1.6rem !important; font-weight: 700 !important; color: #f0f0ff !important;
}
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem; font-weight: 500; letter-spacing: 0.25em;
    text-transform: uppercase; color: #333344;
    margin: 1.8rem 0 0.8rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid #0f0f18;
    display: flex; align-items: center; gap: 8px;
}
.section-header::before {
    content: ''; display: inline-block; width: 16px; height: 1px;
    background: #ffc906; flex-shrink: 0;
}
.compound-pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 700;
    padding: 3px 10px; border-radius: 2px;
    letter-spacing: 0.1em; margin: 2px 3px;
}
.tyre-card {
    background: #0a0a10;
    border: 1px solid #141420;
    border-radius: 4px;
    padding: 1rem;
    margin-bottom: 0.5rem;
}
hr { border-color: #0f0f18 !important; margin: 1.5rem 0 !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #050508; }
::-webkit-scrollbar-thumb { background: #1a1a28; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #ffc906; }
.stSuccess {
    background: rgba(0,180,80,0.08) !important;
    border-left: 3px solid #00b450 !important; border-radius: 3px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important;
}
.stWarning {
    background: rgba(255,160,0,0.08) !important;
    border-left: 3px solid #ffa000 !important; border-radius: 3px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.2rem 0 1.4rem; border-bottom:1px solid #111118; margin-bottom:1.4rem;'>
        <div style='display:flex; align-items:flex-start; gap:10px;'>
            <div style='width:3px; height:48px;
                        background:linear-gradient(180deg,#ffc906,#a07800);
                        border-radius:2px; flex-shrink:0; margin-top:2px;'></div>
            <div>
                <div style='font-family:"Titillium Web",sans-serif; font-size:1.5rem;
                            font-weight:900; color:#f0f0ff; line-height:1;'>TYRE</div>
                <div style='font-family:"Titillium Web",sans-serif; font-size:1.5rem;
                            font-weight:900; color:#ffc906; line-height:1;'>STRATEGY</div>
                <div style='font-family:"JetBrains Mono",monospace; font-size:0.55rem;
                            color:#252530; letter-spacing:0.22em; margin-top:5px;'>
                    F1 TELEMETRY ENGINE
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-family:\'JetBrains Mono\',monospace; font-size:0.6rem; color:#333344; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:6px;">Session</div>', unsafe_allow_html=True)

    year = st.selectbox("Year", [2026, 2025, 2024, 2023, 2022, 2021], index=0)
    race = st.selectbox("Grand Prix", RACES, index=0)

    st.markdown("<br>", unsafe_allow_html=True)
    load_btn = st.button("⬤  Load Race", use_container_width=True)

    st.markdown("""
    <div style='margin-top:2rem; padding-top:1.2rem; border-top:1px solid #0f0f18;'>
        <div style='font-family:"JetBrains Mono",monospace; font-size:0.52rem;
                    color:#1c1c28; letter-spacing:0.12em; text-transform:uppercase;
                    line-height:1.8;'>Race sessions only<br>─────────────────</div>
    </div>
    """, unsafe_allow_html=True)

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='display:flex; align-items:flex-end; justify-content:space-between;
            border-bottom:1px solid #0f0f18; padding-bottom:1rem; margin-bottom:1.2rem;'>
    <div>
        <div style='font-family:"Titillium Web",sans-serif; font-size:2.8rem;
                    font-weight:900; color:#f0f0ff; line-height:0.95;
                    text-shadow:0 0 40px rgba(255,201,6,0.15);'>
            TYRE <span style='color:#ffc906;'>STRATEGY</span>
        </div>
        <div style='font-family:"JetBrains Mono",monospace; font-size:0.65rem;
                    color:#2a2a38; margin-top:6px; letter-spacing:0.2em; text-transform:uppercase;'>
            ◈ &nbsp; {year} &nbsp;·&nbsp; {race.upper()} &nbsp;·&nbsp; Race
        </div>
    </div>
    <div style='text-align:right; padding-bottom:4px;'>
        <div style='font-family:"JetBrains Mono",monospace; font-size:0.6rem;
                    color:#1e1e2a; letter-spacing:0.15em;'>FastF1 · Race Analysis</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "tyre_session" not in st.session_state:
    st.session_state.tyre_session = None
if "tyre_key" not in st.session_state:
    st.session_state.tyre_key = None

if load_btn:
    with st.spinner("Loading race data…"):
        try:
            sess = fastf1.get_session(year, race, "R")
            sess.load()
            st.session_state.tyre_session = sess
            st.session_state.tyre_key = f"{year}_{race}"
            st.success(f"✓  {year} {race} Race loaded — {len(sess.laps)} laps across {sess.laps['Driver'].nunique()} drivers")
        except Exception as e:
            st.error(f"Failed to load session: {e}")

session = st.session_state.tyre_session

if session is None:
    # ── Landing ──
    st.markdown("""
    <div style='margin:2rem 0 2.5rem; padding:2rem 2.5rem;
                background:linear-gradient(135deg,#0a0a10 0%,#070709 100%);
                border:1px solid #141420; border-left:3px solid #ffc906;
                border-radius:4px; position:relative; overflow:hidden;'>
        <div style='position:absolute; top:-20px; right:-20px; width:140px; height:140px;
                    border-radius:50%;
                    background:radial-gradient(circle,rgba(255,201,6,0.06),transparent 70%);'></div>
        <div style='font-family:"JetBrains Mono",monospace; font-size:0.6rem;
                    color:#333344; letter-spacing:0.2em; text-transform:uppercase;
                    margin-bottom:0.8rem;'>Getting started</div>
        <div style='font-family:"Titillium Web",sans-serif; font-size:1.1rem;
                    font-weight:700; color:#c8c8d8; margin-bottom:0.5rem;'>
            Select a year and Grand Prix, then click Load Race
        </div>
        <div style='font-family:"Titillium Web",sans-serif; font-size:0.82rem; color:#333344;'>
            Requires a completed <span style='color:#ffc906; font-weight:600;'>Race session</span>.
            Qualifying tyre data is available in the main dashboard.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    tiles = [
        ("01", "Strategy Timeline", "Full race stint map for every driver", "#ffc906"),
        ("02", "Degradation Curves", "Lap-time drop-off per compound per driver", "#E8002D"),
        ("03", "Pit Stop Analysis", "Stationary time, lap lost, strategy outcome", "#27F4D2"),
        ("04", "Compound Heatmap", "Who ran which compound for how long", "#FF8000"),
    ]
    for col, (num, title, desc, clr) in zip(cols, tiles):
        with col:
            st.markdown(f"""
            <div style='background:#0a0a10; border:1px solid #111118;
                        border-top:2px solid {clr}; border-radius:3px;
                        padding:1.2rem 1rem; height:130px; position:relative; overflow:hidden;
                        box-shadow:0 4px 20px rgba(0,0,0,0.3);'>
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

# ══════════════════════════════════════════════════════════════════════════════
# DATA PROCESSING
# ══════════════════════════════════════════════════════════════════════════════
laps = session.laps.copy()
laps = laps[laps["LapTime"].notna()].copy()
laps["LapTimeSec"] = laps["LapTime"].dt.total_seconds()

# Build stint table: one row per driver per stint
def build_stint_table(laps: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for drv in laps["Driver"].unique():
        drv_laps = laps[laps["Driver"] == drv].sort_values("LapNumber")
        for stint_num in drv_laps["Stint"].dropna().unique():
            stint_laps = drv_laps[drv_laps["Stint"] == stint_num]
            if stint_laps.empty:
                continue
            compound = stint_laps["Compound"].mode().iloc[0] if not stint_laps["Compound"].isna().all() else "UNKNOWN"
            rows.append({
                "Driver":       drv,
                "Stint":        int(stint_num),
                "Compound":     compound.upper() if compound else "UNKNOWN",
                "StartLap":     int(stint_laps["LapNumber"].min()),
                "EndLap":       int(stint_laps["LapNumber"].max()),
                "Laps":         int(len(stint_laps)),
                "AvgPace":      round(stint_laps["LapTimeSec"].mean(), 3),
                "BestLap":      round(stint_laps["LapTimeSec"].min(), 3),
                "Degradation":  _calc_deg(stint_laps),
            })
    return pd.DataFrame(rows)


def _calc_deg(stint_laps: pd.DataFrame) -> float:
    """Simple linear degradation: seconds lost per lap across the stint."""
    if len(stint_laps) < 3:
        return 0.0
    valid = stint_laps["LapTimeSec"].dropna()
    if len(valid) < 3:
        return 0.0
    x = np.arange(len(valid))
    try:
        slope = float(np.polyfit(x, valid.values, 1)[0])
        return round(slope, 4)
    except Exception:
        return 0.0


stint_df = build_stint_table(laps)

# Driver order: by final race position if available
try:
    results     = session.results
    driver_order = results.sort_values("Position")["Abbreviation"].tolist()
    # Keep only drivers that actually have lap data
    driver_order = [d for d in driver_order if d in laps["Driver"].unique()]
    # Add any remaining drivers not in results
    remaining = [d for d in laps["Driver"].unique() if d not in driver_order]
    driver_order += remaining
except Exception:
    driver_order = sorted(laps["Driver"].unique())

total_laps = int(laps["LapNumber"].max())

# ── Key metrics ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Race Overview</div>', unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.metric("Total Race Laps", total_laps)
with m2:
    st.metric("Drivers", len(driver_order))
with m3:
    most_common = stint_df["Compound"].value_counts().index[0] if not stint_df.empty else "—"
    st.metric("Dominant Compound", most_common)
with m4:
    avg_stops = round(stint_df.groupby("Driver")["Stint"].max().mean() - 1, 1)
    st.metric("Avg Pit Stops", avg_stops)
with m5:
    fastest_lap = laps["LapTimeSec"].min()
    fl_driver   = laps.loc[laps["LapTimeSec"].idxmin(), "Driver"]
    fl_str      = f"{int(fastest_lap//60)}:{fastest_lap%60:06.3f}"
    st.metric("Fastest Lap", f"{fl_str}  ({fl_driver})")


# ══════════════════════════════════════════════════════════════════════════════
# 1 — STRATEGY TIMELINE (Gantt-style stint map)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Strategy Timeline — Stint Map</div>',
            unsafe_allow_html=True)

st.markdown("""
<div style='display:flex; gap:12px; flex-wrap:wrap; margin-bottom:1rem;'>
""" + "".join([
    f"<div style='display:flex;align-items:center;gap:6px;'>"
    f"<div style='width:28px;height:12px;border-radius:2px;"
    f"background:{compound_color(c)};opacity:0.9;'></div>"
    f"<span style='font-family:\"JetBrains Mono\",monospace;font-size:0.65rem;"
    f"color:#555570;letter-spacing:0.08em;'>{c}</span></div>"
    for c in ["SOFT", "MEDIUM", "HARD", "INTER", "WET"]
]) + "</div>", unsafe_allow_html=True)

fig_timeline = go.Figure()

for i, drv in enumerate(driver_order):
    drv_stints = stint_df[stint_df["Driver"] == drv].sort_values("Stint")
    clr        = driver_color(drv, year)

    for _, row in drv_stints.iterrows():
        cmpd     = row["Compound"]
        c_clr    = compound_color(cmpd)
        short    = COMPOUND_SHORT.get(cmpd, cmpd[0])
        lap_span = row["EndLap"] - row["StartLap"] + 1
        deg_str  = f"+{row['Degradation']:.3f}s/lap" if row['Degradation'] > 0 else f"{row['Degradation']:.3f}s/lap"

        # Main stint bar
        fig_timeline.add_trace(go.Bar(
            x=[lap_span],
            y=[drv],
            base=row["StartLap"] - 1,
            orientation="h",
            marker=dict(
                color=hex_to_rgba(c_clr, 0.85),
                line=dict(color=hex_to_rgba(c_clr, 1.0), width=1.5),
            ),
            name=cmpd,
            legendgroup=cmpd,
            showlegend=bool(i == 0),
            hovertemplate=(
                f"<b>{drv}</b> — Stint {int(row['Stint'])}<br>"
                f"Compound: <b>{cmpd}</b><br>"
                f"Laps: {row['StartLap']} → {row['EndLap']} ({lap_span} laps)<br>"
                f"Avg pace: {row['AvgPace']:.3f}s<br>"
                f"Best lap: {row['BestLap']:.3f}s<br>"
                f"Degradation: {deg_str}"
                "<extra></extra>"
            ),
            text=short if lap_span >= 4 else "",
            textposition="inside",
            textfont=dict(
                color="#000000" if cmpd in ("MEDIUM","HARD","INTER") else "#ffffff",
                size=11, family=FONT_MONO, weight=700,
            ),
            insidetextanchor="middle",
        ))

        # Pit stop marker (vertical line at stint end, except last stint)
        max_stint = drv_stints["Stint"].max()
        if row["Stint"] < max_stint:
            fig_timeline.add_shape(
                type="line",
                x0=row["EndLap"], x1=row["EndLap"],
                y0=i - 0.4, y1=i + 0.4,
                line=dict(color="#ffffff", width=1.5, dash="dot"),
            )

    # Driver name label colour
    fig_timeline.add_annotation(
        x=-1, y=drv,
        text=f"<span style='color:{clr};font-weight:700;'>{drv}</span>",
        showarrow=False, xanchor="right",
        font=dict(family=FONT_MONO, size=10),
    )

fig_timeline.update_layout(
    paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
    font=dict(family=FONT_MAIN, color=TEXT_CLR, size=11),
    title_font=dict(family=FONT_MAIN, size=14, color="#c8c8d8"),
    hoverlabel=dict(bgcolor="#0d0d18", bordercolor=LINE_CLR,
                    font=dict(family=FONT_MONO, size=11, color="#c8c8d8")),
    margin=dict(l=55, r=20, t=50, b=50),
    height=max(420, len(driver_order) * 30 + 80),
    barmode="overlay",
    title="Full Race Strategy — All Drivers",
    xaxis=dict(
        title="Lap Number",
        range=[0, total_laps + 1],
        gridcolor=GRID_CLR, linecolor=LINE_CLR,
        tickfont=dict(size=10, color="#2a2a38", family=FONT_MONO),
        dtick=5,
    ),
    yaxis=dict(
        categoryorder="array",
        categoryarray=list(reversed(driver_order)),
        gridcolor=GRID_CLR, linecolor=LINE_CLR,
        tickfont=dict(size=10, color="#888898", family=FONT_MONO),
        tickmode="array",
        tickvals=driver_order,
        ticktext=[f'<span style="color:{driver_color(d)}">{d}</span>' for d in driver_order],
    ),
    legend=dict(
        orientation="h", y=1.02, x=0, xanchor="left",
        bgcolor="rgba(0,0,0,0)", borderwidth=0,
        font=dict(size=11, family=FONT_MONO),
        traceorder="normal",
    ),
    showlegend=True,
)
st.plotly_chart(fig_timeline, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# 2 — DEGRADATION CURVES (pace per lap coloured by compound)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Tyre Degradation Curves</div>',
            unsafe_allow_html=True)

# Driver filter
all_drivers = driver_order
selected_drivers = st.multiselect(
    "Select drivers to compare",
    options=all_drivers,
    default=all_drivers[:5],
    key="deg_drivers",
)

if selected_drivers:
    fig_deg = go.Figure()

    for drv in selected_drivers:
        drv_laps = laps[laps["Driver"] == drv].sort_values("LapNumber")
        clr      = driver_color(drv, year)

        for stint_num in drv_laps["Stint"].dropna().unique():
            stint_laps = drv_laps[drv_laps["Stint"] == stint_num].copy()
            if len(stint_laps) < 2:
                continue

            cmpd   = stint_laps["Compound"].mode().iloc[0] if not stint_laps["Compound"].isna().all() else "UNKNOWN"
            cmpd   = (cmpd or "UNKNOWN").upper()
            c_clr  = compound_color(cmpd)
            # Tyre age within stint
            stint_laps["TyreAge"] = range(1, len(stint_laps) + 1)

            # Remove outliers (> 3 std from mean) — safety car, pit-in laps
            mean_t = stint_laps["LapTimeSec"].mean()
            std_t  = stint_laps["LapTimeSec"].std()
            clean  = stint_laps[
                (stint_laps["LapTimeSec"] > mean_t - 2 * std_t) &
                (stint_laps["LapTimeSec"] < mean_t + 2 * std_t)
            ]
            if len(clean) < 2:
                continue

            # Scatter: actual laps
            fig_deg.add_trace(go.Scatter(
                x=clean["TyreAge"], y=clean["LapTimeSec"],
                mode="markers",
                name=f"{drv} S{int(stint_num)} {cmpd}",
                marker=dict(color=c_clr, size=6, opacity=0.6,
                            line=dict(color=clr, width=1)),
                legendgroup=f"{drv}_{stint_num}",
                showlegend=True,
                hovertemplate=f"<b>{drv}</b> Stint {int(stint_num)}<br>"
                              f"Lap {{}}<br>Time: %{{y:.3f}}s<br>Tyre age: %{{x}}<extra></extra>",
            ))

            # Trend line
            x_vals = clean["TyreAge"].values
            y_vals = clean["LapTimeSec"].values
            if len(x_vals) >= 3:
                try:
                    coefs  = np.polyfit(x_vals, y_vals, 1)
                    x_fit  = np.linspace(x_vals.min(), x_vals.max(), 50)
                    y_fit  = np.polyval(coefs, x_fit)
                    slope  = coefs[0]
                    fig_deg.add_trace(go.Scatter(
                        x=x_fit, y=y_fit,
                        mode="lines",
                        name=f"  trend ({slope:+.3f}s/lap)",
                        line=dict(color=c_clr, width=2, dash="solid"),
                        legendgroup=f"{drv}_{stint_num}",
                        showlegend=True,
                        hoverinfo="skip",
                    ))
                except Exception:
                    pass

    fig_deg.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_MAIN, color=TEXT_CLR, size=11),
        title_font=dict(family=FONT_MAIN, size=14, color="#c8c8d8"),
        hoverlabel=dict(bgcolor="#0d0d18", bordercolor=LINE_CLR,
                        font=dict(family=FONT_MONO, size=11, color="#c8c8d8")),
        margin=dict(l=55, r=20, t=50, b=50),
        height=480,
        title="Lap Time vs Tyre Age — Degradation Trends",
        xaxis=dict(title="Tyre Age (laps into stint)",
                   gridcolor=GRID_CLR, linecolor=LINE_CLR,
                   tickfont=dict(size=10, color="#2a2a38", family=FONT_MONO)),
        yaxis=dict(title="Lap Time (s)",
                   gridcolor=GRID_CLR, linecolor=LINE_CLR,
                   tickfont=dict(size=10, color="#2a2a38", family=FONT_MONO)),
        legend=dict(orientation="v", x=1.01, y=1.0,
                    bgcolor="rgba(6,6,12,0.9)", bordercolor=LINE_CLR,
                    borderwidth=1, font=dict(size=10, family=FONT_MONO)),
    )
    st.plotly_chart(fig_deg, use_container_width=True)
else:
    st.info("Select at least one driver above.")


# ══════════════════════════════════════════════════════════════════════════════
# 3 — PIT STOP ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Pit Stop Analysis</div>',
            unsafe_allow_html=True)

try:
    pit_laps = laps[laps["PitOutTime"].notna() | laps["PitInTime"].notna()].copy()

    # Build pit stop records
    pit_records = []
    for drv in driver_order:
        drv_laps = laps[laps["Driver"] == drv].sort_values("LapNumber")
        pit_in   = drv_laps[drv_laps["PitInTime"].notna()]
        pit_out  = drv_laps[drv_laps["PitOutTime"].notna()]

        for _, row in pit_in.iterrows():
            lap_num = int(row["LapNumber"])
            # Find matching pit out (usually next lap)
            out_laps = pit_out[pit_out["LapNumber"] >= lap_num]
            if out_laps.empty:
                continue
            out_row = out_laps.iloc[0]

            # Stationary time = PitOutTime of out lap - PitInTime of in lap
            try:
                stat = (out_row["PitOutTime"] - row["PitInTime"]).total_seconds()
                if stat < 0 or stat > 120:
                    continue
            except Exception:
                continue

            # Compound change
            in_cmpd  = row.get("Compound", "?") or "?"
            out_cmpd = out_row.get("Compound", "?") or "?"

            pit_records.append({
                "Driver":         drv,
                "Lap":            lap_num,
                "StationaryTime": round(stat, 2),
                "CompoundIn":     in_cmpd.upper(),
                "CompoundOut":    out_cmpd.upper(),
                "Change":         f"{in_cmpd} → {out_cmpd}",
            })

    pit_df = pd.DataFrame(pit_records)

    if not pit_df.empty:
        col_chart, col_table = st.columns([3, 2])

        with col_chart:
            # Bar chart — stationary time per driver per stop, coloured by compound out
            fig_pit = go.Figure()
            pit_sorted = pit_df.sort_values(["Driver", "Lap"])

            for cmpd in pit_df["CompoundOut"].unique():
                sub = pit_df[pit_df["CompoundOut"] == cmpd]
                fig_pit.add_trace(go.Bar(
                    x=sub["Driver"] + " L" + sub["Lap"].astype(str),
                    y=sub["StationaryTime"],
                    name=cmpd,
                    marker_color=compound_color(cmpd),
                    hovertemplate="<b>%{x}</b><br>Stationary: %{y:.2f}s<extra></extra>",
                ))

            # Fastest pit line
            if not pit_df.empty:
                fastest_pit = pit_df["StationaryTime"].min()
                fig_pit.add_hline(
                    y=fastest_pit,
                    line_dash="dot", line_color="#ffc906", line_width=1.5,
                    annotation_text=f"  Fastest: {fastest_pit:.2f}s",
                    annotation_font=dict(color="#ffc906", size=10, family=FONT_MONO),
                )

            fig_pit.update_layout(
                paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_MAIN, color=TEXT_CLR, size=11),
        title_font=dict(family=FONT_MAIN, size=14, color="#c8c8d8"),
        hoverlabel=dict(bgcolor="#0d0d18", bordercolor=LINE_CLR,
                        font=dict(family=FONT_MONO, size=11, color="#c8c8d8")),
        margin=dict(l=55, r=20, t=50, b=50),
                height=360,
                barmode="group",
                title="Stationary Time per Pit Stop",
                xaxis=dict(title="", tickangle=-45,
                           gridcolor=GRID_CLR, linecolor=LINE_CLR,
                           tickfont=dict(size=9, color="#2a2a38", family=FONT_MONO)),
                yaxis=dict(title="Stationary Time (s)",
                           gridcolor=GRID_CLR, linecolor=LINE_CLR,
                           tickfont=dict(size=10, color="#2a2a38", family=FONT_MONO)),
            )
            st.plotly_chart(fig_pit, use_container_width=True)

        with col_table:
            st.markdown('<div class="section-header" style="margin-top:0.5rem;">Stop Log</div>',
                        unsafe_allow_html=True)
            # Styled table
            display_df = pit_df[["Driver","Lap","StationaryTime","Change"]].copy()
            display_df.columns = ["Driver", "Lap", "Stop Time (s)", "Tyres"]
            display_df = display_df.sort_values("Stop Time (s)")

            # Colour the fastest stop
            st.dataframe(
                display_df.reset_index(drop=True),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Driver": st.column_config.TextColumn("Driver", width="small"),
                    "Lap": st.column_config.NumberColumn("Lap", width="small", format="%d"),
                    "Stop Time (s)": st.column_config.NumberColumn(
                        "Stop (s)", format="%.2f", width="small"),
                    "Tyres": st.column_config.TextColumn("Tyres", width="medium"),
                },
            )
    else:
        st.info("No pit stop data available for this session.")

except Exception as e:
    st.warning(f"Pit stop analysis unavailable: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 4 — COMPOUND USAGE HEATMAP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Compound Usage Heatmap</div>',
            unsafe_allow_html=True)

try:
    compounds_used = [c for c in ["SOFT","MEDIUM","HARD","INTER","WET"]
                      if c in stint_df["Compound"].values]

    # Matrix: driver × compound → total laps on that compound
    matrix_data = []
    for drv in driver_order:
        row_data = {}
        drv_stints = stint_df[stint_df["Driver"] == drv]
        for c in compounds_used:
            row_data[c] = int(drv_stints[drv_stints["Compound"] == c]["Laps"].sum())
        matrix_data.append(row_data)

    matrix_df = pd.DataFrame(matrix_data, index=driver_order)

    fig_heat = go.Figure(go.Heatmap(
        z=matrix_df.values,
        x=compounds_used,
        y=driver_order,
        colorscale=[
            [0.0, "#06060c"],
            [0.1, "#1a1a2e"],
            [0.4, "#3d1a00"],
            [0.7, "#a05000"],
            [1.0, "#ffc906"],
        ],
        showscale=True,
        colorbar=dict(
            title=dict(text="Laps", font=dict(size=11, color=TEXT_CLR)),
            tickfont=dict(size=10, color=TEXT_CLR, family=FONT_MONO),
            bgcolor="#0d0d18", bordercolor=LINE_CLR,
        ),
        hovertemplate="<b>%{y}</b> on <b>%{x}</b><br>%{z} laps<extra></extra>",
        text=matrix_df.values,
        texttemplate="%{text}",
        textfont=dict(size=11, family=FONT_MONO, color="#c8c8d8"),
    ))

    # Compound colour bar at top
    for j, c in enumerate(compounds_used):
        fig_heat.add_annotation(
            x=j, y=len(driver_order) + 0.6,
            text=f"<b>{c[0]}</b>",
            showarrow=False,
            font=dict(size=13, color=compound_color(c), family=FONT_MONO),
            bgcolor=hex_to_rgba(compound_color(c), 0.12),
        )

    fig_heat.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_MAIN, color=TEXT_CLR, size=11),
        title_font=dict(family=FONT_MAIN, size=14, color="#c8c8d8"),
        hoverlabel=dict(bgcolor="#0d0d18", bordercolor=LINE_CLR,
                        font=dict(family=FONT_MONO, size=11, color="#c8c8d8")),
        height=max(380, len(driver_order) * 24 + 80),
        title="Laps Completed per Compound per Driver",
        xaxis=dict(
            tickfont=dict(size=11, color="#888898", family=FONT_MONO),
            gridcolor=GRID_CLR, linecolor=LINE_CLR,
            side="bottom",
        ),
        yaxis=dict(
            categoryorder="array",
            categoryarray=list(reversed(driver_order)),
            tickfont=dict(
                size=10, family=FONT_MONO,
                color="#888898",
            ),
            gridcolor=GRID_CLR, linecolor=LINE_CLR,
        ),
        margin=dict(l=70, r=80, t=50, b=50),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

except Exception as e:
    st.warning(f"Compound heatmap unavailable: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 5 — RACE PACE COMPARISON (rolling average per stint)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Race Pace — Lap-by-Lap</div>',
            unsafe_allow_html=True)

pace_drivers = st.multiselect(
    "Select drivers",
    options=driver_order,
    default=driver_order[:6],
    key="pace_drivers",
)

if pace_drivers:
    fig_pace = go.Figure()

    for drv in pace_drivers:
        drv_laps = laps[laps["Driver"] == drv].sort_values("LapNumber").copy()
        clr      = driver_color(drv, year)

        # Remove outlier laps (SC, VSC, pit laps)
        mean_t = drv_laps["LapTimeSec"].mean()
        std_t  = drv_laps["LapTimeSec"].std()
        clean  = drv_laps[
            (drv_laps["LapTimeSec"] > mean_t - 2.5 * std_t) &
            (drv_laps["LapTimeSec"] < mean_t + 2.5 * std_t)
        ]

        # Plot laps coloured by compound segment
        for stint_num in clean["Stint"].dropna().unique():
            stint_laps = clean[clean["Stint"] == stint_num]
            if stint_laps.empty:
                continue
            cmpd  = stint_laps["Compound"].mode().iloc[0] if not stint_laps["Compound"].isna().all() else "UNKNOWN"
            cmpd  = (cmpd or "UNKNOWN").upper()
            c_clr = compound_color(cmpd)
            show  = bool(stint_num == clean["Stint"].dropna().iloc[0])

            fig_pace.add_trace(go.Scatter(
                x=stint_laps["LapNumber"],
                y=stint_laps["LapTimeSec"],
                mode="lines+markers",
                name=drv,
                legendgroup=drv,
                showlegend=show,
                line=dict(color=clr, width=1.5),
                marker=dict(
                    color=c_clr, size=6,
                    line=dict(color=clr, width=1.5),
                ),
                hovertemplate=f"<b>{drv}</b> Lap %{{x}}<br>"
                              f"Time: %{{y:.3f}}s<br>Compound: {cmpd}"
                              "<extra></extra>",
            ))

    fig_pace.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_MAIN, color=TEXT_CLR, size=11),
        title_font=dict(family=FONT_MAIN, size=14, color="#c8c8d8"),
        hoverlabel=dict(bgcolor="#0d0d18", bordercolor=LINE_CLR,
                        font=dict(family=FONT_MONO, size=11, color="#c8c8d8")),
        margin=dict(l=55, r=20, t=50, b=50),
        height=420,
        title="Race Pace per Lap  (marker = compound, line = driver colour)",
        xaxis=dict(title="Lap Number", dtick=5,
                   gridcolor=GRID_CLR, linecolor=LINE_CLR,
                   tickfont=dict(size=10, color="#2a2a38", family=FONT_MONO)),
        yaxis=dict(title="Lap Time (s)",
                   gridcolor=GRID_CLR, linecolor=LINE_CLR,
                   tickfont=dict(size=10, color="#2a2a38", family=FONT_MONO)),
        legend=dict(orientation="v", x=1.01, y=1.0,
                    bgcolor="rgba(6,6,12,0.9)", bordercolor=LINE_CLR,
                    borderwidth=1, font=dict(size=11, family=FONT_MAIN)),
    )
    st.plotly_chart(fig_pace, use_container_width=True)