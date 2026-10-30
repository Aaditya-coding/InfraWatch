# InfraWatch Architecture

## Initial data flow
Sensor stream / simulator -> validation and preprocessing -> feature extraction -> anomaly detection -> risk assessment -> explanation and maintenance recommendation -> dashboard.

## Components
- `frontend/`: Streamlit UI and visualizations.
- `backend/simulation/`: synthetic sensor data and controllable failure scenarios.
- `backend/detection/`: anomaly detection and baseline comparisons.
- `backend/services/`: health/risk scoring and recommendation logic.
- `tests/`: unit and integration tests.

## Initial sensor signals
- Temperature (°C)
- Vibration (mm/s or clearly labelled simulated units)
- Pressure (bar)
- Power consumption (kW)

## MVP design principles
- Begin with deterministic synthetic data so the demo is reproducible.
- Compare normal operation with at least two simulated fault scenarios.
- Explain alerts using observed signal changes; do not present unsupported failure certainty.
- Keep anomaly detection separate from risk scoring and recommendations.
- Optional LLM summaries must not be the source of numerical risk calculations.

## Safety
This is a prototype for demonstration and decision support, not a certified predictive-maintenance or safety system. Do not connect it to live machinery or execute control actions.
