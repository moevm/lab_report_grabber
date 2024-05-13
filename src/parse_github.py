from github import Repository, Github
import logging
import json

from src.config import get_config
from src.utils import try_auth, get_work_names
from src.classes import Work

cfg = get_config()


def get_repos_name(args: dict, table: list[list[str]]) -> list[list[str]]:
    groups = set(row[args['group_col'] - 1] for row in table)
    return [args['prefix'].format(group=group).split('/') for group in groups]


def get_repo_list(user: Github, args: dict, table: list[list[str]]) -> list[Repository]:
    repos_name = get_repos_name(args, table)
    repos = []
    logging.info(cfg['Info']['check_repos'].format(repos_name=repos_name))
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
        logging.warning(cfg['Warning']['author'].format(name=content.name))
        return False

    return True


def check_login(login, logins, content) -> bool:
    if login not in logins:
        logging.warning(cfg['Warning']['login'].format(name=content.name, login=login))
        return False

    return True


def check_work_name(name, login, content) -> bool:
    if name in json.loads(cfg['List']['ignore_works']):
        logging.warning(cfg['Warning']['work_name'].format(name=content.name, login=login))
        return False

    return True


def try_get_files(login, repo, content):
    try:
        answer = repo.get_contents(content.path + f"/{cfg['Const']['code_dir']}")
        return answer
    except:
        logging.warning(cfg['Warning']['get_files'].format(name=content.name, login=login))

        return False


def parse_repo(args: dict, table: list[list[str]]) -> dict[str, list[Work]]:
    logging.info(cfg['Info']['parse_repos'])

    g = try_auth(cfg['Error']['github_auth'], args['token_file'])
    logins = get_logins(args, table)
    repos = get_repo_list(g, args, table)

    logging.info(cfg['Info']['repo_names'].format(names=get_repos_list_for_logs(repos)))
    logging.info(cfg['Info']['ignore_works_list'].format(ignore=cfg['List']['ignore_works']))
    works_names = get_work_names(args, table)
    works = {login: [] for login in logins}
    for repo in repos:
        contents = repo.get_contents("")
        uniq_students = set()
        for content in contents:
            if args['eng_names']:
                if content.name not in works_names:
                    continue

                login = works_names[content.name]
            else:
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

            code = {}
            try:
                for file in files:
                    try:
                        code[file.name] = file.decoded_content.decode('utf-8').replace('\n', '\\n')
                    except:
                        logging.warning(cfg['Warning']['get_files'].format(name=content.name, login=login))
            except:
                logging.warning(cfg['Warning']['get_files'].format(name=content.name, login=login))

            index = content.name.rfind('_')

            eng_name = content.name[index + 1:] if index != -1 else content.name
            if not check_work_name(eng_name, login, content):
                continue

            ru_name, description = args['works_structure'].get(eng_name, eng_name)

            logging.info(cfg['Info']['current_student'].format(login=login, name=eng_name))

            works[login].append(Work(eng_name=eng_name, ru_name=ru_name,
                                     description=description, code=code))
            
            if login not in uniq_students:
                uniq_students.add(login)
                print(f"students count: {len(uniq_students)}/{len(logins)}")

    g.close()
    return works
