
class RiskEngine:
    """
    InfraWatch Risk Assessment Engine.

    Calculates infrastructure risk scores using anomalies
    detected by the AnomalyDetector module.
    """

    # Points assigned to each anomaly severity
    SEVERITY_WEIGHTS = {
        "MEDIUM": 10,
        "HIGH": 20,
        "CRITICAL": 30
    }

    def __init__(self, max_score=100):
        """
        Initialize the risk engine.

        Args:
            max_score: Maximum possible risk score.
        """

        if (
            not isinstance(max_score, (int, float))
            or isinstance(max_score, bool)
            or max_score <= 0
        ):
            raise ValueError("Maximum score must be a positive number.")

        self.max_score = max_score

    def calculate_risk(self, detection_result):
        """
        Calculate overall infrastructure risk.

        Args:
            detection_result: Output from AnomalyDetector.detect()

        Returns:
            Dictionary containing risk score, risk level,
            anomaly count and description.
        """

        if not isinstance(detection_result, dict):
            raise TypeError("Detection result must be a dictionary.")

        anomalies = detection_result.get("anomalies", [])

        if not isinstance(anomalies, list):
            raise ValueError("Anomalies must be provided as a list.")

        score = 0

        severity_breakdown = {
            "MEDIUM": 0,
            "HIGH": 0,
            "CRITICAL": 0
        }

        # Calculate risk points for each anomaly
        for anomaly in anomalies:

            if not isinstance(anomaly, dict):
                raise ValueError("Each anomaly must be a dictionary.")

            severity = anomaly.get("severity", "MEDIUM")

            if severity not in self.SEVERITY_WEIGHTS:
                raise ValueError(
                    f"Invalid anomaly severity: {severity}"
                )

            score += self.SEVERITY_WEIGHTS[severity]

            severity_breakdown[severity] += 1

        # Prevent score from exceeding maximum
        score = min(score, self.max_score)

        risk_level = self._get_risk_level(score)

        return {
            "risk_score": score,
            "risk_level": risk_level,
            "anomaly_count": len(anomalies),
            "severity_breakdown": severity_breakdown,
            "description": self._get_description(risk_level)
        }

    @staticmethod
    def _get_risk_level(score):
        """
        Classify numerical risk score.
        """

        if score >= 70:
            return "CRITICAL"

        elif score >= 40:
            return "HIGH"

        elif score >= 20:
            return "MEDIUM"

        else:
            return "LOW"

    @staticmethod
    def _get_description(risk_level):
        """
        Generate a human-readable risk description.
        """

        descriptions = {
            "LOW": (
                "Infrastructure is operating within "
                "acceptable risk levels."
            ),

            "MEDIUM": (
                "Moderate infrastructure risk detected. "
                "Continue monitoring and investigate anomalies."
            ),

            "HIGH": (
                "High infrastructure risk detected. "
                "Immediate investigation is recommended."
            ),

            "CRITICAL": (
                "Critical infrastructure risk detected. "
                "Immediate corrective action is required."
            )
        }

        return descriptions.get(
            risk_level,
            "Unable to determine infrastructure risk."
        )


if __name__ == "__main__":

    engine = RiskEngine()

    # Example anomaly detection output
    sample_detection = {
        "is_anomaly": True,
        "anomaly_count": 3,
        "anomalies": [
            {
                "metric": "cpu_usage",
                "value": 98,
                "threshold": 80,
                "severity": "CRITICAL"
            },
            {
                "metric": "memory_usage",
                "value": 95,
                "threshold": 85,
                "severity": "HIGH"
            },
            {
                "metric": "temperature",
                "value": 90,
                "threshold": 80,
                "severity": "HIGH"
            }
        ]
    }

    print("\n========== INFRWATCH RISK ENGINE ==========")

    result = engine.calculate_risk(sample_detection)

    print("\nInfrastructure Risk Assessment:")

    for key, value in result.items():
        print(f"{key}: {value}")
