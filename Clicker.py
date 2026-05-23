from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import keyboard
import time
import threading
import random
import tkinter as tk

running = False
thread = None
mouse = MouseController()
kb = KeyboardController()

KEY_MAP = {
    'space': Key.space, 'enter': Key.enter, 'shift': Key.shift,
    'ctrl': Key.ctrl, 'alt': Key.alt, 'tab': Key.tab,
    'esc': Key.esc, 'up': Key.up, 'down': Key.down,
    'left': Key.left, 'right': Key.right,
}

def clicker_loop():
    while running:
        mode = click_mode.get()
        if mode == "left":
            mouse.click(Button.left)
        elif mode == "right":
            mouse.click(Button.right)
        elif mode == "double":
            mouse.click(Button.left, 2)
        elif mode == "key":
            k = key_entry.get().strip().lower()
            key = KEY_MAP.get(k, k)
            kb.press(key)
            time.sleep(0.05)
            kb.release(key)

        base = float(interval_var.get())
        delay = base / 1000.0
        if random_var.get():
            delay *= random.uniform(0.8, 1.2)
        time.sleep(max(delay, 0.01))

def toggle(event=None):
    global running, thread
    running = not running
    if running:
        btn.config(text="⏹ Стоп (F6)", bg="#e74c3c", fg="white")
        status_var.set("Работает...")
        thread = threading.Thread(target=clicker_loop, daemon=True)
        thread.start()
    else:
        btn.config(text="▶ Старт (F6)", bg="#2ecc71", fg="white")
        status_var.set("Остановлен")

root = tk.Tk()
root.title("AutoClicker")
root.geometry("300x320")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

tk.Label(root, text="🖱 Автокликер", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

frame1 = tk.Frame(root, bg="#f5f5f5")
frame1.pack(fill="x", padx=20)
tk.Label(frame1, text="Интервал (мс):", bg="#f5f5f5").pack(side="left")
interval_var = tk.StringVar(value="100")
tk.Entry(frame1, textvariable=interval_var, width=8).pack(side="right")

tk.Label(root, text="Тип действия:", bg="#f5f5f5").pack(anchor="w", padx=20, pady=(10,0))
click_mode = tk.StringVar(value="left")
for text, val in [("Левый клик","left"),("Правый клик","right"),("Двойной клик","double"),("Клавиша","key")]:
    tk.Radiobutton(root, text=text, variable=click_mode, value=val, bg="#f5f5f5").pack(anchor="w", padx=30)

frame2 = tk.Frame(root, bg="#f5f5f5")
frame2.pack(fill="x", padx=20, pady=4)
tk.Label(frame2, text="Клавиша:", bg="#f5f5f5").pack(side="left")
key_entry = tk.Entry(frame2, width=8)
key_entry.insert(0, "space")
key_entry.pack(side="right")

random_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Случайный интервал (±20%)", variable=random_var, bg="#f5f5f5").pack(anchor="w", padx=20)

btn = tk.Button(root, text="▶ Старт (F6)", font=("Arial", 12, "bold"),
                bg="#2ecc71", fg="white", relief="flat",
                padx=10, pady=6, command=toggle)
btn.pack(pady=10, padx=20, fill="x")

status_var = tk.StringVar(value="Остановлен")
tk.Label(root, textvariable=status_var, fg="#888", bg="#f5f5f5", font=("Arial", 9)).pack()
tk.Label(root, text="F6 — вкл/выкл", fg="#aaa", bg="#f5f5f5", font=("Arial", 8)).pack()

keyboard.add_hotkey('f6', toggle)
root.mainloop()