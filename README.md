# lab_report_grabber
# get_args()

Парсит аргументы в консоли и возращяет словарь значений.
- ### Обязательные аргументы:
	 -p. --path  -- Путь к исходной csv таблице в формате файловый систему Linux.
  
	 `-p dir/test1.csv`
  
	--num_header_rows -- Количество заголовочных строк в таблице.
  
	`--num_header_rows 1`

	--full_name_col - Номер столбца с ФИО студентов.
  
	`--full_name_col 3`

	--group_col -- Номер столбца с номера групп студентов.
  
	`--group_col 2`

	--github_col - Номер столбца с GitHub логинами студентов.
  
	`--github_col 5`

	-s --works_structure -- Названия работ на русском и английском вида: '{en1:ru1, en2:ru2, ...}'.
  
	`-s '{"Lab 1":"Лабораторная 1", "Lab 2":"Лабораторная 2"}'`

	--prefix -- Префикс репозитория т.е. все, что идет до номера группы.
  
	`--prefix moevm/cs-2023`

	-o --out_table_name -- Имя выходной csv таблицы.
  
	`--out_table_name out1`

	`-o out2.csv`
- ### Дополнительные аргументы:
	Нет
- ## Пример:
	  python3 get_args.py --path test1.csv --num_header_rows 1 --full_name_col 1 --group_col 2 --github_col 3 -s '{"Лабораторная 1": "Lab 1", "Лабораторная 2": "Lab 2"}' --prefix moevm/cs-2023 -o out
        returned value:
        {
        'path' : 'test1.csv'
        'num_header_rows' : 1
        'full_name_col' : 1
        'group_col' : 2
        'github_col' : 3
        'works_structure' : {"Lab 1":"Лабораторная 1", "Lab 2":"Лабораторная 2"}
        'prefix' : 'moevm/cs-2023'
        'out_table_name' : 'out'
        }
