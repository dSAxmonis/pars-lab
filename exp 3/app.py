import os
import io
import wave
import base64
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
AUDIO_PATH = os.path.join(STATIC_DIR, 'sample_audio.wav')

os.makedirs(STATIC_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. GENERATE AUDIO FILE IF NOT PRESENT (16kHz, 5 seconds)
# -------------------------------------------------------------
def ensure_sample_audio():
    if os.path.exists(AUDIO_PATH):
        return
    
    sample_rate = 16000
    duration = 5.0  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Composite multi-segment audio signal simulating varied acoustic events
    signal = np.zeros_like(t)
    
    # 0.0 - 1.0s: Low-frequency harmonic (Voiced speech simulation, ~250 Hz)
    m1 = (t >= 0.0) & (t < 1.0)
    signal[m1] = 0.6 * np.sin(2 * np.pi * 250 * t[m1]) + 0.2 * np.sin(2 * np.pi * 500 * t[m1])
    
    # 1.0 - 2.0s: Mid-frequency tone with harmonics (~600 Hz & 1200 Hz)
    m2 = (t >= 1.0) & (t < 2.0)
    signal[m2] = 0.7 * np.sin(2 * np.pi * 600 * t[m2]) + 0.3 * np.sin(2 * np.pi * 1200 * t[m2])
    
    # 2.0 - 2.5s: Low energy silence / ambient pause
    m3 = (t >= 2.0) & (t < 2.5)
    signal[m3] = 0.02 * np.random.normal(0, 1, np.sum(m3))
    
    # 2.5 - 3.5s: High-frequency friction / noisy burst (Unvoiced / percussive ~3000 Hz)
    m4 = (t >= 2.5) & (t < 3.5)
    signal[m4] = 0.4 * np.sin(2 * np.pi * 3200 * t[m4]) + 0.3 * np.random.normal(0, 1, np.sum(m4))
    
    # 3.5 - 4.5s: Musical tone (~880 Hz harmonic pitch)
    m5 = (t >= 3.5) & (t < 4.5)
    signal[m5] = 0.8 * np.sin(2 * np.pi * 880 * t[m5]) + 0.25 * np.sin(2 * np.pi * 1760 * t[m5])
    
    # 4.5 - 5.0s: Decay / fade-out tone (~440 Hz)
    m6 = (t >= 4.5) & (t <= 5.0)
    decay = np.linspace(1.0, 0.1, np.sum(m6))
    signal[m6] = 0.5 * decay * np.sin(2 * np.pi * 440 * t[m6])
    
    # Normalize to 16-bit integer range [-32767, 32767]
    signal = signal / np.max(np.abs(signal)) * 0.9
    audio_int16 = (signal * 32767).astype(np.int16)
    
    with wave.open(AUDIO_PATH, 'wb') as wf:
        wf.setnchannels(1)        # Mono
        wf.setsampwidth(2)        # 16-bit (2 bytes)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())

# -------------------------------------------------------------
# 2. FEATURE EXTRACTION ACROSS 10 TIMESTAMPS
# -------------------------------------------------------------
def extract_audio_features():
    ensure_sample_audio()
    
    with wave.open(AUDIO_PATH, 'rb') as wf:
        sample_rate = wf.getframerate()
        n_frames = wf.getnframes()
        raw_bytes = wf.readframes(n_frames)
        
    signal = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32)
    signal = signal / 32768.0  # Normalized to [-1.0, 1.0]
    
    # Exactly 10 timestamp samples across the 5.0-second file
    timestamps = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    window_duration = 0.05  # 50 ms window
    window_size = int(sample_rate * window_duration)
    
    features = []
    
    for ts in timestamps:
        center_sample = int(ts * sample_rate)
        start_idx = max(0, center_sample - window_size // 2)
        end_idx = min(len(signal), start_idx + window_size)
        window = signal[start_idx:end_idx]
        
        N = len(window)
        if N == 0:
            continue
            
        # 1. Feature 1: Root Mean Square (RMS) Energy
        rms_energy = np.sqrt(np.mean(window ** 2))
        
        # 2. Feature 2: Zero Crossing Rate (ZCR)
        signs = np.sign(window)
        signs[signs == 0] = 1
        zcr = 0.5 * np.mean(np.abs(np.diff(signs)))
        
        # 3. Feature 3: Spectral Centroid (Hz)
        fft_mags = np.abs(np.fft.rfft(window))
        freqs = np.fft.rfftfreq(N, d=1.0 / sample_rate)
        sum_mags = np.sum(fft_mags)
        if sum_mags > 1e-8:
            spectral_centroid = np.sum(freqs * fft_mags) / sum_mags
        else:
            spectral_centroid = 0.0
            
        # Inferred acoustic state
        if rms_energy < 0.05:
            inferred_state = "Silence / Ambient"
        elif zcr > 0.25:
            inferred_state = "Unvoiced / High Noise"
        elif spectral_centroid > 1200:
            inferred_state = "High Pitch Voiced"
        else:
            inferred_state = "Low Harmonic Voiced"
            
        features.append({
            'sample_id': len(features) + 1,
            'timestamp_sec': ts,
            'window_range': f"[{round(ts - window_duration/2, 3)}s - {round(ts + window_duration/2, 3)}s]",
            'rms_energy': round(float(rms_energy), 4),
            'zcr': round(float(zcr), 4),
            'spectral_centroid_hz': round(float(spectral_centroid), 2),
            'inferred_state': inferred_state
        })
        
    return features, sample_rate, len(signal) / sample_rate

# -------------------------------------------------------------
# 3. VISUALIZATION PLOT ACROSS TIMESTAMPS
# -------------------------------------------------------------
def generate_feature_plot(features):
    df = pd.DataFrame(features)
    
    fig, axes = plt.subplots(3, 1, figsize=(11, 7), sharex=True)
    
    # Plot 1: RMS Energy
    axes[0].plot(df['timestamp_sec'], df['rms_energy'], marker='o', color='#1b5e20', linewidth=2, markersize=6)
    axes[0].set_ylabel('RMS Energy', fontsize=10, fontweight='bold')
    axes[0].set_title('Extracted Audio Features Across 10 Timestamps', fontsize=12, fontweight='bold', pad=10)
    axes[0].grid(True, linestyle='--', alpha=0.5)
    for _, row in df.iterrows():
        axes[0].annotate(f"{row['rms_energy']:.2f}", (row['timestamp_sec'], row['rms_energy']),
                         textcoords="offset points", xytext=(0, 7), ha='center', fontsize=8)

    # Plot 2: Zero Crossing Rate
    axes[1].plot(df['timestamp_sec'], df['zcr'], marker='s', color='#d84315', linewidth=2, markersize=6)
    axes[1].set_ylabel('Zero Crossing Rate', fontsize=10, fontweight='bold')
    axes[1].grid(True, linestyle='--', alpha=0.5)
    for _, row in df.iterrows():
        axes[1].annotate(f"{row['zcr']:.2f}", (row['timestamp_sec'], row['zcr']),
                         textcoords="offset points", xytext=(0, 7), ha='center', fontsize=8)

    # Plot 3: Spectral Centroid (Hz)
    axes[2].plot(df['timestamp_sec'], df['spectral_centroid_hz'], marker='^', color='#0d47a1', linewidth=2, markersize=6)
    axes[2].set_ylabel('Centroid (Hz)', fontsize=10, fontweight='bold')
    axes[2].set_xlabel('Timestamp (seconds)', fontsize=10, fontweight='bold')
    axes[2].grid(True, linestyle='--', alpha=0.5)
    for _, row in df.iterrows():
        axes[2].annotate(f"{int(row['spectral_centroid_hz'])}", (row['timestamp_sec'], row['spectral_centroid_hz']),
                         textcoords="offset points", xytext=(0, 7), ha='center', fontsize=8)

    axes[2].set_xticks(df['timestamp_sec'])
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=130)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/')
def index():
    features, sample_rate, duration = extract_audio_features()
    plot_b64 = generate_feature_plot(features)
    
    justifications = [
        {
            'feature': 'RMS Energy (Root Mean Square)',
            'formula': 'sqrt( (1/N) * sum(x[n]^2) )',
            'meaning': 'Measures instantaneous physical signal power, loudness, and amplitude.',
            'objective': 'Voice Activity Detection (VAD), silence removal in speech systems, audio segment boundary identification.'
        },
        {
            'feature': 'Zero Crossing Rate (ZCR)',
            'formula': '(1 / 2N) * sum(|sgn(x[n]) - sgn(x[n-1])|)',
            'meaning': 'Measures the rate of sign changes between successive discrete audio samples.',
            'objective': 'Distinguishing voiced speech (low ZCR vowels) from unvoiced speech (high ZCR fricatives like /s/, /sh/) and percussion.'
        },
        {
            'feature': 'Spectral Centroid (Frequency Center)',
            'formula': 'sum(f_k * |X[k]|) / sum(|X[k]|)',
            'meaning': 'Indicates the center of gravity of the frequency spectrum; corresponds to acoustic brightness.',
            'objective': 'Musical timbre classification, audio genre recognition, instrument identification, speaker voice quality profiling.'
        }
    ]
    
    return render_template(
        'index.html',
        features=features,
        sample_rate=sample_rate,
        duration=duration,
        plot_b64=plot_b64,
        justifications=justifications
    )

if __name__ == '__main__':
    print("Starting Experiment 3 Flask Server on http://127.0.0.1:5005")
    app.run(host='127.0.0.1', port=5005, debug=True)
