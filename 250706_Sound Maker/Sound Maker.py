import numpy as np
from scipy.io.wavfile import write
import os
import tkinter as tk
from tkinter import messagebox
import pygame
import json

class MusicMaker:
    # --- 설정 상수 ---
    SAMPLE_RATE = 44100
    OUTPUT_DIR = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/TIL_Today-Learn/250706_Sound Maker/Download"
    
    FREQS = {
        "도": 261.63, "레": 293.66, "미": 329.63, "파": 349.23, 
        "솔": 392.00, "라": 440.00, "시": 493.88
    }
    
    Y_OFFSETS = {
        "-": 80, "": 24, "+": -32 # 옥타브별 기본 오프셋
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Python 8-Bit Music Maker")
        self.root.geometry("720x900")
        
        # 데이터 초기화
        self.selected_notes = []
        self.bpm = 120
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        
        # Pygame 초기화
        pygame.mixer.init()

        self._setup_ui()

    def _setup_ui(self):
        """GUI 구성요소 배치"""
        # 음표 버튼 프레임 (낮은음, 일반음, 높은음)
        for label, suffix in [("낮은 음", "-"), ("일반 음", ""), ("높은 음", "+")]:
            frame = tk.LabelFrame(self.root, text=label)
            frame.pack(fill="x", padx=10, pady=3)
            for note in ["도", "레", "미", "파", "솔", "라", "시"]:
                full_note = f"{note}{suffix}"
                btn = tk.Button(frame, text=full_note, width=6, 
                                command=lambda n=full_note: self.add_note(n))
                btn.pack(side="left", padx=2, pady=2)

        tk.Button(self.root, text="쉼표", width=6, command=lambda: self.add_note("쉼표")).pack(pady=5)

        # 오선지 캔버스
        self.canvas = tk.Canvas(self.root, width=690, height=440, bg="white")
        self.canvas.pack(padx=10, pady=5)
        self._draw_staff_lines()

        # 설정 프레임 (반복, 파일명)
        self._setup_settings_ui()

        # 컨트롤 버튼
        ctrl_frame = tk.Frame(self.root)
        ctrl_frame.pack(pady=15)
        buttons = [
            ("⏪ 초기화", self.reset_notes), ("❌ 삭제", self.delete_last_note),
            ("🎶 생성", self.generate_music), ("▶️ 재생", self.play_music),
            ("💾 저장", self.save_project), ("📂 불러오기", self.load_project)
        ]
        for txt, cmd in buttons:
            tk.Button(ctrl_frame, text=txt, command=cmd, width=10).pack(side="left", padx=5)

    def _setup_settings_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        
        tk.Label(frame, text="반복:").pack(side="left")
        self.repeat_var = tk.StringVar(value="1")
        tk.Entry(frame, width=4, textvariable=self.repeat_var).pack(side="left")
        
        tk.Label(frame, text=" 회  파일명:").pack(side="left")
        self.filename_var = tk.StringVar(value="my_music.wav")
        tk.Entry(frame, width=20, textvariable=self.filename_var).pack(side="left", padx=5)
        
        tk.Label(frame, text=" 음 길이:").pack(side="left")
        self.note_len_var = tk.StringVar(value="4분")
        tk.OptionMenu(frame, self.note_len_var, "2분", "4분", "8분").pack(side="left")

    def _draw_staff_lines(self):
        """오선지 기본선 그리기"""
        for row in range(5):
            y_base = row * 100 + 30
            for i in range(5):
                y = y_base + i * 20
                self.canvas.create_line(10, y, 680, y, fill="black")

    # --- 로직 메서드 ---
    def get_note_freq(self, note):
        if note == "쉼표": return 0
        base_name = note[0]
        freq = self.FREQS.get(base_name, 0)
        if "+" in note: return freq * 2
        if "-" in note: return freq * 0.5
        return freq

    def adsr_envelope(self, n):
        sr = self.SAMPLE_RATE
        a = min(int(0.01 * sr), int(n * 0.1))
        d = min(int(0.05 * sr), int(n * 0.2))
        r = min(int(0.05 * sr), int(n * 0.2))
        s_len = max(n - (a + d + r), 0)
        
        envelope = np.concatenate([
            np.linspace(0, 1, a),        # Attack
            np.linspace(1, 0.8, d),      # Decay
            np.full(s_len, 0.8),         # Sustain
            np.linspace(0.8, 0, r)       # Release
        ])
        return envelope[:n]

    def create_wave(self, freq, duration):
        n = int(self.SAMPLE_RATE * duration)
        if freq == 0: return np.zeros(n, dtype=np.float32)
        
        t = np.arange(n) / self.SAMPLE_RATE
        wave = 0.5 * np.sign(np.sin(2 * np.pi * freq * t))
        return (wave * self.adsr_envelope(n)).astype(np.float32)

    def update_staff(self):
        self.canvas.delete("note")
        for idx, note in enumerate(self.selected_notes):
            row, col = divmod(idx, 20)
            x = 30 + col * 30
            y_base = 30 + row * 100
            
            # 음표 그리기
            if note != "쉼표":
                # 상세 위치 계산 로직 개선
                suffix = note[-1] if note[-1] in ["+", "-"] else ""
                base_note = note[0]
                # 기존 딕셔너리 기반 y값 계산
                y_val = y_base + 70 + self._get_y_offset(note)
                self.canvas.create_oval(x-5, y_val-5, x+5, y_val+5, fill="black", tag="note")
            else:
                self.canvas.create_rectangle(x-4, y_base+66, x+4, y_base+74, outline="black", tag="note")
            
            self.canvas.create_text(x, y_base + 90, text=note, font=("맑은 고딕", 8), tag="note")

    def _get_y_offset(self, note):
        mapping = {
            "도": 40, "레": 30, "미": 20, "파": 10, "솔": 0, "라": -10, "시": -20
        }
        base = mapping.get(note[0], 0)
        if "+" in note: return base - 70 
        if "-" in note: return base + 70
        return base

    def add_note(self, note):
        self.selected_notes.append(note)
        self.update_staff()

    def generate_music(self):
        if not self.selected_notes: return
        
        dur_map = {"2분": 1.0, "4분": 0.5, "8분": 0.25}
        base_dur = dur_map.get(self.note_len_var.get(), 0.5)
        
        full_melody = []
        reps = int(self.repeat_var.get() if self.repeat_var.get().isdigit() else 1)
        
        for _ in range(reps):
            for note in self.selected_notes:
                wave = self.create_wave(self.get_note_freq(note), base_dur)
                full_melody.extend(wave)
                full_melody.extend(np.zeros(int(self.SAMPLE_RATE * 0.05))) # 휴지기
        
        filepath = os.path.join(self.OUTPUT_DIR, self.filename_var.get())
        out_data = (np.array(full_melody) * 32767).astype(np.int16)
        write(filepath, self.SAMPLE_RATE, out_data)
        messagebox.showinfo("완료", f"저장되었습니다: {filepath}")

    # --- 나머지 버튼 기능들 (삭제, 초기화 등) ---
    def delete_last_note(self):
        if self.selected_notes: self.selected_notes.pop(); self.update_staff()

    def reset_notes(self):
        self.selected_notes.clear(); self.update_staff()

    def play_music(self):
        path = os.path.join(self.OUTPUT_DIR, self.filename_var.get())
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

    def save_project(self):
        path = os.path.join(self.OUTPUT_DIR, "project.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"notes": self.selected_notes, "bpm": self.bpm}, f, ensure_ascii=False)
        messagebox.showinfo("완료", "프로젝트 저장 성공")

    def load_project(self):
        path = os.path.join(self.OUTPUT_DIR, "project.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.selected_notes = data.get("notes", [])
                self.update_staff()

#if __name__ == "__main__":
    root = tk.Tk()
    app = MusicMaker(root)
    root.mainloop()