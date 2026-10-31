"""
Sensor Cards Component for InfraWatch Dashboard.
Renders high-visibility KPI cards with industrial thresholds and status badges.
"""

import streamlit as st


def render_sensor_cards(latest_data):
    """
    Renders top KPI cards with styling and thresholds.
    """
    if not latest_data:
        return

    temp = latest_data.get("temperature", 58.0)
    vib = latest_data.get("vibration", 2.4)
    press = latest_data.get("pressure", 4.2)
    power = latest_data.get("power", 7.5)
    health = latest_data.get("risk_score", 95)
    risk_level = latest_data.get("risk_level", "NORMAL")
    rul_hours = latest_data.get("rul_hours", 720)

    # Determine status colors
    if health >= 80:
        health_color = "#10b981"  # Emerald
        health_badge = "OPTIMAL"
    elif health >= 50:
        health_color = "#f59e0b"  # Amber
        health_badge = "WARNING"
    else:
        health_color = "#ef4444"  # Crimson
        health_badge = "CRITICAL"

    # Vibration ISO Thresholds (ISO 10816-3 Class II pumps)
    if vib < 2.8:
        vib_badge = "ZONE A (Good)"
        vib_color = "#10b981"
    elif vib < 4.5:
        vib_badge = "ZONE B (Satisfactory)"
        vib_color = "#38bdf8"
    elif vib < 7.1:
        vib_badge = "ZONE C (Unsatisfactory)"
        vib_color = "#f59e0b"
    else:
        vib_badge = "ZONE D (Unacceptable)"
        vib_color = "#ef4444"

    # Temperature threshold (Motor & Bearing limit: 80°C warning, 90°C trip)
    temp_color = "#ef4444" if temp > 80.0 else ("#f59e0b" if temp > 72.0 else "#10b981")

    # Pressure threshold (Nominal 4.2 bar, <3.0 cavitation risk)
    press_color = "#ef4444" if press < 2.5 else ("#f59e0b" if press < 3.2 else "#10b981")

    cols = st.columns([1.2, 1, 1, 1, 1])

    with cols[0]:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1); border-left: 5px solid {health_color}; border-radius: 10px; padding: 14px; margin-bottom: 15px;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Pump Health Index</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: {health_color}; line-height: 1.1;">{health}%</div>
            <div style="margin-top: 6px; display: flex; align-items: center; justify-content: space-between;">
                <span style="background: {health_color}22; color: {health_color}; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 700;">{health_badge}</span>
                <span style="font-size: 0.75rem; color: #94a3b8;">RUL: <b>{rul_hours}h</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cols[1]:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1); border-left: 5px solid {vib_color}; border-radius: 10px; padding: 14px; margin-bottom: 15px;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Vibration (RMS)</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: {vib_color}; line-height: 1.1;">{vib:.2f} <span style="font-size: 1rem; color: #64748b;">mm/s</span></div>
            <div style="margin-top: 6px;">
                <span style="background: {vib_color}22; color: {vib_color}; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700;">{vib_badge}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cols[2]:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1); border-left: 5px solid {temp_color}; border-radius: 10px; padding: 14px; margin-bottom: 15px;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Bearing Temp</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: {temp_color}; line-height: 1.1;">{temp:.1f} <span style="font-size: 1rem; color: #64748b;">°C</span></div>
            <div style="margin-top: 6px;">
                <span style="font-size: 0.72rem; color: #94a3b8;">Max Trip: <b>85.0°C</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cols[3]:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1); border-left: 5px solid {press_color}; border-radius: 10px; padding: 14px; margin-bottom: 15px;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Discharge Pressure</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: {press_color}; line-height: 1.1;">{press:.2f} <span style="font-size: 1rem; color: #64748b;">bar</span></div>
            <div style="margin-top: 6px;">
                <span style="font-size: 0.72rem; color: #94a3b8;">Nominal: <b>4.20 bar</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cols[4]:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1); border-left: 5px solid #38bdf8; border-radius: 10px; padding: 14px; margin-bottom: 15px;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Motor Active Power</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: #38bdf8; line-height: 1.1;">{power:.2f} <span style="font-size: 1rem; color: #64748b;">kW</span></div>
            <div style="margin-top: 6px;">
                <span style="font-size: 0.72rem; color: #94a3b8;">Rated: <b>11.0 kW</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
