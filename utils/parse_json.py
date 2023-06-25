import random
import json
import os


def parse_json(filepath):
    data = None
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
    else:
        raise FileNotFoundError
    random.shuffle(data)
    return data
