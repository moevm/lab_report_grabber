class Student:
    def __init__(self, full_name, group, github, works):
        self.full_name = full_name
        self.group = group
        self.github = github
        self.works = works


class Work:
    def __init__(self, eng_name, ru_name, description, code):
        self.eng_name = eng_name
        self.ru_name = ru_name
        self.description = description
        self.code = code
