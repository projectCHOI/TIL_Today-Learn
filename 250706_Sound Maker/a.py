import numpy as np
from scipy.io.wavfile import write
import os

# === 설정 ===
sample_rate = 44100
duration = 1.0
volume = 0.95
filename = "boom.wav"
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(output_dir, exist_ok=True)

# 시간 축
t = np.linspace(0, duration, int(sample_rate * duration), False)

# [1] 강한 백색소음 임펄스 (0~0.15초 사이)
impulse_duration = 0.15
impulse_len = int(sample_rate * impulse_duration)
impulse = np.random.normal(0, 1, impulse_len)
impulse *= np.hanning(impulse_len)
impulse *= np.exp(-12 * np.linspace(0, 1, impulse_len))

# [2] 묵직한 저주파 진동 (40~60Hz)
rumble = 1.2 * np.sin(2 * np.pi * 50 * t) * np.exp(-4 * t)

# [3] 저음 노이즈 (Low-pass white noise)
low_noise = np.random.normal(0, 0.6, t.shape[0])
low_noise = np.convolve(low_noise, np.ones(400)/400, mode='same')  # 저주파 필터
low_noise *= np.exp(-3 * t)

# [4] 클리핑 느낌 – 강한 순간 압력
clipped = 0.5 * np.sign(np.sin(2 * np.pi * 55 * t)) * np.exp(-6 * t)

# [5] 전체 합성
wave = np.zeros_like(t)
wave[:impulse_len] += impulse
wave += rumble
wave += low_noise
wave += clipped

# 정규화 및 저장
wave *= volume
sound_pcm = (wave / np.max(np.abs(wave)) * 32767).astype(np.int16)
filepath = os.path.join(output_dir, filename)
write(filepath, sample_rate, sound_pcm)
print(f"[✔] 묵직한 폭발음 '쾅!' 생성 완료!\n경로: {filepath}")

# =============
import numpy as np
from scipy.io.wavfile import write
import os

# === 설정 ===
sample_rate = 44100
duration = 1
filename = "explosion_sf.wav"
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(output_dir, exist_ok=True)

# 시간축
t = np.linspace(0, duration, int(sample_rate * duration), False)

# [1] 레이저 휘익 (고주파 스윕 + 감쇠)
sweep_freq = np.linspace(1000, 200, t.shape[0])
laser_sweep = np.sin(2 * np.pi * sweep_freq * t)
laser_sweep *= np.exp(-3 * t)

# [2] 디지털 임펄스 (짧은 백색노이즈)
impulse_duration = 0.05
impulse_len = int(sample_rate * impulse_duration)
impulse = np.random.normal(0, 1, impulse_len)
impulse *= np.hamming(impulse_len)
impulse *= 0.9

# [3] 저음 붐 (묵직한 사인파 + 클리핑 느낌)
bass = 1.2 * np.sin(2 * np.pi * 45 * t) * np.exp(-4 * t)
buzz = 0.4 * np.sign(np.sin(2 * np.pi * 60 * t)) * np.exp(-5 * t)

# [4] glitch 느낌을 주는 비선형 왜곡 톤
glitch = 0.3 * np.sin(2 * np.pi * (300 + 30*np.sin(2*np.pi*3*t)) * t)
glitch *= np.exp(-3 * t)

# [5] 전체 합성
wave = np.zeros_like(t)
wave[:impulse_len] += impulse
wave += laser_sweep
wave += bass
wave += buzz
wave += glitch

# 정규화 및 저장
wave /= np.max(np.abs(wave))  # normalize
wave_pcm = (wave * 32767).astype(np.int16)
filepath = os.path.join(output_dir, filename)
write(filepath, sample_rate, wave_pcm)
print(f"[✔] SF 스타일 폭발음 생성 완료!\n경로: {filepath}")
