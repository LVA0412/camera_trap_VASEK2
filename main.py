import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
import time
import subprocess
import os
from find_defect_json2csv import processing_dataset

# Директории
DIR_CURRENT=current_directory = os.getcwd()
DIR_IMAGE = DIR_CURRENT
DIR_TO_RESULT = DIR_CURRENT
DIR_TO_BROKEN = 'D:\\Camera_trap\\megadetector\\result\\broken'
DIR_TO_EMPTY = 'D:\\Camera_trap\\megadetector\\result\\empty'
DIR_TO_ANIMAL = "D:\\Camera_trap\\megadetector\\result\\animal"


# вызов кнопок
def button1():
    global DIR_IMAGE
    d = filedialog.askdirectory()
    if d:  # если выбрали дирректорию, то поменяем переменную
        DIR_IMAGE = d
        dir1.config(text=f'Исходные фото: {DIR_IMAGE}')


def button2():
    global DIR_TO_RESULT
    global DIR_TO_BROKEN
    global DIR_TO_EMPTY
    global DIR_TO_ANIMAL
    d = filedialog.askdirectory()
    if d:  # если выбрали дирректорию, то поменяем переменную
        DIR_TO_RESULT = d
        dir2.config(text=f'Результат: {DIR_TO_RESULT}')
        #DIR_TO_BROKEN = DIR_TO_RESULT+'/broken'
        #DIR_TO_EMPTY = DIR_TO_RESULT+'/empty'
        #DIR_TO_ANIMAL = DIR_TO_RESULT+'/animal'
#***********************************************************
# процесс запускаем анализа файлов
def button4():
    global DIR_IMAGE
    run1.config(text='Процесс запущен. Ожидайте...', state='disabled')
    win1.update()
    """
    def toggle_label():
        if label.cget("text") == "":
            label.config(text="Ждите, идет обработка")
        else:
            label.config(text="Идет процесс обработки...")
        label.after(500, toggle_label)  # Меняем текст каждые 500 миллисекунд (0.5 секунды)

    root = tk.Tk()
    root.title("Не прерывайте обработку!")
    root.geometry("700x100")

    label = tk.Label(root, font=("Arial", 16))
    label.pack(pady=20)

    toggle_label()  # Запускаем функцию для мигания надпис
    """
    # Задайте путь к вашему второму приложению (second.py)
    second_app_path = 'detection/run_detector_batch.py'

    # Параметры, которые вы хотите передать во второе приложение
    model_params = r'./detection/md_v5b.0.0.pt'
    temp_output = os.path.join(DIR_TO_RESULT, 'temp_output.json')
    optional_params = r'--output_relative_filenames --recursive --checkpoint_frequency 10000 --quiet'

    # Вызовите second.py с параметрами с помощью subprocess
    cd_command = '(cd ../MegaDetector)'
    activate_mamba = '(mamba activate cameratraps-detector)'
    current_path = os.path.dirname(os.path.realpath(__file__))
    set_params = 'set PYTHONPATH=%PYTHONPATH%;D:\Camera_trap\megadetector\MegaDetector;D:\Camera_trap\megadetector\yolov5'
    run_detector = f'python {second_app_path} {model_params} {DIR_IMAGE} {temp_output} {optional_params}'
    commands = [cd_command, activate_mamba, set_params, run_detector]
    p = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for cmd in commands:
        p.stdin.write((cmd + "\n").encode())
    p.stdin.close()
    p.stdout.read()
    # Вывести результат выполнения, если это необходимо

    run1.config(text='Процесс запущен... сохраняем датасет', state='disabled')
    win1.update()

    processing_dataset(DIR_IMAGE, DIR_TO_RESULT, temp_output)

    run1.config(text='Процесс закончен', state='disabled')
    win1.update()
    time.sleep(2)
    run1.config(text='Запустить процесс', state='normal')

#    root.after(0, root.destroy)  # закрываем окно
#    root.mainloop()


def button5():
    global DIR_TO_ANIMAL
    try:
        subprocess.Popen(['explorer', DIR_TO_ANIMAL])  # Открывает папку в проводнике Windows
    except Exception as e:
        print(f"Ошибка при открытии папки: {e}")


def button6():
    global DIR_TO_EMPTY
    try:
        print(DIR_TO_EMPTY)
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
image_win = Image.open("belka.png")

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

# 2. Кнопка для выбора директории результата
ttk.Button(win1, text="Выбор папки для результата", command=button2).place(x=10, y=70)
dir2 = tk.Label(win1, text=f'Результат: {DIR_TO_RESULT}', width=39, anchor='w')
dir2.place(x=10, y=100)
# Добавление тени к тексту
dir2.config(font=("Helvetica", 8))
dir2.config(fg="black")
dir2.config(bg="lightblue")
dir2.config(bd=2, relief="groove")

t=250
# 4. Кнопка для запуска процесса
run1 = ttk.Button(win1, text="Запустить процесс", command=button4)
run1.place(x=70, y=t+20)

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
