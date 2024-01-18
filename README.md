# Python Discord Bot

## Описание
Бот позволяет постить мемы с **Reddit** с помощью `Reddit API`, а также использовать **ChatGPT**
в определенных каналах с помощью `ChatGPT API`

## Используемый стек
Python 3.11, Disnake.

## Локальный запуск проекта
Редактируем / создаём файл *.env* по примеру *.env_example*.

Создаём и активируем виртуальное окружение:
```shell
python -m venv venv
source venv/Scripts/activate
```
Устанавливаем зависимости:
```shell
python -m pip install -r requirements.txt
```
Находясь в коренной папке проекта `path_to_folder/`
```shell
python main.py
```

Всё готово, осталось подгрузить коги, зайдите в любой Discord канал и напишите
команду `/load_cogs`, выберите конкретные или все коги.

***Авторы**: Нечепуренко Артём* 
