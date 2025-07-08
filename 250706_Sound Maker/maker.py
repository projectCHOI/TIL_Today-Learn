import numpy as np
from scipy.io.wavfile import write
import os

# === 설정 ===
sample_rate = 44100
duration = 10.0  # 10초
volume = 0.6
filename = "game_over.wav"
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(output_dir, exist_ok=True)

# 시간 축
t = np.linspace(0, duration, int(sample_rate * duration), False)

# 주파수 변화 (낮고 무거운 톤)
base_freq = np.linspace(200, 80, t.shape[0])  # 점점 낮아지는 주파수

# 떨림 효과 (느리고 깊게 흔들리는 느낌)
vibrate = 0.4 * np.sin(2 * np.pi * 3 * t)  # 3Hz 느린 진동

# 랜덤한 불안정성 (불규칙 주파수 변화)
unstable = 0.2 * np.sin(2 * np.pi * (base_freq + np.random.uniform(-10, 10, t.shape[0])) * t)

# 배경 노이즈 추가 (심리적 불안정)
noise = 0.05 * np.random.normal(0, 1, t.shape[0])

# 전체 파형 합성
wave = np.sin(2 * np.pi * base_freq * t) + vibrate + unstable + noise
wave *= np.exp(-0.3 * t)  # 천천히 사라지는 느낌
wave *= volume

# PCM 변환
sound_pcm = (wave * 32767).astype(np.int16)
filepath = os.path.join(output_dir, filename)
write(filepath, sample_rate, sound_pcm)

print(f"사운드 생성 완료!\n파일 경로: {filepath}")
