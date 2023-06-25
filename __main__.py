from configs import USER_AGENTS_FILE_PATH
from utils.parse_json import parse_json
from configs import PROXIES_FILE_PATH
from sites import blog_dera_jobs


user_agents = parse_json(USER_AGENTS_FILE_PATH)
proxies_list = parse_json(PROXIES_FILE_PATH)
