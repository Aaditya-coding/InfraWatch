
import random
import time
from datetime import datetime, timezone


class SensorSimulator:
    """
    Simulates infrastructure sensor readings.
    Generates CPU, memory, disk, and network metrics.
    """

    def __init__(self, seed=None):
        self.random = random.Random(seed)

    def generate_reading(self):
        """Generate one simulated sensor reading."""

        reading = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cpu_usage": round(self.random.uniform(10, 95), 2),
            "memory_usage": round(self.random.uniform(20, 90), 2),
            "disk_usage": round(self.random.uniform(10, 95), 2),
            "network_usage": round(self.random.uniform(5, 1000), 2),
            "temperature": round(self.random.uniform(25, 85), 2),
        }

        return reading

    def generate_anomalous_reading(self):
        """Generate a reading containing unusually high metrics."""

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cpu_usage": round(self.random.uniform(90, 100), 2),
            "memory_usage": round(self.random.uniform(90, 100), 2),
            "disk_usage": round(self.random.uniform(90, 100), 2),
            "network_usage": round(self.random.uniform(900, 1500), 2),
            "temperature": round(self.random.uniform(85, 100), 2),
        }

    def generate_multiple_readings(self, count=10):
        """Generate multiple sensor readings."""

        if count < 0:
            raise ValueError("Count cannot be negative.")

        return [self.generate_reading() for _ in range(count)]

    def stream_readings(self, interval=1):
        """Continuously generate readings."""

        if interval < 0:
            raise ValueError("Interval cannot be negative.")

        while True:
            yield self.generate_reading()
            time.sleep(interval)


if __name__ == "__main__":
    simulator = SensorSimulator()

    print("InfraWatch Sensor Simulator")
    print("-" * 40)

    for reading in simulator.generate_multiple_readings(5):
        print(reading)
