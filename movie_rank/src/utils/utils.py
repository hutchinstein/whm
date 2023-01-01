import json
import requests
import time
import sys
sys.path.append('..')
sys.path.append('.')
from const.const import PROJECT_LOCATION # noqa


def get_data_from_json_file(file: str) -> dict:
    with open(file, 'r', encoding='utf-8') as in_file:
        return json.load(in_file)


def write_json_to_file(data: dict, file_path_and_name: str) -> None:
    with open(file_path_and_name, "w+") as write_file:
        json.dump(data, write_file, indent=4)


def attempt_download_from_api(url: str) -> requests.models.Response:
    for _ in range(5):
        response = requests.get(url)
        if response.status_code == 200:
            break
        else:
            time.sleep(1)
    return response


def get_key() -> str:
    with open(f"{PROJECT_LOCATION}/src/const/api.key", 'r') as key_in:
        KEY = key_in.read().strip('\n')
    return KEY
