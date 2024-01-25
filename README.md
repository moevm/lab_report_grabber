# lab_report_grabber
## Пример запуска 1:
	  python3 main.py -p students_table.csv  --full_name_col 1 --group_col 2 --github_col 6 --prefix moevm/cs-2023-{group} --token_file token.txt -s struct_of_works.csv -o result2.cs --num_header_rows 2
## Пример запуска 2:
	  python3 main.py  --nfull_name_col "ФИО" --ngroup_col "Группа" --ngithub_col "Логин на github" --prefix moevm/cs-2023-{group} --token "ghp_MyGitHubLogin" -s struct_of_works.csv -o result2.cs --num_header_rows 2 --google_table https://docs.google.com/spreadsheets/d/1VdUE351rvOXpVUGOLoc7PlbT1HJTMGBYtdvmE6ncBG0/edit#gid=1030499006

## Как взять корректную ссылку гугл таблицы:
Открыть нужный лист, скопировать ссылку из адрессной строки
