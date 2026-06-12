"""
driver_compare_cli.py — interactive CLI telemetry comparison using Plotly.
"""
import sys
import fastf1
import plotly.graph_objects as go
from plotly.subplots import make_subplots

TEAM_COLORS = {
    "VER": "#3671C6", "PER": "#3671C6",
    "HAM": "#27F4D2", "RUS": "#27F4D2",
    "LEC": "#E8002D", "SAI": "#E8002D",
    "NOR": "#FF8000", "PIA": "#FF8000",
    "ALO": "#358C75", "STR": "#358C75",
    "GAS": "#2293D1", "OCO": "#2293D1",
    "TSU": "#5E8FAA", "LAW": "#5E8FAA",
    "BOT": "#C92D4B", "ZHO": "#C92D4B",
    "MAG": "#B6BABD", "HUL": "#B6BABD",
    "ALB": "#64C4FF", "SAR": "#64C4FF",
}
DEFAULT_COLOR = "#FFFFFF"

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#0a0a10",
    font=dict(family="sans-serif", color="#888898", size=11),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1a1a28", borderwidth=1,
               orientation="h", y=1.02, x=1, xanchor="right"),
)


def driver_color(drv: str) -> str:
    return TEAM_COLORS.get(drv.upper(), DEFAULT_COLOR)


def compare_drivers(session, driver1: str, driver2: str) -> go.Figure:
    lap1 = session.laps.pick_drivers(driver1).pick_fastest()
    lap2 = session.laps.pick_drivers(driver2).pick_fastest()
    tel1 = lap1.get_telemetry().add_distance()
    tel2 = lap2.get_telemetry().add_distance()

    channels = [
        ("Speed",    "Speed (km/h)"),
        ("Throttle", "Throttle (%)"),
        ("Brake",    "Brake"),
        ("nGear",    "Gear"),
        ("RPM",      "RPM"),
    ]
    available = [(c, l) for c, l in channels
                 if c in tel1.columns and c in tel2.columns]

    n = len(available)
    fig = make_subplots(
        rows=n, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.035,
        subplot_titles=[l for _, l in available],
    )

    color1 = driver_color(driver1)
    color2 = driver_color(driver2)

    for i, (col, _) in enumerate(available, start=1):
        show_leg = (i == 1)
        fig.add_trace(go.Scatter(
            x=tel1["Distance"], y=tel1[col],
            name=driver1, line=dict(color=color1, width=1.6),
            showlegend=show_leg,
        ), row=i, col=1)
        fig.add_trace(go.Scatter(
            x=tel2["Distance"], y=tel2[col],
            name=driver2, line=dict(color=color2, width=1.6),
            showlegend=show_leg,
        ), row=i, col=1)

    fig.update_layout(
        **PLOT_LAYOUT,
        height=220 * n,
        title=dict(
            text=f"<b>{driver1}</b>  vs  <b>{driver2}</b>  —  Telemetry Comparison",
            font=dict(size=16, color="#f0f0ff"),
        ),
    )
    for i in range(1, n + 1):
        fig.update_xaxes(gridcolor="#13131e", linecolor="#1a1a28", row=i, col=1)
        fig.update_yaxes(gridcolor="#13131e", linecolor="#1a1a28", row=i, col=1)
    fig.update_xaxes(title_text="Distance (m)", row=n, col=1)

    return fig


def main():
    fastf1.Cache.enable_cache("cache")

    print("═" * 40)
    print("  F1 Telemetry — Driver Comparison")
    print("═" * 40)

    try:
        year         = int(input("Year [2025]: ").strip() or "2025")
        race         = input("Race [Australia]: ").strip() or "Australia"
        session_type = input("Session Q/R/FP1 [Q]: ").strip().upper() or "Q"
        driver1      = input("Driver A [NOR]: ").strip().upper() or "NOR"
        driver2      = input("Driver B [VER]: ").strip().upper() or "VER"
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)

    print(f"\nLoading {year} {race} {session_type}…")
    session = fastf1.get_session(year, race, session_type)
    session.load()
    print("Session loaded.\n")

    fig = compare_drivers(session, driver1, driver2)
    fig.show()


if __name__ == "__main__":
    main()