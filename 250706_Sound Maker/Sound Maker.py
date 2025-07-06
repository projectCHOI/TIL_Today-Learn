import numpy as np
from scipy.io.wavfile import write
import os

# 저장 경로 설정
download_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(download_dir, exist_ok=True)

# 사운드 설정
sample_rate = 44100  # 44.1kHz
duration = 1.0       # 2초

# "삐" 소리: 고정된 고주파 (예: 1000Hz, 0.3초)
def beep_part(duration=0.3, freq=1000.0):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    return wave

# "용" 소리: 점점 낮아지는 주파수 (sweeping from high to low)
def yong_part(duration=0.7, start_freq=1000.0, end_freq=300.0):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    freqs = np.linspace(start_freq, end_freq, t.shape[0])
    wave = 0.5 * np.sin(2 * np.pi * freqs * t)
    return wave * np.exp(-2 * t)  # 자연스럽게 줄어들게 감쇠

# 합치기
beep = beep_part()
yong = yong_part()
full_sound = np.concatenate((beep, yong))
sound_pcm = (full_sound * 32767).astype(np.int16)

# 파일 저장
filename = "Attack_sound.wav" # 파일 이름
filepath = os.path.join(download_dir, filename)
write(filepath, sample_rate, sound_pcm)

print(f'{filename}'"사운드가 성공적으로 생성되었습니다!\n파일 경로: {filepath}")
