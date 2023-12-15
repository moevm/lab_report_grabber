import os


def check_path(path):
    if not os.path.exists(path):
        raise Exception("Path of the file is Invalid")
    return
