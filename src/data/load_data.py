"""
load_data.py — session loader with caching and basic summary.
"""
import fastf1
import pandas as pd


def load_session(year: int, race: str, session_type: str = "Q") -> fastf1.core.Session:
    fastf1.Cache.enable_cache("cache")
    session = fastf1.get_session(year, race, session_type)
    session.load()
    return session


def session_summary(session: fastf1.core.Session) -> pd.DataFrame:
    """Return a clean DataFrame of fastest laps per driver."""
    records = []
    for drv in session.laps["Driver"].unique():
        drv_laps = session.laps.pick_drivers(drv)
        try:
            fl = drv_laps.pick_fastest()
            records.append({
                "Driver": drv,
                "LapTime": fl["LapTime"],
                "Compound": fl.get("Compound", "N/A"),
                "TyreLife": fl.get("TyreLife", None),
                "Sector1": fl.get("Sector1Time", None),
                "Sector2": fl.get("Sector2Time", None),
                "Sector3": fl.get("Sector3Time", None),
            })
        except Exception:
            continue
    return pd.DataFrame(records).sort_values("LapTime").reset_index(drop=True)


if __name__ == "__main__":
    sess = load_session(2025, "Australia", "Q")
    summary = session_summary(sess)
    print(summary.to_string())
