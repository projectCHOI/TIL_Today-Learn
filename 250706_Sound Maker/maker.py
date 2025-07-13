import numpy as np
from scipy.io.wavfile import write
import os
import tkinter as tk
from tkinter import messagebox
import pygame

# === 사운드 설정 ===
sample_rate = 44100
note_duration = 0.3
pause_duration = 0.05
volume = 0.5
filename = "click_composed.wav"
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
filepath = os.path.join(output_dir, filename)
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

# === 정사각파 생성 함수 ===
def square_wave(freq, duration, volume=1.0):
    if freq == 0:
        return np.zeros(int(sample_rate * duration))
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sign(np.sin(2 * np.pi * freq * t))
    return wave * volume

# === 음계 해석 함수 (+ / - 처리 포함) ===
def get_note_freq(note):
    if note == "공백":
        return 0
    base = note_base_freqs.get(note[0], 0)
    if note.endswith("+"):
        return base * 2
    elif note.endswith("-"):
        return base * 0.5
    else:
        return base

# === 선택된 음 리스트 ===
selected_notes = []

# === pygame 초기화 (재생용) ===
pygame.init()
pygame.mixer.init()

# === GUI 업데이트: 오선지에 선택된 음 표시 ===
def update_staff():
    staff_canvas.delete("note")
    # staff lines are static
    for idx, note in enumerate(selected_notes):
        x = 20 + idx * 30
        y = 60
        staff_canvas.create_text(x, y, text=note, tag="note", font=("맑은 고딕", 12))

# === 노트 추가/초기화 함수 ===
def add_note(note):
    selected_notes.append(note)
    update_staff()

def reset_notes():
    selected_notes.clear()
    update_staff()
    repeat_var.set(1)

# === 음악 생성 함수 ===
def generate_music():
    pygame.mixer.music.stop()
    # 반복 횟수
    try:
        reps = int(repeat_var.get())
        if reps < 1:
            reps = 1
    except ValueError:
        reps = 1
    sequence = selected_notes * reps

    melody = []
    for note in sequence:
        freq = get_note_freq(note)
        tone = square_wave(freq, note_duration, volume)
        pause = np.zeros(int(sample_rate * pause_duration))
        melody.extend(tone)
        melody.extend(pause)

    # PCM 변환 및 저장
    sound_pcm = (np.array(melody) * 32767).astype(np.int16)
    write(filepath, sample_rate, sound_pcm)
    messagebox.showinfo("완료", f"음악 생성 완료: {filepath}")

# === 음악 재생 함수 ===
def play_music():
    if not os.path.exists(filepath):
        messagebox.showwarning("재생 오류", "먼저 음악을 생성하세요.")
        return
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

# === tkinter GUI ===
root = tk.Tk()
root.title("마우스 클릭 8비트 작곡기")
root.geometry("700x400")

# 낮은 음 버튼 프레임
frame_low = tk.LabelFrame(root, text="낮은 음")
frame_low.pack(fill="x", padx=10, pady=5)
for note in ["도-", "레-", "미-", "파-", "솔-", "라-", "시-"]:
    btn = tk.Button(frame_low, text=note, width=6,
                    command=lambda n=note: add_note(n))
    btn.pack(side="left", padx=2, pady=2)

# 일반 음 버튼 프레임
frame_mid = tk.LabelFrame(root, text="일반 음")
frame_mid.pack(fill="x", padx=10, pady=5)
for note in ["도", "레", "미", "파", "솔", "라", "시"]:
    btn = tk.Button(frame_mid, text=note, width=6,
                    command=lambda n=note: add_note(n))
    btn.pack(side="left", padx=2, pady=2)

# 높은 음 버튼 프레임
frame_high = tk.LabelFrame(root, text="높은 음")
frame_high.pack(fill="x", padx=10, pady=5)
for note in ["도+", "레+", "미+", "파+", "솔+", "라+", "시+"]:
    btn = tk.Button(frame_high, text=note, width=6,
                    command=lambda n=note: add_note(n))
    btn.pack(side="left", padx=2, pady=2)

# 공백 버튼
btn_blank = tk.Button(root, text="공백", width=6,
                      command=lambda: add_note("공백"))
btn_blank.pack(pady=5)

# 오선지 Canvas
staff_canvas = tk.Canvas(root, width=680, height=120, bg="white")
staff_canvas.pack(padx=10, pady=5)
# 그리기: 5개의 오선
for i in range(5):
    y = 30 + i * 20
    staff_canvas.create_line(10, y, 670, y)

# 반복 횟수 입력
frame_repeat = tk.Frame(root)
frame_repeat.pack(pady=5)
tk.Label(frame_repeat, text="반복:").pack(side="left")
repeat_var = tk.StringVar(value="1")
ent_repeat = tk.Entry(frame_repeat, width=4, textvariable=repeat_var)
ent_repeat.pack(side="left")
tk.Label(frame_repeat, text="회").pack(side="left")

# 제어 버튼 프레임
frame_ctrl = tk.Frame(root)
frame_ctrl.pack(pady=15)
btn_reset = tk.Button(frame_ctrl, text="⏪ 초기화", command=reset_notes, width=10)
btn_reset.pack(side="left", padx=10)
btn_gen = tk.Button(frame_ctrl, text="🎶 생성", command=generate_music, width=10)
btn_gen.pack(side="left", padx=10)
btn_play = tk.Button(frame_ctrl, text="▶️ 재생", command=play_music, width=10)
btn_play.pack(side="left", padx=10)

root.mainloop()
