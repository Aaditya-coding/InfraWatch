"""
Digital Twin Schematic Component for InfraWatch Dashboard.
Renders an interactive, SVG-based asset view of the industrial water pump
with color-coded component health indicators (NDE Bearing, DE Bearing, Motor, Impeller, Seal).
"""

import streamlit as st


def render_digital_twin_view(latest_data):
    """
    Renders 2D asset schematic with live component health statuses.
    """
    comp_health = latest_data.get("comp_health", {
        "motor": "HEALTHY",
        "de_bearing": "HEALTHY",
        "nde_bearing": "HEALTHY",
        "impeller": "HEALTHY",
        "seal": "HEALTHY"
    })

    def get_status_props(status):
        if status == "HEALTHY":
            return "#10b981", "rgba(16, 185, 129, 0.2)", "HEALTHY (Optimal)"
        elif status == "DEGRADING":
            return "#38bdf8", "rgba(56, 189, 248, 0.2)", "DEGRADING (Monitor)"
        elif status == "WARNING":
            return "#f59e0b", "rgba(245, 158, 11, 0.2)", "WARNING (Maintenance Req)"
        else:
            return "#ef4444", "rgba(239, 68, 68, 0.3)", "CRITICAL (Trip Risk)"

    motor_col, motor_bg, motor_txt = get_status_props(comp_health.get("motor", "HEALTHY"))
    nde_col, nde_bg, nde_txt = get_status_props(comp_health.get("nde_bearing", "HEALTHY"))
    de_col, de_bg, de_txt = get_status_props(comp_health.get("de_bearing", "HEALTHY"))
    imp_col, imp_bg, imp_txt = get_status_props(comp_health.get("impeller", "HEALTHY"))
    seal_col, seal_bg, seal_txt = get_status_props(comp_health.get("seal", "HEALTHY"))

    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div>
                <span style="font-size: 1.1rem; font-weight: 700; color: #f8fafc;">ASSET DIGITAL TWIN — SUBSYSTEM STATUS</span>
                <span style="font-size: 0.8rem; color: #94a3b8; margin-left: 10px;">ID: PUMP-402A (Grundfos CRN 32-4)</span>
            </div>
            <span style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid #10b98144; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">
                ● 5 SENSOR NODES ONLINE
            </span>
        </div>

        <!-- SVG Digital Twin Schematic -->
        <div style="display: flex; justify-content: center; align-items: center; padding: 15px 0;">
            <svg viewBox="0 0 760 170" width="100%" style="max-width: 760px; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.5));">
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
                <!-- Motor Cooling Fins -->
                <line x1="80" y1="34" x2="80" y2="132" stroke="#334155" stroke-width="3"/>
                <line x1="110" y1="34" x2="110" y2="132" stroke="#334155" stroke-width="3"/>
                <line x1="140" y1="34" x2="140" y2="132" stroke="#334155" stroke-width="3"/>
                <line x1="170" y1="34" x2="170" y2="132" stroke="#334155" stroke-width="3"/>
                <line x1="200" y1="34" x2="200" y2="132" stroke="#334155" stroke-width="3"/>
                <text x="160" y="88" fill="#e2e8f0" font-size="13" font-weight="bold" text-anchor="middle">ELECTRIC MOTOR</text>

                <!-- 2. Non-Drive End (NDE) Bearing Housing -->
                <rect x="35" y="60" width="30" height="46" rx="4" fill="#0f172a" stroke="{nde_col}" stroke-width="2.5"/>
                <circle cx="50" cy="83" r="7" fill="{nde_col}"/>

                <!-- 3. Drive End (DE) Bearing Housing -->
                <rect x="255" y="60" width="30" height="46" rx="4" fill="#0f172a" stroke="{de_col}" stroke-width="2.5"/>
                <circle cx="270" cy="83" r="7" fill="{de_col}"/>

                <!-- Flexible Coupling -->
                <rect x="300" y="66" width="35" height="34" rx="3" fill="#334155" stroke="#64748b" stroke-dasharray="4"/>
                <text x="317" y="55" fill="#94a3b8" font-size="10" text-anchor="middle">Coupling</text>

                <!-- 4. Mechanical Seal Chamber -->
                <rect x="350" y="58" width="45" height="50" rx="4" fill="#0f172a" stroke="{seal_col}" stroke-width="2"/>
                <circle cx="372" cy="83" r="6" fill="{seal_col}"/>

                <!-- 5. Multi-Stage Impeller Volute Casing -->
                <path d="M 410,35 L 610,35 L 630,70 L 630,96 L 610,131 L 410,131 Z" fill="url(#bodyGrad)" stroke="{imp_col}" stroke-width="2.5"/>
                <!-- Impeller Vanes Indicator -->
                <circle cx="520" cy="83" r="30" fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="6,4"/>
                <circle cx="520" cy="83" r="10" fill="{imp_col}"/>
                <text x="520" y="88" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">IMPELLER</text>

                <!-- Discharge Flange (Upward) -->
                <rect x="485" y="5" width="40" height="30" fill="url(#pipeGrad)" stroke="#64748b" stroke-width="1.5"/>
                <rect x="475" y="2" width="60" height="7" rx="2" fill="#475569"/>
                <text x="505" y="22" fill="#94a3b8" font-size="9" text-anchor="middle">Outflow</text>

                <!-- Suction Flange (Right End) -->
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

        <!-- Component Cards Grid -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-top: 10px;">
            <div style="background: {nde_bg}; border: 1px solid {nde_col}55; border-radius: 8px; padding: 8px 12px; text-align: center;">
                <div style="font-size: 0.72rem; color: #94a3b8;">NDE Bearing</div>
                <div style="font-size: 0.8rem; font-weight: 700; color: {nde_col};">{comp_health.get('nde_bearing')}</div>
            </div>
            <div style="background: {de_bg}; border: 1px solid {de_col}55; border-radius: 8px; padding: 8px 12px; text-align: center;">
                <div style="font-size: 0.72rem; color: #94a3b8;">DE Bearing</div>
                <div style="font-size: 0.8rem; font-weight: 700; color: {de_col};">{comp_health.get('de_bearing')}</div>
            </div>
            <div style="background: {motor_bg}; border: 1px solid {motor_col}55; border-radius: 8px; padding: 8px 12px; text-align: center;">
                <div style="font-size: 0.72rem; color: #94a3b8;">Motor Stator</div>
                <div style="font-size: 0.8rem; font-weight: 700; color: {motor_col};">{comp_health.get('motor')}</div>
            </div>
            <div style="background: {imp_bg}; border: 1px solid {imp_col}55; border-radius: 8px; padding: 8px 12px; text-align: center;">
                <div style="font-size: 0.72rem; color: #94a3b8;">Impeller Volute</div>
                <div style="font-size: 0.8rem; font-weight: 700; color: {imp_col};">{comp_health.get('impeller')}</div>
            </div>
            <div style="background: {seal_bg}; border: 1px solid {seal_col}55; border-radius: 8px; padding: 8px 12px; text-align: center;">
                <div style="font-size: 0.72rem; color: #94a3b8;">Mechanical Seal</div>
                <div style="font-size: 0.8rem; font-weight: 700; color: {seal_col};">{comp_health.get('seal')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
