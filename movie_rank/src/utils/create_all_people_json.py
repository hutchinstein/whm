import sys
import os
import utils
sys.path.append('..')
sys.path.append('.')
from obj.local_logs import LocalLog # noqa
from const.const import PROJECT_LOCATION # noqa
from const.const import MAX_CAST_SIZE # noqa


def get_top_10_people(people_to_movies: dict,
                      id_to_people: dict,
                      id_to_movie: dict) -> dict:
    sorted_people_to_movies = {key: value for key, value
                               in sorted(people_to_movies.items(),
                                         key=lambda item: len(item[1]),
                                         reverse=True)}
    counter = 0
    for person_id, movie_list in sorted_people_to_movies.items():
        print(person_id, id_to_people[person_id], len(movie_list))
        for movie_id in movie_list:
            print(f"\t{id_to_movie[movie_id]} {movie_id}")
        counter += 1
        if counter == 10:
            break


def is_actor_or_director(individual: dict) -> bool:
    if individual.get('job') in ('Director', 'Novel'):
        return True
    if individual.get('character') and\
            individual.get('id') not in get_ids_to_skip()\
            and individual.get('order') < MAX_CAST_SIZE:
        return True
    return False


def get_ids_to_skip() -> list:
    return list({
            15831: "Frank Welker",
            7624: "Stan Lee"
           }.keys())


def main():
    people_to_movies: dict[int, list[int]] = {}
    movies_to_people: dict[int, list[int]] = {}
    id_to_people: dict[int, str] = {}
    id_to_movie: dict[int, str] = {}

    credits_location = f"{PROJECT_LOCATION}/data/credits"
    for file in os.listdir(credits_location):
        data = utils.get_data_from_json_file(f"{credits_location}/{file}")
        movie_id = data['id']
        cast_and_crew = data['cast'] + data['crew']

        id_to_movie.setdefault(data['id'],
                               file.replace('_', ' ')[:-5])
        for individual in cast_and_crew:
            if is_actor_or_director(individual):
                id_to_people.setdefault(individual['id'],
                                        individual['name'])

                people_to_movies.setdefault(individual['id'], [])
                if movie_id not in people_to_movies[individual['id']]:
                    people_to_movies[individual['id']].append(movie_id)

                movies_to_people.setdefault(movie_id, [])
                if individual['id'] not in movies_to_people[movie_id]:
                    movies_to_people[movie_id].append(individual['id'])

    get_top_10_people(people_to_movies, id_to_people, id_to_movie)
    utils.write_json_to_file(id_to_people,
                             f"{PROJECT_LOCATION}/data/id_to_people/"
                             f"id_to_people.json")
    utils.write_json_to_file(people_to_movies,
                             f"{PROJECT_LOCATION}/data/people_to_movie/"
                             f"people_to_movie.json")
    utils.write_json_to_file(id_to_movie,
                             f"{PROJECT_LOCATION}/data/id_to_movie/"
                             f"id_to_movie.json")
    utils.write_json_to_file(movies_to_people,
                             f"{PROJECT_LOCATION}/data/movies_to_people/"
                             f"movies_to_people.json")
    
if __name__ == '__main__':
    main()
