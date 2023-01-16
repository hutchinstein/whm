from __future__ import annotations
import csv
import time
import utils

import sys
sys.path.append('..')
sys.path.append('.')
from const.const import API_URL_BASE # noqa
from const.const import PROJECT_LOCATION # noqa
from obj.local_logs import LocalLog # noqa


def clean_title(title: str) -> str:
    title = title.split(' - ')[1]
    if "(" in title:
        title = title.split(" (")[0]
    return title.replace(":", "")


def get_movie_title_dict() -> dict:
    with open(f"{PROJECT_LOCATION}/data/csv/whm_content_year.csv",
              'r') as csv_in:
        out_dict: dict[str, dict] = {}
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


def update_movie_details(movie_details: dict,
                         title: str,
                         response: dict,
                         log: LocalLog) -> dict:

    log.info(f"Found title: {title}. Checking for ID.")
    log.debug(f"CSV data: {title} {movie_details[title]}")
    log.debug(f"Full API response:\n{response}")

    for result in response['results']:
        if result['release_date'].split('-')[0] ==\
                movie_details[title]['content_year']:
            log.info("Title and year match")
            movie_details[title]['id'] = result['id']
            break

    return movie_details


def get_ids(movie_details: dict, url_base: str, log: LocalLog) -> dict:
    films_to_download, downloaded = len(movie_details.keys()), 1

    for key in movie_details.keys():
        print(f"Attempting to download IDs...{downloaded}/{films_to_download}",
              end='\r')
        downloaded += 1

        url = f"{url_base}{key.replace(' ', '+')}"
        response = utils.attempt_download_from_api(url)
        if response.status_code == 200 and response.json()['results']:
            movie_details = update_movie_details(movie_details,
                                                 key,
                                                 response.json(),
                                                 log)
        else:
            log.info(f"Title: {key} did not return any data")
        time.sleep(.05)
    return movie_details


def main():
    KEY = utils.get_key()
    URL_BASE = f"{API_URL_BASE}/search/movie?api_key={KEY}&query="
    DATA_LOCATION = f"{PROJECT_LOCATION}/data"

    log = LocalLog('download_json_from_csv.log')
    log.info("Script started.")

    movie_details: dict[str, dict] = get_movie_title_dict()
    movie_details = get_ids(movie_details, URL_BASE, log)
    utils.write_json_to_file(movie_details,
                             f"{DATA_LOCATION}/title_id/title_id.json")

    log.info("Complete!")


if __name__ == '__main__':
    main()
