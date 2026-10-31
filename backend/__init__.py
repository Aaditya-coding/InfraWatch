"""
InfraWatch Backend Intelligence Package.
Provides modules for synthetic sensor simulation, multivariate anomaly detection,
risk assessment, and prescriptive maintenance recommendations.
"""

from backend.simulation.sensor_simulator import SensorSimulator, generate_sensor_stream
from backend.detection.anomaly_detector import AnomalyDetector, detect_anomalies
from backend.services.risk_engine import RiskEngine, calculate_risk
from backend.services.recommendation_engine import RecommendationEngine, generate_recommendations

__all__ = [
    "SensorSimulator",
    "generate_sensor_stream",
    "AnomalyDetector",
    "detect_anomalies",
    "RiskEngine",
    "calculate_risk",
    "RecommendationEngine",
    "generate_recommendations",
]
