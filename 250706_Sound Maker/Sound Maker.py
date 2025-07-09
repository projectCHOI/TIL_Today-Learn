import numpy as np
from scipy.io.wavfile import write
import os

# === 설정 ===
sample_rate = 44100
note_duration = 0.3  # 각 음표 길이
volume = 0.5
filename = "scale_8bit.wav"
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(output_dir, exist_ok=True)

# 음계: 도레미파솔라시도 (C4~C5)
notes = [
    261.63,  # 도
    293.66,  # 레
    329.63,  # 미
    349.23,  # 파
    392.00,  # 솔
    440.00,  # 라
    493.88,  # 시
    523.25   # 도 (높은 도)
]

# 정사각파 생성 함수 (8비트 스타일)
def square_wave(freq, duration, volume=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sign(np.sin(2 * np.pi * freq * t))  # 사각파
    return wave * volume

# 전체 멜로디 생성
melody = np.concatenate([square_wave(f, note_duration, volume) for f in notes])
sound_pcm = (melody * 32767).astype(np.int16)

# 저장
filepath = os.path.join(output_dir, filename)
write(filepath, sample_rate, sound_pcm)

print(f"8비트 사운드 생성 완료!\n경로: {filepath}")
