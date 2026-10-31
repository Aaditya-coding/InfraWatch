
class AnomalyDetector:
    """
    InfraWatch Anomaly Detection Engine.

    Identifies unusual infrastructure behaviour by comparing
    sensor readings against predefined thresholds.
    """

    DEFAULT_THRESHOLDS = {
        "cpu_usage": 80,
        "memory_usage": 85,
        "disk_usage": 90,
        "network_usage": 900,
        "temperature": 80,
        "vibration": 4.5,
        "power": 10.5,
        "pressure": 5.5
    }

    def __init__(self, thresholds=None):
        """
        Initialize detector with default or custom thresholds.
        """

        self.thresholds = self.DEFAULT_THRESHOLDS.copy()

        if thresholds:
            for metric, value in thresholds.items():

                if metric not in self.DEFAULT_THRESHOLDS:
                    raise ValueError(
                        f"Unknown metric: {metric}"
                    )

                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    raise ValueError(
                        f"Threshold for {metric} must be numeric."
                    )

                if value <= 0:
                    raise ValueError(
                        f"Threshold for {metric} must be positive."
                    )

                self.thresholds[metric] = value

    def detect(self, reading):
        """
        Analyze a single infrastructure sensor reading.

        Returns:
            Dictionary containing anomaly information.
        """

        if not isinstance(reading, dict):
            raise TypeError("Reading must be a dictionary.")

        anomalies = []

        for metric, threshold in self.thresholds.items():

            # Skip metrics that are not available
            if metric not in reading:
                continue

            value = reading[metric]

            # Validate sensor values
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
            ):
                raise ValueError(
                    f"Invalid value for {metric}: {value}"
                )

            if value < 0:
                raise ValueError(
                    f"{metric} cannot have a negative value."
                )

            # Detect threshold violations
            if value > threshold:

                severity = self._get_severity(
                    value,
                    threshold
                )

                anomaly = {
                    "metric": metric,
                    "value": value,
                    "threshold": threshold,
                    "severity": severity,
                    "message": (
                        f"{metric} exceeded safe threshold. "
                        f"Current: {value}, "
                        f"Threshold: {threshold}"
                    )
                }

                anomalies.append(anomaly)

        return {
            "is_anomaly": len(anomalies) > 0,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies
        }

    @staticmethod
    def _get_severity(value, threshold):
        """
        Determine severity based on threshold violation.
        """

        ratio = value / threshold

        if ratio >= 1.25:
            return "CRITICAL"

        elif ratio >= 1.10:
            return "HIGH"

        else:
            return "MEDIUM"

    def detect_batch(self, readings):
        """
        Detect anomalies across multiple sensor readings.
        """

        if not isinstance(readings, list):
            raise TypeError("Readings must be a list.")

        return [
            self.detect(reading)
            for reading in readings
        ]


_default_detector = None


def detect_anomalies(reading, thresholds=None):
    """
    Convenience function to analyze a sensor reading using AnomalyDetector.
    """
    global _default_detector
    if thresholds is not None:
        return AnomalyDetector(thresholds).detect(reading)
    if _default_detector is None:
        _default_detector = AnomalyDetector()
    return _default_detector.detect(reading)


if __name__ == "__main__":

    detector = AnomalyDetector()

    # Example normal reading
    normal_reading = {
        "cpu_usage": 45,
        "memory_usage": 60,
        "disk_usage": 55,
        "network_usage": 300,
        "temperature": 40
    }

    # Example abnormal reading
    abnormal_reading = {
        "cpu_usage": 98,
        "memory_usage": 95,
        "disk_usage": 94,
        "network_usage": 500,
        "temperature": 90
    }

    print("\n========== INFRWATCH ANOMALY DETECTOR ==========")

    print("\nNormal Reading:")
    print(detector.detect(normal_reading))

    print("\nAbnormal Reading:")
    print(detector.detect(abnormal_reading))
