import tkinter as tk
from tkinter import messagebox
import random

def generate_numbers():
    # 입력값 가져오기
    required_input = entry_required.get()
    exclude_input = entry_exclude.get()

    # 포함할 숫자 처리
    if required_input.strip() == '':
        required_numbers = []
    else:
        try:
            required_numbers = [int(num) for num in required_input.strip().split()]
        except ValueError:
            messagebox.showerror("입력 오류", "포함할 숫자는 띄어쓰기로 구분된 숫자여야 합니다.")
            return

    # 제외할 숫자 처리
    if exclude_input.strip() == '':
        exclude_numbers = []
    else:
        try:
            exclude_numbers = [int(num) for num in exclude_input.strip().split()]
        except ValueError:
            messagebox.showerror("입력 오류", "제외할 숫자는 띄어쓰기로 구분된 숫자여야 합니다.")
            return

    # 유효성 검사
    if set(required_numbers) & set(exclude_numbers):
        messagebox.showerror("입력 오류", "포함할 숫자와 제외할 숫자가 겹칩니다.")
        return

    if not all(1 <= num <= 45 for num in required_numbers + exclude_numbers):
        messagebox.showerror("입력 오류", "숫자는 1부터 45 사이여야 합니다.")
        return

    if len(required_numbers) > 6:
        messagebox.showerror("입력 오류", "포함할 숫자는 최대 6개까지 가능합니다.")
        return

    # 결과 초기화
    text_result.delete('1.0', tk.END)

    # 5회 반복하여 번호 생성 및 출력
    for _ in range(5):
        # 사용 가능한 숫자 목록 생성
        available_numbers = set(range(1, 46)) - set(required_numbers) - set(exclude_numbers)
        available_numbers = sorted(available_numbers)

        # 필요한 숫자 개수 확인
        required_random_numbers = 6 - len(required_numbers)
        if len(available_numbers) < required_random_numbers:
            messagebox.showerror("오류", "사용 가능한 숫자가 부족합니다.")
            return

        # 랜덤 숫자 생성
        random_numbers = random.sample(available_numbers, required_random_numbers)

        # 최종 번호 조합
        final_numbers = required_numbers + random_numbers
        final_numbers.sort()

        # 결과 출력
        text_result.insert(tk.END, f"{final_numbers}\n")

# Tkinter 초기화
root = tk.Tk()
root.title("랜덤 번호 생성기")
root.geometry("500x500")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')

# 폰트 설정 (필요한 경우)
# import tkinter.font as tkFont
# font_default = tkFont.Font(family="서평원 꺾깎체", size=12)

# 포함할 숫자 입력 레이블 및 입력 필드
label_required = tk.Label(root, text="반드시 포함해야 하는 숫자 (띄어쓰기로 구분):")  # , font=font_default
label_required.pack(pady=(20, 5))
entry_required = tk.Entry(root, width=50)
entry_required.pack()

# 제외할 숫자 입력 레이블 및 입력 필드
label_exclude = tk.Label(root, text="반드시 제외해야 하는 숫자 (띄어쓰기로 구분):")  # , font=font_default
label_exclude.pack(pady=(10, 5))
entry_exclude = tk.Entry(root, width=50)
entry_exclude.pack()

# 번호 생성 버튼
button_generate = tk.Button(root, text="번호 생성", command=generate_numbers)  # , font=font_default
button_generate.pack(pady=20)

# 결과 표시 텍스트 박스
text_result = tk.Text(root, height=10, width=60)
text_result.pack()

# 이벤트 루프 시작
root.mainloop()
