
import unittest

from backend.simulation.sensor_simulator import SensorSimulator


class TestSensorSimulator(unittest.TestCase):

    def setUp(self):
        self.simulator = SensorSimulator(seed=42)

    def test_generate_reading(self):
        reading = self.simulator.generate_reading()

        self.assertIsInstance(reading, dict)

        expected_keys = [
            "timestamp",
            "cpu_usage",
            "memory_usage",
            "disk_usage",
            "network_usage",
            "temperature"
        ]

        for key in expected_keys:
            self.assertIn(key, reading)

    def test_reading_values_are_numeric(self):
        reading = self.simulator.generate_reading()

        metrics = [
            "cpu_usage",
            "memory_usage",
            "disk_usage",
            "network_usage",
            "temperature"
        ]

        for metric in metrics:
            self.assertIsInstance(reading[metric], (int, float))

    def test_generate_multiple_readings(self):
        readings = self.simulator.generate_multiple_readings(5)

        self.assertEqual(len(readings), 5)

    def test_generate_zero_readings(self):
        readings = self.simulator.generate_multiple_readings(0)

        self.assertEqual(readings, [])

    def test_negative_count_raises_error(self):
        with self.assertRaises(ValueError):
            self.simulator.generate_multiple_readings(-1)

    def test_anomalous_reading(self):
        reading = self.simulator.generate_anomalous_reading()

        self.assertGreaterEqual(reading["cpu_usage"], 90)
        self.assertGreaterEqual(reading["memory_usage"], 90)


if __name__ == "__main__":
    unittest.main()
