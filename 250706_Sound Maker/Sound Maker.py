import numpy as np
from scipy.io.wavfile import write
import os

# === 설정 ===
sample_rate = 44100
note_duration = 0.3      # 각 음표 길이
pause_duration = 0.05    # 음 사이 무음 시간
volume = 0.5
filename = "custom_8bit_music.wav"
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(output_dir, exist_ok=True)

# === 음계 매핑 (한글 → 주파수) ===
note_freqs = {
    "도": 261.63,  # C4
    "레": 293.66,  # D4
    "미": 329.63,  # E4
    "파": 349.23,  # F4
    "솔": 392.00,  # G4
    "라": 440.00,  # A4
    "시": 493.88,  # B4
    "도+": 523.25,  # C5 (높은 도)
    "레+": 587.33,  # D5
    "미+": 659.25,  # E5
    "파+": 698.46,  # F5
    "솔+": 783.99,  # G5
    "라+": 880.00,  # A5
    "시+": 987.77,  # B5
    " ": 0          # 쉼표 처리
}

# === 사용자 입력 ===
user_input = input("음계를 입력하세요 (예: 도레미파솔라시도+): ")

# === 정사각파 생성 함수 ===
def square_wave(freq, duration, volume=1.0):
    if freq == 0:  # 쉼표 처리
        return np.zeros(int(sample_rate * duration))
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sign(np.sin(2 * np.pi * freq * t))
    return wave * volume

# === 입력 문자열 → 음 리스트로 변환
# 예: "도레미솔도" → ["도", "레", "미", "솔", "도"]
# 높은음 구분 위해 "도+", "레+"도 인식
i = 0
notes = []
while i < len(user_input):
    if i + 1 < len(user_input) and user_input[i+1] == "+":
        notes.append(user_input[i] + "+")
        i += 2
    else:
        notes.append(user_input[i])
        i += 1

# === 파형 생성
melody = []
for note in notes:
    freq = note_freqs.get(note, 0)
    tone = square_wave(freq, note_duration, volume)
    pause = np.zeros(int(sample_rate * pause_duration))
    melody.extend(tone)
    melody.extend(pause)

# === 저장
sound_pcm = (np.array(melody) * 32767).astype(np.int16)
filepath = os.path.join(output_dir, filename)
write(filepath, sample_rate, sound_pcm)

print(f"[✔] '{filename}' 생성 완료!\n입력 음계: {notes}\n파일 경로: {filepath}")
