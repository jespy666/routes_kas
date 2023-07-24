import os


TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_PATH = f"{TESTS_DIR}/fixtures/"


def get_fixture_path(file_name: str) -> str:
    """
    Function Takes file name and return path to file.
    """
    return f'{FIXTURES_PATH}{file_name}'


def get_result(file_path: str) -> str:
    """
    Reads content and return it to str format.
    """
    with open(file_path) as result:
        return result.read().strip()
