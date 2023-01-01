import sys
from utils import get_data_from_json_file
sys.path.append('..')
sys.path.append('.')
from const.const import PROJECT_LOCATION # noqa


def find_missing_ids(movie_details: dict) -> None:
    for movie in movie_details.keys():
        if movie_details[movie]['id'] == 0:
            print(movie, movie_details[movie]['content_year'],
                  movie_details[movie]['id'])


def main():
    json_location = f"{PROJECT_LOCATION}/data/title_id"
    file = f"{json_location}/title_id.json"
    title_id = get_data_from_json_file(file)

    find_missing_ids(title_id)


if __name__ == '__main__':
    main()
