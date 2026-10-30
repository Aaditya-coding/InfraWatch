# InfraWatch
**AI-Powered Predictive Infrastructure Monitoring & Failure Intelligence**

Hacktoberfest Hack Day Prayagraj × CC Club MNNIT — October 31, 2026

## Problem
Infrastructure operators often discover equipment problems only after performance degrades or equipment fails. Sensor readings can contain early warning patterns that are difficult to identify by looking at individual thresholds.

## Proposed solution
InfraWatch analyzes time-series sensor readings, detects abnormal behaviour, estimates equipment health/risk, explains contributing signals, and recommends preventive maintenance actions.

## Initial MVP
- Simulated sensor stream for a water pump or electric motor.
- Live dashboard for temperature, vibration, pressure and power.
- Anomaly detection and explainable alerts.
- Equipment health/risk indicator.
- Failure-pattern explanation and maintenance recommendations.
- Historical trend visualization and scenario simulation.

## Tech stack (proposed)
- Python
- Streamlit
- Pandas, NumPy
- Scikit-learn (Isolation Forest or a simple statistical baseline)
- Plotly
- Optional Gemini API for natural-language incident summaries

## Repository layout
- `frontend/`: Streamlit dashboard
- `backend/`: data generation, detection and risk logic
- `backend/detection/`: anomaly detection
- `backend/simulation/`: synthetic sensor data and failure scenarios
- `backend/services/`: analysis and recommendation services
- `tests/`: automated tests
- `docs/`: architecture and demo notes

## Setup
1. Create a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` only if using optional AI summaries.
4. Run instructions will be added as the MVP entrypoints are implemented.

## Safety and honesty
InfraWatch is a hackathon prototype, not a certified safety or industrial control system. Predictions are estimates, not guarantees. Never connect the prototype to live control equipment or automatically shut down machinery.

## Team workflow
Use feature branches and pull requests. Keep `main` stable. Commit meaningful work throughout the event.

## License
MIT. See `LICENSE`.
