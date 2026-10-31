
from backend.simulation.sensor_simulator import SensorSimulator
from backend.detection.anomaly_detector import AnomalyDetector
from backend.services.risk_engine import RiskEngine


# Initialize all three modules
simulator = SensorSimulator(seed=42)
detector = AnomalyDetector()
risk_engine = RiskEngine()


print("\n========== INFRWATCH INTEGRATION TEST ==========")

# Step 1: Generate sensor readings
reading = simulator.generate_anomalous_reading()

print("\n1. SENSOR DATA")
print(reading)

# Step 2: Detect anomalies
detection_result = detector.detect(reading)

print("\n2. ANOMALY DETECTION")
print(detection_result)

# Step 3: Calculate infrastructure risk
risk_result = risk_engine.calculate_risk(detection_result)

print("\n3. RISK ASSESSMENT")

for key, value in risk_result.items():
    print(f"{key}: {value}")

print("\n========== TEST COMPLETED ==========")
