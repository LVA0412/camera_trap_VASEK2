import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
import time
import subprocess
import os
import ctypes

# ����������
DIR_CURRENT=current_directory = os.getcwd()
DIR_IMAGE = DIR_CURRENT+'\_IMAGE'
DIR_TO_BROKEN = DIR_CURRENT+'\_BROKEN'
DIR_TO_EMPTY = DIR_CURRENT+'\_EMPTY'
DIR_TO_ANIMAL = DIR_CURRENT+'\_ANIMAL'



# ����� ������
def button1():
    global DIR_IMAGE
    d = filedialog.askdirectory()
    if d:  # ���� ������� �����������, �� �������� ����������
        DIR_IMAGE = d
        dir1.config(text=f'�������� ����: {DIR_IMAGE}')


def button2():
    global DIR_TO_BROKEN
    d = filedialog.askdirectory()
    if d:  # ���� ������� �����������, �� �������� ����������
        DIR_TO_GOOD = d
        dir2.config(text=f'������� ����: {DIR_TO_BROKEN}')


def button3():
    global DIR_TO_EMPTY
    d = filedialog.askdirectory()
    if d:  # ���� ������� �����������, �� �������� ����������
        DIR_TO_BAD = d
        dir3.config(text=f'������ ����: {DIR_TO_EMPTY}')


def button3_1():
    global DIR_TO_ANIMAL
    d = filedialog.askdirectory()
    if d:  # ���� ������� �����������, �� �������� ����������
        DIR_TO_BAD = d
        dir3.config(text=f'������ ����: {DIR_TO_ANIMAL}')

def button4():
    run1.config(text='������� �������... �����', state='disabled')
    win1.update()
    time.sleep(5)
    run1.config(text='������� ��������', state='disabled')
    win1.update()
    time.sleep(2)
    run1.config(text='��������� �������', state='normal')


def button5():
    global DIR_TO_ANIMAL
    try:
        subprocess.Popen(['explorer', DIR_TO_ANIMAL])  # ��������� ����� � ���������� Windows
    except Exception as e:
        print(f"������ ��� �������� �����: {e}")


def button6():
    global DIR_TO_EMPTY
    try:
        subprocess.Popen(['explorer', DIR_TO_EMPTY])  # ��������� ����� � ���������� Windows
    except Exception as e:
        print(f"������ ��� �������� �����: {e}")

def button6_1():
    global DIR_TO_BROKEN
    try:
        subprocess.Popen(['explorer', DIR_TO_BROKEN])  # ��������� ����� � ���������� Windows
    except Exception as e:
        print(f"������ ��� �������� �����: {e}")

def button_about(x, y):
    about_dialog = tk.Toplevel(win1)
    about_dialog.title("� ���������")
    # ���������� ����������� ����
    x_0 = x + 150
    y_0 = y + 100
    about_dialog.geometry(f"300x200+{x_0}+{y_0}")

    about_text = """
    ��������� ��� ���������� ����������� � 
    ����������� �������� ������������� ��� 
    ������ �4.206�-3
    �� ����� �������� 2023 ....
    ������� VASEK2

    """

    about_label = tk.Label(about_dialog, text=about_text, padx=10, pady=10)
    about_label.pack()

    close_button = tk.Button(about_dialog, text="�������", command=about_dialog.destroy)
    close_button.pack()


# -------------------------
# ���� ���������
#

# ���
image_win = Image.open("belka.png")

width, height = image_win.size

# ������� ���� Tkinter
win1 = tk.Tk()
icon = PhotoImage(file="vasek2.gif")
win1.tk.call('wm', 'iconphoto', win1._w, icon)
win1.title("������������� ������� � ����������� (������� 2023 ������� VASEK2)")
win1.geometry(f'{width}x{height}')
win1.resizable(False, False)

# ������� ��� �� ����������
tk_image = ImageTk.PhotoImage(image_win)

# ������� Canvas ��� ���������� �������� �����������
canvas = tk.Canvas(win1, width=tk_image.width(), height=tk_image.height())
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

# ������� �������� ������ � ������ ���������� (0:0) ��������� ������ �����
x = (win1.winfo_screenwidth() - width) // 2
y = (win1.winfo_screenheight() - height) // 2
win1.geometry(f'{width}x{height}+{x}+{y}')

# 1. ������ ��� ������ ���������� �������� ����
ttk.Button(win1, text="����� ����� �������� ����", command=button1).place(x=10, y=10)
dir1 = tk.Label(win1, text=f'�������� ����: {DIR_IMAGE}')
dir1.place(x=40, y=40)

# 2. ������ ��� ������ ���������� ��������� ����
ttk.Button(win1, text="����� ����� ��� ���������� ����", command=button2).place(x=10, y=70)
dir2 = tk.Label(win1, text=f'���������� ����: {DIR_TO_BROKEN}')
dir2.place(x=40, y=100)

# 3. ������ ��� ������ ���������� ���� ��� ��������
ttk.Button(win1, text="����� ����� ��� ���� ��� ��������", command=button3).place(x=10, y=130)
dir3 = tk.Label(win1, text=f'���� ��� ��������: {DIR_TO_EMPTY}')
dir3.place(x=40, y=160)

# 3_3. ������ ��� ������ ���������� ���� � ���������
ttk.Button(win1, text="����� ����� ��� ���� � ���������", command=button3_1).place(x=10, y=190)
dir3_1 = tk.Label(win1, text=f'������� ���� � ���������: {DIR_TO_ANIMAL}')
dir3_1.place(x=40, y=220)

t=250
# 4. ������ ��� ������� ��������
run1 = ttk.Button(win1, text="��������� �������", command=button4)
run1.place(x=70, y=t+20)

# 5. ������ ��� ��������� ������� ����
ttk.Button(win1, text="���������� ���� � ���������", command=button5).place(x=10, y=t+60)

# 6. ������ ��� ��������� ������ ����
ttk.Button(win1, text="���������� ���� ��� ���������", command=button6).place(x=10, y=t+90)

# 6_1. ������ ��� ��������� ������ ����
ttk.Button(win1, text="���������� ���������� ����", command=button6_1).place(x=10, y=t+120)

# 7. ������ "� ���������"
ttk.Button(win1, text="� ���������", command=lambda: button_about(x, y)).place(x=80, y=t+190)

# 8. ������ ��� �������� ����������
ttk.Button(win1, text="�������", command=win1.quit).place(x=85, y=t+220)

# ������ ����������
if __name__ == '__main__':
    win1.mainloop()