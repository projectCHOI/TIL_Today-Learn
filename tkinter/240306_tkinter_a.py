import tkinter as tk

def on_button_click():
    label.config(text="Hello, " + entry.get())

root = tk.Tk()
root.title("My Python App")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

entry = tk.Entry(frame, width=25)
entry.pack(side=tk.LEFT)

button = tk.Button(frame, text="Greet", command=on_button_click)
button.pack(side=tk.LEFT, padx=5)

label = tk.Label(frame, text="")
label.pack(side=tk.LEFT)

root.mainloop()
