from __future__ import annotations
import sys
import utils
import os
sys.path.append('..')
sys.path.append('.')
from const.const import PROJECT_LOCATION # noqa
from const.const import API_GET_CREDITS # noqa
from obj.local_logs import LocalLog # noqa


def get_credit(id: int, url: str) -> None:
    response = utils.attempt_download_from_api(url)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Unable to download {url} due to {response.status_code}")


def generate_url(id: int, special_format: str = None) -> str:
    if not special_format:
        return API_GET_CREDITS.replace("@", str(id))
    return API_GET_CREDITS.replace("@", str(id)).replace(
                                   '/movie/', f'/{special_format}/')


def download_cast_data(movie_id: dict, data_location: str,
                       log: LocalLog) -> None:
    print("Downloading cast data")
    for movie in movie_id.keys():
        movie_name = movie.replace(" ", "_").replace('/', ' ')
        file_name = f"{data_location}/{movie_name}.json"
        if os.path.isfile(file_name):
            log.info(f"{movie_name} already exists, skipping.")
            continue
        url = generate_url(movie_id[movie]['id'],
                           movie_id[movie]['special_format'])
        log.info(f"Attempting to download {movie_name}.")
        response = utils.attempt_download_from_api(url)
        if response.status_code == 200:
            utils.write_json_to_file(response.json(), file_name)
            log.info(f"Wrote {movie_name} to file")
        else:
            log.info(f"Unable to download credits data for {movie_name}. "
                     f"Recived status code: {response.status_code}.")


def main():
    print("Downloading credits...")
    log = LocalLog('download_credits.log')
    log.info("Script started.")
    movie_id_file = f"{PROJECT_LOCATION}/data/title_id/title_id.json"
    output_location = f"{PROJECT_LOCATION}/data/credits"
    movie_id = utils.get_data_from_json_file(movie_id_file)
    download_cast_data(movie_id, output_location, log)
    print("Done!")


if __name__ == '__main__':
    main()
