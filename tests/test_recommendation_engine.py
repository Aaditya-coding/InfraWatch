
import unittest

from backend.services.recommendation_engine import RecommendationEngine


class TestRecommendationEngine(unittest.TestCase):

    def setUp(self):
        self.engine = RecommendationEngine()

    def test_cpu_recommendation(self):

        detection = {
            "anomalies": [
                {
                    "metric": "cpu_usage",
                    "severity": "CRITICAL"
                }
            ]
        }

        result = self.engine.generate_recommendations(detection)

        self.assertEqual(result["recommendation_count"], 1)
        self.assertEqual(
            result["recommendations"][0]["metric"],
            "cpu_usage"
        )

    def test_memory_recommendation(self):

        detection = {
            "anomalies": [
                {
                    "metric": "memory_usage",
                    "severity": "HIGH"
                }
            ]
        }

        result = self.engine.generate_recommendations(detection)

        self.assertEqual(
            result["recommendations"][0]["priority"],
            "HIGH"
        )

    def test_critical_priority(self):

        detection = {
            "anomalies": [
                {
                    "metric": "temperature",
                    "severity": "CRITICAL"
                }
            ]
        }

        result = self.engine.generate_recommendations(detection)

        self.assertEqual(
            result["recommendations"][0]["priority"],
            "URGENT"
        )

    def test_multiple_recommendations(self):

        detection = {
            "anomalies": [
                {"metric": "cpu_usage", "severity": "HIGH"},
                {"metric": "memory_usage", "severity": "MEDIUM"},
                {"metric": "disk_usage", "severity": "CRITICAL"}
            ]
        }

        result = self.engine.generate_recommendations(detection)

        self.assertEqual(result["recommendation_count"], 3)

    def test_recommendations_sorted_by_priority(self):

        detection = {
            "anomalies": [
                {"metric": "memory_usage", "severity": "MEDIUM"},
                {"metric": "cpu_usage", "severity": "CRITICAL"},
                {"metric": "disk_usage", "severity": "HIGH"}
            ]
        }

        result = self.engine.generate_recommendations(detection)

        priorities = [
            item["priority"]
            for item in result["recommendations"]
        ]

        self.assertEqual(
            priorities,
            ["URGENT", "HIGH", "MEDIUM"]
        )

    def test_no_anomalies(self):

        detection = {
            "is_anomaly": False,
            "anomalies": []
        }

        result = self.engine.generate_recommendations(detection)

        self.assertEqual(result["recommendation_count"], 1)
        self.assertEqual(
            result["recommendations"][0]["priority"],
            "LOW"
        )

    def test_risk_level(self):

        detection = {
            "anomalies": []
        }

        risk = {
            "risk_level": "CRITICAL"
        }

        result = self.engine.generate_recommendations(
            detection,
            risk
        )

        self.assertEqual(result["risk_level"], "CRITICAL")

    def test_unknown_metric(self):

        detection = {
            "anomalies": [
                {
                    "metric": "unknown_metric",
                    "severity": "HIGH"
                }
            ]
        }

        result = self.engine.generate_recommendations(detection)

        self.assertIn(
            "unknown_metric",
            result["recommendations"][0]["metric"]
        )

    def test_invalid_detection_input(self):

        with self.assertRaises(TypeError):
            self.engine.generate_recommendations("invalid")

    def test_invalid_severity(self):

        detection = {
            "anomalies": [
                {
                    "metric": "cpu_usage",
                    "severity": "UNKNOWN"
                }
            ]
        }

        with self.assertRaises(ValueError):
            self.engine.generate_recommendations(detection)

    def test_invalid_risk_input(self):

        with self.assertRaises(TypeError):
            self.engine.generate_recommendations(
                {"anomalies": []},
                "invalid"
            )


if __name__ == "__main__":
    unittest.main()
