"""
delta_time.py — delta time computation and matplotlib visualisation.
"""
import fastf1
import fastf1.utils
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


DARK_BG   = "#0a0a0f"
GRID_CLR  = "#1a1a28"
TEXT_CLR  = "#c8c8d8"
ZERO_CLR  = "#333348"


def compute_delta(session: fastf1.core.Session, driver_ref: str, driver_cmp: str):
    """
    Returns (delta_time, ref_tel, cmp_tel).
    delta > 0 means driver_ref is ahead (faster).
    """
    lap_ref = session.laps.pick_drivers(driver_ref).pick_fastest()
    lap_cmp = session.laps.pick_drivers(driver_cmp).pick_fastest()
    return fastf1.utils.delta_time(lap_ref, lap_cmp)


def plot_delta(session: fastf1.core.Session,
               driver_ref: str,
               driver_cmp: str,
               color_ref: str = "#FF8000",
               color_cmp: str = "#3671C6"):

    delta_time, ref_tel, cmp_tel = compute_delta(session, driver_ref, driver_cmp)

    fig, axes = plt.subplots(
        3, 1, figsize=(14, 10),
        gridspec_kw={"height_ratios": [2.5, 1.2, 1.2]},
        facecolor=DARK_BG,
    )
    fig.subplots_adjust(hspace=0.08)

    dist = ref_tel["Distance"].values
    delta = delta_time.values if hasattr(delta_time, "values") else np.array(delta_time)

    # ── Panel 1 — Delta time ──────────────────────────────────────────────────
    ax = axes[0]
    ax.set_facecolor(DARK_BG)

    pos_mask = delta >= 0
    ax.fill_between(dist, delta, 0, where=pos_mask,
                    color=color_ref, alpha=0.18, interpolate=True)
    ax.fill_between(dist, delta, 0, where=~pos_mask,
                    color=color_cmp, alpha=0.18, interpolate=True)
    ax.plot(dist, delta, color="#ffffff", linewidth=1.4, zorder=3)
    ax.axhline(0, color=ZERO_CLR, linewidth=0.8, linestyle="--")

    # Annotate net gap
    net = float(delta[-1])
    winner = driver_ref if net > 0 else driver_cmp
    ax.annotate(
        f"{winner}  +{abs(net):.3f}s",
        xy=(dist[-1], net),
        xytext=(-12, 6 if net > 0 else -14),
        textcoords="offset points",
        color="#f0f0ff",
        fontsize=9,
        fontfamily="monospace",
    )

    ax.set_ylabel("Delta (s)", color=TEXT_CLR, fontsize=10)
    ax.tick_params(colors=TEXT_CLR, labelsize=8)
    ax.set_xticklabels([])
    ax.grid(color=GRID_CLR, linewidth=0.5)
    ax.spines[:].set_color(GRID_CLR)

    # ── Panel 2 — Speed overlay ───────────────────────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor(DARK_BG)
    ax2.plot(dist, ref_tel["Speed"], color=color_ref, linewidth=1.3, label=driver_ref)
    ax2.plot(cmp_tel["Distance"], cmp_tel["Speed"],
             color=color_cmp, linewidth=1.3, label=driver_cmp)
    ax2.set_ylabel("Speed (km/h)", color=TEXT_CLR, fontsize=10)
    ax2.tick_params(colors=TEXT_CLR, labelsize=8)
    ax2.set_xticklabels([])
    ax2.grid(color=GRID_CLR, linewidth=0.5)
    ax2.spines[:].set_color(GRID_CLR)
    ax2.legend(facecolor="#0d0d18", edgecolor=GRID_CLR,
               labelcolor=TEXT_CLR, fontsize=9)

    # ── Panel 3 — Throttle overlay ────────────────────────────────────────────
    ax3 = axes[2]
    ax3.set_facecolor(DARK_BG)
    if "Throttle" in ref_tel.columns and "Throttle" in cmp_tel.columns:
        ax3.plot(dist, ref_tel["Throttle"], color=color_ref, linewidth=1.3)
        ax3.plot(cmp_tel["Distance"], cmp_tel["Throttle"],
                 color=color_cmp, linewidth=1.3)
    ax3.set_ylabel("Throttle (%)", color=TEXT_CLR, fontsize=10)
    ax3.set_xlabel("Distance (m)", color=TEXT_CLR, fontsize=10)
    ax3.tick_params(colors=TEXT_CLR, labelsize=8)
    ax3.grid(color=GRID_CLR, linewidth=0.5)
    ax3.spines[:].set_color(GRID_CLR)
    ax3.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))

    fig.suptitle(
        f"{driver_ref}  vs  {driver_cmp}  —  Delta Time Analysis",
        color="#f0f0ff",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )

    plt.tight_layout()
    plt.show()
    return fig


if __name__ == "__main__":
    fastf1.Cache.enable_cache("cache")
    session = fastf1.get_session(2025, "Australia", "Q")
    session.load()
    plot_delta(session, "NOR", "VER")
