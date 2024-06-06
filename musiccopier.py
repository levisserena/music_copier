"""Программа для копирования файлов из одной папки в другую.

Программа копирует только те файлы, которых нет во второй.
"""
import os
import shutil
import tkinter

win = tkinter.Tk()
win.geometry('1000x400+200+200')
win.title('Music Copier LS')
win.mainloop()

directory_source: str = r'C:\Users\Levis\Desktop\source'  # Откуда.
directory_receiver: str = r'C:\Users\Levis\Desktop\receiver'  # Куда.

format_files: str = 'txt'
substring_end: str = f'.{format_files}'

list_files_source: list[str] = os.listdir(directory_source)
list_files_receiver: list[str] = os.listdir(directory_receiver)

files_to_copy: list[str] = [
    files for files in list_files_source if files not in list_files_receiver
]

filtered_files_to_copy: list[str] = [
    files for files in files_to_copy if files.endswith(substring_end)
]

for files in filtered_files_to_copy:
    paht_to_files = fr'{directory_source}\{files}'
    shutil.copy2(paht_to_files, directory_receiver)


# try:
#     assert os.path.isdir(r'C:\\Users\\User\\Python\\Data\\Samples'), 'Нету'
# except AssertionError:
#     print('Нету!!!')

# shutil.copyfile(directory_source, directory_receiver)

# print(list_files_source)
# print(list_files_receiver)
# print(files_to_copy)
# print(filtered_files_to_copy)
