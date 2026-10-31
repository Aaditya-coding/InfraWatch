
class RecommendationEngine:
    """
    InfraWatch Recommendation Engine.

    Converts infrastructure anomalies and risk assessments
    into actionable recommendations.
    """

    # Recommendations based on infrastructure metrics
    RECOMMENDATIONS = {
        "cpu_usage": {
            "MEDIUM": "Monitor CPU consumption and identify processes using excessive resources.",
            "HIGH": "Investigate CPU-intensive processes and optimize resource allocation.",
            "CRITICAL": "Immediately reduce CPU load, terminate unnecessary workloads if safe, or scale computing resources."
        },

        "memory_usage": {
            "MEDIUM": "Monitor memory consumption and check for unnecessary background processes.",
            "HIGH": "Identify memory-intensive applications and optimize RAM allocation.",
            "CRITICAL": "Investigate possible memory leaks and free memory or increase available RAM."
        },

        "disk_usage": {
            "MEDIUM": "Monitor disk capacity and review unnecessary stored files.",
            "HIGH": "Remove unnecessary files, archive old data, and investigate storage growth.",
            "CRITICAL": "Free disk space immediately or expand storage to prevent service disruption."
        },

        "network_usage": {
            "MEDIUM": "Monitor network traffic for unusual activity.",
            "HIGH": "Investigate traffic spikes and identify bandwidth-intensive services.",
            "CRITICAL": "Investigate possible network congestion or abnormal traffic and apply appropriate traffic controls."
        },

        "temperature": {
            "MEDIUM": "Monitor server temperature and verify cooling system performance.",
            "HIGH": "Inspect cooling fans, ventilation, and airflow.",
            "CRITICAL": "Reduce system load and immediately inspect cooling equipment to prevent overheating."
        },

        "vibration": {
            "MEDIUM": "Inspect mechanical alignment and monitor bearing vibration signatures.",
            "HIGH": "Re-lubricate bearing assembly and schedule acoustic vibration spectral analysis.",
            "CRITICAL": "Emergency shutdown: excessive vibration indicates severe bearing spalling or impeller unbalance."
        },

        "pressure": {
            "MEDIUM": "Verify suction line valve clearance and filter mesh.",
            "HIGH": "Inspect suction strainer for debris and adjust inlet throttling to prevent cavitation.",
            "CRITICAL": "Halt pump to prevent permanent impeller volute damage from severe hydraulic cavitation."
        },

        "power": {
            "MEDIUM": "Monitor electrical phase balance and motor active load.",
            "HIGH": "Inspect motor windings and check for excessive mechanical drag.",
            "CRITICAL": "Trip motor circuit breaker immediately to prevent stator burnout from overload."
        }
    }

    PRIORITY_LEVELS = {
        "MEDIUM": "MEDIUM",
        "HIGH": "HIGH",
        "CRITICAL": "URGENT"
    }

    def generate_recommendations(self, detection_result, risk_result=None):
        """
        Generate recommendations from anomaly detection
        and optional risk assessment results.

        Args:
            detection_result: Output from AnomalyDetector.detect()
            risk_result: Output from RiskEngine.calculate_risk()

        Returns:
            Structured recommendation dictionary.
        """

        if not isinstance(detection_result, dict):
            raise TypeError("Detection result must be a dictionary.")

        if risk_result is not None and not isinstance(risk_result, dict):
            raise TypeError("Risk result must be a dictionary.")

        anomalies = detection_result.get("anomalies", [])

        if not isinstance(anomalies, list):
            raise ValueError("Anomalies must be a list.")

        risk_level = (
            risk_result.get("risk_level", "UNKNOWN")
            if risk_result
            else "UNKNOWN"
        )

        recommendations = []
        seen_metrics = set()

        # Generate metric-specific recommendations
        for anomaly in anomalies:

            if not isinstance(anomaly, dict):
                raise ValueError("Each anomaly must be a dictionary.")

            metric = anomaly.get("metric")
            severity = anomaly.get("severity", "MEDIUM")

            if not isinstance(metric, str) or not metric:
                raise ValueError("Anomaly metric must be a non-empty string.")

            if severity not in self.PRIORITY_LEVELS:
                raise ValueError(
                    f"Invalid anomaly severity: {severity}"
                )

            # Prevent duplicate recommendations
            if metric in seen_metrics:
                continue

            seen_metrics.add(metric)

            metric_recommendations = self.RECOMMENDATIONS.get(metric, {})

            recommendation = metric_recommendations.get(
                severity,
                "Investigate the abnormal metric and monitor infrastructure performance."
            )

            recommendations.append({
                "metric": metric,
                "severity": severity,
                "priority": self.PRIORITY_LEVELS[severity],
                "recommendation": recommendation
            })

        # Add general recommendation when no anomaly exists
        if not recommendations:
            recommendations.append({
                "metric": "general",
                "severity": "LOW",
                "priority": "LOW",
                "recommendation": (
                    "No anomalies detected. Continue routine "
                    "infrastructure monitoring."
                )
            })

        # Sort recommendations by urgency
        priority_order = {
            "URGENT": 0,
            "HIGH": 1,
            "MEDIUM": 2,
            "LOW": 3
        }

        recommendations.sort(
            key=lambda item: priority_order[item["priority"]]
        )

        # Add risk-specific guidance
        risk_recommendation = self._get_risk_recommendation(
            risk_level
        )

        return {
            "risk_level": risk_level,
            "recommendation_count": len(recommendations),
            "risk_recommendation": risk_recommendation,
            "recommendations": recommendations
        }

    @staticmethod
    def _get_risk_recommendation(risk_level):
        """
        Generate general guidance based on overall risk.
        """

        guidance = {
            "LOW": (
                "Infrastructure risk is low. Continue normal monitoring."
            ),

            "MEDIUM": (
                "Infrastructure risk is moderate. Monitor affected "
                "services and investigate anomalies."
            ),

            "HIGH": (
                "Infrastructure risk is high. Prioritize investigation "
                "and corrective actions."
            ),

            "CRITICAL": (
                "Infrastructure risk is critical. Prioritize immediate "
                "incident response and protect affected services."
            )
        }

        return guidance.get(
            risk_level,
            "Risk level unavailable. Review infrastructure metrics."
        )


_default_recommendation_engine = None


def generate_recommendations(detection_result, risk_result=None):
    """
    Convenience function to generate prescriptive maintenance recommendations.
    Accepts (detection_result, risk_result) or handles single-argument usage.
    """
    global _default_recommendation_engine
    if _default_recommendation_engine is None:
        _default_recommendation_engine = RecommendationEngine()

    if isinstance(detection_result, dict) and "risk_score" in detection_result and "anomalies" not in detection_result:
        # User passed risk_result as the only argument
        return _default_recommendation_engine.generate_recommendations({"anomalies": []}, detection_result)

    return _default_recommendation_engine.generate_recommendations(detection_result, risk_result)


if __name__ == "__main__":

    engine = RecommendationEngine()

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

    sample_risk = {
        "risk_score": 70,
        "risk_level": "CRITICAL",
        "anomaly_count": 3
    }

    print("\n========== INFRWATCH RECOMMENDATION ENGINE ==========")

    result = engine.generate_recommendations(
        sample_detection,
        sample_risk
    )

    print("\nOverall Risk:")
    print(result["risk_level"])

    print("\nRisk Guidance:")
    print(result["risk_recommendation"])

    print("\nRecommended Actions:")

    for index, recommendation in enumerate(
        result["recommendations"],
        start=1
    ):
        print(f"\n{index}. {recommendation['metric']}")
        print(f"   Severity: {recommendation['severity']}")
        print(f"   Priority: {recommendation['priority']}")
        print(f"   Action: {recommendation['recommendation']}")
