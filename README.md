# InfraWatch
**AI-Powered Predictive Infrastructure Monitoring & Digital Twin Intelligence**

Hacktoberfest Hack Day Prayagraj × CC Club MNNIT — October 31, 2026  
Track 1: Applied AI / IoT Condition Monitoring

---

## ⚡ Quick Start (Single-Click Web Launch)

To start the application on the web, simply **double-click** the launcher file in the project folder:

```
start.bat
```
*(Alternatively, `run.bat` is also available).*

This launcher will automatically:
1. Detect your configured Python virtual environment (`venv`).
2. Start the Streamlit application server.
3. Automatically launch your default web browser directly to `http://localhost:8501`.

---

## Problem & Solution
* **Problem:** Industrial and infrastructure operators often discover equipment degradation only after catastrophic mechanical breakdown or unscheduled outage. Traditional SCADA alerts rely on static, single-point thresholds that fail to detect early multivariate failure signatures.
* **Solution:** **InfraWatch** integrates continuous synthetic sensor telemetry with a multi-stage predictive pipeline:
  1. **Sensor Simulator (Module A):** Physics-modeled telemetry stream (Vibration, Temperature, Discharge Pressure, Active Power).
  2. **Anomaly Detector (Module B):** Multivariate anomaly engine using statistical thresholding and rolling Z-score detection.
  3. **Risk Engine (Module C):** Dynamic severity assessment and risk classification.
  4. **Recommendation Engine (Module D):** ISO/OEM-aligned prescriptive maintenance work order actions.
  5. **Digital Twin Web Dashboard:** Live animated SVG schematic, real-time Plotly spectral/correlation analytics, acoustic vibration sonification, and SCADA work order export.

---

## Tech Stack
* **Language & Framework:** Python 3.10+, Streamlit
* **Data Processing & ML:** NumPy, Pandas, Scikit-learn
* **Visualizations:** Plotly Interactive Charts, SVG Animated Schematics
* **Signal Analysis:** Fast Fourier Transform (FFT) Harmonics & Audio Waveform Sonification
* **Testing:** Pytest, Unittest

---

## Repository Layout
```
InfraWatch/
├── backend/
│   ├── detection/             # Module B: Anomaly Detection Engine
│   │   └── anomaly_detector.py
│   ├── services/              # Module C & D: Risk Assessment & Prescriptive Actions
│   │   ├── risk_engine.py
│   │   └── recommendation_engine.py
│   └── simulation/            # Module A: Sensor Simulation & Fault Modes
│       └── sensor_simulator.py
├── frontend/
│   ├── app.py                 # Streamlit entrypoint
│   ├── components/            # UI components (KPI cards, SVG Digital Twin, FFT, Alerts)
│   └── utils/                 # Audio synthesizer & backend bridge
├── tests/                     # Automated unit test suite (35 tests)
│   ├── test_anomaly_detector.py
│   ├── test_recommendation_engine.py
│   ├── test_risk_engine.py
│   └── test_sensor_simulator.py
├── start.bat                  # Single-click Windows launcher
├── run.bat                    # Single-click Windows launcher alias
├── requirements.txt           # Project dependencies
└── README.md
```

---

## Manual Execution

If you prefer running from PowerShell or Command Prompt:

```powershell
# 1. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run the Streamlit web dashboard
streamlit run frontend/app.py
```

---

## Running Automated Tests

Run the full automated test suite (35 passing unit tests):
```powershell
pytest
```

Run integration test scripts:
```powershell
python test_full_pipeline.py
python test_module_b_integration.py
python test_module_c_integration.py
```

---

## Safety and Prototype Scope
InfraWatch is an applied AI decision-support prototype built for hackathon demonstration. Predictions and RUL estimates are simulated heuristics and not certified industrial safety control systems. Do not connect directly to high-voltage industrial actuators.

---

## License
MIT. See `LICENSE`.
