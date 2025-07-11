import numpy as np
from scipy.io.wavfile import write
import os
import tkinter as tk
from tkinter import messagebox

# === 사운드 설정 ===
sample_rate = 44100
note_duration = 0.3
pause_duration = 0.05
volume = 0.5
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(output_dir, exist_ok=True)

# === 음계 주파수 (C4 기준) ===
note_base_freqs = {
    "도": 261.63,
    "레": 293.66,
    "미": 329.63,
    "파": 349.23,
    "솔": 392.00,
    "라": 440.00,
    "시": 493.88
}

# === 정사각파 생성 ===
def square_wave(freq, duration, volume=1.0):
    if freq == 0:
        return np.zeros(int(sample_rate * duration))
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sign(np.sin(2 * np.pi * freq * t))
    return wave * volume

# === 음계 해석 함수 ===
def get_note_freq(note):
    if note == " ":
        return 0
    base = note_base_freqs.get(note[0], 0)
    if note.endswith("+"):
        return base * 2
    elif note.endswith("-"):
        return base * 0.5
    else:
        return base

# === GUI 동작 ===
def generate_music():
    user_input = entry.get()
    notes = []
    i = 0
    while i < len(user_input):
        ch = user_input[i]
        if ch == " ":
            notes.append(" ")
            i += 1
        elif ch in note_base_freqs:
            if i + 1 < len(user_input) and user_input[i+1] in "+-":
                notes.append(ch + user_input[i+1])
                i += 2
            else:
                notes.append(ch)
                i += 1
        else:
            i += 1

    # 파형 생성
    melody = []
    for note in notes:
        freq = get_note_freq(note)
        tone = square_wave(freq, note_duration, volume)
        pause = np.zeros(int(sample_rate * pause_duration))
        melody.extend(tone)
        melody.extend(pause)

    # 저장
    filename = "gui_custom_music.wav"
    filepath = os.path.join(output_dir, filename)
    sound_pcm = (np.array(melody) * 32767).astype(np.int16)
    write(filepath, sample_rate, sound_pcm)

    messagebox.showinfo("완료", f"'{filename}' 생성 완료!\n{filepath}")

# === tkinter GUI ===
root = tk.Tk()
root.title("8비트 음악 생성기")
root.geometry("400x140")

label = tk.Label(root, text="음계를 입력하세요 (예: 도미솔도+ 라+시도)", font=("맑은 고딕", 11))
label.pack(pady=10)

entry = tk.Entry(root, width=40, font=("맑은 고딕", 12))
entry.pack()

button = tk.Button(root, text="🎵 음악 생성", command=generate_music, font=("맑은 고딕", 12))
button.pack(pady=10)

root.mainloop()
