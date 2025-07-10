import numpy as np
from scipy.io.wavfile import write
import os

# === 설정 ===
sample_rate = 44100
note_duration = 0.3
pause_duration = 0.05
volume = 0.5
filename = "custom_8bit_music_with_low_high.wav"
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(output_dir, exist_ok=True)

# === 기본 음계 주파수 (C4 기준)
note_base_freqs = {
    "도": 261.63,
    "레": 293.66,
    "미": 329.63,
    "파": 349.23,
    "솔": 392.00,
    "라": 440.00,
    "시": 493.88
}

# === 정사각파 생성 함수
def square_wave(freq, duration, volume=1.0):
    if freq == 0:
        return np.zeros(int(sample_rate * duration))
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sign(np.sin(2 * np.pi * freq * t))
    return wave * volume

# === 사용자 입력
user_input = input("음계를 입력하세요 (예: 도레미파솔라시도+ 도-시-): ")

# === 입력 해석 (도, 도+, 도-, etc.)
notes = []
i = 0
while i < len(user_input):
    char = user_input[i]
    if char == " ":
        notes.append(" ")  # 쉼표
        i += 1
    elif char in note_base_freqs:
        if i + 1 < len(user_input) and user_input[i+1] == "+":
            notes.append(char + "+")
            i += 2
        elif i + 1 < len(user_input) and user_input[i+1] == "-":
            notes.append(char + "-")
            i += 2
        else:
            notes.append(char)
            i += 1
    else:
        i += 1  # 무시

# === 음계 조합 → 주파수 리스트
def get_note_freq(note):
    if note == " ":
        return 0
    base = note_base_freqs.get(note[0], 0)
    if note.endswith("+"):
        return base * 2.0       # 1옥타브 위
    elif note.endswith("-"):
        return base * 0.5       # 1옥타브 아래
    else:
        return base

# === 파형 생성
melody = []
for note in notes:
    freq = get_note_freq(note)
    tone = square_wave(freq, note_duration, volume)
    pause = np.zeros(int(sample_rate * pause_duration))
    melody.extend(tone)
    melody.extend(pause)

# === 저장
sound_pcm = (np.array(melody) * 32767).astype(np.int16)
filepath = os.path.join(output_dir, filename)
write(filepath, sample_rate, sound_pcm)

print(f"음악 생성 완료!\n입력: {notes}\n파일: {filepath}")
