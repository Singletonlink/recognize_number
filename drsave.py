# draw_and_recognize.py
import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np
import joblib
import os


model = joblib.load("digits_model.joblib")
window = tk.Tk()
window.title("Распознавание цифр")
window.geometry("320x450")
current_color="black"

def set_color_black():
    global current_color
    current_color="black"

def set_color_red():
    global current_color
    current_color="red"

def set_color_skyblue():
    global current_color
    current_color="skyblue"


canvas = tk.Canvas(window, width=720, height=590, bg="white", cursor="cross")
canvas.pack(pady=20)

def draw(event):
    x, y = event.x, event.y
    canvas.create_oval(x-6, y-6, x+6, y+6, fill=current_color, outline=current_color)
canvas.bind("<B1-Motion>", draw)

def clear_canvas():
    canvas.delete("all")
    result_label.config(text="Нарисуй цифру и нажми 'Распознать'")

def recognize_digit():
    x = window.winfo_rootx() + canvas.winfo_x()
    y = window.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    img = ImageGrab.grab((x, y, x1, y1)).convert("L")

   
    img = img.resize((8, 8), Image.Resampling.LANCZOS)
    img_array = np.array(img)
    img_array = 255 - img_array  # инвертируем цвета
    img_array = (img_array / 255.0) * 16.0
    flat = img_array.reshape(1, -1)

    pred = model.predict(flat)
    result_label.config(text=f"Это цифра: {pred[0]}")


def save_drawing():

    os.makedirs("saved_digits", exist_ok=True)

    # Сохраняем изображение области холста
    x = window.winfo_rootx() + canvas.winfo_x()
    y = window.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    img = ImageGrab.grab((x, y, x1, y1)).convert("L")

    # Считаем, сколько уже сохранено
    count = len(os.listdir("saved_digits"))
    filename = f"saved_digits/digit_{count + 1}.png"

    img.save(filename)
    result_label.config(text=f"Сохранено как: {filename}")

# Кнопки
btn_frame = tk.Frame(window)
btn_frame.pack()

tk.Button(btn_frame, text="Очистить", command=clear_canvas).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Распознать", command=recognize_digit).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Сохранить", command=save_drawing).pack(side=tk.LEFT, padx=5)

color_frame = tk.Frame(window)
color_frame.pack(pady=10)

tk.Button(color_frame, text="Черный", command=set_color_black, fg="black").pack(side=tk.LEFT, padx=5)
tk.Button(color_frame, text="Красный", command=set_color_red, fg="red").pack(side=tk.LEFT, padx=5)
tk.Button(color_frame, text="Голубой", command=set_color_skyblue, fg="skyblue").pack(side=tk.LEFT, padx=5)


# Текст результата
result_label = tk.Label(window, text="Нарисуй цифру и нажми 'Распознать'", font=("Arial", 12))
result_label.pack(pady=20)

window.mainloop()