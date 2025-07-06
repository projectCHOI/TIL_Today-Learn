import numpy as np
from scipy.io.wavfile import write
import os

# 저장 경로 설정
download_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(download_dir, exist_ok=True)  # 폴더가 없으면 생성

# 사운드 설정
sample_rate = 44100  # 44.1kHz
duration = 2.0       # 2초
frequency = 440.0    # Hz (기본 A음)

# 기계음 파형 생성
def generate_mechanical_sound():
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    wave += 0.3 * np.sin(2 * np.pi * (frequency * 1.5) * t)
    wave += 0.2 * np.sin(2 * np.pi * (frequency * 2.0) * t)
    wave *= np.exp(-2 * t)  # 감쇠
    return (wave * 32767).astype(np.int16)  # 16-bit PCM 변환

# 사운드 생성
sound = generate_mechanical_sound()

# 파일 저장
filename = "mechanical_sound.wav" # 파일 이름
filepath = os.path.join(download_dir, filename)
write(filepath, sample_rate, sound)

print(f'{filename}'"사운드가 성공적으로 생성되었습니다!\n파일 경로: {filepath}")
