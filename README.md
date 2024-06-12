# Music Copier

### О проекте.
Программа позволяет копировать файлы из одной папки в другую, без замены одноименных файлов.
Да, я знаю, что операционная система справляется с этим на "ура!".
Но это мой первый обсолютно самостоятельный проект. Надо же с чего то начинать.
А тут мне нужно было копировать музыку на телефон, но так чтоб дублеров не было.
___
### Информация об авторе.
Акчурин Лев Ливатович.<br>Студент курса Яндекс Практикума Python-разработчик плюс.
___
### При создании проекта использовалось:
- язык программирования `Python` версии 3.9.13;
- встроенная библиотека `os`;
- встроенная библиотека `shutil`;
- встроенная библиотека `tkinter`;
___
### В планах на доработку:
- Чтобы при пересохранение - спрашивало;
- чтоб принемала кортеж, какие форматы копировать;
- удалять сохранки;
- ползунок прогресса копирования;
- валидация полей;
- сделать нормальную костомизацию;
- настройки кастомизации;
- рефакторинг.
___
### Как развернуть проект.
Чтобы развернуть проект необходимо следующие:
- Форкнуть проект себе на репозиторий с:
```
https://github.com/levisserena/music_copier
```

>*активная ссылка под этой кнопкой* -> [КНОПКА](https://github.com/levisserena/music_copier)
- Клонировать репозиторий со своего GitHub и перейти в него в командной строке:

```
git clone https://github.com/<имя вашего акаунта>/music_copier
```
- Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

- Запустить проект:

```
python musiccopier.py
```
