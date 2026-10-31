
import unittest

from backend.services.risk_engine import RiskEngine


class TestRiskEngine(unittest.TestCase):

    def setUp(self):
        self.engine = RiskEngine()

    def test_low_risk(self):

        detection = {
            "anomalies": []
        }

        result = self.engine.calculate_risk(detection)

        self.assertEqual(result["risk_score"], 0)
        self.assertEqual(result["risk_level"], "LOW")

    def test_medium_risk(self):

        detection = {
            "anomalies": [
                {"severity": "MEDIUM"},
                {"severity": "MEDIUM"}
            ]
        }

        result = self.engine.calculate_risk(detection)

        self.assertEqual(result["risk_score"], 20)
        self.assertEqual(result["risk_level"], "MEDIUM")

    def test_high_risk(self):

        detection = {
            "anomalies": [
                {"severity": "HIGH"},
                {"severity": "HIGH"}
            ]
        }

        result = self.engine.calculate_risk(detection)

        self.assertEqual(result["risk_score"], 40)
        self.assertEqual(result["risk_level"], "HIGH")

    def test_critical_risk(self):

        detection = {
            "anomalies": [
                {"severity": "CRITICAL"},
                {"severity": "CRITICAL"},
                {"severity": "CRITICAL"}
            ]
        }

        result = self.engine.calculate_risk(detection)

        self.assertEqual(result["risk_score"], 90)
        self.assertEqual(result["risk_level"], "CRITICAL")

    def test_risk_score_cannot_exceed_100(self):

        detection = {
            "anomalies": [
                {"severity": "CRITICAL"}
                for _ in range(10)
            ]
        }

        result = self.engine.calculate_risk(detection)

        self.assertEqual(result["risk_score"], 100)

    def test_severity_breakdown(self):

        detection = {
            "anomalies": [
                {"severity": "MEDIUM"},
                {"severity": "HIGH"},
                {"severity": "CRITICAL"}
            ]
        }

        result = self.engine.calculate_risk(detection)

        self.assertEqual(
            result["severity_breakdown"],
            {
                "MEDIUM": 1,
                "HIGH": 1,
                "CRITICAL": 1
            }
        )

    def test_invalid_detection_input(self):

        with self.assertRaises(TypeError):
            self.engine.calculate_risk("invalid")

    def test_invalid_severity(self):

        detection = {
            "anomalies": [
                {"severity": "UNKNOWN"}
            ]
        }

        with self.assertRaises(ValueError):
            self.engine.calculate_risk(detection)

    def test_invalid_max_score(self):

        with self.assertRaises(ValueError):
            RiskEngine(max_score=0)

    def test_custom_max_score(self):

        engine = RiskEngine(max_score=50)

        detection = {
            "anomalies": [
                {"severity": "CRITICAL"},
                {"severity": "CRITICAL"}
            ]
        }

        result = engine.calculate_risk(detection)

        self.assertEqual(result["risk_score"], 50)

    def test_anomaly_count(self):

        detection = {
            "anomalies": [
                {"severity": "HIGH"},
                {"severity": "MEDIUM"}
            ]
        }

        result = self.engine.calculate_risk(detection)

        self.assertEqual(result["anomaly_count"], 2)


if __name__ == "__main__":
    unittest.main()
