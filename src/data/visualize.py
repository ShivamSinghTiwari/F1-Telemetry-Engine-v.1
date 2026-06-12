"""
visualize.py — multi-channel Plotly telemetry visualisation.
"""
import fastf1
import plotly.graph_objects as go
from plotly.subplots import make_subplots

TEAM_COLORS = {
    "VER": "#3671C6", "NOR": "#FF8000", "LEC": "#E8002D",
    "HAM": "#27F4D2", "RUS": "#27F4D2", "SAI": "#E8002D",
    "PIA": "#FF8000", "ALO": "#358C75",
}

PLOT_BG = "#0a0a10"
PAPER_BG = "rgba(0,0,0,0)"
GRID = "#13131e"
LINE = "#1a1a28"
TEXT = "#888898"


def color(drv): return TEAM_COLORS.get(drv.upper(), "#FFFFFF")


def plot_comparison(session, driver1: str, driver2: str, save_html: str = None):
    lap1 = session.laps.pick_drivers(driver1).pick_fastest()
    lap2 = session.laps.pick_drivers(driver2).pick_fastest()
    tel1 = lap1.get_telemetry().add_distance()
    tel2 = lap2.get_telemetry().add_distance()

    channels = ["Speed", "Throttle", "Brake", "nGear"]
    labels   = ["Speed (km/h)", "Throttle (%)", "Brake", "Gear"]

    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True,
        vertical_spacing=0.04,
        subplot_titles=labels,
    )

    for i, (ch, _) in enumerate(zip(channels, labels), 1):
        if ch not in tel1.columns:
            continue
        show = (i == 1)
        fig.add_trace(go.Scatter(
            x=tel1["Distance"], y=tel1[ch],
            name=driver1, line=dict(color=color(driver1), width=1.6),
            showlegend=show,
        ), row=i, col=1)
        fig.add_trace(go.Scatter(
            x=tel2["Distance"], y=tel2[ch],
            name=driver2, line=dict(color=color(driver2), width=1.6),
            showlegend=show,
        ), row=i, col=1)

    fig.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT, size=11),
        height=720,
        title=dict(
            text=f"<b>{driver1}</b>  vs  <b>{driver2}</b>  —  Speed Comparison",
            font=dict(size=15, color="#f0f0ff"),
        ),
        legend=dict(orientation="h", y=1.02, x=1, xanchor="right",
                    bgcolor="rgba(0,0,0,0)", bordercolor=LINE, borderwidth=1),
    )
    for i in range(1, 5):
        fig.update_xaxes(gridcolor=GRID, linecolor=LINE, row=i, col=1)
        fig.update_yaxes(gridcolor=GRID, linecolor=LINE, row=i, col=1)
    fig.update_xaxes(title_text="Distance (m)", row=4, col=1)

    if save_html:
        fig.write_html(save_html)
        print(f"Saved to {save_html}")

    fig.show()
    return fig


if __name__ == "__main__":
    fastf1.Cache.enable_cache("cache")
    session = fastf1.get_session(2025, "Australia", "Q")
    session.load()
    plot_comparison(session, "NOR", "VER")
