"""
Interactive Plotly Charts for InfraWatch Dashboard.
Visualizes real-time sensor streams, safety threshold bands, and ML anomaly markers.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def render_sensor_charts(df_history: pd.DataFrame):
    """
    Renders 4 synchronized sensor plots in a 2x2 grid with anomaly highlights.
    """
    if df_history is None or df_history.empty:
        return None

    # Subplots: 2 rows x 2 columns
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Vibration RMS (mm/s) — ISO 10816-3",
            "Bearing Temperature (°C)",
            "Discharge Pressure (bar)",
            "Motor Active Power (kW)"
        ),
        vertical_spacing=0.15,
        horizontal_spacing=0.08
    )

    timestamps = df_history["timestamp"]

    # 1. Vibration
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=df_history["vibration"],
            mode="lines",
            name="Vibration",
            line=dict(color="#00f2fe", width=2),
            hovertemplate="Vib: %{y:.2f} mm/s<extra></extra>"
        ),
        row=1, col=1
    )
    # Anomaly points for vibration
    anomalies = df_history[df_history["anomaly"] == True]
    if not anomalies.empty:
        fig.add_trace(
            go.Scatter(
                x=anomalies["timestamp"],
                y=anomalies["vibration"],
                mode="markers",
                name="Vib Anomaly",
                marker=dict(color="#ef4444", size=8, symbol="cross-thin-open", line_width=2),
                hovertemplate="ANOMALY Vib: %{y:.2f} mm/s<extra></extra>"
            ),
            row=1, col=1
        )
    # ISO Warning Line (4.5 mm/s) & Danger (7.1 mm/s)
    fig.add_hline(y=4.5, line_dash="dash", line_color="#f59e0b", opacity=0.7, row=1, col=1, annotation_text="ISO Warning (4.5)", annotation_position="top left", annotation_font_size=10)
    fig.add_hline(y=7.1, line_dash="dash", line_color="#ef4444", opacity=0.7, row=1, col=1, annotation_text="ISO Danger (7.1)", annotation_position="top left", annotation_font_size=10)

    # 2. Temperature
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=df_history["temperature"],
            mode="lines",
            name="Temperature",
            line=dict(color="#f59e0b", width=2),
            hovertemplate="Temp: %{y:.1f} °C<extra></extra>"
        ),
        row=1, col=2
    )
    if not anomalies.empty:
        fig.add_trace(
            go.Scatter(
                x=anomalies["timestamp"],
                y=anomalies["temperature"],
                mode="markers",
                name="Temp Anomaly",
                marker=dict(color="#ef4444", size=8, symbol="cross-thin-open", line_width=2),
                hovertemplate="ANOMALY Temp: %{y:.1f} °C<extra></extra>"
            ),
            row=1, col=2
        )
    fig.add_hline(y=75.0, line_dash="dash", line_color="#f59e0b", opacity=0.7, row=1, col=2, annotation_text="Warning (75°C)", annotation_position="top left", annotation_font_size=10)
    fig.add_hline(y=85.0, line_dash="dash", line_color="#ef4444", opacity=0.7, row=1, col=2, annotation_text="Trip (85°C)", annotation_position="top left", annotation_font_size=10)

    # 3. Discharge Pressure
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=df_history["pressure"],
            mode="lines",
            name="Pressure",
            line=dict(color="#10b981", width=2),
            hovertemplate="Pressure: %{y:.2f} bar<extra></extra>"
        ),
        row=2, col=1
    )
    if not anomalies.empty:
        fig.add_trace(
            go.Scatter(
                x=anomalies["timestamp"],
                y=anomalies["pressure"],
                mode="markers",
                name="Pressure Anomaly",
                marker=dict(color="#ef4444", size=8, symbol="cross-thin-open", line_width=2),
                hovertemplate="ANOMALY Press: %{y:.2f} bar<extra></extra>"
            ),
            row=2, col=1
        )
    fig.add_hline(y=3.0, line_dash="dash", line_color="#ef4444", opacity=0.7, row=2, col=1, annotation_text="Min NPSH (3.0 bar)", annotation_position="bottom left", annotation_font_size=10)

    # 4. Motor Power
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=df_history["power"],
            mode="lines",
            name="Power",
            line=dict(color="#a855f7", width=2),
            hovertemplate="Power: %{y:.2f} kW<extra></extra>"
        ),
        row=2, col=2
    )
    fig.add_hline(y=10.0, line_dash="dash", line_color="#f59e0b", opacity=0.7, row=2, col=2, annotation_text="Rated Pwr (10.0 kW)", annotation_position="top left", annotation_font_size=10)

    # Dark Theme Layout
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.4)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        font=dict(color="#94a3b8", family="system-ui, -apple-system, sans-serif"),
        height=540,
        margin=dict(l=40, r=30, t=50, b=40),
        showlegend=False
    )

    # Polish axes
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(size=9))
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(size=9))

    return fig
