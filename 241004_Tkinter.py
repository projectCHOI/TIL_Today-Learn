import tkinter as tk

# 덧셈 연산
result = 2 + 3

# Tkinter 초기화
root = tk.Tk()
root.title("덧셈 결과")
root.geometry("400x300")  # 창의 크기를 너비 400픽셀, 높이 300픽셀로 설정

# 레이블 생성
label = tk.Label(root, text=f"덧셈 결과는 {result}입니다.", font=("맑은 고딕", 16))

# 레이블 배치 (중앙에 위치하도록 설정)
label.place(relx=0.5, rely=0.5, anchor='center')

# 이벤트 루프 시작
root.mainloop()
