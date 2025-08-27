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
output_dir = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
os.makedirs(output_dir, exist_ok=True)

# === 박자/BPM 설정 ===
BPM = 120
beat_per_sec = BPM / 60.0
quarter_sec = 1.0 / beat_per_sec  # 4분음표 길이(초)

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

def adsr_envelope(total_samples, sr, A=0.005, D=0.03, S=0.8, R=0.02):
    a = int(A * sr); d = int(D * sr); r = int(R * sr)
    s = max(total_samples - (a + d + r), 0)
    env = np.zeros(total_samples, dtype=np.float32)
    # Attack
    if a > 0:
        env[:a] = np.linspace(0.0, 1.0, a, endpoint=False)
    # Decay
    if d > 0:
        env[a:a+d] = np.linspace(1.0, S, d, endpoint=False)
    # Sustain
    if s > 0:
        env[a+d:a+d+s] = S
    # Release
    if r > 0:
        env[a+d+s:a+d+s+r] = np.linspace(S, 0.0, r, endpoint=False)
    if a + d + s + r < total_samples:
        env[a+d+s+r:] = 0.0
    return env

def get_note_seconds(note_length_label: str):
    # "2분", "4분", "8분" 중 선택된 라벨을 초 단위 길이로 변환
    if note_length_label == "2분":
        return quarter_sec * 2.0
    elif note_length_label == "8분":
        return quarter_sec * 0.5
    else:
        return quarter_sec  # 기본: 4분음표
    
def square_wave(freq, duration, volume=1.0):
    n = int(sample_rate * duration)
    if n <= 0:
        return np.array([], dtype=np.float32)
    if freq == 0:
        return np.zeros(n, dtype=np.float32)

    t = np.arange(n) / sample_rate

    # 기본 정사각파
    wave = 0.5 * np.sign(np.sin(2 * np.pi * freq * t)).astype(np.float32)

    # ADSR 적용
    env = adsr_envelope(n, sample_rate, A=0.005, D=0.03, S=0.8, R=0.02)
    wave *= env

    # 미세 페이드(경계 클릭 더 줄이기, 2ms)
    fade = int(0.002 * sample_rate)
    if fade > 1 and fade*2 < n:
        wave[:fade] *= np.linspace(0, 1, fade, endpoint=False).astype(np.float32)
        wave[-fade:] *= np.linspace(1, 0, fade, endpoint=False).astype(np.float32)

    return wave * float(volume)

# === 음계 해석 함수 (+ / - 처리 포함) ===
def get_note_freq(note):
    if note == "쉼표":
        return 0
    base = note_base_freqs.get(note[0], 0)
    if note.endswith("+"):
        return base * 2
    elif note.endswith("-"):
        return base * 0.5
    else:
        return base

# 미리듣기(짧게 0.15초)
_preview_sound = None

def preview_tone(freq, dur=0.15, vol=0.6):
    global _preview_sound
    try:
        if freq <= 0:
            return
        snd = square_wave(freq, dur, vol)
        snd_pcm = (snd * 32767).astype(np.int16)

        import pygame.sndarray
        _preview_sound = pygame.sndarray.make_sound(snd_pcm)
        _preview_sound.play()
    except Exception:
        pass

# === 선택된 음 리스트 ===
selected_notes = []

# === pygame 초기화 (재생용) ===
pygame.init()
pygame.mixer.init()

# === GUI 업데이트: 오선지에 선택된 음 표시 ===
def update_staff():
    staff_canvas.delete("note")
    max_per_row = 20
    for idx, note in enumerate(selected_notes):
        row = idx // max_per_row
        col = idx % max_per_row
        x = 30 + col * 30
        y = 30 + row * 100
        staff_canvas.create_text(x, y + 40, text=note, tag="note", font=("맑은 고딕", 12))

# === 노트 추가/초기화/삭제 함수 ===
def add_note(note):
    selected_notes.append(note)
    update_staff()

def reset_notes():
    selected_notes.clear()
    update_staff()
    repeat_var.set(1)
    filename_var.set("click_composed.wav")

def delete_last_note():
    if selected_notes:
        selected_notes.pop()
        update_staff()

# === 음악 생성 함수 ===
def generate_music():
    if not selected_notes:
        messagebox.showwarning("생성 오류", "먼저 음을 하나 이상 추가하세요.")
        return
    pygame.mixer.music.stop()
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
        dur = get_note_seconds(note_len_var.get())  # 추가: 선택한 음 길이(초)
        tone = square_wave(freq, dur, volume)
        pause = np.zeros(int(sample_rate * pause_duration))
        melody.extend(tone)
        melody.extend(pause)

    filename = filename_var.get().strip()
    if not filename.endswith(".wav"):
        filename += ".wav"
    filepath = os.path.join(output_dir, filename)

    sound_pcm = (np.array(melody) * 32767).astype(np.int16)
    write(filepath, sample_rate, sound_pcm)
    messagebox.showinfo("완료", f"음악 생성 완료: {filepath}")

# === 음악 재생 함수 ===
def play_music():
    filename = filename_var.get().strip()
    if not filename.endswith(".wav"):
        filename += ".wav"
    filepath = os.path.join(output_dir, filename)
    if not os.path.exists(filepath):
        messagebox.showwarning("재생 오류", "먼저 음악을 생성하세요.")
        return
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

# === tkinter GUI ===
root = tk.Tk()
root.title("마우스 클릭 8비트 작곡기")
root.geometry("720x900")

frame_low = tk.LabelFrame(root, text="낮은 음")
frame_low.pack(fill="x", padx=10, pady=3)
for note in ["도-", "레-", "미-", "파-", "솔-", "라-", "시-"]:
    btn = tk.Button(frame_low, text=note, width=6, command=lambda n=note: add_note(n))
    btn.pack(side="left", padx=2, pady=2)

frame_mid = tk.LabelFrame(root, text="일반 음")
frame_mid.pack(fill="x", padx=10, pady=3)
for note in ["도", "레", "미", "파", "솔", "라", "시"]:
    btn = tk.Button(frame_mid, text=note, width=6, command=lambda n=note: add_note(n))
    btn.pack(side="left", padx=2, pady=2)

frame_high = tk.LabelFrame(root, text="높은 음")
frame_high.pack(fill="x", padx=10, pady=3)
for note in ["도+", "레+", "미+", "파+", "솔+", "라+", "시+"]:
    btn = tk.Button(frame_high, text=note, width=6, command=lambda n=note: add_note(n))
    btn.pack(side="left", padx=2, pady=2)

btn_blank = tk.Button(root, text="쉼표", width=6, command=lambda: add_note("쉼표"))
btn_blank.pack(pady=5)

staff_canvas = tk.Canvas(root, width=690, height=540, bg="white")
staff_canvas.pack(padx=10, pady=5)

for row in range(5):
    y_offset = row * 100
    for i in range(5):
        y = 30 + i * 20 + y_offset
        staff_canvas.create_line(10, y, 680, y, fill="black")
    staff_canvas.create_text(10, 30 + y_offset, text=chr(97 + row), anchor="e", font=("맑은 고딕", 12), fill="green")

for i in range(1, 6):
    x = 30 * i * 4
    staff_canvas.create_line(x, 20, x, 520, fill="orange")
    staff_canvas.create_text(x - 5, 20, text=str(i), fill="orange", font=("맑은 고딕", 10))

frame_repeat = tk.Frame(root)
frame_repeat.pack(pady=5)
tk.Label(frame_repeat, text="반복:").pack(side="left")
repeat_var = tk.StringVar(value="1")
ent_repeat = tk.Entry(frame_repeat, width=4, textvariable=repeat_var)
ent_repeat.pack(side="left")
tk.Label(frame_repeat, text="회").pack(side="left")

# 파일 이름 입력창
tk.Label(frame_repeat, text="  파일명:").pack(side="left")
filename_var = tk.StringVar(value="click_composed.wav")
entry_filename = tk.Entry(frame_repeat, width=20, textvariable=filename_var)
entry_filename.pack(side="left", padx=5)

# 음 길이 선택
frame_len = tk.Frame(root)
frame_len.pack(pady=5)

tk.Label(frame_len, text="음 길이:").pack(side="left")

note_len_var = tk.StringVar(value="4분")  # 기본값
opt_len = tk.OptionMenu(frame_len, note_len_var, "2분", "4분", "8분")
opt_len.pack(side="left", padx=6)

frame_ctrl = tk.Frame(root)
frame_ctrl.pack(pady=15)
btn_reset = tk.Button(frame_ctrl, text="⏪ 초기화", command=reset_notes, width=10)
btn_reset.pack(side="left", padx=10)
btn_delete = tk.Button(frame_ctrl, text="❌ 삭제", command=delete_last_note, width=10)
btn_delete.pack(side="left", padx=10)
btn_gen = tk.Button(frame_ctrl, text="🎶 생성", command=generate_music, width=10)
btn_gen.pack(side="left", padx=10)
btn_play = tk.Button(frame_ctrl, text="▶️ 재생", command=play_music, width=10)
btn_play.pack(side="left", padx=10)

root.mainloop()
