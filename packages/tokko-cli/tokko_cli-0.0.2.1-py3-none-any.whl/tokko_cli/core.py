from contextlib import suppress
import getpass
import shutil
import os

from tokko_cli.exceptions import (
    IAlreadyKnowYou,
    WhoAreYou,
)


def get_home_folder_path(user: str = None, home_folder: str = None) -> str:
    home_folder = home_folder or "/home"
    user = user or getpass.getuser()
    return os.path.join(home_folder, user)


def exists_cli_folder(username: str = None, home_folder: str = None) -> bool:
    home_folder = get_home_folder_path(home_folder=home_folder, user=username)
    return os.path.exists(os.path.join(home_folder, ".tokko"))


def is_installed_for(user) -> bool:
    """Return True when TokkoCLI folder exists"""
    return exists_cli_folder(user)


def get_required_folders(user, **settings):
    root_folder = get_home_folder_path(user)
    return [
        os.path.join(root_folder, settings.get("cli_home", ".tokko")),
        os.path.join(root_folder, settings.get("code_home", "tokko/sources")),
    ]


def create_required_folders(user, **settings):
    required_folders = get_required_folders(user, **settings)
    for idx, folder in enumerate(required_folders):
        os.makedirs(folder, exist_ok=True)


def delete_required_folders(user, **settings):
    required_folders = get_required_folders(user, **settings)
    for folder in required_folders:
        with suppress(FileNotFoundError):
            shutil.rmtree(folder, ignore_errors=True)


def initialize_work_environment(user, is_new=True):
    if is_new:
        create_required_folders(user)


def be_welcome(user):
    if is_installed_for(user):
        raise IAlreadyKnowYou(current_user=user)
    initialize_work_environment(user, is_new=True)


def say_goodbye(user=None, **settings):
    user = user or getpass.getuser()
    if not is_installed_for(user):
        raise WhoAreYou(f" for user '{user}'.")
    delete_required_folders(user=user, **settings)

