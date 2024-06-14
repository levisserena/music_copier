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
copying_all_files: bool = False


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
        try:
            file = open(file=f'{DIR_SAVE}/{file_ms}.ms', mode='r')
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
        except FileNotFoundError:
            label_name_window['text'] = ('Что-то пошло не так!\nКажется кто-то'
                                         f'уже удалил файл {file_ms}.')
            ms_listbox.delete(selection[0])
    else:
        label_name_window['text'] = 'Ну выбери что нибудь!'


def delete_file(
    selection, file_ms, ms_listbox, label_name_window, window_conf_del
):
    """Удаление файла конфигурации."""
    path_delete = f'{DIR_SAVE}/{file_ms}.ms'
    try:
        os.remove(path_delete)
    except FileNotFoundError:
        label_name_window['text'] = ('Что-то пошло не так!\nКажется кто-то'
                                     f'уже удалил файл {file_ms}.')
    finally:
        ms_listbox.delete(selection[0])
        finish(window_conf_del)


def confirmation_deletion(ms_listbox, label_name_window):
    """
    Попросит выбрать файл для удаления.
    Откроет окно подтверждения удаления файла сохраненной конфигурации.
    """
    selection = ms_listbox.curselection()
    if selection:
        file_ms = ms_listbox.get(selection)
        window_conf_del = tkinter.Toplevel()
        window_conf_del.title('Точно удалить?')
        window_conf_del.geometry('250x140')
        window_conf_del.resizable(False, False)
        window_conf_del.protocol(
            'WCD_DELETE_WINDOW',
            func=lambda: finish(window_conf_del)
        )
        label_name_window = ttk.Label(
            master=window_conf_del, text=f'Удалить файл {file_ms}?'
        )
        label_name_window.pack(anchor='nw', padx=PAD, pady=PAD)
        button_yas_del = ttk.Button(
            master=window_conf_del,
            text='Да, в топку его!',
            command=lambda: delete_file(
                selection,
                file_ms,
                ms_listbox,
                label_name_window,
                window_conf_del,
            ),
        )
        button_yas_del.pack(anchor='nw', padx=PAD, pady=PAD)
        button_no_del = ttk.Button(
            master=window_conf_del,
            text='Нет, я передумал',
            command=lambda: finish(window_conf_del),
        )
        button_no_del.pack(anchor='nw', padx=PAD, pady=PAD)
        window_conf_del.grab_set()  # захватываем пользовательский ввод
    else:
        label_name_window['text'] = 'Ну выбери что нибудь!'


def open_configuration_filled() -> None:
    """Открывает окно для выбора файла конфигурациию."""
    create_folder_save()
    list_in_save: list[str] = os.listdir(DIR_SAVE)
    substring_end_save: str = f'.{FORMAT_SAVE}'
    list_ms: list[str] = [
        ms.rstrip(substring_end_save) for ms in list_in_save
        if ms.endswith(substring_end_save)
    ]
    window_open = tkinter.Toplevel()
    window_open.title('Открыть')
    window_open.geometry('300x280')
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
    button_open = ttk.Button(
        master=window_open,
        text='Открыть и применить',
        command=lambda: open_file(ms_listbox, window_open, label_name_window),
    )
    button_open.pack(anchor='nw', padx=PAD, pady=PAD)
    button_delete = tkinter.Button(
        master=window_open,
        text='Удалить запись',
        command=lambda: confirmation_deletion(ms_listbox, label_name_window),
    )
    button_delete.pack(anchor='nw', padx=PAD, pady=PAD)
    window_open.grab_set()  # захватываем пользовательский ввод


def still_writing(name_file, path_file, window_save, window_overwriting=None):
    """Создаёт файл сохранения конфигурации."""
    file = open(file=path_file, mode='w')
    line = f'{directory_source}\n{directory_receiver}\n{format_file}'
    file.write(line)
    file.close()
    if window_overwriting:
        finish(window_overwriting)
    finish(window_save)
    messagebox.showinfo(
        title='Информация', message=f'Файл {name_file} сохранен.'
    )


def overwriting_or_writing(name_file, path_file, window_save):
    """
    Открывает окно подтверждения перезаписи конфигурации и вызывает сохранение
    файла.
    """
    if os.path.isfile(path_file):
        window_overwriting = tkinter.Toplevel()
        window_overwriting.title('Точно?')
        window_overwriting.geometry('220x140')
        window_overwriting.resizable(False, False)
        window_overwriting.protocol(
            'WOW_DELETE_WINDOW',
            func=lambda: finish(window_overwriting)
        )
        label_name_window = ttk.Label(
            master=window_overwriting,
            text=f'Файл с именем {name_file} существует.\nПерезаписать?',
        )
        label_name_window.pack(anchor='nw', padx=PAD, pady=PAD)
        button_yas = ttk.Button(
            master=window_overwriting,
            text='Да, перезапиши',
            command=lambda: still_writing(
                name_file, path_file, window_save, window_overwriting
            ),
        )
        button_yas.pack(anchor='nw', padx=PAD, pady=PAD)
        button_no = ttk.Button(
            master=window_overwriting,
            text='Нет, я передумал',
            command=lambda: finish(window_overwriting),
        )
        button_no.pack(anchor='nw', padx=PAD, pady=PAD)
        window_overwriting.grab_set()  # захватываем пользовательский ввод
    else:
        still_writing(name_file, path_file, window_save)


def preparation_save_file(entry_save, window_save):
    """
    Создаст папку для сохранений, если её нет. Получит из ввода имя файла и
    его путь. Перешлёт дальше.
    """
    create_folder_save()
    name_file = entry_save.get()
    path_file = f'{DIR_SAVE}/{name_file}.ms'
    overwriting_or_writing(name_file, path_file, window_save)


def save_configuration_filled():
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
    entry_save = ttk.Entry(master=window_save, width=33)
    entry_save.pack(anchor='nw', padx=PAD, pady=PAD)
    button_save = ttk.Button(
        master=window_save,
        text='Сохранить',
        command=lambda: preparation_save_file(entry_save, window_save),
    )
    button_save.pack(anchor='nw', padx=PAD, pady=PAD)
    window_save.grab_set()  # захватываем пользовательский ввод


def setting_program():
    """Настройка программы."""
    message = 'Тут пока нечего нет. :('
    messagebox.showwarning(title='Информация', message=message)


def about_program():
    """Информация о программе."""
    message = (
        'Программа для копирования файлов из одной папки в другую.\n'
        'Программа копирует только те файлы, которых нет во второй папке.\n'
        'Разработал Акчурин Лев.\n'
        '06.2024\n'
    )
    messagebox.showinfo(title='Информация', message=message)


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


def get_format_file(entry_format, label):
    """Открывает диалоговое окно с проводником. Выбирает куда копирует"""
    global format_file
    format_file = entry_format.get()
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
    botton_directory_source = ttk.Button(
        master=frame, text='Откуда копируем',
        command=lambda: get_directory_source(label_directory_source),
    )
    botton_directory_source.pack(anchor='nw')
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
    botton_directory_receiver = ttk.Button(
        master=frame, text='Куда копируем',
        command=lambda: get_directory_receiver(label_directory_receiver),
    )
    botton_directory_receiver.pack(anchor='nw')
    return frame


def activate_deactivate(check_all_format):
    """Активирует и деактивирует поля в зависимости от чекбокса."""
    global copying_all_files
    label_format = window_main.nametowidget(
        'frame_entry_format.label_format'
    )
    entry_format = window_main.nametowidget(
        'frame_entry_format.entry_format'
    )
    button_entry_format = window_main.nametowidget(
        'frame_entry_format.button_entry_format'
    )
    if check_all_format:
        label_format['state'] = 'disabled'
        entry_format['state'] = 'disabled'
        button_entry_format['state'] = 'disabled'
        copying_all_files = True
    else:
        label_format['state'] = 'enabled'
        entry_format['state'] = 'enabled'
        button_entry_format['state'] = 'enabled'
        copying_all_files = False


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
    check_all_format = tkinter.IntVar()
    checkbutton_all_format = ttk.Checkbutton(
        master=frame,
        text='Все файлы',
        variable=check_all_format,
        command=lambda: activate_deactivate(check_all_format.get()),
    )
    checkbutton_all_format.pack(anchor='nw')
    label_format = ttk.Label(
        master=frame, name='label_format', text=format_file
    )
    label_format.pack(anchor='nw')
    entry_format = ttk.Entry(master=frame, name='entry_format', width=50)
    entry_format.pack(anchor='nw', padx=PAD, pady=PAD)
    button_entry_format = ttk.Button(
        master=frame,
        text='Ввод',
        name='button_entry_format',
        command=lambda: get_format_file(entry_format, label_format),
    )
    button_entry_format.pack(anchor='nw')
    return frame


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
        if not copying_all_files:
            files_to_copy = [
                files for files in files_to_copy
                if files.endswith(substring_end)
            ]
        for files in files_to_copy:
            paht_to_files = fr'{directory_source}\{files}'
            shutil.copy2(paht_to_files, directory_receiver)


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
file_menu.add_command(label='Открыть', command=open_configuration_filled)
file_menu.add_command(label='Сохранить', command=save_configuration_filled)
file_menu.add_separator()
file_menu.add_command(label='Выйти', command=finish)
parameter_menu = tkinter.Menu()
parameter_menu.add_command(label='Настройки', command=setting_program)
parameter_menu.add_command(label='О программе', command=about_program)
main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Опции', menu=parameter_menu)
window_main.config(menu=main_menu)

directory_source_frame = create_frame_source()
directory_source_frame.pack(anchor='nw', fill='x', padx=PAD, pady=PAD)
directory_receiver_frame = create_frame_receiver()
directory_receiver_frame.pack(anchor='nw', fill='x', padx=PAD, pady=PAD)
format_frame = create_frame_entry_format()
format_frame.pack(anchor='nw', fill='x', padx=PAD, pady=PAD)

button_copy = ttk.Button(
    text='Копировать!',
    command=copy_file,
)
button_copy.pack(anchor='center', padx=20, pady=6, ipadx=20, ipady=10)

window_main.mainloop()
