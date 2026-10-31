
import unittest

from backend.detection.anomaly_detector import AnomalyDetector


class TestAnomalyDetector(unittest.TestCase):

    def setUp(self):
        self.detector = AnomalyDetector()

    def test_detect_normal_reading(self):

        reading = {
            "cpu_usage": 40,
            "memory_usage": 50,
            "disk_usage": 60,
            "network_usage": 200,
            "temperature": 35
        }

        result = self.detector.detect(reading)

        self.assertFalse(result["is_anomaly"])
        self.assertEqual(result["anomaly_count"], 0)

    def test_detect_cpu_anomaly(self):

        reading = {
            "cpu_usage": 95,
            "memory_usage": 50,
            "disk_usage": 60,
            "network_usage": 200,
            "temperature": 35
        }

        result = self.detector.detect(reading)

        self.assertTrue(result["is_anomaly"])
        self.assertEqual(result["anomaly_count"], 1)
        self.assertEqual(
            result["anomalies"][0]["metric"],
            "cpu_usage"
        )

    def test_detect_multiple_anomalies(self):

        reading = {
            "cpu_usage": 95,
            "memory_usage": 95,
            "disk_usage": 95,
            "network_usage": 200,
            "temperature": 35
        }

        result = self.detector.detect(reading)

        self.assertEqual(result["anomaly_count"], 3)

    def test_critical_severity(self):

        reading = {
            "cpu_usage": 100,
            "memory_usage": 50,
            "disk_usage": 60,
            "network_usage": 200,
            "temperature": 35
        }

        result = self.detector.detect(reading)

        self.assertEqual(
            result["anomalies"][0]["severity"],
            "CRITICAL"
        )

    def test_invalid_reading(self):

        with self.assertRaises(TypeError):
            self.detector.detect("invalid")

    def test_invalid_metric_value(self):

        reading = {
            "cpu_usage": "high"
        }

        with self.assertRaises(ValueError):
            self.detector.detect(reading)

    def test_custom_threshold(self):

        detector = AnomalyDetector({
            "cpu_usage": 50
        })

        result = detector.detect({
            "cpu_usage": 60
        })

        self.assertTrue(result["is_anomaly"])


if __name__ == "__main__":
    unittest.main()
