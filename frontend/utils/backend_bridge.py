"""
Backend Bridge for InfraWatch with Physics-Based Operational Dynamics.
Provides seamless integration between Om's frontend and Aditya's backend.
If Aditya's backend modules are available, it uses them; otherwise, it provides
a realistic fallback simulator that strictly adheres to the team's data contract.
"""

import sys
import os
import math
import random
import pandas as pd
import numpy as np
from datetime import datetime

# Add repository root to path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

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
    """High-fidelity Industrial Water Pump telemetry simulator with physics modeling."""

    def __init__(self):
        self.history = []
        self._init_baseline()

    def _init_baseline(self):
        self.base_temp = 58.0      # °C
        self.base_vib = 2.4        # mm/s RMS (ISO 10816 Zone A/B)
        self.base_press = 4.2      # bar (Discharge)
        self.base_power = 7.5      # kW
        self.step_idx = 0

    def generate_point(self, scenario="Normal Operation", inject_spike=False, rpm=2950, throttle=100, ambient_temp=28.0, sensitivity_z=2.5):
        self.step_idx += 1
        now = datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")

        # Harmonic oscillations
        wave = math.sin(self.step_idx * 0.15)
        
        # Physics modifiers based on user interactive sliders
        speed_factor = (rpm / 2950.0)
        throttle_factor = (throttle / 100.0)
        thermal_ambient_offset = (ambient_temp - 28.0) * 0.35

        temp = (self.base_temp + thermal_ambient_offset) + wave * 0.5 + random.uniform(-0.3, 0.3)
        vib = (self.base_vib * (speed_factor ** 1.3)) + abs(wave * 0.25) + random.uniform(-0.1, 0.1)
        press = (self.base_press * (speed_factor ** 1.8) * throttle_factor) + wave * 0.08 + random.uniform(-0.04, 0.04)
        power = (self.base_power * (speed_factor ** 2.2) * (0.4 + 0.6 * throttle_factor)) + wave * 0.15 + random.uniform(-0.1, 0.1)

        # Suction throttling below 65% induces flow turbulence and cavitation
        if throttle < 65:
            throttle_cav_vib = ((65 - throttle) / 10.0) * 0.65
            vib += throttle_cav_vib + random.uniform(0.1, 0.3)
            press = max(0.5, press - ((65 - throttle) / 20.0) * 0.8)

        risk_score = 95
        risk_level = "NORMAL"
        root_cause = "Operating within normal parameters."
        recommendation = "Routine scheduled inspection according to preventive maintenance plan."
        rul_hours = 720

        comp_health = {
            "motor": "HEALTHY",
            "de_bearing": "HEALTHY",
            "nde_bearing": "HEALTHY",
            "impeller": "HEALTHY",
            "seal": "HEALTHY"
        }

        # Subsystem Detailed Specs for Drill-Down Inspector
        subsystem_specs = {
            "nde_bearing": {
                "model": "SKF 6308-2Z C3 Deep Groove Ball Bearing",
                "lubricant_health": "96% (Shell Gadus S2 V220)",
                "clearance_mm": "0.018 mm (Normal)",
                "vibration_envelope_g": f"{round(vib * 0.32, 2)} g pk-pk",
                "recommended_action": "Routine grease replenishment in 400 operating hours."
            },
            "de_bearing": {
                "model": "SKF 6310-2Z Roller Bearing",
                "lubricant_health": "94%",
                "clearance_mm": "0.022 mm (Normal)",
                "vibration_envelope_g": f"{round(vib * 0.28, 2)} g pk-pk",
                "recommended_action": "Coupling alignment check on next scheduled shutdown."
            },
            "motor": {
                "model": "Siemens 1LE1001-1DB2 11kW Induction Motor",
                "winding_temp": f"{round(temp + 6.5, 1)} °C (Class F Insulation Limit: 155°C)",
                "phase_current": f"{round(power * 1.82, 1)} A",
                "efficiency": "91.8% (IE3 Premium)",
                "recommended_action": "Check fan cowl airflow intake."
            },
            "impeller": {
                "model": "Grundfos 4-Stage Laser-Welded AISI 316 Stainless Steel",
                "npsh_available": f"{round(press * 1.45, 2)} bar",
                "cavitation_risk_index": "LOW (Normal laminar flow)",
                "volute_pressure": f"{round(press, 2)} bar",
                "recommended_action": "No hydraulic wear observed."
            },
            "seal": {
                "model": "Burgmann MG1 Silicon Carbide / Carbon Cartridge Seal",
                "barrier_pressure": f"{round(press + 0.4, 2)} bar",
                "leakage_rate": "0.0 ml/min",
                "face_temp": f"{round(temp - 4.0, 1)} °C",
                "recommended_action": "Inspect barrier fluid reservoir level."
            }
        }

        # Fault Scenarios
        if scenario == "Bearing Fault (BPFO/BPFI)":
            severity = min(1.0, 0.35 + (self.step_idx % 60) * 0.015)
            vib += severity * 5.8 + random.uniform(0.2, 0.9)
            temp += severity * 24.0 + random.uniform(-0.5, 1.2)
            power += severity * 1.8
            risk_score = max(18, int(95 - severity * 65))
            if risk_score > 70:
                risk_level = "LOW_RISK"
                root_cause = "Micro-frictional warming detected in Non-Drive End (NDE) bearing."
                recommendation = "Schedule acoustic vibration check on next shift."
                rul_hours = 180
                comp_health["nde_bearing"] = "DEGRADING"
                subsystem_specs["nde_bearing"]["lubricant_health"] = "62% (Thermal degradation)"
            elif risk_score > 40:
                risk_level = "WARNING"
                root_cause = "Outer race fault harmonic (BPFO @ 107.5 Hz) with elevated thermal rise."
                recommendation = "Re-lubricate NDE bearing with ISO VG 68 synthetic grease within 24h."
                rul_hours = 48
                comp_health["nde_bearing"] = "WARNING"
                comp_health["de_bearing"] = "DEGRADING"
                subsystem_specs["nde_bearing"]["lubricant_health"] = "34% (Grease depletion)"
                subsystem_specs["nde_bearing"]["clearance_mm"] = "0.045 mm (High)"
                subsystem_specs["nde_bearing"]["recommended_action"] = "Immediate re-lubrication (25g ISO VG 68 grease)."
            else:
                risk_level = "CRITICAL"
                root_cause = "Severe bearing raceway spalling and thermal runaway imminent."
                recommendation = "Trigger emergency de-rate or switch load to standby pump unit."
                rul_hours = 6
                comp_health["nde_bearing"] = "CRITICAL"
                comp_health["de_bearing"] = "WARNING"
                subsystem_specs["nde_bearing"]["lubricant_health"] = "12% (Burnt)"
                subsystem_specs["nde_bearing"]["clearance_mm"] = "0.092 mm (EXCESSIVE)"

        elif scenario == "Impeller Cavitation & Blockage":
            severity = min(1.0, 0.35 + (self.step_idx % 60) * 0.014)
            press -= severity * 2.4 + random.uniform(-0.1, 0.1)
            vib += severity * 3.2 + random.uniform(0.4, 1.4)
            power += severity * 2.8 + random.uniform(-0.2, 0.5)
            risk_score = max(22, int(92 - severity * 60))
            if risk_score > 65:
                risk_level = "LOW_RISK"
                root_cause = "Suction head fluctuation causing minor hydraulic turbulence."
                recommendation = "Verify suction line valve clearance and filter mesh."
                rul_hours = 120
                comp_health["impeller"] = "DEGRADING"
                subsystem_specs["impeller"]["cavitation_risk_index"] = "MODERATE (Turbulent eddies)"
            elif risk_score > 35:
                risk_level = "WARNING"
                root_cause = "Cavitation bubble collapse detected; pressure dropped below Net Positive Suction Head (NPSH)."
                recommendation = "Inspect suction strainer for debris and adjust inlet throttling."
                rul_hours = 36
                comp_health["impeller"] = "WARNING"
                comp_health["seal"] = "DEGRADING"
                subsystem_specs["impeller"]["cavitation_risk_index"] = "HIGH (Vapor bubble micro-implosions)"
                subsystem_specs["impeller"]["recommended_action"] = "Open suction throttling valve to > 85%."
            else:
                risk_level = "CRITICAL"
                root_cause = "Severe impeller pitting and hydraulic stall risk; pressure loss > 55%."
                recommendation = "Halt pump to prevent permanent impeller volute damage."
                rul_hours = 4
                comp_health["impeller"] = "CRITICAL"
                comp_health["seal"] = "WARNING"
                subsystem_specs["impeller"]["cavitation_risk_index"] = "CRITICAL (Severe pitting erosion)"

        elif scenario == "Critical Multi-Fault":
            severity = min(1.0, 0.5 + (self.step_idx % 50) * 0.015)
            temp += severity * 32.0 + random.uniform(0.5, 2.0)
            vib += severity * 7.5 + random.uniform(0.5, 2.0)
            press -= severity * 2.6
            power += severity * 4.2
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
            risk_score = min(risk_score, 30)
            risk_level = "CRITICAL"
            root_cause = "Transient mechanical shock or sudden electrical load disturbance detected."
            recommendation = "Investigate telemetry transient log for sudden load change."

        # Dynamic Anomaly Evaluation using Sensitivity Slider (Z-Threshold)
        # Normal baseline: vib ~2.4 (std ~0.4), temp ~58.0 (std ~2.5), press ~4.2 (std ~0.3)
        z_vib = abs(vib - self.base_vib) / 0.45
        z_temp = abs(temp - self.base_temp) / 3.0
        z_press = abs(press - self.base_press) / 0.4
        
        is_anomaly = (z_vib > sensitivity_z) or (z_temp > sensitivity_z) or (z_press > sensitivity_z) or (risk_score < 60)

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
            "comp_health": comp_health,
            "subsystem_specs": subsystem_specs,
            "rpm": int(rpm),
            "throttle": int(throttle)
        }
        self.history.append(point)
        if len(self.history) > 300:
            self.history.pop(0)
        return point


_simulator = FallbackSimulator()


def get_latest_telemetry(scenario="Normal Operation", inject_spike=False, rpm=2950, throttle=100, ambient_temp=28.0, sensitivity_z=2.5):
    """Standard interface function connecting Om's Streamlit frontend with Aditya's backend ML pipeline."""
    point = _simulator.generate_point(
        scenario=scenario,
        inject_spike=inject_spike,
        rpm=rpm,
        throttle=throttle,
        ambient_temp=ambient_temp,
        sensitivity_z=sensitivity_z
    )

    if BACKEND_AVAILABLE:
        try:
            # 1. Feed real-time telemetry into Aditya's AnomalyDetector
            anomaly_payload = {
                "temperature": point["temperature"],
                "vibration": point["vibration"],
                "pressure": point["pressure"],
                "power": point["power"]
            }
            anomaly_info = detect_anomalies(anomaly_payload)

            # 2. Feed detected anomalies into Aditya's RiskEngine
            risk_info = calculate_risk(anomaly_info)

            # 3. Feed risk and anomalies into Aditya's RecommendationEngine
            rec_info = generate_recommendations(anomaly_info, risk_info)

            # Update telemetry flags and prescriptive actions if anomalies detected
            if anomaly_info.get("is_anomaly"):
                point["anomaly"] = True

            # If backend generated prescriptive recommendations, enrich root cause & action
            recs = rec_info.get("recommendations", [])
            urgent_recs = [r for r in recs if r.get("priority") in ["URGENT", "HIGH"]]
            if urgent_recs:
                point["recommendation"] = urgent_recs[0]["recommendation"]
                anom_metrics = [a["metric"] for a in anomaly_info.get("anomalies", [])]
                point["root_cause"] = f"Backend ML detected {risk_info.get('anomaly_count')} anomaly signals ({', '.join(anom_metrics)}). {point['root_cause']}"
        except Exception:
            pass

    return point


def get_initial_history(count=50, scenario="Normal Operation", rpm=2950, throttle=100, ambient_temp=28.0, sensitivity_z=2.5):
    """Pre-populates a warm-up dataset for immediate visualization."""
    data = []
    for _ in range(count):
        pt = _simulator.generate_point(scenario=scenario, rpm=rpm, throttle=throttle, ambient_temp=ambient_temp, sensitivity_z=sensitivity_z)
        data.append(pt)
    return pd.DataFrame(data)
