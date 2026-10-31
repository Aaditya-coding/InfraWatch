"""
InfraWatch — AI-Powered Predictive Infrastructure Monitoring & Digital Twin Dashboard.
Hacktoberfest Hack Day Prayagraj × CC Club MNNIT (2026).
Frontend & Product Lead: Om Gupta (Branch: feat/dashboard)
"""

import streamlit as st
import time
import pandas as pd
import sys
import os
import textwrap

# Add repository root to path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from frontend.utils.backend_bridge import get_latest_telemetry, get_initial_history, BACKEND_AVAILABLE
from frontend.utils.audio_synth import generate_pump_audio
from frontend.components.sensor_cards import render_sensor_cards
from frontend.components.charts import render_sensor_charts
from frontend.components.digital_twin import render_digital_twin_view
from frontend.components.diagnostics import render_fft_spectrum, render_correlation_heatmap
from frontend.components.alerts import render_alert_panel

# 1. Page Configuration
st.set_page_config(
    page_title="InfraWatch — Pump Digital Twin",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Modern Industrial Dark Theme Styling
st.markdown("""
<style>
    /* Dark Slate Background */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Top Header Bar */
    .header-box {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 22px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Custom tab styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px 8px 0px 0px;
        padding: 8px 18px;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(30, 41, 59, 0.9) !important;
        color: #38bdf8 !important;
        border-bottom: 2px solid #38bdf8 !important;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# 3. Initialize Session State
if "history" not in st.session_state or st.session_state.history is None:
    st.session_state.history = get_initial_history(count=40, scenario="Normal Operation")

if "streaming" not in st.session_state:
    st.session_state.streaming = False

if "inject_spike" not in st.session_state:
    st.session_state.inject_spike = False

# 4. Sidebar Controls
with st.sidebar:
    st.markdown(textwrap.dedent("""
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
    <div style="font-size: 2rem;">⚙️</div>
    <div>
        <div style="font-size: 1.3rem; font-weight: 800; color: #38bdf8; letter-spacing: -0.02em;">InfraWatch</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">Predictive Failure Intelligence</div>
    </div>
</div>
"""), unsafe_allow_html=True)

    st.caption("🏆 Hacktoberfest Hack Day × CC Club MNNIT (Track 1: Applied AI)")
    st.divider()

    st.subheader("🎮 Operational Scenarios")

    scenario = st.selectbox(
        "Operating Scenario",
        [
            "Normal Operation",
            "Bearing Fault (BPFO/BPFI)",
            "Impeller Cavitation & Blockage",
            "Critical Multi-Fault"
        ],
        index=0,
        help="Select a fault mode to test multivariate anomaly detection."
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("▶ Start Stream" if not st.session_state.streaming else "⏸ Pause Stream", use_container_width=True):
            st.session_state.streaming = not st.session_state.streaming
    with col_btn2:
        if st.button("⚡ Inject Spike", use_container_width=True):
            st.session_state.inject_spike = True

    if st.button("🔄 Reset Telemetry Buffer", use_container_width=True):
        st.session_state.history = get_initial_history(count=40, scenario=scenario)
        st.rerun()

    # 4.1 Digital Twin Physics & Stress-Testing Sliders
    with st.expander("🎛️ Digital Twin Physics Tuning", expanded=True):
        rpm_val = st.slider("Pump Running Speed (RPM)", min_value=1800, max_value=3600, value=2950, step=50, help="Dynamically shifts running frequency and harmonic vibration.")
        throttle_val = st.slider("Suction Valve Open (%)", min_value=25, max_value=100, value=100, step=5, help="Throttling suction below 65% triggers hydraulic cavitation.")
        ambient_temp_val = st.slider("Ambient Temperature (°C)", min_value=15.0, max_value=50.0, value=28.0, step=1.0, help="Simulates plant room cooling conditions.")

    # 4.2 ML Anomaly Sensitivity Tuning
    with st.expander("🎚️ ML Anomaly Detection Sensitivity", expanded=False):
        sensitivity_z = st.slider("Isolation Z-Threshold (σ)", min_value=1.5, max_value=3.5, value=2.5, step=0.1, help="Adjusts anomaly threshold sensitivity on multivariate telemetry.")

    refresh_rate = st.slider("Stream Refresh Interval (s)", min_value=1.0, max_value=5.0, value=2.0, step=0.5)

    st.divider()
    st.subheader("📋 Asset Specifications")
    st.markdown(f"""
* **Equipment:** Multi-Stage Centrifugal Pump
* **Model:** Grundfos CRN 32-4
* **Tag ID:** `PUMP-402A`
* **Operating Speed:** {rpm_val} RPM ({rpm_val/60:.1f} Hz)
* **ISO Standard:** ISO 10816-3 (Class II)
* **Backend Engine:** %s
    """ % ("🟢 Connected (Aditya's ML Engine)" if BACKEND_AVAILABLE else "🟡 Standalone High-Fidelity Simulator"))

# 5. Telemetry Ingestion Step with Physics Parameters
if st.session_state.streaming or st.session_state.inject_spike:
    new_pt = get_latest_telemetry(
        scenario=scenario,
        inject_spike=st.session_state.inject_spike,
        rpm=rpm_val,
        throttle=throttle_val,
        ambient_temp=ambient_temp_val,
        sensitivity_z=sensitivity_z
    )
    st.session_state.inject_spike = False
    
    # Append to history dataframe
    new_df = pd.DataFrame([new_pt])
    st.session_state.history = pd.concat([st.session_state.history, new_df], ignore_index=True)
    if len(st.session_state.history) > 120:
        st.session_state.history = st.session_state.history.iloc[-120:].reset_index(drop=True)

# Latest point
latest_pt = st.session_state.history.iloc[-1].to_dict() if not st.session_state.history.empty else {}

# 6. Main Header Bar
status_color = "#10b981" if latest_pt.get("risk_level") == "NORMAL" else ("#f59e0b" if latest_pt.get("risk_level") in ["LOW_RISK", "WARNING"] else "#ef4444")
stream_badge = "🟢 STREAMING ACTIVE" if st.session_state.streaming else "⏸ STREAM PAUSED"

st.markdown(textwrap.dedent(f"""
<div class="header-box">
    <div>
        <div style="font-size: 1.35rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em;">
            INDUSTRIAL PUMP DIGITAL TWIN — CONDITION MONITORING
        </div>
        <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 3px;">
            Sector 4 Water Feed Station | Asset Tag: <span style="color: #38bdf8; font-weight: 600;">PUMP-402A</span> | Speed: <span style="color: #f8fafc;">{rpm_val} RPM</span> | Timestamp: <span style="color: #f8fafc;">{latest_pt.get('timestamp', 'N/A')}</span>
        </div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid #38bdf844; padding: 5px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700;">
            {stream_badge}
        </span>
        <span style="background: {status_color}22; color: {status_color}; border: 1px solid {status_color}55; padding: 5px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700;">
            {latest_pt.get('risk_level', 'NORMAL')}
        </span>
    </div>
</div>
"""), unsafe_allow_html=True)

# 7. Render KPI Metric Cards
render_sensor_cards(latest_pt)

# 8. Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛰️ Live Telemetry & Digital Twin",
    "🔬 Advanced FFT Spectrum & Correlations",
    "🎧 Acoustic Machine Sonification",
    "📋 Incident Log & Prescriptive Actions",
    "🧠 Agentic Intelligence & Architecture"
])

with tab1:
    # 2D Animated Digital Twin Schematic
    render_digital_twin_view(latest_pt, is_running=st.session_state.streaming)
    
    # Real-Time Plotly Charts
    fig_charts = render_sensor_charts(st.session_state.history)
    if fig_charts:
        st.plotly_chart(fig_charts, use_container_width=True)

with tab2:
    col_d1, col_d2 = st.columns([1.3, 1])
    with col_d1:
        fig_fft = render_fft_spectrum(scenario=scenario, vibration_level=latest_pt.get("vibration", 2.4), rpm=rpm_val)
        st.plotly_chart(fig_fft, use_container_width=True)
    with col_d2:
        fig_corr = render_correlation_heatmap(st.session_state.history)
        if fig_corr:
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Gathering sensor telemetry buffer for correlation matrix...")

    st.markdown(f"""
    > [!NOTE]
    > **Speed-Coupled Dynamic Analysis:** Operating at **{rpm_val} RPM** places the primary 1X shaft harmonic at **{rpm_val/60.0:.1f} Hz** and outer-race defect frequency (BPFO) at **{(rpm_val/60.0)*2.18:.1f} Hz**. Tuning the RPM slider updates the spectral signature in real-time.
    """)

with tab3:
    st.subheader("🎧 Acoustic Signature & Vibration Sonification")
    st.markdown("""
    Predictive maintenance vibration frequencies can be converted directly into the audible acoustic spectrum. 
    **Listen to the physical condition of the pump below:**
    """)
    
    col_snd1, col_snd2 = st.columns([1.2, 1.8])
    with col_snd1:
        st.markdown(f"**Current Scenario:** `{scenario}`")
        st.markdown(f"**Operating Speed:** `{rpm_val} RPM`")
        # Generate real-time audio
        audio_bytes = generate_pump_audio(scenario=scenario, rpm=rpm_val)
        st.audio(audio_bytes, format="audio/wav")
    
    with col_snd2:
        if scenario == "Normal Operation":
            st.success("🟢 **Normal Harmonic Signature:** Smooth continuous 50 Hz electromagnetic motor hum with low-amplitude aerodynamic blade pass frequencies.")
        elif "Bearing" in scenario:
            st.warning("🟡 **Bearing Raceways Impact Squeal:** Distinct high-frequency harmonic chirping (~1.4 kHz) caused by rolling elements striking raceway spalls.")
        elif "Cavitation" in scenario:
            st.error("🟠 **Hydraulic Cavitation Noise:** Broadband chaotic gravel rattling caused by rapid vapor bubble collapse against the stainless steel impeller.")
        else:
            st.error("🔴 **Multi-Fault Dissonance:** High-amplitude unbalance hum coupled with severe mechanical friction chatter.")

with tab4:
    render_alert_panel(latest_pt, st.session_state.history)

with tab5:
    st.subheader("🏗️ InfraWatch Intelligence Architecture")
    st.markdown("""
    InfraWatch operates as a multi-stage predictive agent pipeline:
    
    1. **Sensor Ingestion Layer:** Continuous ingestion of multivariate time-series (Vibration, Temperature, Pressure, Power).
    2. **Multivariate Anomaly Engine (Aditya):** Uses **Isolation Forest** coupled with rolling Z-score feature extraction to flag multi-sensor deviations that evade single-point threshold limits.
    3. **Subsystem Fault Classifier:** Identifies whether the developing failure is localized to the **NDE Bearing**, **Drive End Bearing**, **Impeller Cavitation**, or **Motor Stator**.
    4. **Digital Twin Health & RUL Estimator:** Computes a composite asset health score (0–100%) and Remaining Useful Life (RUL) in operational hours.
    5. **Prescriptive Maintenance Agent:** Recommends exact ISO/OEM maintenance tasks before catastrophic failure occurs.
    """)
    st.info("💡 **Git Collaboration Status:** Frontend developed on `feat/dashboard` by Om. Backend ML pipeline on `feat/ml-engine` by Aditya. Merging through reviewed Pull Requests into `main`.")

# 9. Auto-refresh loop when streaming is toggled ON
if st.session_state.streaming:
    time.sleep(refresh_rate)
    st.rerun()
