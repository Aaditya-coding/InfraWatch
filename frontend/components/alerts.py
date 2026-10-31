"""
Alerts & Prescriptive Maintenance Component for InfraWatch Dashboard.
Renders real-time anomaly log, incident root-cause analysis, and recommended corrective actions.
"""

import streamlit as st
import pandas as pd
import textwrap


def render_alert_panel(latest_data, df_history: pd.DataFrame, gemini_api_key=None):
    """
    Renders incident diagnostics and maintenance action recommendations.
    """
    risk_level = latest_data.get("risk_level", "NORMAL")
    root_cause = latest_data.get("root_cause", "All parameters nominal.")
    recommendation = latest_data.get("recommendation", "Continue standard operating cycle.")
    rul_hours = latest_data.get("rul_hours", 720)
    health = latest_data.get("risk_score", 95)

    if risk_level == "NORMAL":
        banner_color = "#10b981"
        banner_title = "SYSTEM STATUS: NOMINAL (HEALTHY)"
    elif risk_level == "LOW_RISK":
        banner_color = "#38bdf8"
        banner_title = "SYSTEM STATUS: MINOR DRIFT DETECTED"
    elif risk_level == "WARNING":
        banner_color = "#f59e0b"
        banner_title = "SYSTEM STATUS: PREVENTIVE ACTION REQUIRED"
    else:
        banner_color = "#ef4444"
        banner_title = "SYSTEM STATUS: CRITICAL FAILURE IMMINENT"

    st.markdown(textwrap.dedent(f"""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid {banner_color}66; border-left: 6px solid {banner_color}; border-radius: 10px; padding: 16px; margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="font-size: 1.05rem; font-weight: 700; color: {banner_color};">{banner_title}</div>
        <div style="font-size: 0.85rem; color: #94a3b8;">Estimated Remaining Useful Life: <b style="color: #f8fafc;">{rul_hours} Hours</b></div>
    </div>
    <div style="margin-top: 10px; font-size: 0.95rem; color: #e2e8f0;">
        <b>Root Cause Investigation:</b> {root_cause}
    </div>
    <div style="margin-top: 6px; font-size: 0.95rem; color: #cbd5e1;">
        <b>Prescriptive Action:</b> {recommendation}
    </div>
</div>
"""), unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("⚠️ Recent Anomaly Telemetry Log")
        if df_history is not None and not df_history.empty:
            anomalies = df_history[df_history["anomaly"] == True].tail(8)
            if not anomalies.empty:
                display_df = anomalies[["timestamp", "temperature", "vibration", "pressure", "power", "risk_level"]].copy()
                display_df.columns = ["Timestamp", "Temp (°C)", "Vib (mm/s)", "Press (bar)", "Power (kW)", "Severity"]
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No abnormal sensor events recorded in current telemetry buffer.")
        else:
            st.info("Waiting for telemetry stream...")

    with col2:
        st.subheader("🛠️ Maintenance Task Checklist")
        if risk_level == "NORMAL":
            st.checkbox("Log 24h operational telemetry to SCADA", value=True, disabled=True)
            st.checkbox("Monthly grease replenishment scheduled", value=False)
            st.checkbox("Inspect shaft coupling alignment during next turnaround", value=False)
        elif risk_level in ["LOW_RISK", "WARNING"]:
            st.checkbox("Dispatch technician for ultrasonic bearing inspection", value=True)
            st.checkbox(f"Execute action: {recommendation[:60]}...", value=False)
            st.checkbox("Recalibrate suction pressure sensor", value=False)
            st.warning("⚠️ Maintenance threshold crossed. Work order generated.")
        else:
            st.checkbox("EMERGENCY: Switch fluid load to Standby Pump Unit", value=True)
            st.checkbox("Isolate motor circuit breaker before physical inspection", value=True)
            st.checkbox("Order replacement NDE bearing assembly (SKF 6308-2Z)", value=False)
            st.error("🚨 CRITICAL ALARM: Immediate human intervention mandatory.")
