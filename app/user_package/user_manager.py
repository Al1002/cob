import os # file operation
from pathlib import Path

USERS_DIRECTORY = "/home/sasho_b/Coding/cob/users"

def get_user_dir(name: str) -> Path:
    return Path(USERS_DIRECTORY, name)

def user_exists(name: str) -> bool:
    os.path.isdir(get_user_dir(name))

def create_user(name: str):
    os.mkdir(get_user_dir(name))

