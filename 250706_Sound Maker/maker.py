import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.io.wavfile import write
import pygame
import os

# 설정
sample_rate = 44100
note_duration = 0.3
pause_duration = 0.05
volume = 0.5
filename = "click_composed.wav"
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
filepath = os.path.join(output_dir, filename)
os.makedirs(output_dir, exist_ok=True)

# 음계 주파수
note_base_freqs = {
    "도": 261.63,
    "레": 293.66,
    "미": 329.63,
    "파": 349.23,
    "솔": 392.00,
    "라": 440.00,
    "시": 493.88,
    "도+": 523.25,
    "레+": 587.33,
    "미+": 659.25,
}

# 정사각파
def square_wave(freq, duration, volume=1.0):
    if freq == 0: return np.zeros(int(sample_rate * duration))
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sign(np.sin(2 * np.pi * freq * t))
    return wave * volume

# 선택된 음 리스트
selected_notes = []

# GUI 기능
def add_note(note):
    selected_notes.append(note)
    label_notes.config(text="선택된 음: " + " ".join(selected_notes))

def reset_notes():
    selected_notes.clear()
    label_notes.config(text="선택된 음:")

def generate_music():
    pygame.mixer.music.stop()
    melody = []
    for note in selected_notes:
        freq = note_base_freqs.get(note, 0)
        tone = square_wave(freq, note_duration, volume)
        pause = np.zeros(int(sample_rate * pause_duration))
        melody.extend(tone)
        melody.extend(pause)
    sound_pcm = (np.array(melody) * 32767).astype(np.int16)
    write(filepath, sample_rate, sound_pcm)
    messagebox.showinfo("완료", f"음악 생성 완료: {filepath}")

def play_music():
    if not os.path.exists(filepath):
        messagebox.showwarning("재생 오류", "먼저 음악을 생성하세요.")
        return
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

# Pygame 초기화
pygame.init()
pygame.mixer.init()

# tkinter GUI
root = tk.Tk()
root.title("🎹 마우스 클릭 8비트 작곡기")
root.geometry("500x280")

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

for note in ["도", "레", "미", "파", "솔", "라", "시", "도+", "레+", "미+"]:
    btn = tk.Button(frame_buttons, text=note, width=6, font=("맑은 고딕", 11), command=lambda n=note: add_note(n))
    btn.pack(side="left", padx=3)

label_notes = tk.Label(root, text="선택된 음:", font=("맑은 고딕", 12))
label_notes.pack(pady=10)

frame_ctrl = tk.Frame(root)
frame_ctrl.pack(pady=10)

tk.Button(frame_ctrl, text="⏪ 초기화", command=reset_notes, width=10, font=("맑은 고딕", 11)).pack(side="left", padx=5)
tk.Button(frame_ctrl, text="🎶 생성", command=generate_music, width=10, font=("맑은 고딕", 11)).pack(side="left", padx=5)
tk.Button(frame_ctrl, text="▶️ 재생", command=play_music, width=10, font=("맑은 고딕", 11)).pack(side="left", padx=5)

root.mainloop()
