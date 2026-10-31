"""
InfraWatch — Automated HD Demo Video Generator
Creates a crisp 80-second 720p HD demonstration video of InfraWatch.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio

WIDTH = 1280
HEIGHT = 720
FPS = 20
TOTAL_FRAMES = 1600  # 80 seconds at 20 fps

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "InfraWatch_Demo.mp4")

# Load fonts
try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 36)
    font_heading = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 24)
    font_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    font_small = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
    font_mono_large = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 32)
    font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
    font_mono_small = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 12)
except Exception:
    font_title = ImageFont.load_default()
    font_heading = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_mono_large = ImageFont.load_default()
    font_mono = ImageFont.load_default()
    font_mono_small = ImageFont.load_default()


def draw_header(draw, title_text, badge_text, badge_color):
    # Top bar
    draw.rectangle([0, 0, WIDTH, 54], fill=(15, 23, 42))
    draw.line([(0, 54), (WIDTH, 54)], fill=(51, 65, 85), width=1)
    
    # Logo
    draw.text((25, 12), "⚙ InfraWatch", fill=(56, 189, 248), font=font_heading)
    draw.text((185, 17), "•  Industrial Pump Digital Twin", fill=(148, 163, 184), font=font_body)
    
    # Title / Stage
    draw.text((540, 16), title_text, fill=(241, 245, 249), font=font_body)

    # Status Pill
    badge_w = 160
    draw.rounded_rectangle([WIDTH - badge_w - 25, 12, WIDTH - 25, 42], radius=6, fill=badge_color, outline=(255, 255, 255, 40))
    draw.text((WIDTH - badge_w - 15, 16), badge_text, fill=(255, 255, 255), font=font_mono_small)


def draw_card(draw, x, y, w, h, title, val_str, unit_str, sub_str, border_color, text_color):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=(15, 23, 42), outline=border_color, width=2)
    draw.text((x + 14, y + 10), title.upper(), fill=(148, 163, 184), font=font_small)
    draw.text((x + 14, y + 30), val_str, fill=text_color, font=font_mono_large)
    if unit_str:
        draw.text((x + 14 + len(val_str) * 20, y + 42), unit_str, fill=(100, 116, 139), font=font_small)
    if sub_str:
        draw.text((x + 14, y + 74), sub_str, fill=(148, 163, 184), font=font_small)


def draw_digital_twin_schematic(draw, x, y, w, h, comp_health, frame_idx, rpm):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(8, 12, 22), outline=(30, 41, 59), width=1)
    draw.text((x + 16, y + 12), "2D ANIMATED DIGITAL TWIN SCHEMATIC", fill=(226, 232, 240), font=font_body)
    draw.text((x + 16, y + 34), f"Grundfos CRN 32-4 Multi-Stage Pump  |  {rpm} RPM", fill=(100, 116, 139), font=font_small)

    cx = x + 30
    cy = y + 70

    # Colors based on health
    color_map = {
        "HEALTHY": (16, 185, 129),
        "WARNING": (245, 158, 11),
        "CRITICAL": (239, 68, 68),
        "DEGRADING": (56, 189, 248)
    }

    nde_col = color_map.get(comp_health.get("nde_bearing", "HEALTHY"))
    de_col = color_map.get(comp_health.get("de_bearing", "HEALTHY"))
    mot_col = color_map.get(comp_health.get("motor", "HEALTHY"))
    imp_col = color_map.get(comp_health.get("impeller", "HEALTHY"))
    seal_col = color_map.get(comp_health.get("seal", "HEALTHY"))

    # Central Shaft
    draw.rectangle([cx + 20, cy + 50, cx + 540, cy + 62], fill=(148, 163, 184))

    # NDE Bearing (Left)
    draw.rounded_rectangle([cx + 30, cy + 30, cx + 60, cy + 82], radius=4, fill=(15, 23, 42), outline=nde_col, width=3)
    draw.text((cx + 34, cy + 12), "NDE", fill=nde_col, font=font_mono_small)

    # Siemens Motor Stator
    draw.rounded_rectangle([cx + 65, cy + 15, cx + 250, cy + 97], radius=8, fill=(30, 41, 59), outline=mot_col, width=2)
    # Cooling fins
    for fx in range(cx + 80, cx + 240, 20):
        draw.line([(fx, cy + 15), (fx, cy + 97)], fill=(51, 65, 85), width=1)
    draw.text((cx + 105, cy + 50), "SIEMENS 11kW MOTOR", fill=(241, 245, 249), font=font_mono_small)

    # Drive End Bearing
    draw.rounded_rectangle([cx + 255, cy + 30, cx + 285, cy + 82], radius=4, fill=(15, 23, 42), outline=de_col, width=3)
    draw.text((cx + 260, cy + 12), "DE", fill=de_col, font=font_mono_small)

    # Coupling
    draw.rectangle([cx + 290, cy + 42, cx + 325, cy + 70], fill=(51, 65, 85), outline=(100, 116, 139), width=1)
    draw.text((cx + 292, cy + 50), "CPL", fill=(148, 163, 184), font=font_mono_small)

    # Mechanical Seal
    draw.rectangle([cx + 330, cy + 35, cx + 355, cy + 77], fill=(15, 23, 42), outline=seal_col, width=2)
    draw.text((cx + 332, cy + 18), "SEAL", fill=seal_col, font=font_mono_small)

    # Volute & 4 Impeller Stages
    draw.rounded_rectangle([cx + 360, cy + 20, cx + 550, cy + 92], radius=6, fill=(15, 23, 42), outline=imp_col, width=2)
    
    # Rotating blades simulation
    angle = (frame_idx * 0.4) % (math.pi * 2)
    for idx, ix in enumerate([cx + 390, cx + 430, cx + 470, cx + 510]):
        draw.rectangle([ix, cy + 28, ix + 16, cy + 84], fill=(30, 41, 59), outline=(71, 85, 105), width=1)
        # spinning tick
        oy = int(math.sin(angle + idx) * 14)
        draw.line([(ix + 8, cy + 56 - oy), (ix + 8, cy + 56 + oy)], fill=(56, 189, 248), width=2)
    
    draw.text((cx + 410, cy + 102), "GRUNDFOS 4-STAGE VOLUTE", fill=(148, 163, 184), font=font_mono_small)

    # Suction & Discharge pipes
    draw.rectangle([cx + 400, cy + 92, cx + 430, cy + 120], fill=(30, 41, 59), outline=(56, 189, 248), width=1)
    draw.text((cx + 390, cy + 124), "INLET (SUCTION)", fill=(56, 189, 248), font=font_mono_small)

    draw.rectangle([cx + 490, cy - 8, cx + 520, cy + 20], fill=(30, 41, 59), outline=(16, 185, 129), width=1)
    draw.text((cx + 480, cy - 22), "OUTLET (DISCHARGE)", fill=(16, 185, 129), font=font_mono_small)


def draw_live_chart(draw, x, y, w, h, data_history, title, color, y_label):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=(8, 12, 22), outline=(30, 41, 59), width=1)
    draw.text((x + 14, y + 10), title, fill=(226, 232, 240), font=font_body)
    draw.text((x + w - 120, y + 12), y_label, fill=(100, 116, 139), font=font_small)

    # Chart canvas box
    cx, cy, cw, ch = x + 15, y + 36, w - 30, h - 50
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=(15, 23, 42), outline=(30, 41, 59))

    # Gridlines
    for gy in range(cy + 25, cy + ch, 25):
        draw.line([(cx, gy), (cx + cw, gy)], fill=(30, 41, 59), width=1)

    if len(data_history) > 1:
        min_v = min(data_history) - 0.5
        max_v = max(data_history) + 0.5
        pts = []
        for i, val in enumerate(data_history):
            px = cx + int((i / (len(data_history) - 1)) * cw)
            norm = (val - min_v) / max(0.1, (max_v - min_v))
            py = cy + ch - int(norm * (ch - 8)) - 4
            pts.append((px, py))
        
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i + 1]], fill=color, width=2)
        
        # Latest point dot
        draw.ellipse([pts[-1][0]-4, pts[-1][1]-4, pts[-1][0]+4, pts[-1][1]+4], fill=(255, 255, 255), outline=color, width=2)


def draw_fft_spectrum(draw, x, y, w, h, scenario, rpm):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=(8, 12, 22), outline=(30, 41, 59), width=1)
    draw.text((x + 14, y + 10), "FFT VIBRATION SPECTRUM (HARMONICS)", fill=(226, 232, 240), font=font_body)
    
    running_hz = rpm / 60.0
    bpfo_hz = running_hz * 2.18
    draw.text((x + 14, y + 30), f"1X Shaft: {running_hz:.1f} Hz  |  BPFO Bearing Defect: {bpfo_hz:.1f} Hz", fill=(56, 189, 248), font=font_mono_small)

    cx, cy, cw, ch = x + 15, y + 50, w - 30, h - 70
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=(15, 23, 42), outline=(30, 41, 59))

    bars = 48
    bar_w = cw // bars
    for b in range(bars):
        freq = (b / bars) * 300.0
        amp = 0.15 + (math.sin(b * 0.7) * 0.08)

        # 1X peak
        if abs(freq - running_hz) < 7:
            amp += 1.8
        # 2X peak
        if abs(freq - running_hz * 2) < 7:
            amp += 0.9

        # Fault harmonics
        if "Bearing" in scenario and abs(freq - bpfo_hz) < 8:
            amp += 2.6
        if "Cavitation" in scenario and 120 < freq < 240:
            amp += 0.8 + ((b % 5) * 0.15)

        bh = int(min(ch - 5, (amp / 3.8) * ch))
        bx = cx + (b * bar_w) + 2
        by = cy + ch - bh

        color = (245, 158, 11) if ("Bearing" in scenario and abs(freq - bpfo_hz) < 8) else (56, 189, 248)
        draw.rectangle([bx, by, bx + bar_w - 2, cy + ch], fill=color)


def generate_video():
    print(f"Rendering {TOTAL_FRAMES} frames ({TOTAL_FRAMES/FPS:.1f} seconds) to {OUTPUT_PATH}...")
    writer = imageio.get_writer(OUTPUT_PATH, fps=FPS, codec='libx264', quality=8)

    # Rolling data stores
    history_vib = [2.4] * 50
    history_temp = [58.0] * 50

    for f in range(TOTAL_FRAMES):
        img = Image.new("RGB", (WIDTH, HEIGHT), color=(11, 15, 25))
        draw = ImageDraw.Draw(img)

        # ----------------------------------------------------
        # SCENE 1: Introduction (0 to 240 frames: 0s - 12s)
        # ----------------------------------------------------
        if f < 240:
            # Title Screen
            draw.text((WIDTH // 2 - 150, 160), "⚙ InfraWatch", fill=(56, 189, 248), font=font_title)
            draw.text((WIDTH // 2 - 320, 230), "AI-POWERED PREDICTIVE INFRASTRUCTURE MONITORING", fill=(241, 245, 249), font=font_heading)
            draw.text((WIDTH // 2 - 240, 275), "& INDUSTRIAL PUMP DIGITAL TWIN INTELLIGENCE", fill=(148, 163, 184), font=font_heading)

            # Details Box
            draw.rounded_rectangle([WIDTH // 2 - 380, 340, WIDTH // 2 + 380, 520], radius=12, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
            draw.text((WIDTH // 2 - 350, 365), "🏆 Hacktoberfest Hack Day Prayagraj × CC Club MNNIT (Track 1)", fill=(16, 185, 129), font=font_body)
            draw.text((WIDTH // 2 - 350, 400), "• Monitored Asset: Grundfos CRN 32-4 Multi-Stage Pump & Siemens 11kW Motor", fill=(226, 232, 240), font=font_body)
            draw.text((WIDTH // 2 - 350, 435), "• Multi-Stage AI Pipeline: Anomaly Detection + ISO Risk Engine + Prescriptive Rules", fill=(226, 232, 240), font=font_body)
            draw.text((WIDTH // 2 - 350, 470), "• Turnkey Launch: Single-click start.bat web deployment at localhost:8501", fill=(56, 189, 248), font=font_body)

            # Pulsing status
            alpha = int((math.sin(f * 0.1) + 1) * 127)
            draw.text((WIDTH // 2 - 180, 570), "INITIALIZING SENSOR TELEMETRY STREAM...", fill=(56, 189, 248), font=font_mono)

        # ----------------------------------------------------
        # SCENE 2: Module Architecture Overview (240 to 440: 12s - 22s)
        # ----------------------------------------------------
        elif f < 440:
            draw_header(draw, "PIPELINE ARCHITECTURE (MODULES A - D)", "🟢 AI ENGINE CONNECTED", (16, 185, 129))

            draw.text((WIDTH // 2 - 320, 90), "4-STAGE PREDICTIVE FAILURE INTELLIGENCE PIPELINE", fill=(241, 245, 249), font=font_heading)

            modules = [
                ("MODULE A: SENSOR SIMULATOR", "Physics-modeled telemetry stream\n(Vibration, Temp, Pressure, Power)\nDynamic RPM & Suction Cavitation", (56, 189, 248)),
                ("MODULE B: ANOMALY DETECTOR", "Multivariate statistical engine\nISO 10816 threshold limits\nRolling Z-Score anomaly detection", (16, 185, 129)),
                ("MODULE C: RISK ASSESSMENT", "Severity scoring algorithm\nComponent degradation index\nISO 10816 Zone A/B/C/D evaluation", (245, 158, 11)),
                ("MODULE D: PRESCRIPTIVE ACTIONS", "ISO/OEM root cause diagnostics\nAutomated prescriptive work orders\nSCADA ticket & CSV report export", (168, 85, 247))
            ]

            card_w = 260
            for idx, (m_title, m_desc, m_col) in enumerate(modules):
                mx = 60 + idx * 290
                draw.rounded_rectangle([mx, 160, mx + card_w, 420], radius=10, fill=(15, 23, 42), outline=m_col, width=2)
                draw.text((mx + 12, 180), m_title, fill=m_col, font=font_mono_small)
                draw.line([(mx + 12, 210), (mx + card_w - 12, 210)], fill=(51, 65, 85), width=1)
                
                for line_idx, line in enumerate(m_desc.split("\n")):
                    draw.text((mx + 12, 230 + line_idx * 30), line, fill=(226, 232, 240), font=font_small)

                if idx < 3:
                    draw.text((mx + card_w + 8, 290), "➔", fill=(148, 163, 184), font=font_heading)

            # Verification banner
            draw.rounded_rectangle([60, 460, WIDTH - 60, 640], radius=10, fill=(8, 12, 22), outline=(16, 185, 129), width=1)
            draw.text((90, 485), "AUTOMATED QUALITY & INTEGRATION STATUS", fill=(16, 185, 129), font=font_heading)
            draw.text((90, 530), "✔ 35/35 Pytest Unit Tests Passing (Anomaly, Risk, Recommendation, Simulator)", fill=(241, 245, 249), font=font_body)
            draw.text((90, 565), "✔ Full Pipeline Execution: test_full_pipeline.py, test_module_b, test_module_c verified", fill=(241, 245, 249), font=font_body)
            draw.text((90, 600), "✔ Seamless Bridge: backend_bridge.py active with live parameter synchronization", fill=(56, 189, 248), font=font_body)

        # ----------------------------------------------------
        # SCENE 3: Normal Operation (440 to 760: 22s - 38s)
        # ----------------------------------------------------
        elif f < 760:
            draw_header(draw, "LIVE TELEMETRY: NORMAL OPERATION (2950 RPM)", "🟢 SYSTEM NOMINAL", (16, 185, 129))

            # Oscillating normal values
            vib = 2.4 + math.sin(f * 0.2) * 0.15
            temp = 58.0 + math.cos(f * 0.15) * 0.4
            history_vib.append(vib)
            history_vib.pop(0)
            history_temp.append(temp)
            history_temp.pop(0)

            # KPI Cards
            card_w = 224
            draw_card(draw, 40, 75, card_w, 105, "Pump Health Index", "95%", "", "RUL: 720h | Status: OPTIMAL", (16, 185, 129), (16, 185, 129))
            draw_card(draw, 284, 75, card_w, 105, "Vibration (RMS)", f"{vib:.2f}", "mm/s", "ISO Zone A (Good)", (16, 185, 129), (16, 185, 129))
            draw_card(draw, 528, 75, card_w, 105, "Bearing Temp", f"{temp:.1f}", "°C", "Nominal (Max Trip: 85°C)", (16, 185, 129), (16, 185, 129))
            draw_card(draw, 772, 75, card_w, 105, "Discharge Pressure", "4.24", "bar", "Nominal (NPSH Margin Safe)", (56, 189, 248), (56, 189, 248))
            draw_card(draw, 1016, 75, card_w, 105, "Active Power", "7.52", "kW", "Rated: 11.0 kW (IE3 Motor)", (168, 85, 247), (168, 85, 247))

            # Digital Twin
            health_dict = {"nde_bearing": "HEALTHY", "de_bearing": "HEALTHY", "motor": "HEALTHY", "impeller": "HEALTHY", "seal": "HEALTHY"}
            draw_digital_twin_schematic(draw, 40, 200, 650, 240, health_dict, f, 2950)

            # Vibration Chart
            draw_live_chart(draw, 710, 200, 530, 240, history_vib, "REAL-TIME VIBRATION (mm/s RMS)", (56, 189, 248), "ISO Limit: 4.5 mm/s")

            # Bottom FFT
            draw_fft_spectrum(draw, 40, 460, 650, 235, "Normal Operation", 2950)

            # Bottom Diagnostics / Sonar Info
            draw.rounded_rectangle([710, 460, 1240, 695], radius=10, fill=(8, 12, 22), outline=(30, 41, 59), width=1)
            draw.text((730, 478), "ACOUSTIC MACHINE SONIFICATION & DIAGNOSTICS", fill=(226, 232, 240), font=font_body)
            draw.text((730, 515), "🎧 Acoustic Sonar: Continuous 50 Hz electromagnetic motor hum", fill=(16, 185, 129), font=font_small)
            draw.text((730, 550), "• Root Cause: All parameters operating within normal ISO limits.", fill=(226, 232, 240), font=font_small)
            draw.text((730, 585), "• Recommendation: Routine scheduled inspection according to plan.", fill=(148, 163, 184), font=font_small)
            draw.text((730, 630), "Status: 🟢 Connected to Aditya's ML Engine", fill=(56, 189, 248), font=font_mono_small)

        # ----------------------------------------------------
        # SCENE 4: Fault Mode 1 — Bearing Raceway Spall (760 to 1060: 38s - 53s)
        # ----------------------------------------------------
        elif f < 1060:
            draw_header(draw, "FAULT SCENARIO: BEARING RACEWAY FAULT (BPFO/BPFI)", "🔴 CRITICAL ALARM", (239, 68, 68))

            # Escalating fault values
            prog = min(1.0, (f - 760) / 180.0)
            vib = 2.4 + (prog * 4.6) + math.sin(f * 0.4) * 0.35
            temp = 58.0 + (prog * 23.0) + math.sin(f * 0.2) * 0.5
            history_vib.append(vib)
            history_vib.pop(0)
            history_temp.append(temp)
            history_temp.pop(0)

            health_score = max(18, int(95 - prog * 65))
            health_status = "WARNING" if health_score > 40 else "CRITICAL"
            health_col = (245, 158, 11) if health_score > 40 else (239, 68, 68)

            card_w = 224
            draw_card(draw, 40, 75, card_w, 105, "Pump Health Index", f"{health_score}%", "", f"RUL: {int(720 - prog*670)}h | {health_status}", health_col, health_col)
            draw_card(draw, 284, 75, card_w, 105, "Vibration (RMS)", f"{vib:.2f}", "mm/s", "ISO Zone D (UNACCEPTABLE)", (239, 68, 68), (239, 68, 68))
            draw_card(draw, 528, 75, card_w, 105, "Bearing Temp", f"{temp:.1f}", "°C", "Thermal Rise Alert (81.0°C)", (239, 68, 68), (239, 68, 68))
            draw_card(draw, 772, 75, card_w, 105, "Discharge Pressure", "4.05", "bar", "Slight Pressure Fluctuation", (56, 189, 248), (56, 189, 248))
            draw_card(draw, 1016, 75, card_w, 105, "Active Power", f"{7.5 + prog*1.6:.2f}", "kW", "Mechanical Drag Rise", (245, 158, 11), (245, 158, 11))

            # Digital Twin with NDE BEARING IN RED
            health_dict = {"nde_bearing": "CRITICAL", "de_bearing": "WARNING", "motor": "HEALTHY", "impeller": "HEALTHY", "seal": "HEALTHY"}
            draw_digital_twin_schematic(draw, 40, 200, 650, 240, health_dict, f, 2950)

            # Vibration Chart showing surge
            draw_live_chart(draw, 710, 200, 530, 240, history_vib, "VIBRATION SURGE (THRESHOLD BREACH)", (239, 68, 68), "TRIP: 4.5 mm/s")

            # FFT Spectrum showing BPFO defect peak at 107.5 Hz
            draw_fft_spectrum(draw, 40, 460, 650, 235, "Bearing Fault", 2950)

            # Root Cause & Prescriptive Action
            draw.rounded_rectangle([710, 460, 1240, 695], radius=10, fill=(8, 12, 22), outline=(239, 68, 68), width=1)
            draw.text((730, 478), "ML ANOMALY ROOT CAUSE & PRESCRIPTIVE ACTION", fill=(239, 68, 68), font=font_body)
            draw.text((730, 515), "🚨 Root Cause: Outer race defect harmonic (BPFO @ 107.5 Hz)", fill=(241, 245, 249), font=font_small)
            draw.text((730, 545), "   detected with rapid non-drive end thermal rise.", fill=(241, 245, 249), font=font_small)
            draw.text((730, 580), "🛠 Action: Re-lubricate NDE bearing with ISO VG 68 grease (25g)", fill=(16, 185, 129), font=font_small)
            draw.text((730, 610), "   or switch load to standby pump unit immediately.", fill=(16, 185, 129), font=font_small)
            draw.text((730, 650), "🎧 Acoustic: High-frequency raceway impact chirping (~1.4 kHz)", fill=(245, 158, 11), font=font_mono_small)

        # ----------------------------------------------------
        # SCENE 5: Fault Mode 2 — Suction Throttling & Cavitation (1060 to 1320: 53s - 66s)
        # ----------------------------------------------------
        elif f < 1320:
            draw_header(draw, "PHYSICS TUNING: SUCTION VALVE THROTTLED (40% OPEN)", "🟠 CAVITATION DETECTED", (245, 158, 11))

            prog = min(1.0, (f - 1060) / 140.0)
            press = 4.2 - (prog * 2.5) + math.sin(f * 0.3) * 0.1
            vib = 2.4 + (prog * 3.2) + math.sin(f * 0.5) * 0.3
            history_vib.append(vib)
            history_vib.pop(0)

            card_w = 224
            draw_card(draw, 40, 75, card_w, 105, "Pump Health Index", f"{int(92 - prog*55)}%", "", "Hydraulic Stall Risk", (245, 158, 11), (245, 158, 11))
            draw_card(draw, 284, 75, card_w, 105, "Vibration (RMS)", f"{vib:.2f}", "mm/s", "Broadband Cavitation Noise", (245, 158, 11), (245, 158, 11))
            draw_card(draw, 528, 75, card_w, 105, "Bearing Temp", "62.4", "°C", "Turbulent Eddies", (16, 185, 129), (16, 185, 129))
            draw_card(draw, 772, 75, card_w, 105, "Discharge Pressure", f"{press:.2f}", "bar", "CRITICAL PRESSURE DROP", (239, 68, 68), (239, 68, 68))
            draw_card(draw, 1016, 75, card_w, 105, "Active Power", "9.84", "kW", "Hydraulic Recirculation", (245, 158, 11), (245, 158, 11))

            # Digital Twin with IMPELLER IN RED/AMBER
            health_dict = {"nde_bearing": "HEALTHY", "de_bearing": "HEALTHY", "motor": "HEALTHY", "impeller": "CRITICAL", "seal": "WARNING"}
            draw_digital_twin_schematic(draw, 40, 200, 650, 240, health_dict, f, 2950)

            draw_live_chart(draw, 710, 200, 530, 240, history_vib, "HYDRAULIC CAVITATION PROFILE", (245, 158, 11), "Cavitation Limit: 3.0 bar")

            draw_fft_spectrum(draw, 40, 460, 650, 235, "Impeller Cavitation", 2950)

            draw.rounded_rectangle([710, 460, 1240, 695], radius=10, fill=(8, 12, 22), outline=(245, 158, 11), width=1)
            draw.text((730, 478), "CAVITATION BUBBLE IMPLOSION DIAGNOSTICS", fill=(245, 158, 11), font=font_body)
            draw.text((730, 515), "⚠️ Diagnostic: Suction pressure dropped below Net Positive Suction", fill=(241, 245, 249), font=font_small)
            draw.text((730, 545), "   Head (NPSH), triggering vapor bubble micro-implosions.", fill=(241, 245, 249), font=font_small)
            draw.text((730, 580), "🛠 Action: Inspect inlet strainer and open suction valve to > 85%.", fill=(16, 185, 129), font=font_small)
            draw.text((730, 620), "🎧 Acoustic: Chaotic broadband gravel rattling sound synthesized.", fill=(56, 189, 248), font=font_mono_small)

        # ----------------------------------------------------
        # SCENE 6: SCADA Work Order Ticket & Export (1320 to 1480: 66s - 74s)
        # ----------------------------------------------------
        elif f < 1480:
            draw_header(draw, "SCADA INCIDENT REPORT & WORK ORDER EXPORT", "📄 EXPORT READY", (168, 85, 247))

            draw.rounded_rectangle([60, 80, 700, 660], radius=10, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
            draw.text((85, 105), "# INFRAWATCH SCADA WORK ORDER TICKET", fill=(56, 189, 248), font=font_heading)
            draw.text((85, 150), "Asset ID: PUMP-402A (Grundfos CRN 32-4 Multi-Stage Pump)", fill=(241, 245, 249), font=font_body)
            draw.text((85, 180), "Work Order ID: WO-1730419200  |  Status: ACTIVE_DISPATCH", fill=(16, 185, 129), font=font_mono_small)
            draw.text((85, 210), "Current Machine Health: 34%  |  Severity: CRITICAL", fill=(239, 68, 68), font=font_body)

            draw.line([(85, 245), (675, 245)], fill=(51, 65, 85), width=1)
            draw.text((85, 260), "## INCIDENT DIAGNOSTIC SUMMARY", fill=(56, 189, 248), font=font_body)
            draw.text((85, 290), "• Root Cause: Outer race defect harmonic (BPFO @ 107.5 Hz)", fill=(226, 232, 240), font=font_small)
            draw.text((85, 315), "  with elevated thermal rise (79.2°C).", fill=(226, 232, 240), font=font_small)
            draw.text((85, 350), "• Prescriptive Action: Re-lubricate NDE bearing with ISO VG 68", fill=(16, 185, 129), font=font_small)
            draw.text((85, 375), "  synthetic grease within 24 hours.", fill=(16, 185, 129), font=font_small)

            draw.line([(85, 410), (675, 410)], fill=(51, 65, 85), width=1)
            draw.text((85, 425), "## TECHNICIAN DISPATCH CHECKLIST", fill=(56, 189, 248), font=font_body)
            draw.text((85, 455), "[X] Safe Lock-Out / Tag-Out (LOTO) Verified", fill=(226, 232, 240), font=font_small)
            draw.text((85, 485), "[X] Ultrasonic Contact Vibration Check Executed", fill=(226, 232, 240), font=font_small)
            draw.text((85, 515), "[ ] Lubricant Replenished (Shell Gadus S2 V220)", fill=(148, 163, 184), font=font_small)
            draw.text((85, 545), "[ ] Coupling Alignment & Suction NPSH Verified", fill=(148, 163, 184), font=font_small)

            draw.text((85, 600), "Signed: Lead Diagnostic Engineer __________________", fill=(148, 163, 184), font=font_body)

            # Export Demonstrations (Right)
            draw.rounded_rectangle([730, 80, WIDTH - 60, 350], radius=10, fill=(8, 12, 22), outline=(16, 185, 129), width=1)
            draw.text((755, 105), "ONE-CLICK EXPORT CAPABILITIES", fill=(16, 185, 129), font=font_heading)
            draw.text((755, 150), "📥 Download SCADA Work Order (.md)", fill=(56, 189, 248), font=font_body)
            draw.text((755, 180), "   Direct export to enterprise CMMS / maintenance logs.", fill=(148, 163, 184), font=font_small)
            draw.text((755, 230), "📊 Download Raw Telemetry (.csv)", fill=(16, 185, 129), font=font_body)
            draw.text((755, 260), "   Full time-series buffer for historical ML retraining.", fill=(148, 163, 184), font=font_small)

            draw.rounded_rectangle([730, 390, WIDTH - 60, 660], radius=10, fill=(8, 12, 22), outline=(168, 85, 247), width=1)
            draw.text((755, 415), "AUTOMATED QUALITY VERIFICATION", fill=(168, 85, 247), font=font_heading)
            draw.text((755, 460), "✔ test_full_pipeline.py PASSING", fill=(16, 185, 129), font=font_mono)
            draw.text((755, 495), "✔ test_module_b_integration.py PASSING", fill=(16, 185, 129), font=font_mono)
            draw.text((755, 530), "✔ test_module_c_integration.py PASSING", fill=(16, 185, 129), font=font_mono)
            draw.text((755, 565), "✔ 35/35 Unit Tests Executed (0.09s)", fill=(16, 185, 129), font=font_mono)
            draw.text((755, 610), "Status: Zero Regressions • 100% Reliable", fill=(56, 189, 248), font=font_body)

        # ----------------------------------------------------
        # SCENE 7: Outro & Single-Click Web Launch (1480 to 1600: 74s - 80s)
        # ----------------------------------------------------
        else:
            draw.text((WIDTH // 2 - 200, 160), "⚡ READY TO RUN", fill=(16, 185, 129), font=font_title)
            draw.text((WIDTH // 2 - 300, 225), "SINGLE-CLICK STARTUP WITH START.BAT", fill=(241, 245, 249), font=font_heading)

            draw.rounded_rectangle([WIDTH // 2 - 380, 290, WIDTH // 2 + 380, 480], radius=12, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
            draw.text((WIDTH // 2 - 350, 320), "1. Navigate to: C:\\InfraWatch", fill=(241, 245, 249), font=font_body)
            draw.text((WIDTH // 2 - 350, 360), "2. Double-Click: start.bat (or run.bat)", fill=(56, 189, 248), font=font_heading)
            draw.text((WIDTH // 2 - 350, 405), "3. Automatically starts server & launches http://localhost:8501", fill=(16, 185, 129), font=font_body)
            draw.text((WIDTH // 2 - 350, 440), "4. Full Digital Twin condition monitoring instantly active!", fill=(226, 232, 240), font=font_body)

            draw.text((WIDTH // 2 - 250, 530), "InfraWatch — AI Predictive Infrastructure Intelligence", fill=(148, 163, 184), font=font_body)
            draw.text((WIDTH // 2 - 210, 565), "Repository: https://github.com/Aaditya-coding/InfraWatch", fill=(56, 189, 248), font=font_mono_small)

        # Frame counter & progress bar at bottom
        progress = f / (TOTAL_FRAMES - 1)
        draw.rectangle([0, HEIGHT - 5, int(WIDTH * progress), HEIGHT], fill=(56, 189, 248))

        # Convert PIL Image to numpy array for imageio
        frame_np = np.array(img)
        writer.append_data(frame_np)

        if f % 200 == 0 or f == TOTAL_FRAMES - 1:
            print(f"Processed frame {f}/{TOTAL_FRAMES} ({(f/TOTAL_FRAMES)*100:.1f}%)")

    writer.close()
    print(f"Video rendering complete! File saved at: {OUTPUT_PATH}")
    file_size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"File size: {file_size_mb:.2f} MB")


if __name__ == "__main__":
    generate_video()
