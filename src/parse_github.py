from github import ContentFile, Repository, Github
import logging

from src.utils import try_auth
from src.classes import Work

CODE_DIR = 'src'
IGNORE_WORKS = ['cw']


def have_code_dir(contents: list[ContentFile], code_dir: str = CODE_DIR) -> bool:
    for content in contents:
        if content.name == code_dir and content.type == 'dir':
            return True
    return False


def get_repos_name(args: dict, table: list[list[str]]) -> list[list[str]]:
    groups = set(row[args['group_col'] - 1] for row in table)
    return [args['prefix'].format(group=group).split('/') for group in groups]


def get_repo_list(user: Github, args: dict, table: list[list[str]]) -> list[Repository]:
    repos_name = get_repos_name(args, table)
    repos = []
    logging.info(f"Checking repos with names:{repos_name}")
    for repo in user.get_user().get_repos():
        for name in repos_name:
            if repo.owner.login == name[0] and repo.name == name[1]:
                repos.append(repo)
                break
    return repos


def get_repos_list_for_logs(repos: list[Repository]) -> list[str]:
    return [f"{repo.owner.login}/{repo.name}" for repo in repos]


def get_logins(args: dict, table: list[list[str]]) -> set[str]:
    logins = set(row[args['github_col'] - 1].lower() for row in table)
    return logins


def check_autor(author, content) -> bool:
    if not author:
        logging.warning(f"The content is not processed due to the absence of the author\n"
                        f"\tName of content: {content.name}")
        return False

    return True


def check_login(login, logins, content) -> bool:
    if login not in logins:
        logging.warning(f"The content is not processed due to the absence of a username in the list of "
                        f"allowed logins\n\tName of content: {content.name} . Owner login: {login}")
        return False

    return True


def check_work_name(name, login, content, ignore=IGNORE_WORKS) -> bool:
    if name in ignore:
        logging.warning(f"The content was ignore because name of work in ignore list."
                        f"\n\tName of content: {content.name} . Owner login: {login}")
        return False

    return True


def try_get_files(login, repo, content, code_dir=CODE_DIR):
    try:
        return repo.get_contents(content.path + f'/{code_dir}')

    except Exception as e:
        logging.warning(f"The content is not processed due to a violation of the structure."
                        f"\n\tName of content: {content.name} . Owner login: {login}")

        return False


def parse_repo(args: dict, table: list[list[str]], ignore=IGNORE_WORKS) -> dict[str, list[Work]]:
    logging.info("Parse repo")

    g = try_auth("Work with GitHub error", args['token_file'])
    logins = get_logins(args, table)
    repos = get_repo_list(g, args, table)

    logging.info(f"Repos names: {get_repos_list_for_logs(repos)}")
    logging.info(f"Ignore works list: {ignore}")

    works = {login: [] for login in logins}
    for repo in repos:
        contents = repo.get_contents("")

        for content in contents:
            last_commit = repo.get_commits(path=content.path)[0]
            author = last_commit.author
            if not check_autor(author, content):
                continue

            login = author.login.lower()
            if not check_login(login, logins, content):
                continue

            files = try_get_files(login, repo, content)
            if not files:
                continue

            code = {file.name: file.decoded_content.decode('utf-8').replace('\n', '\\n') for file in files}

            index = content.name.rfind('_')

            eng_name = content.name[index + 1:] if index != -1 else content.name
            if not check_work_name(eng_name, login, content):
                continue

            ru_name, description = args['works_structure'].get(eng_name, eng_name)

            logging.info(f"Current student login: {login} . Work name: {eng_name}")

            works[login].append(Work(eng_name=eng_name, ru_name=ru_name,
                                     description=description, code=code))

    g.close()
    return works
