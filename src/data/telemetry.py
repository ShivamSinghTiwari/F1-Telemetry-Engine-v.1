"""
telemetry.py — telemetry extraction helpers.
"""
import fastf1
import pandas as pd


TELEMETRY_CHANNELS = ["Distance", "Speed", "Throttle", "Brake", "nGear", "RPM", "X", "Y", "Z"]


def get_fastest_lap_telemetry(session: fastf1.core.Session, driver: str) -> pd.DataFrame:
    """Return telemetry DataFrame for a driver's fastest lap."""
    lap = session.laps.pick_drivers(driver).pick_fastest()
    tel = lap.get_telemetry().add_distance()
    available = [c for c in TELEMETRY_CHANNELS if c in tel.columns]
    return tel[available]


def get_lap_telemetry(session: fastf1.core.Session, driver: str, lap_number: int) -> pd.DataFrame:
    """Return telemetry for a specific lap number."""
    lap = session.laps.pick_drivers(driver).pick_lap(lap_number)
    tel = lap.get_telemetry().add_distance()
    available = [c for c in TELEMETRY_CHANNELS if c in tel.columns]
    return tel[available]


def telemetry_summary(tel: pd.DataFrame) -> dict:
    """Return key stats from a telemetry DataFrame."""
    summary = {}
    if "Speed" in tel.columns:
        summary["top_speed_kmh"] = round(tel["Speed"].max(), 1)
        summary["avg_speed_kmh"] = round(tel["Speed"].mean(), 1)
    if "Throttle" in tel.columns:
        summary["full_throttle_pct"] = round((tel["Throttle"] == 100).mean() * 100, 1)
    if "Brake" in tel.columns:
        summary["braking_pct"] = round((tel["Brake"] > 0).mean() * 100, 1)
    if "nGear" in tel.columns:
        summary["avg_gear"] = round(tel["nGear"].mean(), 2)
    return summary


if __name__ == "__main__":
    fastf1.Cache.enable_cache("cache")
    session = fastf1.get_session(2025, "Australia", "Q")
    session.load()

    lap = session.laps.pick_fastest()
    print("Driver :", lap["Driver"])
    print("Lap Time:", lap["LapTime"])

    tel = get_fastest_lap_telemetry(session, lap["Driver"])
    print("\nColumns :", list(tel.columns))
    print("\nFirst 5 rows:")
    print(tel.head())
    print("\nSummary:")
    for k, v in telemetry_summary(tel).items():
        print(f"  {k}: {v}")
