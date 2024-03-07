import tkinter as tk
import random

def numbers(required_numbers, exclude_numbers):
    all_numbers = list(range(1, 46))
    
    # 반드시 포함해야 하는 숫자 추가
    for num in required_numbers:
        if num not in all_numbers:
            all_numbers.append(num)
    
    # 제외할 숫자 제거
    for num in exclude_numbers:
        if num in all_numbers:
            all_numbers.remove(num)
    
    return random.sample(all_numbers, 6)

def get_numbers():
    # 입력된 값 파싱
    required_input = required_entry.get()
    required_list = [int(num) for num in required_input.split()] if required_input else []
    exclude_input = exclude_entry.get()
    exclude_list = [int(num) for num in exclude_input.split()] if exclude_input else []
    
    # 추첨 및 결과 표시
    results.delete('1.0', tk.END)  # 기존 결과를 클리어
    for _ in range(5):
        happy = numbers(required_list, exclude_list)
        results.insert(tk.END, "출력된 번호: " + str(happy) + "\n")

# GUI 설정
root = tk.Tk()
root.title("로또 번호 생성기")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

required_label = tk.Label(frame, text="반드시 포함해야 하는 숫자 ex)10 20 30")
required_label.pack(side=tk.TOP)
required_entry = tk.Entry(frame, width=50)
required_entry.pack(side=tk.TOP)

exclude_label = tk.Label(frame, text="반드시 제외할 숫자 ex)11 22 33")
exclude_label.pack(side=tk.TOP)
exclude_entry = tk.Entry(frame, width=50)
exclude_entry.pack(side=tk.TOP)

generate_button = tk.Button(frame, text="번호 생성", command=get_numbers)
generate_button.pack(side=tk.TOP, pady=5)

results = tk.Text(frame, height=10, width=50)
results.pack(side=tk.TOP)

root.mainloop()
