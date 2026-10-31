
from backend.simulation.sensor_simulator import SensorSimulator
from backend.detection.anomaly_detector import AnomalyDetector


# Initialize both modules
simulator = SensorSimulator(seed=42)
detector = AnomalyDetector()

# Generate normal sensor data
reading = simulator.generate_reading()

# Detect anomalies
result = detector.detect(reading)

print("\n========== INFRWATCH INTEGRATION TEST ==========")

print("\nGenerated Sensor Reading:")
print(reading)

print("\nAnomaly Detection Result:")
print(result)

# Generate an intentionally abnormal reading
abnormal_reading = simulator.generate_anomalous_reading()

abnormal_result = detector.detect(abnormal_reading)

print("\nAbnormal Sensor Reading:")
print(abnormal_reading)

print("\nAbnormal Detection Result:")
print(abnormal_result)
