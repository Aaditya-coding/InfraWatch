
from backend.simulation.sensor_simulator import SensorSimulator
from backend.detection.anomaly_detector import AnomalyDetector
from backend.services.risk_engine import RiskEngine
from backend.services.recommendation_engine import RecommendationEngine


# Initialize all four modules
simulator = SensorSimulator(seed=42)
detector = AnomalyDetector()
risk_engine = RiskEngine()
recommendation_engine = RecommendationEngine()


print("\n==============================================")
print("       INFRWATCH INTELLIGENCE PIPELINE")
print("==============================================")


# MODULE A: Generate sensor readings
print("\n[MODULE A] SENSOR SIMULATOR")

reading = simulator.generate_anomalous_reading()

print(reading)


# MODULE B: Detect anomalies
print("\n[MODULE B] ANOMALY DETECTOR")

detection_result = detector.detect(reading)

print(detection_result)


# MODULE C: Calculate risk
print("\n[MODULE C] RISK ENGINE")

risk_result = risk_engine.calculate_risk(
    detection_result
)

print(risk_result)


# MODULE D: Generate recommendations
print("\n[MODULE D] RECOMMENDATION ENGINE")

recommendation_result = recommendation_engine.generate_recommendations(
    detection_result,
    risk_result
)

print("\nOVERALL RISK:")
print(recommendation_result["risk_level"])

print("\nRISK GUIDANCE:")
print(recommendation_result["risk_recommendation"])

print("\nRECOMMENDED ACTIONS:")

for index, item in enumerate(
    recommendation_result["recommendations"],
    start=1
):
    print(f"\n{index}. {item['metric']}")

    print(f"Priority: {item['priority']}")

    print(f"Action: {item['recommendation']}")


print("\n==============================================")
print("       PIPELINE EXECUTION COMPLETED")
print("==============================================")
