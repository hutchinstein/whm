from __future__ import annotations
import sys
import utils
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
        print("Missing")


def generate_url(id: int) -> str:
    return API_GET_CREDITS.replace("@", str(id))


def download_cast_data(movie_id: dict, data_location: str,
                       log: LocalLog) -> None:
    movie_counter, total_movies = 1, len(movie_id.keys())
    for movie in movie_id.keys():
        print(f"Downloading cast data... {movie_counter}/{total_movies}",
              end='\r')
        movie_counter += 1
        movie_name = movie.replace(" ", "_").replace('/', ' ')
        file_name = f"{data_location}/{movie_name}.json"
        url = generate_url(movie_id[movie]['id'])
        log.info(f"Attempting to download {movie_name}.")
        response = utils.attempt_download_from_api(url)
        if response.status_code == 200:
            utils.write_json_to_file(response.json(), file_name)
            log.info(f"Wrote {movie_name} to file")
        else:
            log.info(f"Unable to download credits data for {movie_name}. "
                     f"Recived status code: {response.status_code}.")


def main():
    log = LocalLog('download_credits.log')
    log.info("Script started.")
    movie_id_file = f"{PROJECT_LOCATION}/data/title_id/title_id.json"
    output_location = f"{PROJECT_LOCATION}/data/credits"
    movie_id = utils.get_data_from_json_file(movie_id_file)
    download_cast_data(movie_id, output_location, log)


if __name__ == '__main__':
    main()
