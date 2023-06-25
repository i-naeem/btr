from configs import PROXIES_FILE_PATH
import random
import json

proxies_list = []

with open(file=PROXIES_FILE_PATH, mode="r", encoding="utf-8") as f:
    proxies_list = json.load(f)
    random.shuffle(proxies_list)
