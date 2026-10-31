"""
Backend Bridge for InfraWatch
Provides seamless integration between Om's frontend and Aditya's backend.
If Aditya's backend modules are available, it uses them; otherwise, it provides
a realistic fallback simulator that strictly adheres to the team's data contract.
"""

import sys
import os
import time
import math
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add repository root to path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Check if Aditya's backend modules are imported successfully
BACKEND_AVAILABLE = False
try:
    from backend.simulation.sensor_simulator import generate_sensor_stream  # type: ignore
    from backend.detection.anomaly_detector import detect_anomalies  # type: ignore
    from backend.services.risk_engine import calculate_risk  # type: ignore
    from backend.services.recommendation_engine import generate_recommendations  # type: ignore
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False


class FallbackSimulator:
    """High-fidelity Industrial Water Pump telemetry simulator adhering to contract."""

    def __init__(self):
        self.history = []
        self._init_baseline()

    def _init_baseline(self):
        # Baseline normal values for a multi-stage centrifugal feed pump
        self.base_temp = 58.0      # °C
        self.base_vib = 2.4        # mm/s RMS (ISO 10816 Zone A/B)
        self.base_press = 4.2      # bar (Discharge)
        self.base_power = 7.5      # kW
        self.step_idx = 0

    def generate_point(self, scenario="Normal Operation", inject_spike=False):
        self.step_idx += 1
        now = datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")

        # Harmonic oscillations
        wave = math.sin(self.step_idx * 0.15)
        jitter = random.uniform(-0.15, 0.15)

        temp = self.base_temp + wave * 0.5 + random.uniform(-0.3, 0.3)
        vib = self.base_vib + abs(wave * 0.3) + random.uniform(-0.1, 0.1)
        press = self.base_press + wave * 0.1 + random.uniform(-0.05, 0.05)
        power = self.base_power + wave * 0.2 + random.uniform(-0.1, 0.1)

        is_anomaly = False
        risk_score = 95  # Health score: 95% = Healthy
        risk_level = "NORMAL"
        root_cause = "Operating within normal parameters."
        recommendation = "Routine scheduled inspection according to preventive maintenance plan."
        rul_hours = 720  # Remaining Useful Life

        # Component health states
        comp_health = {
            "motor": "HEALTHY",
            "de_bearing": "HEALTHY",
            "nde_bearing": "HEALTHY",
            "impeller": "HEALTHY",
            "seal": "HEALTHY"
        }

        # Fault Scenarios
        if scenario == "Bearing Fault (BPFO/BPFI)":
            severity = min(1.0, 0.3 + (self.step_idx % 60) * 0.015)
            vib += severity * 5.8 + random.uniform(0.2, 0.9)
            temp += severity * 24.0 + random.uniform(-0.5, 1.2)
            power += severity * 1.8
            is_anomaly = vib > 4.5 or temp > 72.0
            risk_score = max(18, int(95 - severity * 65))
            if risk_score > 70:
                risk_level = "LOW_RISK"
                root_cause = "Micro-frictional warming detected in Non-Drive End (NDE) bearing."
                recommendation = "Schedule acoustic vibration check on next shift."
                rul_hours = 180
                comp_health["nde_bearing"] = "DEGRADING"
            elif risk_score > 40:
                risk_level = "WARNING"
                root_cause = "Outer race fault harmonic (BPFO @ 107Hz) with elevated thermal rise."
                recommendation = "Re-lubricate NDE bearing with ISO VG 68 synthetic grease within 24h."
                rul_hours = 48
                comp_health["nde_bearing"] = "WARNING"
                comp_health["de_bearing"] = "DEGRADING"
            else:
                risk_level = "CRITICAL"
                root_cause = "Severe bearing raceway spalling and thermal runaway imminent."
                recommendation = "Trigger emergency de-rate or switch load to standby pump unit."
                rul_hours = 6
                comp_health["nde_bearing"] = "CRITICAL"
                comp_health["de_bearing"] = "WARNING"

        elif scenario == "Impeller Cavitation & Blockage":
            severity = min(1.0, 0.35 + (self.step_idx % 60) * 0.014)
            press -= severity * 2.4 + random.uniform(-0.1, 0.1)
            vib += severity * 3.2 + random.uniform(0.4, 1.4)  # Cavitation high-frequency broad noise
            power += severity * 2.8 + random.uniform(-0.2, 0.5)
            is_anomaly = press < 3.0 or vib > 4.2
            risk_score = max(22, int(92 - severity * 60))
            if risk_score > 65:
                risk_level = "LOW_RISK"
                root_cause = "Suction head fluctuation causing minor hydraulic turbulence."
                recommendation = "Verify suction line valve clearance and filter mesh."
                rul_hours = 120
                comp_health["impeller"] = "DEGRADING"
            elif risk_score > 35:
                risk_level = "WARNING"
                root_cause = "Cavitation bubble collapse detected; pressure dropped below Net Positive Suction Head (NPSH)."
                recommendation = "Inspect suction strainer for debris and adjust inlet throttling."
                rul_hours = 36
                comp_health["impeller"] = "WARNING"
                comp_health["seal"] = "DEGRADING"
            else:
                risk_level = "CRITICAL"
                root_cause = "Severe impeller pitting and hydraulic stall risk; pressure loss > 55%."
                recommendation = "Halt pump to prevent permanent impeller volute damage."
                rul_hours = 4
                comp_health["impeller"] = "CRITICAL"
                comp_health["seal"] = "WARNING"

        elif scenario == "Critical Multi-Fault":
            severity = min(1.0, 0.5 + (self.step_idx % 50) * 0.015)
            temp += severity * 32.0 + random.uniform(0.5, 2.0)
            vib += severity * 7.5 + random.uniform(0.5, 2.0)
            press -= severity * 2.6
            power += severity * 4.2
            is_anomaly = True
            risk_score = max(10, int(90 - severity * 75))
            risk_level = "CRITICAL"
            root_cause = "Multivariate failure: Combined thermal overload, shaft deflection, and hydraulic collapse."
            recommendation = "IMMEDIATE ACTION: Trip motor circuit breaker and inspect mechanical coupling."
            rul_hours = 1
            comp_health["motor"] = "CRITICAL"
            comp_health["nde_bearing"] = "CRITICAL"
            comp_health["impeller"] = "CRITICAL"

        # Transient manual spike injection
        if inject_spike:
            vib += random.uniform(4.0, 7.0)
            temp += random.uniform(8.0, 15.0)
            is_anomaly = True
            risk_score = min(risk_score, 30)
            risk_level = "CRITICAL"
            root_cause = "Transient mechanical shock or sudden electrical load disturbance detected."
            recommendation = "Investigate telemetry transient log for sudden load change."

        point = {
            "timestamp": timestamp_str,
            "temperature": round(float(temp), 2),
            "vibration": round(float(vib), 2),
            "pressure": round(float(max(0.1, press)), 2),
            "power": round(float(power), 2),
            "anomaly": bool(is_anomaly),
            "risk_score": int(risk_score),
            "risk_level": risk_level,
            "root_cause": root_cause,
            "recommendation": recommendation,
            "rul_hours": rul_hours,
            "comp_health": comp_health
        }
        self.history.append(point)
        if len(self.history) > 300:
            self.history.pop(0)
        return point


# Global simulator instance
_simulator = FallbackSimulator()


def get_latest_telemetry(scenario="Normal Operation", inject_spike=False):
    """
    Standard interface function used by Om's Streamlit frontend.
    Delegates to Aditya's backend if present, else uses fallback simulator.
    """
    if BACKEND_AVAILABLE:
        try:
            # When Aditya's functions are ready
            data_point = generate_sensor_stream(scenario=scenario)
            anomaly_info = detect_anomalies(data_point)
            risk_info = calculate_risk(anomaly_info)
            recommendations = generate_recommendations(risk_info)
            data_point.update(anomaly_info)
            data_point.update(risk_info)
            data_point.update(recommendations)
            return data_point
        except Exception:
            # Safe fallback if backend is still being finalized
            return _simulator.generate_point(scenario, inject_spike)
    else:
        return _simulator.generate_point(scenario, inject_spike)


def get_initial_history(count=50, scenario="Normal Operation"):
    """Pre-populates a warm-up dataset for immediate visualization."""
    data = []
    for _ in range(count):
        pt = _simulator.generate_point(scenario=scenario)
        data.append(pt)
    return pd.DataFrame(data)
