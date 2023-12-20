from Work import Work
from github import Github
from github import Auth

TOKEN = ""


def have_src(contents):
    for content in contents:
        if content.name == 'src' and content.type == 'dir':
            return True
    return False


def get_repo_list(user, args):
    repo_owner, repo_prefix = args['prefix'].split('/')
    repos = []
    for repo in user.get_user().get_repos():
        if repo.owner.login == repo_owner and repo.name.startswith(repo_prefix):
            repos.append(repo)

    return repos


def get_logins(args, table):
    logins = set(row[args['github_col'] - 1] for row in table)
    return logins


def parse_repo(args, table):
    auth = Auth.Token(TOKEN)
    g = Github(auth=auth)
    logins = get_logins(args, table)
    repos = get_repo_list(g, args)
    works = {login: [] for login in logins}

    for repo in repos:
        contents = repo.get_contents("")
        for content in contents:
            if content.type != 'dir' or not have_src(repo.get_contents(content.path)):
                continue

            last_commit = repo.get_commits(path=content.path)[0]
            author = last_commit.author
            if not author:
                continue

            login = author.login
            if login not in logins:
                continue

            files = repo.get_contents(content.path + '/src')
            code = {file.name: file.decoded_content.decode('utf-8') for file in files}

            index = content.name.rfind('_')
            eng_name = content.name[index + 1:] if index != -1 else content.name
            ru_name, description = args['works_structure'].get(eng_name, eng_name)

            works[login].append(Work(eng_name=eng_name, ru_name=ru_name, description=description,
                                     code=code))

    g.close()
    return works
