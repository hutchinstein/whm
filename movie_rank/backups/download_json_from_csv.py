from __future__ import annotations
import requests
import csv
import time
import json
import os

import sys
sys.path.append('..')
sys.path.append('.')
from const.const import CONST_API_URL_BASE # noqa
from const.const import CONST_PROJECT_LOCATION # noqa
from obj.local_logs import LocalLog # noqa


def get_key() -> str:
    with open(f"{CONST_PROJECT_LOCATION}/src/const/api.key", 'r') as key_in:
        KEY = key_in.read().strip('\n')
    return KEY


def clean_title(title: str) -> str:
    title = title.split(' - ')[1]
    if "(" in title:
        title = title.split(" (")[0]
    return title.replace(":", "")


def get_movie_title_dict() -> dict:
    with open(f"{CONST_PROJECT_LOCATION}/data/csv/whm_content_year.csv",
              'r') as csv_in:
        out_dict: dict[str, str] = {}
        reader = csv.DictReader(csv_in)
        ep_num = 2
        for row in reader:
            if 'Episode' in row['Title']:
                out_dict[clean_title(row['Title'])] =\
                        {'content_year': row['Content Year'],
                         'id': 0,
                         'whm_episode': ep_num}
                ep_num += 1
    return out_dict


def get_ids(movie_details: str, url_base: str, log: LocalLog) -> dict:
    films_to_download, downloaded = len(movie_details.keys()), 1

    for key in movie_details.keys():
        print(f"Attempting to download IDs...{downloaded}/{films_to_download}",
              end='\r')
        downloaded += 1
        url = f"{url_base}{key.replace(' ', '+')}"

        for _ in range(5):
            response = requests.get(url)
            if response.status_code == 200:
                break
            else:
                time.sleep(1)

        if response.status_code == 200 and response.json()['results']:
            file_name = key.replace(' ', '_')
            file_name = file_name.replace('/', '_')
            log.info(f"Found title: {key}. Checking for ID.")
            log.debug(f"CSV data: {key} {movie_details[key]}")
            log.debug(f"Full API response:\n{response.json()}")
            for result in response.json()['results']:
                if result['release_date'].split('-')[0] ==\
                        movie_details[key]['content_year']:
                    log.info("Title and year match")
                    movie_details[key]['id'] = result['id']
                    break
        else:
            log.info(f"Title: {key} did not return any data")
        time.sleep(.05)
    return movie_details


def display_download_results(download_results: dict, log: LocalLog) -> None:
    for key in download_results.keys():
        for val in download_results[key]:
            log.info(f"{key}: \t{val}")
    log.info("********SUMMARY********")
    log.info(f"Total downloaded: {len(download_results['downloaded'])}")
    log.info(f"Total missing: {len(download_results['missing'])}")


def find_missing_ids(movie_details: dict, log: LocalLog) -> None:
    for movie in movie_details.keys():
        if movie_details[movie]['id'] == 0:
            print(movie, movie_details['content_year'], movie_details['id'])


def write_json_to_file(data: dict, file_path_and_name: str) -> None:
    with open(file_path_and_name, "w+") as write_file:
        json.dump(data, write_file, indent=4)


def main():
    KEY = get_key()
    URL_BASE = f"{CONST_API_URL_BASE}/search/movie?api_key={KEY}&query="
    DATA_LOCATION = f"{CONST_PROJECT_LOCATION}/data"

    log = LocalLog('download_json_from_csv.log')
    log.info("Script started.")

    movie_details: dict[str, str] = get_movie_title_dict()
    movie_details = get_ids(movie_details, URL_BASE, log)
    write_json_to_file(movie_details,
                       f"{DATA_LOCATION}/title_id/title_id.json")
    find_missing_ids(movie_details, log)

    log.info("Complete!")


if __name__ == '__main__':
    main()
