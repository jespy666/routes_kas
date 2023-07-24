import os
from kas.user_data import USER_DIR
from tests import FIXTURES_PATH
import json


def parse(file, fixtures=False):
    if fixtures:
        path = os.path.abspath(os.path.join(FIXTURES_PATH, file))
    else:
        path = os.path.abspath(os.path.join(USER_DIR, file))

    with open(path) as f:
        text = f.read()

    return json.loads(text)
