from src.config import get_config

cfg = get_config()


class Work:
    def __init__(self, eng_name: str, ru_name: str, description: str, code: dict):
        self.eng_name = eng_name
        self.ru_name = ru_name
        self.description = description
        self.code = code

    def code_to_string(self) -> str:
        code = ""
        for file_name in self.code:
            code += "&^<\\multiline>{file_name}:\n{code}".format(file_name=file_name, code=self.code[file_name])

        return code


class Student:
    def __init__(self, full_name: str, group: str, github: str, works: list[Work]):
        self.full_name = full_name
        self.group = group
        self.github = github
        self.works = works

    def get_fields(self) -> list[list[str]]:
        fields = []
        for work in self.works:
            fields.append([self.full_name, self.group, work.ru_name,
                           work.description, work.code_to_string()])

        return fields
