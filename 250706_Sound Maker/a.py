import numpy as np
from scipy.io.wavfile import write
import os

# === 설정 ===
sample_rate = 44100
duration = 1.0  # 폭발은 짧기 때문에 전체 길이를 줄임
volume = 0.9
filename = "explosion.wav"
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(output_dir, exist_ok=True)

# 시간 축
t = np.linspace(0, duration, int(sample_rate * duration), False)

# [1] 순간 폭발 임펄스 (노이즈 + 빠른 감쇠)
impulse_duration = 0.2
impulse_len = int(impulse_duration * sample_rate)
impulse = np.random.normal(0, 1, impulse_len)  # white noise
impulse *= np.hanning(impulse_len)            # fade-in/out
impulse *= np.exp(-10 * np.linspace(0, 1, impulse_len))  # 빠른 감쇠

# [2] 저음 잔향 – 저주파 진동
rumble_t = t
rumble = 0.8 * np.sin(2 * np.pi * 60 * rumble_t) * np.exp(-3 * rumble_t)

# [3] 고음 금속 진동 – 짧은 여운 (선택)
metallic = 0.4 * np.sin(2 * np.pi * 800 * t) * np.exp(-8 * t)

# [4] 전체 합성
wave = np.zeros_like(t)
wave[:impulse_len] += impulse
wave += rumble
wave += metallic
wave *= volume

# 정규화 및 저장
sound_pcm = (wave / np.max(np.abs(wave)) * 32767).astype(np.int16)
filepath = os.path.join(output_dir, filename)
write(filepath, sample_rate, sound_pcm)
print(f"[✔] 폭발음 생성 완료!\n경로: {filepath}")
