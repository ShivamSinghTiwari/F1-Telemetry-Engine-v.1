"""
speed_track_map.py — side-by-side speed maps for two drivers.
"""
import fastf1
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


PAPER_BG = "rgba(0,0,0,0)"
PLOT_BG  = "#0a0a10"
TEXT     = "#888898"

SPEED_PALETTE = [
    [0.00, "#1a0a30"],
    [0.25, "#3671C6"],
    [0.50, "#27F4D2"],
    [0.75, "#FF8000"],
    [1.00, "#E8002D"],
]

TEAM_COLORS = {
    "VER": "#3671C6", "NOR": "#FF8000", "LEC": "#E8002D",
    "HAM": "#27F4D2", "RUS": "#27F4D2",
}


def _speed_color(speeds: np.ndarray, palette=SPEED_PALETTE) -> list[str]:
    """Map speed values to hex colours using the palette."""
    vmin, vmax = speeds.min(), speeds.max()
    norm = (speeds - vmin) / max(vmax - vmin, 1)

    stops = [(p[0], p[1]) for p in palette]

    def lerp_hex(c1: str, c2: str, t: float) -> str:
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    colors = []
    for n in norm:
        for j in range(len(stops) - 1):
            if stops[j][0] <= n <= stops[j + 1][0]:
                local_t = (n - stops[j][0]) / (stops[j + 1][0] - stops[j][0])
                colors.append(lerp_hex(stops[j][1], stops[j + 1][1], local_t))
                break
        else:
            colors.append(stops[-1][1])
    return colors


def plot_speed_comparison(session, driver1: str, driver2: str):
    """Side-by-side speed-coloured track maps."""
    lap1 = session.laps.pick_drivers(driver1).pick_fastest()
    lap2 = session.laps.pick_drivers(driver2).pick_fastest()
    tel1 = lap1.get_telemetry()
    tel2 = lap2.get_telemetry()

    speeds1 = tel1["Speed"].values.astype(float)
    speeds2 = tel2["Speed"].values.astype(float)

    all_speeds = np.concatenate([speeds1, speeds2])
    vmin, vmax = all_speeds.min(), all_speeds.max()

    def norm_colors(speeds):
        norm = (speeds - vmin) / max(vmax - vmin, 1)
        stops = [(p[0], p[1]) for p in SPEED_PALETTE]

        def lerp_hex(c1, c2, t):
            r1,g1,b1 = int(c1[1:3],16),int(c1[3:5],16),int(c1[5:7],16)
            r2,g2,b2 = int(c2[1:3],16),int(c2[3:5],16),int(c2[5:7],16)
            return "#{:02x}{:02x}{:02x}".format(
                int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t))

        out = []
        for n in norm:
            for j in range(len(stops)-1):
                if stops[j][0] <= n <= stops[j+1][0]:
                    t = (n-stops[j][0])/(stops[j+1][0]-stops[j][0])
                    out.append(lerp_hex(stops[j][1], stops[j+1][1], t))
                    break
            else:
                out.append(stops[-1][1])
        return out

    colors1 = norm_colors(speeds1)
    colors2 = norm_colors(speeds2)

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            f"{driver1}  —  top {speeds1.max():.0f} km/h",
            f"{driver2}  —  top {speeds2.max():.0f} km/h",
        ],
        horizontal_spacing=0.06,
    )

    for col_idx, (tel, colors, drv) in enumerate(
        [(tel1, colors1, driver1), (tel2, colors2, driver2)], start=1
    ):
        # Track shadow
        fig.add_trace(go.Scatter(
            x=tel["X"], y=tel["Y"],
            mode="lines",
            line=dict(color="#1a1a2e", width=10),
            hoverinfo="skip", showlegend=False,
        ), row=1, col=col_idx)

        # Speed-coloured dots
        fig.add_trace(go.Scatter(
            x=tel["X"], y=tel["Y"],
            mode="markers",
            marker=dict(color=colors, size=3.5, opacity=0.95),
            hovertemplate="Speed: %{customdata:.0f} km/h<extra></extra>",
            customdata=tel["Speed"],
            showlegend=False,
            name=drv,
        ), row=1, col=col_idx)

    # Shared colour scale legend (invisible scatter for colorbar)
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(
            colorscale=SPEED_PALETTE,
            cmin=vmin, cmax=vmax,
            colorbar=dict(
                title=dict(text="km/h", font=dict(size=11, color=TEXT)),
                tickfont=dict(size=10, color=TEXT),
                bgcolor="#0d0d18",
                bordercolor="#1a1a28",
                x=1.02,
            ),
            showscale=True,
            size=0,
        ),
        showlegend=False,
    ))

    fig.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT, size=11),
        height=500,
        title=dict(
            text=f"Speed Map Comparison — {driver1}  vs  {driver2}",
            font=dict(size=14, color="#f0f0ff"),
        ),
        margin=dict(l=10, r=80, t=60, b=10),
    )
    for col_idx in [1, 2]:
        fig.update_xaxes(visible=False, row=1, col=col_idx)
        fig.update_yaxes(visible=False, scaleanchor="x", scaleratio=1, row=1, col=col_idx)

    fig.show()
    return fig


if __name__ == "__main__":
    fastf1.Cache.enable_cache("cache")
    session = fastf1.get_session(2025, "Australia", "Q")
    session.load()
    plot_speed_comparison(session, "NOR", "VER")