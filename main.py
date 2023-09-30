import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
import time
import subprocess
import os
import json_to_csv
import find_def
# Директории
DIR_CURRENT=current_directory = os.getcwd()
DIR_IMAGE = DIR_CURRENT+'\_IMAGE'
DIR_TO_BROKEN = DIR_CURRENT+'\_BROKEN'
DIR_TO_EMPTY = DIR_CURRENT+'\_EMPTY'
DIR_TO_ANIMAL = DIR_CURRENT+'\_ANIMAL'




# вызов кнопок
def button1():
    global DIR_IMAGE
    d = filedialog.askdirectory()
    if d:  # если выбрали дирректорию, то поменяем переменную
        DIR_IMAGE = d
        dir1.config(text=f'Исходные фото: {DIR_IMAGE}')


def button2():
    global DIR_TO_BROKEN
    d = filedialog.askdirectory()
    if d:  # если выбрали дирректорию, то поменяем переменную
        DIR_TO_GOOD = d
        dir2.config(text=f'Хорошие фото: {DIR_TO_BROKEN}')


def button3():
    global DIR_TO_EMPTY
    d = filedialog.askdirectory()
    if d:  # если выбрали дирректорию, то поменяем переменную
        DIR_TO_BAD = d
        dir3.config(text=f'Плохие фото: {DIR_TO_EMPTY}')


def button3_1():
    global DIR_TO_ANIMAL
    d = filedialog.askdirectory()
    if d:  # если выбрали дирректорию, то поменяем переменную
        DIR_TO_BAD = d
        dir3.config(text=f'Плохие фото: {DIR_TO_ANIMAL}')

#***********************************************************
# процесс запускаем анализа файлов
def button4():
    global DIR_IMAGE
    run1.config(text='Процесс запущен... формируем датасет', state='disabled')
    win1.update()
    # Задайте путь к вашему второму приложению (second.py)
    second_app_path = 'C:\\MegaDetector\\detection\\run_detector_batch.py'

    # Параметры, которые вы хотите передать во второе приложение
    param1 = r'C:\\MegaDetector\\md_v5a.0.0.pt'
    param2 = r'C:\\_IMAGE'
    param3 = r'C:\\_IMAGE\\test_output.json'
    param4 = r'--output_relative_filenames --recursive --checkpoint_frequency 10000 --quiet'
    # Вызовите second.py с параметрами с помощью subprocess
    result = subprocess.run(['C:\\Хахатон\\venv\\Scripts\\python', second_app_path, param1, param2, param3,param4], capture_output=True, text=True)
    f_jsn="имя_файла.json"
    file_path_1 = os.path.join(directory, f_jsn)
    file_path_2=os.path.join(directory, 'resalting.csv')
    filtration((f_jsn,DIR_TO_ANIMAL,DIR_TO_EMPTY, DIR_TO_BROKEN))
    # Вывести результат выполнения, если это необходимо

    if result.returncode == 0:
        print("Второе приложение успешно выполнено.")
    else:
        print("Произошла ошибка при выполнении второго приложения.")
        print("Код ошибки:", result.returncode)
        print("Сообщение об ошибке:", result.stderr)


    run1.config(text='Процесс запущен... сохраняем датасет', state='disabled')
    win1.update()

    run1.config(text='Процесс закончен', state='disabled')
    win1.update()
    time.sleep(2)
    run1.config(text='Запустить процесс', state='normal')


def button5():
    global DIR_TO_ANIMAL
    try:
        subprocess.Popen(['explorer', DIR_TO_ANIMAL])  # Открывает папку в проводнике Windows
    except Exception as e:
        print(f"Ошибка при открытии папки: {e}")


def button6():
    global DIR_TO_EMPTY
    try:
        subprocess.Popen(['explorer', DIR_TO_EMPTY])  # Открывает папку в проводнике Windows
    except Exception as e:
        print(f"Ошибка при открытии папки: {e}")

def button6_1():
    global DIR_TO_BROKEN
    try:
        subprocess.Popen(['explorer', DIR_TO_BROKEN])  # Открывает папку в проводнике Windows
    except Exception as e:
        print(f"Ошибка при открытии папки: {e}")

def button_about(x, y):
    about_dialog = tk.Toplevel(win1)
    about_dialog.title("О программе")
    # координаты отображения окна
    x_0 = x + 150
    y_0 = y + 100
    about_dialog.geometry(f"300x200+{x_0}+{y_0}")

    about_text = """
    Программа для сортировки изображений с 
    фотоловушек написана магистрантами АГУ 
    группа М4.206М-3
    во время хахатона 2023
    команда VASEK2

    """

    about_label = tk.Label(about_dialog, text=about_text, padx=10, pady=10)
    about_label.pack()

    close_button = tk.Button(about_dialog, text="Закрыть", command=about_dialog.destroy)
    close_button.pack()


# -------------------------
# тело программы
#

# фон
image_win = Image.open("belka4.png")

width, height = image_win.size

# Создаем окно Tkinter
win1 = tk.Tk()
icon = PhotoImage(file="vasek2.gif")
win1.tk.call('wm', 'iconphoto', win1._w, icon)
win1.title("Классификация снимков с фотоловушек (Хакатон 2023 команда VASEK2)")
win1.geometry(f'{width}x{height}')
win1.resizable(False, False)

# Создаем фон на приложении
tk_image = ImageTk.PhotoImage(image_win)

# Создаем Canvas для размещения фонового изображения
canvas = tk.Canvas(win1, width=tk_image.width(), height=tk_image.height())
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

# размеры монитора ширина и высота координаты (0:0) находится сверху слева
x = (win1.winfo_screenwidth() - width) // 2
y = (win1.winfo_screenheight() - height) // 2
win1.geometry(f'{width}x{height}+{x}+{y}')

# 1. Кнопка для выбора директории исходных фото
ttk.Button(win1, text="Выбор папки исходных фото", command=button1).place(x=10, y=10)
dir1 = tk.Label(win1, text=f'Исходные фото: {DIR_IMAGE}', width=39, anchor='w')
dir1.place(x=10, y=40)
# Добавление тени к тексту
dir1.config(font=("Helvetica", 8))
dir1.config(fg="black")
dir1.config(bg="lightblue")
dir1.config(bd=2, relief="groove")

# 2. Кнопка для выбора директории поломаных фото
ttk.Button(win1, text="Выбор папки для поломанных фото", command=button2).place(x=10, y=70)
dir2 = tk.Label(win1, text=f'Поломанные фото: {DIR_TO_BROKEN}', width=39, anchor='w')
dir2.place(x=10, y=100)
# Добавление тени к тексту
dir2.config(font=("Helvetica", 8))
dir2.config(fg="black")
dir2.config(bg="lightblue")
dir2.config(bd=2, relief="groove")

# 3. Кнопка для выбора директории фото без животных
ttk.Button(win1, text="Выбор папки для фото без животных", command=button3).place(x=10, y=130)
dir3 = tk.Label(win1, text=f'Фото без животных: {DIR_TO_EMPTY}', width=39, anchor='w')
dir3.place(x=10, y=160)
dir3.config(font=("Helvetica", 8))
dir3.config(fg="black")
dir3.config(bg="lightblue")
dir3.config(bd=2, relief="groove")

# 3_3. Кнопка для выбора директории фото с животными
ttk.Button(win1, text="Выбор папки для фото с животными", command=button3_1).place(x=10, y=190)
dir3_1 = tk.Label(win1, text=f'Хорошие фото: {DIR_TO_ANIMAL}', width=39, anchor='w')
dir3_1.place(x=10, y=220)
dir3_1.config(font=("Helvetica", 8))
dir3_1.config(fg="black")
dir3_1.config(bg="lightblue")
dir3_1.config(bd=2, relief="groove")

t=250
# 4. Кнопка для запуска процесса
run1 = ttk.Button(win1, text="Запустить процесс", command=button4)
run1.place(x=70, y=t+20)
#здесь должен быть мега детектор???

# 5. Кнопка для просмотра хороших фото
ttk.Button(win1, text="Посмотреть фото с животными", command=button5).place(x=10, y=t+60)

# 6. Кнопка для просмотра плохих фото
ttk.Button(win1, text="Посмотреть фото БЕЗ животных", command=button6).place(x=10, y=t+90)

# 6_1. Кнопка для просмотра плохих фото
ttk.Button(win1, text="Посмотреть поломанные фото", command=button6_1).place(x=10, y=t+120)

# 7. Кнопка "О программе"
ttk.Button(win1, text="О программе", command=lambda: button_about(x, y)).place(x=80, y=t+190)

# 8. Кнопка для закрытия приложения
ttk.Button(win1, text="Закрыть", command=win1.quit).place(x=85, y=t+220)

# запуск приложения
if __name__ == '__main__':
    win1.mainloop()