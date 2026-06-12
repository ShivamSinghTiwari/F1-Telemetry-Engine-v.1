"""
track_map.py — circuit outline with optional gear/speed colouring.
"""
import fastf1
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


PLOT_BG   = "#0a0a10"
PAPER_BG  = "rgba(0,0,0,0)"
GRID      = "#13131e"
TEXT      = "#888898"


def plot_track_outline(session, driver: str = None):
    """Thin circuit outline from fastest lap positional data."""
    lap = session.laps.pick_fastest() if driver is None \
        else session.laps.pick_drivers(driver).pick_fastest()
    tel = lap.get_telemetry()
    drv = lap["Driver"]

    fig = go.Figure()
    # Shadow / thickness layer
    fig.add_trace(go.Scatter(
        x=tel["X"], y=tel["Y"],
        mode="lines",
        line=dict(color="#1a1a2e", width=12),
        hoverinfo="skip", showlegend=False,
    ))
    # Main outline
    fig.add_trace(go.Scatter(
        x=tel["X"], y=tel["Y"],
        mode="lines",
        line=dict(color="#2e2e44", width=7),
        hoverinfo="skip", showlegend=False,
    ))
    # Centre line
    fig.add_trace(go.Scatter(
        x=tel["X"], y=tel["Y"],
        mode="lines",
        line=dict(color="#e10600", width=1.5),
        name=f"{drv} — racing line",
    ))

    fig.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT, size=11),
        height=540,
        title=dict(
            text=f"Track Map — {drv}",
            font=dict(size=14, color="#f0f0ff"),
        ),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    fig.show()
    return fig


def plot_speed_map(session, driver: str = None):
    """Track map coloured by speed using a racing-inspired palette."""
    lap = session.laps.pick_fastest() if driver is None \
        else session.laps.pick_drivers(driver).pick_fastest()
    tel = lap.get_telemetry()
    drv = lap["Driver"]

    PALETTE = [
        [0.00, "#1a0a30"],
        [0.25, "#3671C6"],
        [0.50, "#27F4D2"],
        [0.75, "#FF8000"],
        [1.00, "#E8002D"],
    ]

    fig = px.scatter(
        tel, x="X", y="Y", color="Speed",
        color_continuous_scale=PALETTE,
        title=f"Speed Map — {drv} — Fastest Lap",
    )
    fig.update_traces(marker=dict(size=3.5, opacity=0.9))
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT, size=11),
        height=540,
        title_font=dict(size=14, color="#f0f0ff"),
        coloraxis_colorbar=dict(
            title=dict(text="km/h", font=dict(size=11, color=TEXT)),
            tickfont=dict(size=10, color=TEXT),
            bgcolor="#0d0d18",
            bordercolor="#1a1a28",
        ),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=10, r=60, t=50, b=10),
    )
    fig.show()
    return fig


def plot_gear_map(session, driver: str = None):
    """Track map coloured by gear selection."""
    lap = session.laps.pick_fastest() if driver is None \
        else session.laps.pick_drivers(driver).pick_fastest()
    tel = lap.get_telemetry()
    if "nGear" not in tel.columns:
        print("nGear column not available for this session.")
        return

    drv = lap["Driver"]
    fig = px.scatter(
        tel, x="X", y="Y", color="nGear",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"Gear Map — {drv} — Fastest Lap",
    )
    fig.update_traces(marker=dict(size=3.5, opacity=0.9))
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT, size=11),
        height=540,
        title_font=dict(size=14, color="#f0f0ff"),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=10, r=60, t=50, b=10),
    )
    fig.show()
    return fig


if __name__ == "__main__":
    fastf1.Cache.enable_cache("cache")
    session = fastf1.get_session(2025, "Australia", "Q")
    session.load()

    plot_track_outline(session)
    plot_speed_map(session)
    plot_gear_map(session)