"""
Digital Twin Schematic Component for InfraWatch Dashboard.
Renders an animated SVG asset view with spinning shaft/impeller when running,
pulsing emergency beacon on degrading subsystems, and an interactive drill-down inspector.
"""

import streamlit as st
import streamlit.components.v1 as components


def render_digital_twin_view(latest_data, is_running=False, selected_subsystem="NDE Bearing"):
    """
    Renders 2D animated asset schematic with live component health statuses
    and an interactive subsystem X-Ray inspection panel.
    """
    comp_health = latest_data.get("comp_health", {
        "motor": "HEALTHY",
        "de_bearing": "HEALTHY",
        "nde_bearing": "HEALTHY",
        "impeller": "HEALTHY",
        "seal": "HEALTHY"
    })
    subsystem_specs = latest_data.get("subsystem_specs", {})

    def get_status_props(status):
        if status == "HEALTHY":
            return "#10b981", "rgba(16, 185, 129, 0.2)", "HEALTHY"
        elif status == "DEGRADING":
            return "#38bdf8", "rgba(56, 189, 248, 0.2)", "DEGRADING"
        elif status == "WARNING":
            return "#f59e0b", "rgba(245, 158, 11, 0.2)", "WARNING"
        else:
            return "#ef4444", "rgba(239, 68, 68, 0.3)", "CRITICAL"

    motor_col, motor_bg, motor_txt = get_status_props(comp_health.get("motor", "HEALTHY"))
    nde_col, nde_bg, nde_txt = get_status_props(comp_health.get("nde_bearing", "HEALTHY"))
    de_col, de_bg, de_txt = get_status_props(comp_health.get("de_bearing", "HEALTHY"))
    imp_col, imp_bg, imp_txt = get_status_props(comp_health.get("impeller", "HEALTHY"))
    seal_col, seal_bg, seal_txt = get_status_props(comp_health.get("seal", "HEALTHY"))

    # Animation CSS triggers
    shaft_anim = "animation: rotateShaft 0.6s linear infinite;" if is_running else ""
    impeller_anim = "animation: spinImpeller 0.8s linear infinite; transform-origin: 520px 83px;" if is_running else ""
    
    # Pulsing beacon for faulty bearing or impeller
    nde_pulse = "animation: pulseBeacon 1s ease-in-out infinite;" if comp_health.get("nde_bearing") != "HEALTHY" else ""
    imp_pulse = "animation: pulseBeacon 1s ease-in-out infinite;" if comp_health.get("impeller") != "HEALTHY" else ""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: transparent;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                color: #e2e8f0;
            }}
            .twin-container {{
                background: rgba(15, 23, 42, 0.85);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 12px;
                padding: 16px 20px;
                box-sizing: border-box;
            }}
            .header-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }}
            .title {{
                font-size: 0.95rem;
                font-weight: 700;
                color: #f8fafc;
                letter-spacing: 0.03em;
            }}
            .asset-id {{
                font-size: 0.78rem;
                color: #94a3b8;
                margin-left: 8px;
            }}
            .badge-online {{
                background: rgba(16, 185, 129, 0.15);
                color: #10b981;
                border: 1px solid rgba(16, 185, 129, 0.3);
                padding: 3px 10px;
                border-radius: 20px;
                font-size: 0.72rem;
                font-weight: 600;
            }}
            .svg-wrap {{
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 8px 0;
            }}
            .grid-badges {{
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 8px;
                margin-top: 8px;
            }}
            .badge-card {{
                border-radius: 6px;
                padding: 6px 4px;
                text-align: center;
                font-size: 0.72rem;
            }}
            .sub-name {{
                color: #94a3b8;
                font-size: 0.68rem;
            }}
            .sub-status {{
                font-weight: 700;
                margin-top: 2px;
            }}

            @keyframes rotateShaft {{
                0% {{ stroke-dashoffset: 0; }}
                100% {{ stroke-dashoffset: 24; }}
            }}
            @keyframes spinImpeller {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            @keyframes pulseBeacon {{
                0% {{ r: 6px; opacity: 0.4; filter: drop-shadow(0 0 2px #ef4444); }}
                50% {{ r: 10px; opacity: 1; filter: drop-shadow(0 0 8px #ef4444); }}
                100% {{ r: 6px; opacity: 0.4; filter: drop-shadow(0 0 2px #ef4444); }}
            }}
        </style>
    </head>
    <body>
        <div class="twin-container">
            <div class="header-row">
                <div>
                    <span class="title">ASSET DIGITAL TWIN — SUBSYSTEM STATUS</span>
                    <span class="asset-id">ID: PUMP-402A (Grundfos CRN 32-4)</span>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <span style="font-size: 0.72rem; color: #94a3b8;">{'🌀 ROTATING @ ' + str(latest_data.get('rpm', 2950)) + ' RPM' if is_running else '⏸ STANDSTILL'}</span>
                    <span class="badge-online">● 5 SENSOR NODES ACTIVE</span>
                </div>
            </div>

            <div class="svg-wrap">
                <svg viewBox="0 0 760 170" width="100%" style="max-width: 760px; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));">
                    <defs>
                        <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#1e293b"/>
                            <stop offset="100%" stop-color="#0f172a"/>
                        </linearGradient>
                        <linearGradient id="pipeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#334155"/>
                            <stop offset="100%" stop-color="#1e293b"/>
                        </linearGradient>
                    </defs>

                    <!-- Base plate -->
                    <rect x="20" y="145" width="720" height="15" rx="4" fill="#1e293b" stroke="#334155" stroke-width="2"/>
                    
                    <!-- Shaft -->
                    <rect x="70" y="76" width="600" height="14" fill="#475569" stroke="#64748b"/>

                    <!-- 1. Motor Assembly -->
                    <rect x="50" y="30" width="220" height="106" rx="8" fill="url(#bodyGrad)" stroke="#38bdf8" stroke-width="2"/>
                    <line x1="80" y1="34" x2="80" y2="132" stroke="#334155" stroke-width="3"/>
                    <line x1="110" y1="34" x2="110" y2="132" stroke="#334155" stroke-width="3"/>
                    <line x1="140" y1="34" x2="140" y2="132" stroke="#334155" stroke-width="3"/>
                    <line x1="170" y1="34" x2="170" y2="132" stroke="#334155" stroke-width="3"/>
                    <line x1="200" y1="34" x2="200" y2="132" stroke="#334155" stroke-width="3"/>
                    <text x="160" y="88" fill="#e2e8f0" font-size="13" font-weight="bold" text-anchor="middle">ELECTRIC MOTOR</text>

                    <!-- 2. Non-Drive End (NDE) Bearing Housing -->
                    <rect x="35" y="60" width="30" height="46" rx="4" fill="#0f172a" stroke="{nde_col}" stroke-width="2.5"/>
                    <circle cx="50" cy="83" r="7" fill="{nde_col}" style="{nde_pulse}"/>

                    <!-- 3. Drive End (DE) Bearing Housing -->
                    <rect x="255" y="60" width="30" height="46" rx="4" fill="#0f172a" stroke="{de_col}" stroke-width="2.5"/>
                    <circle cx="270" cy="83" r="7" fill="{de_col}"/>

                    <!-- Flexible Coupling with rotation effect -->
                    <rect x="300" y="66" width="35" height="34" rx="3" fill="#334155" stroke="#38bdf8" stroke-dasharray="6,4" stroke-width="2" style="{shaft_anim}"/>
                    <text x="317" y="55" fill="#94a3b8" font-size="10" text-anchor="middle">Coupling</text>

                    <!-- 4. Mechanical Seal Chamber -->
                    <rect x="350" y="58" width="45" height="50" rx="4" fill="#0f172a" stroke="{seal_col}" stroke-width="2"/>
                    <circle cx="372" cy="83" r="6" fill="{seal_col}"/>

                    <!-- 5. Multi-Stage Impeller Volute Casing -->
                    <path d="M 410,35 L 610,35 L 630,70 L 630,96 L 610,131 L 410,131 Z" fill="url(#bodyGrad)" stroke="{imp_col}" stroke-width="2.5"/>
                    
                    <!-- Spinning Impeller Vanes Group -->
                    <g style="{impeller_anim}">
                        <circle cx="520" cy="83" r="30" fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="6,4"/>
                        <line x1="520" y1="55" x2="520" y2="111" stroke="#38bdf8" stroke-width="1.5"/>
                        <line x1="492" y1="83" x2="548" y2="83" stroke="#38bdf8" stroke-width="1.5"/>
                    </g>
                    <circle cx="520" cy="83" r="8" fill="{imp_col}" style="{imp_pulse}"/>
                    <text x="520" y="118" fill="#e2e8f0" font-size="11" font-weight="bold" text-anchor="middle">IMPELLER</text>

                    <!-- Discharge Flange (Outflow) -->
                    <rect x="485" y="5" width="40" height="30" fill="url(#pipeGrad)" stroke="#64748b" stroke-width="1.5"/>
                    <rect x="475" y="2" width="60" height="7" rx="2" fill="#475569"/>
                    <text x="505" y="22" fill="#94a3b8" font-size="9" text-anchor="middle">Outflow</text>

                    <!-- Suction Flange (Inlet) -->
                    <rect x="630" y="63" width="35" height="40" fill="url(#pipeGrad)" stroke="#64748b" stroke-width="1.5"/>
                    <rect x="665" y="55" width="8" height="56" rx="2" fill="#475569"/>
                    <text x="695" y="87" fill="#94a3b8" font-size="9" text-anchor="middle">Inlet</text>

                    <!-- Indicator Labels -->
                    <line x1="50" y1="60" x2="50" y2="20" stroke="{nde_col}" stroke-width="1.5"/>
                    <text x="50" y="15" fill="{nde_col}" font-size="10" font-weight="bold" text-anchor="middle">NDE Bearing</text>

                    <line x1="270" y1="60" x2="270" y2="20" stroke="{de_col}" stroke-width="1.5"/>
                    <text x="270" y="15" fill="{de_col}" font-size="10" font-weight="bold" text-anchor="middle">DE Bearing</text>

                    <line x1="372" y1="108" x2="372" y2="135" stroke="{seal_col}" stroke-width="1.5"/>
                    <text x="372" y="147" fill="{seal_col}" font-size="10" font-weight="bold" text-anchor="middle">Mech Seal</text>
                </svg>
            </div>

            <div class="grid-badges">
                <div class="badge-card" style="background: {nde_bg}; border: 1px solid {nde_col}55;">
                    <div class="sub-name">NDE Bearing</div>
                    <div class="sub-status" style="color: {nde_col};">{comp_health.get('nde_bearing')}</div>
                </div>
                <div class="badge-card" style="background: {de_bg}; border: 1px solid {de_col}55;">
                    <div class="sub-name">DE Bearing</div>
                    <div class="sub-status" style="color: {de_col};">{comp_health.get('de_bearing')}</div>
                </div>
                <div class="badge-card" style="background: {motor_bg}; border: 1px solid {motor_col}55;">
                    <div class="sub-name">Motor Stator</div>
                    <div class="sub-status" style="color: {motor_col};">{comp_health.get('motor')}</div>
                </div>
                <div class="badge-card" style="background: {imp_bg}; border: 1px solid {imp_col}55;">
                    <div class="sub-name">Impeller Volute</div>
                    <div class="sub-status" style="color: {imp_col};">{comp_health.get('impeller')}</div>
                </div>
                <div class="badge-card" style="background: {seal_bg}; border: 1px solid {seal_col}55;">
                    <div class="sub-name">Mechanical Seal</div>
                    <div class="sub-status" style="color: {seal_col};">{comp_health.get('seal')}</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_content, height=295, scrolling=False)

    # Subsystem Drill-Down X-Ray Inspector
    st.markdown("#### 🔍 Subsystem Deep Diagnostic Inspector")
    sub_key_map = {
        "NDE Bearing": "nde_bearing",
        "DE Bearing": "de_bearing",
        "Motor Stator": "motor",
        "Impeller Volute": "impeller",
        "Mechanical Seal": "seal"
    }
    
    sub_choice = st.pills(
        "Select Subsystem to Inspect",
        options=["NDE Bearing", "DE Bearing", "Motor Stator", "Impeller Volute", "Mechanical Seal"],
        default=selected_subsystem
    )
    
    active_key = sub_key_map.get(sub_choice, "nde_bearing")
    specs = subsystem_specs.get(active_key, {})
    status = comp_health.get(active_key, "HEALTHY")
    status_col, _, _ = get_status_props(status)

    col1, col2, col3 = st.columns([1.2, 1.2, 1.5])
    with col1:
        st.markdown(f"**Hardware Specification:** `{specs.get('model', 'Standard Component')}`")
        if "lubricant_health" in specs:
            st.markdown(f"**Lubrication Quality:** `{specs.get('lubricant_health')}`")
        elif "winding_temp" in specs:
            st.markdown(f"**Winding Thermal Index:** `{specs.get('winding_temp')}`")
        elif "npsh_available" in specs:
            st.markdown(f"**NPSH Margin:** `{specs.get('npsh_available')}`")
        elif "barrier_pressure" in specs:
            st.markdown(f"**Barrier Fluid Pressure:** `{specs.get('barrier_pressure')}`")
            
    with col2:
        if "clearance_mm" in specs:
            st.markdown(f"**Radial Clearance:** `{specs.get('clearance_mm')}`")
            st.markdown(f"**Vibration Envelope:** `{specs.get('vibration_envelope_g')}`")
        elif "phase_current" in specs:
            st.markdown(f"**Current Draw:** `{specs.get('phase_current')}`")
            st.markdown(f"**Motor Efficiency:** `{specs.get('efficiency')}`")
        elif "cavitation_risk_index" in specs:
            st.markdown(f"**Cavitation Risk:** `{specs.get('cavitation_risk_index')}`")
            st.markdown(f"**Volute Pressure:** `{specs.get('volute_pressure')}`")
        elif "leakage_rate" in specs:
            st.markdown(f"**Seal Leakage Rate:** `{specs.get('leakage_rate')}`")
            st.markdown(f"**Face Temperature:** `{specs.get('face_temp')}`")

    with col3:
        st.markdown(f"**Subsystem Status:** <span style='color:{status_col}; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)
        st.info(f"💡 **Recommended Action:** {specs.get('recommended_action', 'Continue normal monitoring.')}")
