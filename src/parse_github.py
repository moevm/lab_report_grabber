from classes import Work
from github import Github
from github import Auth
import logging
import log_config

CODE_DIR = 'src'
IGNORE_WORKS = ['cw']


def have_code_dir(contents, code_dir=CODE_DIR):
    for content in contents:
        if content.name == code_dir and content.type == 'dir':
            return True
    return False


def get_repos_name(args, table):
    groups = set(row[args['group_col'] - 1] for row in table)
    return [args['prefix'].format(group=group).split('/') for group in groups]


def get_repos_list_for_logs(repos):
    return [f"{repo.owner.login}/{repo.name}" for repo in repos]


def get_repo_list(user, args, table):
    repos_name = get_repos_name(args, table)
    repos = []
    logging.info(f"Checking repos with names:{repos_name}")
    for repo in user.get_user().get_repos():
        for name in repos_name:
            if repo.owner.login == name[0] and repo.name == name[1]:
                repos.append(repo)
                break
    return repos


def get_logins(args, table):
    logins = set(row[args['github_col'] - 1].lower() for row in table)
    return logins


def parse_repo(args, table, code_dir=CODE_DIR, ignore=IGNORE_WORKS):
    logging.info("Parse repo")
    try:
        auth = Auth.Token(args['token_file'])
    except Exception as e:
        print(f"Work with GitHub error: {e}")
        exit(0)
    g = Github(auth=auth)
    logins = get_logins(args, table)
    repos = get_repo_list(g, args, table)
    logging.info(f"Repos names:{get_repos_list_for_logs(repos)}")
    works = {login: [] for login in logins}
    for repo in repos:
        contents = repo.get_contents("")
        for content in contents:
            if content.type != 'dir' or not have_code_dir(repo.get_contents(content.path)):
                logging.warning(f"The content is not processed due to a violation of the structure."
                                f"\nName of content:{content.name}. Owner login:{repo.get_commits(path=content.path)[0].author}")
                continue

            last_commit = repo.get_commits(path=content.path)[0]
            author = last_commit.author
            if not author:
                logging.warning(f"The content is not processed due to the absence of the author\n"
                                f"Name of content:{content.name}")
                continue

            login = author.login.lower()
            if login not in logins:
                logging.warning(f"The content is not processed due to the absence of a username in the list of "
                                f"allowed logins\nName of content:{content.name}. Owner login:{login}")
                continue

            files = repo.get_contents(content.path + f'/{code_dir}')
            code = {file.name: file.decoded_content.decode('utf-8') for file in files}

            index = content.name.rfind('_')
            eng_name = content.name[index + 1:] if index != -1 else content.name
            if eng_name in ignore:
                continue

            ru_name, description = args['works_structure'].get(eng_name, eng_name)

            logging.info(f"Current student login: {login}. Work name: {eng_name}")

            works[login].append(Work(eng_name=eng_name, ru_name=ru_name,
                                     description=description, code=code))

    g.close()
    return works
