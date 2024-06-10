"""Программа для копирования файлов из одной папки в другую.

Программа копирует только те файлы, которых нет во второй.
"""
import os
import shutil
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


PADDING: tuple[float, ...] = (5, 5, 5, 5)
PAD: int = 5

# Переменные.
directory_source: str = ''
directory_receiver: str = ''
format_file: str = 'mp3'


def finish():
    """Остановит работу окна."""
    window.destroy()


def open_pre_filled():
    """Открывает файл конфигурации, с предварительно заполнеными полями."""
    pass


def save_pre_filled():
    """Сохраняет файл конфигурации, с предварительно заполнеными полями."""
    pass


def setting_program():
    """Настройка программы."""
    message = 'Тут пока нечего нет. :('
    messagebox.showwarning(title="Информация", message=message)


def about_program():
    """Информация о программе."""
    message = (
        'Программа для копирования файлов из одной папки в другую.\n'
        'Разработал Акчурин Лев.\n'
        '06.2024\n'
    )
    messagebox.showinfo(title="Информация", message=message)


window = tkinter.Tk()
window.geometry('600x400')
window.resizable(False, False)  # Запрещает растягивать окно.
window.title('Music Copier LS')
icon = tkinter.PhotoImage(file='icon.png')
window.iconphoto(False, icon)
window.protocol('WM_DELETE_WINDOW', finish)
window.option_add("*tearOff", tkinter.FALSE)  # Уберает из меню пунктир.

main_menu = tkinter.Menu()
file_menu = tkinter.Menu()
file_menu.add_command(label='Открыть', command=open_pre_filled)
file_menu.add_command(label='Сохранить', command=save_pre_filled)
file_menu.add_separator()
file_menu.add_command(label='Выйти', command=finish)
parameter_menu = tkinter.Menu()
parameter_menu.add_command(label='Настройки', command=setting_program)
parameter_menu.add_command(label='О программе', command=about_program)
main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Опции', menu=parameter_menu)
window.config(menu=main_menu)


def get_directory_source(label):
    """Открывает диалоговое окно с проводником. Выбирает откуда копирует"""
    global directory_source
    directory = filedialog.askdirectory()
    directory_source = directory
    label['text'] = directory


def get_directory_receiver(label):
    """Открывает диалоговое окно с проводником. Выбирает куда копирует"""
    global directory_receiver
    directory = filedialog.askdirectory()
    directory_receiver = directory
    label['text'] = directory


def get_format_file(entry, label):
    """Открывает диалоговое окно с проводником. Выбирает куда копирует"""
    global format_file
    format_file = entry.get()
    label['text'] = format_file


def create_source_frame():
    """Создваёт фрейм с кнопкой получения адреса откуда копирование."""
    frame = ttk.Frame(borderwidth=1, relief='solid', padding=PADDING)
    label_name_frame = ttk.Label(
        master=frame, text='Выберете папку, откуда копировать'
    )
    label_name_frame.pack(anchor='nw')
    label_directory_source = ttk.Label(master=frame, text=directory_source)
    label_directory_source.pack(anchor='nw')
    directory_botton = ttk.Button(
        master=frame, text='Откуда копируем',
        command=lambda: get_directory_source(label_directory_source),
    )
    directory_botton.pack(anchor='nw')
    return frame


def create_receiver_frame():
    """Создваёт фрейм с кнопкой получения адреса куда копирование."""
    frame = ttk.Frame(borderwidth=1, relief='solid', padding=PADDING)
    label_name_frame = ttk.Label(
        master=frame, text='Выберете папку, куда копировать'
    )
    label_name_frame.pack(anchor='nw')
    label_directory_receiver = ttk.Label(master=frame, text=directory_receiver)
    label_directory_receiver.pack(anchor='nw')
    directory_botton = ttk.Button(
        master=frame, text='Куда копируем',
        command=lambda: get_directory_receiver(label_directory_receiver),
    )
    directory_botton.pack(anchor='nw')
    return frame


def create_entry_format_frame():
    """Создваёт фрейм с полем для ввода формата копируемых файлов."""
    frame = ttk.Frame(borderwidth=1,  relief='solid', padding=PADDING)
    label_name_frame = ttk.Label(
        master=frame, text='Введите формат копируемых файлов')
    label_name_frame.pack(anchor='nw')
    label_format = ttk.Label(master=frame, text=format_file)
    label_format.pack(anchor='nw')
    entry = ttk.Entry(master=frame, width=50)
    entry.pack(anchor='nw', padx=PAD, pady=PAD)
    button = ttk.Button(
        master=frame, text='Ввод',
        command=lambda: get_format_file(entry, label_format),
    )
    button.pack(anchor='nw')
    return frame


directory_source_frame = create_source_frame()
directory_source_frame.pack(anchor='nw', fill='x', padx=5, pady=5)
directory_receiver_frame = create_receiver_frame()
directory_receiver_frame.pack(anchor='nw', fill='x', padx=5, pady=5)
format_frame = create_entry_format_frame()
format_frame.pack(anchor='nw', fill='x', padx=5, pady=5)


def copy_file() -> None:
    """Копирует файлы."""
    substring_end: str = f'.{format_file}'
    if directory_source and directory_receiver:
        list_files_source: list[str] = os.listdir(directory_source)
        list_files_receiver: list[str] = os.listdir(directory_receiver)
        files_to_copy: list[str] = [
            files for files in list_files_source
            if files not in list_files_receiver
        ]
        filtered_files_to_copy: list[str] = [
            files for files in files_to_copy if files.endswith(substring_end)
        ]
        for files in filtered_files_to_copy:
            paht_to_files = fr'{directory_source}\{files}'
            shutil.copy2(paht_to_files, directory_receiver)


button_copy = ttk.Button(
        text='Копировать!',
        command=copy_file,
    )
button_copy.pack(anchor='center', padx=20, pady=6, ipadx=20, ipady=10)

window.mainloop()
