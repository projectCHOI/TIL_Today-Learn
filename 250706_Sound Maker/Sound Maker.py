import numpy as np
from scipy.io.wavfile import write
import os

# === 사용자 설정 ===
duration     = 0.5       # 전체 소리 길이 (초)
start_freq   = 1200.0    # 시작 주파수           ========= 클수록 날카롭고 높은 소리
end_freq     = 800.0     # 끝 주파수             ========= 시작보다 낮게 설정하면 점점 낮아지는 느낌
volume       = 0.5       # 전체 음량 (0 ~ 1)
decay_factor = 3         # 감쇠 강도 (볼륨 줄어드는 속도) == 숫자가 클수록 소리가 빨리 줄어든다.
vibrate_rate = 0        # 진동 추가 주파수 (Hz) ========== 기계적인 "위이잉" 느낌 클수록 강함
noise_level  = 0      # 기계적 노이즈 정도 ============= 약간의 노이즈(지직지직한 잡음) 0.05는 가벼운 잡음 포함
filename     = "ding_sound.wav"
# ====================

# 저장 경로
download_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(download_dir, exist_ok=True)

sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration), False)

# 주파수를 선형으로 변화 (고주파 → 저주파)
freqs = np.linspace(start_freq, end_freq, t.shape[0])
base_wave = np.sin(2 * np.pi * freqs * t)

# 떨림 효과 (고주파 떨림 추가)
vibrate = np.sin(2 * np.pi * vibrate_rate * t) * 0.2
combined = base_wave + vibrate

# 감쇠 곡선 적용
combined *= np.exp(-decay_factor * t)

# 노이즈 추가
noise = np.random.normal(0, noise_level, t.shape[0])
combined += noise

# 음량 조정 및 PCM 변환
sound_pcm = (combined * volume * 32767).astype(np.int16)

# 저장
filepath = os.path.join(download_dir, filename)
write(filepath, sample_rate, sound_pcm)

print(f'{filename}'"사운드가 성공적으로 생성되었습니다!\n파일 경로: {filepath}")
