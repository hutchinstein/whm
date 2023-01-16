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
                         'whm_episode': ep_num,
                         'title': clean_title(row['Title']),
                         'media_type': row['Media Type'],
                         'whm_release_date': row['Originally Posted']}
                ep_num += 1
    return out_dict


def update_csv_movie_info(csv_movie_info: dict, title: str, response: dict,
                          log: LocalLog, id_to_movie: dict) -> dict:

    log.info(f"Found title: {title}. Checking for ID.")
    log.debug(f"CSV data: {title} {csv_movie_info[title]}")
    log.debug(f"Full API response:\n{response}")

    for result in response['results']:
        if result['release_date'].split('-')[0] ==\
                csv_movie_info[title]['content_year']:
            log.info("Title and year match")
            id_to_movie[result['id']] = csv_movie_info[title]
            break

    return id_to_movie


def get_ids(csv_movie_info: dict, url_base: str, log: LocalLog) -> dict:
    films_to_download, downloaded = len(csv_movie_info.keys()), 1
    id_to_movie: dict[int, dict] = {}

    for key in csv_movie_info.keys():
        print(f"Attempting to download IDs...{downloaded}/{films_to_download}",
              end='\r')
        downloaded += 1

        url = f"{url_base}{key.replace(' ', '+')}"
        response = utils.attempt_download_from_api(url)
        if response.status_code == 200 and response.json()['results']:
            update_csv_movie_info(csv_movie_info,
                                  key,
                                  response.json(),
                                  log,
                                  id_to_movie)
        else:
            log.info(f"Title: {key} did not return any data")
        time.sleep(.05)
    return id_to_movie


def main():
    KEY = utils.get_key()
    URL_BASE = f"{API_URL_BASE}/search/movie?api_key={KEY}&query="
    DATA_LOCATION = f"{PROJECT_LOCATION}/data"

    log = LocalLog('download_json_from_csv.log')
    log.info("Script started.")

    csv_movie_info: dict[str, dict] = get_movie_title_dict()
    id_to_movie: dict[int, dict] = get_ids(csv_movie_info, URL_BASE, log)
    utils.write_json_to_file(id_to_movie,
                             f"{DATA_LOCATION}/title_id/title_id.json")

    log.info("Complete!")


if __name__ == '__main__':
    main()
