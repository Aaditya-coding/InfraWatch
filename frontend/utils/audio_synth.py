"""
Acoustic Sonification Engine for InfraWatch.
Synthesizes real-time audio signatures of industrial equipment using physics models:
- Normal Operation: Smooth 50 Hz fundamental motor hum + 2X harmonics.
- Bearing Fault: High-pitched bearing harmonic raceway impact & friction squeal.
- Cavitation: Hydraulic turbulence & broadband "gravel rattling" implosion noise.
- Critical Multi-Fault: Severe mechanical dissonance, abrasive grinding, and motor overload hum.
"""

import io
import wave
import numpy as np


def generate_pump_audio(scenario="Normal Operation", rpm=2950, duration=2.5, sample_rate=22050):
    """
    Generates synthetic 16-bit PCM WAV audio bytes simulating the pump's acoustic signature.
    Uses pure standard library wave + numpy (no heavy audio dependencies).
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    f_run = float(rpm) / 60.0  # e.g., 2950 RPM ≈ 49.17 Hz

    if "Bearing" in scenario:
        # 1. Base running speed hum
        base_hum = 0.25 * np.sin(2 * np.pi * f_run * t)
        
        # 2. Outer race impact frequency (BPFO ≈ 3.5x shaft speed)
        bpfo = f_run * 3.55  # ~174 Hz
        # High-frequency metallic ringing excited by impacts (around 1200 Hz & 2400 Hz)
        ring_freq = 1450.0
        impact_envelope = np.maximum(0, np.sin(2 * np.pi * bpfo * t)) ** 4
        bearing_squeal = 0.45 * impact_envelope * np.sin(2 * np.pi * ring_freq * t)
        
        # 3. Micro-frictional dry scraping noise
        scrape = 0.2 * np.random.normal(0, 0.15, size=len(t)) * (1 + 0.3 * np.sin(2 * np.pi * f_run * t))
        
        signal = base_hum + bearing_squeal + scrape

    elif "Cavitation" in scenario:
        # 1. Base hydraulic hum
        base_hum = 0.3 * np.sin(2 * np.pi * f_run * t)
        
        # 2. Broadband turbulence noise (flow eddies)
        flow_noise = 0.35 * np.random.normal(0, 0.2, size=len(t))
        
        # 3. Cavitation vapor bubble collapse bursts ("gravel noise" around 3 kHz)
        bubble_bursts = np.random.poisson(lam=0.08, size=len(t)).astype(float)
        gravel_noise = bubble_bursts * np.sin(2 * np.pi * 3200 * t) * 0.6
        
        signal = base_hum + flow_noise + gravel_noise

    elif "Critical" in scenario:
        # Heavy dissonance: unbalance vibration, severe rubbing, overheating squeal
        unbalance = 0.5 * np.sin(2 * np.pi * f_run * t)
        harm2 = 0.35 * np.sin(2 * np.pi * (f_run * 2) * t)
        harm3 = 0.25 * np.sin(2 * np.pi * (f_run * 3) * t)
        violent_chatter = 0.45 * np.sin(2 * np.pi * 880 * t) * np.random.normal(0, 0.3, size=len(t))
        signal = unbalance + harm2 + harm3 + violent_chatter

    else:
        # Normal healthy pump: clean fundamental running hum + mild electrical 100 Hz harmonic + soft smooth airflow
        base_hum = 0.45 * np.sin(2 * np.pi * f_run * t)
        hum_2x = 0.2 * np.sin(2 * np.pi * (f_run * 2) * t)
        cooling_fan = 0.1 * np.random.normal(0, 0.05, size=len(t))
        signal = base_hum + hum_2x + cooling_fan

    # Normalize audio signal to prevent clipping (-1.0 to 1.0)
    max_val = np.max(np.abs(signal))
    if max_val > 0:
        signal = signal / max_val

    # Convert to 16-bit PCM integers
    audio_int16 = (signal * 32767 * 0.85).astype(np.int16)

    # Encode to WAV buffer in memory
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)       # Mono
        wav_file.setsampwidth(2)      # 16-bit (2 bytes per sample)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int16.tobytes())

    buffer.seek(0)
    return buffer.read()
