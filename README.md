

# lab_report_grabber
## Установка (Linux)

Базовое требование - версия python 3.10 или выше. 

1. Клонирование репозитория 

```git clone -b demo git@github.com:moevm/lab_report_grabber.git```

2. Переход в директорию lab_report_grabber

```cd lab_report_grabber/```

3. Создание виртуального окружения

```python3 -m venv venv```

4. Активация виртуального окружения

```source venv/bin/activate```

5. Установка зависимостей

```pip3 install -r requirements.txt```

## Запуск
``` python3 main.py --arg1 --arg2 ...``` 
## Документация
### Обязательные аргументы
| Название | Описание                                                     |
|----------|--------------------------------------------------------------|
| `--works_structure` `-s`   | Путь до сsv таблица с английскими постфиксами работ, полным названием на русском и аннотацией работы          |
##### Пример
|  |  ||
|--|--|--|
|lb1|Лабораторная работа №1|Введение|
|lb2|Лабораторная работа №2|Работа с библиотеками|
|lb3|Лабораторная работа №3|Работа со строками|
|lb4|Лабораторная работа №4|Работа с сортировкой|

`-s struct_of_works.csv`
<br/>

| Название | Описание                                                     |
|----------|--------------------------------------------------------------|
| `--prefix`   | Префикс репозиториев в виде форматной строки: owner/repo-{group}|
#### Пример
`-prefix moevm/cs-2023-{group}`
<br/>

| Название | Описание                                                     |
|----------|--------------------------------------------------------------|
| `--path` `-p` ИЛИ `--google_table`  | Путь до csv таблицы со студентами / ссылка на гугл таблицу со студентами (как правильно взять ссылку см. ниже)|
|`--token_file`ИЛИ `--token`| Файл с github токеном в первой строке / github токен 
|`--full_name_col`ИЛИ `--nfull_name_col`| Номер столбца с ФИО студентов (нумерация с единицы) / название столбца с ФИО студентов|
|`--group_col`ИЛИ `--ngroup_col`| Номер столбца с группой студентов (нумерация с единицы) / название столбца с группой студентов|
|`--github_col`ИЛИ `--ngithub_col`| Номер столбца с github логинами студентов (нумерация с единицы) / название столбца с github логинами студентов|студентов|
|`--eng_name_col` ИЛИ `--neng_name_col`|Номер столбца с транслитирироваными на англиский язык именами студентов (нумерация с единицы) / название столбца с транслитирироваными на англиский язык именами студентов|
|`--eng_surname_col` ИЛИ `--neng_surname_col`|Номер столбца с транслитирироваными на англиский язык фамилиями студентов (нумерация с единицы) / название столбца с транслитирироваными на англиский язык фамилиями студентов|
#### Примеры
`-p students_table.csv`\
 `--google_table https://docs.google.com/spreadsheets/d/MyGoogleTable#gid=07` \
 `--token_file token.txt` \
 `--token ghp_MyGitGubToken`
 ##### Примечание
 в аргументах начинающихся на 'n' поиск столбца происходит в первых `num_header_rows` (см. ниже)
 
 `--full_name_col 1`\
 `--nfull_name_col "ФИО"`\
 `--group_col 2`\
 `--ngroup_col "Группа"`\
 `--github_col 3`\
 `--ngithub_col 3 "Github логин"`

### Необязательные аргументы
| Название | Описание                                                     |
|----------|--------------------------------------------------------------|
| `--out_table_name` `-o`  | Название выходной csv таблицы. Значение по умолчанию: `out`|
| `--num_header_rows` | Количество заголовочных строк, которые не будут учитываться в обработке данных (не учитываются первые 'n' строк). Значение по умолчанию: `1`|
|`--eng_names`|Значение `True`, если необходимо производить поиск работ по английским именам студентов. В этом случае надо указать два дополнительных аргумента: (`--eng_name_col` ИЛИ `--neng_name_col`) и (`--eng_surname_col` ИЛИ `--neng_surname_col`), где аргументы без приставки `n` -- это номера столбцов, а с приставкой `n` их названия в таблицы. Значение по умолчанию: `False`|
#### Примеры
`-o result.csv`\
`--out_table_name result_table` \
`--num_header_rows 2`
### Как взять корректную ссылку гугл таблицы
Открыть нужный лист, скопировать ссылку из адрессной строки

## Примеры запуска
```python3 main.py -p input/students_table_example.csv  --full_name_col 1 --group_col 2 --github_col 6 --prefix moevm/cs-2023-{group} --token_file input/token.txt -s input/struct_of_works_example.csv -o result2.cs --num_header_rows 2```

``` python3 main.py  --nfull_name_col "ФИО" --ngroup_col "Группа" --ngithub_col "Логин на github" --prefix moevm/pr-2023-{group} --token "ghp_MyGitHubLogin" -s input/struct_of_works_example.csv -o result2.cs --num_header_rows 2 --google_table https://docs.google.com/spreadsheets/d/MyGoogleTable/edit#gid=1030499006```

```python3 main.py --neng_name_col "Имя" --neng_surname_col "Фамилия" --nfull_name_col "ФИО" --ngroup_col "Группа" --ngithub_col "Логин на github" --prefix moevm/pr-2023-{group} --token "ghp_MyGitHubToken" -s input/struct_of_works_example.csv -o result2.cs --num_header_rows 2 --google_table https://docs.google.com/spreadsheets/d/MyGoogleTable/edit#gid=1030499006 --eng_names True```
