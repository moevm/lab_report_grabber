from get_args import *
from parse_table import *
from parse_github import *
from Work import *
from get_students import *
from fill_table import *

args = get_args()
table = parse_table(args)
works = parse_repo(args, table)
students = get_students(works, args, table)
write_rows(args, students)
