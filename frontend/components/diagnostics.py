"""
Diagnostics & Frequency Spectrum Component for InfraWatch Dashboard.
Renders FFT vibration harmonic analysis dynamically linked to RPM speed and sensor correlation heatmap.
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def render_fft_spectrum(scenario="Normal Operation", vibration_level=2.4, rpm=2950):
    """
    Simulates and visualizes the vibration frequency spectrum (FFT) dynamically based on RPM.
    Highlights 1X (shaft speed), 2X, BPFO (outer race fault), and BPFI (inner race fault).
    """
    frequencies = np.linspace(0, 500, 300)
    
    # Dynamic 1X Running speed based on user-selected RPM
    base_1x = round(float(rpm) / 60.0, 1)  # e.g., 2950 RPM ≈ 49.2 Hz; 1800 RPM = 30 Hz
    bpfo = round(base_1x * 2.18, 1)       # Ball Pass Frequency Outer Race
    bpfi = round(base_1x * 3.31, 1)       # Ball Pass Frequency Inner Race

    # Base noise floor
    amplitude = np.random.normal(0.08, 0.02, size=len(frequencies))

    # Add 1X shaft speed peak
    amp_1x = 0.5 + min(1.2, vibration_level * 0.1)
    amplitude += amp_1x * np.exp(-((frequencies - base_1x) ** 2) / (2 * (1.8 ** 2)))

    # Add 2X harmonic peak
    amplitude += (amp_1x * 0.35) * np.exp(-((frequencies - (base_1x * 2)) ** 2) / (2 * (1.8 ** 2)))

    # Bearing fault scenario adds sharp BPFO and BPFI peaks
    if "Bearing" in scenario or vibration_level > 4.5:
        fault_severity = min(2.5, (vibration_level - 3.0) * 0.6)
        # BPFO Peak
        amplitude += fault_severity * np.exp(-((frequencies - bpfo) ** 2) / (2 * (2.2 ** 2)))
        # BPFI Peak
        amplitude += (fault_severity * 0.7) * np.exp(-((frequencies - bpfi) ** 2) / (2 * (2.2 ** 2)))
        # Sidebands
        amplitude += (fault_severity * 0.25) * np.exp(-((frequencies - (bpfo - base_1x)) ** 2) / (2 * (2.0 ** 2)))
        amplitude += (fault_severity * 0.25) * np.exp(-((frequencies - (bpfo + base_1x)) ** 2) / (2 * (2.0 ** 2)))

    # Impeller cavitation adds broad high-frequency turbulence
    elif "Cavitation" in scenario:
        cav_noise = np.exp(-((frequencies - 320) ** 2) / (2 * (80.0 ** 2))) * 0.7
        amplitude += cav_noise

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=frequencies,
        y=amplitude,
        mode="lines",
        line=dict(color="#38bdf8", width=1.8),
        name="Spectral Density (g RMS)",
        hovertemplate="Freq: %{x:.1f} Hz<br>Amp: %{y:.3f} g RMS<extra></extra>"
    ))

    # Annotate key harmonic markers dynamically based on RPM
    annotations = [
        dict(x=base_1x, y=amp_1x, text=f"1X ({base_1x} Hz)", showarrow=True, arrowhead=2, arrowcolor="#10b981", font=dict(color="#10b981", size=10)),
        dict(x=base_1x * 2, y=amp_1x * 0.35, text=f"2X ({base_1x*2:.1f} Hz)", showarrow=True, arrowhead=2, arrowcolor="#64748b", font=dict(color="#94a3b8", size=9))
    ]

    if "Bearing" in scenario or vibration_level > 4.5:
        annotations.append(
            dict(x=bpfo, y=max(amplitude), text=f"BPFO ({bpfo} Hz) FAULT", showarrow=True, arrowhead=2, arrowcolor="#ef4444", font=dict(color="#ef4444", size=11, family="monospace"))
        )
        annotations.append(
            dict(x=bpfi, y=max(amplitude) * 0.7, text=f"BPFI ({bpfi} Hz)", showarrow=True, arrowhead=2, arrowcolor="#f59e0b", font=dict(color="#f59e0b", size=10))
        )

    fig.update_layout(
        title=f"FFT SPECTRUM — SPEED-SYNCHRONIZED HARMONIC ANALYSIS ({rpm} RPM)",
        title_font=dict(size=13, color="#f8fafc"),
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.4)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        xaxis_title="Frequency (Hz)",
        yaxis_title="Spectral Amplitude (g RMS)",
        height=320,
        margin=dict(l=40, r=20, t=40, b=40),
        annotations=annotations
    )

    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)")

    return fig


def render_correlation_heatmap(df_history: pd.DataFrame):
    """
    Renders correlation matrix between all 4 sensors to demonstrate multivariate coupling.
    """
    if df_history is None or df_history.empty or len(df_history) < 5:
        return None

    cols = ["temperature", "vibration", "pressure", "power"]
    corr = df_history[cols].corr()

    labels = ["Temperature", "Vibration", "Pressure", "Power"]

    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=labels,
        y=labels,
        colorscale=[
            [0.0, "#0f172a"],
            [0.5, "#334155"],
            [1.0, "#38bdf8"]
        ],
        zmin=-1.0,
        zmax=1.0,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        textfont=dict(size=12, color="#ffffff")
    ))

    fig.update_layout(
        title="MULTIVARIATE SENSOR COUPLING (CORRELATION MATRIX)",
        title_font=dict(size=13, color="#f8fafc"),
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.4)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        height=320,
        margin=dict(l=40, r=20, t=40, b=40)
    )

    return fig
