"""Программа для копирования файлов из одной папки в другую.

Программа копирует только те файлы, которых нет во второй.
"""
import os
import shutil
import tkinter
from tkinter import filedialog, messagebox, ttk


PADDING: tuple[float, ...] = (5, 5, 5, 5)
PAD: int = 5
DIR_SAVE: str = 'save'
FORMAT_SAVE: str = 'ms'

# Переменные.
directory_source: str = ''
directory_receiver: str = ''
format_file: str = 'mp3'


def finish(window=None) -> None:
    """Остановит работу окна или программы."""
    if not window:
        exit(1)
    window.grab_release()  # Возвращаем контроль.
    window.destroy()


def create_folder_save():
    """Если нет папки для сохранений конфигураций, то она будет создана."""
    if not os.path.isdir(f'{DIR_SAVE}'):
        os.mkdir(f'{DIR_SAVE}')


def open_file(ms_listbox, window_open, label_name_window):
    """Открывает файл конфигурации и применяет инструкции из него."""
    global directory_source
    global directory_receiver
    global format_file
    selection = ms_listbox.curselection()
    if selection:
        file_ms = ms_listbox.get(selection)
        file = open(file=f'save/{file_ms}.ms', mode='r')
        directory_source = file.readline().strip()
        directory_receiver = file.readline().strip()
        format_file = file.readline().strip()
        label_directory_source = window_main.nametowidget(
            'frame_source.label_directory_source'
        )
        label_directory_receiver = window_main.nametowidget(
            'frame_receiver.label_directory_receiver'
        )
        label_format = window_main.nametowidget(
            'frame_entry_format.label_format'
        )
        label_directory_source['text'] = directory_source
        label_directory_receiver['text'] = directory_receiver
        label_format['text'] = format_file
        finish(window_open)
    else:
        label_name_window['text'] = 'Ну выбери что нибудь!'


def open_pre_filled() -> None:
    """Открывает окно для выбора файла конфигурациию"""
    create_folder_save()
    list_in_save: list[str] = os.listdir(DIR_SAVE)
    substring_end_save: str = f'.{FORMAT_SAVE}'
    list_ms: list[str] = [
        ms.rstrip(substring_end_save) for ms in list_in_save
        if ms.endswith(substring_end_save)
    ]
    window_open = tkinter.Toplevel()
    window_open.title('Открыть')
    window_open.geometry('300x270')
    window_open.resizable(False, False)
    window_open.protocol(
        'WO_DELETE_WINDOW',
        func=lambda: finish(window_open)
    )
    label_name_window = ttk.Label(
        master=window_open, text='Выберите файл'
    )
    label_name_window.pack(anchor='nw', padx=PAD, pady=PAD)
    list_ms_var = tkinter.Variable(value=list_ms)
    ms_listbox = tkinter.Listbox(master=window_open, listvariable=list_ms_var)
    ms_listbox.pack(anchor='nw', fill='x', padx=PAD, pady=PAD)
    button = ttk.Button(
        master=window_open,
        text='Открыть и применить',
        command=lambda: open_file(ms_listbox, window_open, label_name_window),
    )
    button.pack(anchor='nw', padx=PAD, pady=PAD)
    window_open.grab_set()  # захватываем пользовательский ввод


def save_file(entry, window_save):
    """Сохраняет файл, закрывает окно для сохранений."""
    create_folder_save()
    name = entry.get()
    file = open(file=f'save/{name}.ms', mode='w')
    line = f'{directory_source}\n{directory_receiver}\n{format_file}'
    file.write(line)
    file.close()
    finish(window_save)
    messagebox.showinfo(title='Информация', message=f'Файл {name} сохранен.')


def save_pre_filled():
    """Открывает окно для сохранение конфигурации."""
    window_save = tkinter.Toplevel()
    window_save.title('Сохранить')
    window_save.geometry('240x100')
    window_save.resizable(False, False)
    window_save.protocol(
        'WS_DELETE_WINDOW',
        func=lambda: finish(window_save)
    )
    label_name_window = ttk.Label(
        master=window_save, text='Введите название файла'
    )
    label_name_window.pack(anchor='nw', padx=PAD, pady=PAD)
    entry = ttk.Entry(master=window_save, width=33)
    entry.pack(anchor='nw', padx=PAD, pady=PAD)
    button = ttk.Button(
        master=window_save,
        text='Сохранить',
        command=lambda: save_file(entry, window_save),
    )
    button.pack(anchor='nw', padx=PAD, pady=PAD)
    window_save.grab_set()  # захватываем пользовательский ввод


def setting_program():
    """Настройка программы."""
    message = 'Тут пока нечего нет. :('
    messagebox.showwarning(title='Информация', message=message)


def about_program():
    """Информация о программе."""
    message = (
        'Программа для копирования файлов из одной папки в другую.\n'
        'Разработал Акчурин Лев.\n'
        '06.2024\n'
    )
    messagebox.showinfo(title='Информация', message=message)


window_main = tkinter.Tk()
window_main.geometry('600x400')
window_main.resizable(False, False)  # Запрещает растягивать окно.
window_main.title('Music Copier LS')
icon = tkinter.PhotoImage(file='icon.png')
window_main.iconphoto(False, icon)
window_main.protocol('WM_DELETE_WINDOW', finish)
window_main.option_add('*tearOff', tkinter.FALSE)  # Уберает из меню пунктир.

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
window_main.config(menu=main_menu)


def get_directory_source(label):
    """Открывает диалоговое окно с проводником. Выбирает откуда копирует"""
    global directory_source
    directory_source = filedialog.askdirectory()
    label['text'] = directory_source


def get_directory_receiver(label):
    """Открывает диалоговое окно с проводником. Выбирает куда копирует"""
    global directory_receiver
    directory_receiver = filedialog.askdirectory()
    label['text'] = directory_receiver


def get_format_file(entry, label):
    """Открывает диалоговое окно с проводником. Выбирает куда копирует"""
    global format_file
    format_file = entry.get()
    label['text'] = format_file


def create_frame_source():
    """Создваёт фрейм с кнопкой получения адреса откуда копирование."""
    frame = ttk.Frame(
        borderwidth=1, name='frame_source', relief='solid', padding=PADDING
    )
    label_name_frame = ttk.Label(
        master=frame, text='Выберете папку, откуда копировать'
    )
    label_name_frame.pack(anchor='nw')
    label_directory_source = ttk.Label(
        master=frame, name='label_directory_source', text=directory_source
    )
    label_directory_source.pack(anchor='nw')
    directory_botton = ttk.Button(
        master=frame, text='Откуда копируем',
        command=lambda: get_directory_source(label_directory_source),
    )
    directory_botton.pack(anchor='nw')
    return frame


def create_frame_receiver():
    """Создваёт фрейм с кнопкой получения адреса куда копирование."""
    frame = ttk.Frame(
        borderwidth=1, name='frame_receiver', relief='solid', padding=PADDING
    )
    label_name_frame = ttk.Label(
        master=frame, text='Выберете папку, куда копировать'
    )
    label_name_frame.pack(anchor='nw')
    label_directory_receiver = ttk.Label(
        master=frame, name='label_directory_receiver', text=directory_receiver
    )
    label_directory_receiver.pack(anchor='nw')
    directory_botton = ttk.Button(
        master=frame, text='Куда копируем',
        command=lambda: get_directory_receiver(label_directory_receiver),
    )
    directory_botton.pack(anchor='nw')
    return frame


def create_frame_entry_format():
    """Создваёт фрейм с полем для ввода формата копируемых файлов."""
    frame = ttk.Frame(
        borderwidth=1,
        name='frame_entry_format',
        relief='solid', padding=PADDING,
    )
    label_name_frame = ttk.Label(
        master=frame, text='Введите формат копируемых файлов')
    label_name_frame.pack(anchor='nw')
    label_format = ttk.Label(
        master=frame, name='label_format', text=format_file
    )
    label_format.pack(anchor='nw')
    entry = ttk.Entry(master=frame, width=50)
    entry.pack(anchor='nw', padx=PAD, pady=PAD)
    button = ttk.Button(
        master=frame, text='Ввод',
        command=lambda: get_format_file(entry, label_format),
    )
    button.pack(anchor='nw')
    return frame


directory_source_frame = create_frame_source()
directory_source_frame.pack(anchor='nw', fill='x', padx=PAD, pady=PAD)
directory_receiver_frame = create_frame_receiver()
directory_receiver_frame.pack(anchor='nw', fill='x', padx=PAD, pady=PAD)
format_frame = create_frame_entry_format()
format_frame.pack(anchor='nw', fill='x', padx=PAD, pady=PAD)


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

window_main.mainloop()