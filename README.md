# 🏎️ F1 Telemetry Engine

A professional Formula 1 telemetry and race analytics platform built using FastF1, Streamlit, Plotly, Pandas, and NumPy.

F1 Telemetry Engine enables in-depth analysis of real Formula 1 timing, telemetry, positional, and strategy data through an interactive dashboard inspired by tools used by race engineers and performance analysts.

The platform supports telemetry comparison, delta-time analysis, racing line visualization, tyre strategy evaluation, and GPS-based race tracking using official Formula 1 timing feeds.

---

## ✨ Key Features

### 📊 Driver Performance Analysis

* Compare any two drivers across Practice, Qualifying, Sprint, or Race sessions
* Select any lap from a session, not just fastest laps
* Interactive telemetry overlays:

  * Speed
  * Throttle
  * Brake
  * Gear
  * RPM
* Corner-aware analysis using official circuit geometry

### ⏱ Delta Time Analysis

* Visualize time gained and lost throughout an entire lap
* Sector-by-sector performance breakdown
* Speed and telemetry overlays for deeper insights

### 🗺 Track & Racing Line Visualizations

* Interactive circuit maps generated from GPS telemetry
* Speed heatmaps across the circuit
* Driver racing line comparisons
* Gear and speed distribution analysis

### 🏁 Race Tracking

* Animated race replay using real positional telemetry
* Live position visualization for all drivers
* Team-accurate coloring
* Lap counter and session timeline controls

### 🛞 Tyre Strategy Analytics

* Strategy timeline visualization
* Compound usage analysis
* Tyre degradation trends
* Pit stop performance analysis
* Race pace comparison across stints

---

## 🚀 Why This Project?

Most Formula 1 analytics projects stop at plotting a fastest-lap speed trace.

F1 Telemetry Engine was designed to go further by combining telemetry analysis, positional tracking, tyre strategy evaluation, and interactive visualizations into a unified platform.

Key differentiators:

* Compare any lap from any session
* Cross-session analysis (Practice vs Qualifying, different years, etc.)
* Team-aware color mapping across seasons
* Real GPS-based race tracking
* Session-specific timing tower formatting
* Interactive multi-page analytics dashboard

---

## 🛠 Technology Stack

| Technology | Purpose                                          |
| ---------- | ------------------------------------------------ |
| FastF1     | Formula 1 telemetry, timing, and positional data |
| Streamlit  | Interactive dashboard framework                  |
| Plotly     | Interactive visualizations and animation         |
| Pandas     | Data processing and transformation               |
| NumPy      | Numerical operations and interpolation           |
| Matplotlib | Supplemental visualizations                      |
| Python     | Core application development                     |

---

## 📂 Project Structure

```text
F1-Telemetry-Engine/
│
├── cache/
├── src/
│   ├── data/
│   ├── analysis/
│   └── visualizations/
│
├── app/
│   ├── dashboard.py
│   └── pages/
│
├── requirements.txt
└── README.md
```

---

## 🎯 Skills Demonstrated

* Data Engineering
* Data Visualization
* Telemetry Analysis
* Time-Series Analytics
* Sports Analytics
* Interactive Dashboard Development
* Performance Optimization
* Python Development
* Data Processing with Pandas
* Scientific Computing with NumPy

---

## 🔮 Future Enhancements

* Strategy simulation module
* Tyre degradation prediction
* Driver performance forecasting
* Live session monitoring
* Cloud deployment
* REST API integration

---

## Acknowledgements

* FastF1 by Philipp Schaefer
* Formula 1 timing data © Formula One Management
* Open-source motorsport analytics community

This project is not affiliated with or endorsed by Formula 1, FIA, or any Formula 1 team.
