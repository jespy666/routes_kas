import os


def get_path(file_name: str) -> str:
    user_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(user_path, file_name))
