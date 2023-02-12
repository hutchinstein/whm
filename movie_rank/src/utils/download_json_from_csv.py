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

CSV_FILE = f'{PROJECT_LOCATION}/data/csv/whm_content_year.csv'


def clean_title(title: str) -> str:
    title = title.split(' - ')[1]
    if "(" in title:
        title = title.split(" (")[0]
    return title.replace(":", "")


def get_movie_title_dict() -> tuple(dict, dict):
    with open(CSV_FILE, 'r') as csv_in:
        out_dict: dict[str, dict] = {}
        csv_updater: dict[str, int] = {}
        reader = csv.DictReader(csv_in)
        ep_num = 2
        for row in reader:
            if 'Episode' in row['Title']:
                out_dict[clean_title(row['Title'])] =\
                        {'content_year': row['Content Year'],
                         'id': row['movie_id'],
                         'whm_episode': ep_num}
                csv_updater[row['Title']] = ep_num
                ep_num += 1
    return out_dict, csv_updater


def update_csv(csv_updater: dict[str, int], key_column, val_column):
    rows = []
    with open(CSV_FILE, 'r') as file_in:
        reader = csv.DictReader(file_in)
        header = reader.fieldnames
        for row in reader:
            # print(row[key_column], row[val_column])
            # print(type(row[key_column]), type(row[val_column]))
            if row[key_column] in csv_updater.keys():
                row[val_column] = csv_updater[row[key_column]]
            rows.append(row)

    with open(CSV_FILE, 'w', newline='') as file_out:
        writer = csv.DictWriter(file_out, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def get_movie_by_release_year(movie_details: dict, title: str,
                              response: dict, log: LocalLog,
                              ep_to_id: dict) -> tuple(dict, dict):
    log.info(f"Found title: {title}. Checking for ID.")
    log.debug(f"CSV data: {title} {movie_details[title]}")
    log.debug(f"Full API response:\n{response}")

    # ep_to_id: dict[int, int] = {} # this makes a new blank dict each time, fix it
    for result in response['results']:
        if result['release_date'].split('-')[0] ==\
                movie_details[title]['content_year']:
            log.info("Title and year match")
            movie_details[title]['id'] = result['id']
            ep_to_id[str(movie_details[title]['whm_episode'])] =\
                str(result['id'])
            break

    return (movie_details, ep_to_id)


def get_ids(movie_details: dict, url_base: str, log: LocalLog,
            ep_to_id) -> tuple(dict, dict):
    remaining, downloaded = len(movie_details.keys()), 1
    for key in movie_details.keys():
        if movie_details[key]['id']:
            # print("Movie ID exists in csv file, skipping...")
            continue
        # print(f"Attempting to download IDs...{downloaded}/{remaining}")# ,
        print(movie_details[key])
              # end='\r')
        downloaded += 1

        url = f"{url_base}{key.replace(' ', '+')}"
        r = utils.attempt_download_from_api(url)
        if r.status_code == 200 and r.json()['results']:
            movie_details, ep_to_id = get_movie_by_release_year(movie_details,
                                                                key,
                                                                r.json(),
                                                                log,
                                                                ep_to_id)

        else:
            log.info(f"Title: {key} did not return any data")
        time.sleep(.05)
    return (movie_details, ep_to_id)


def main():
    KEY = utils.get_key()
    URL_BASE = f"{API_URL_BASE}/search/movie?api_key={KEY}&query="
    DATA_LOCATION = f"{PROJECT_LOCATION}/data"

    log = LocalLog('download_json_from_csv.log')
    log.info("Script started.")

    movie_details, csv_updater = get_movie_title_dict()
    update_csv(csv_updater, 'Title', 'movie_counter')
    ep_to_id = {}
    movie_details, ep_to_id = get_ids(movie_details, URL_BASE, log, ep_to_id)
    utils.write_json_to_file(movie_details,
                             f"{DATA_LOCATION}/title_id/title_id.json")
    update_csv(ep_to_id, 'movie_counter', 'movie_id')

    log.info("Complete!")


if __name__ == '__main__':
    main()
