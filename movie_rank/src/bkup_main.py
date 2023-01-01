from __future__ import annotations
from statistics import mean
from obj.movie import Movie
from obj.person import Person
from utils.utils import get_data_from_json_file # noqa
from const.const import PROJECT_LOCATION # noqa

MOVIES_TO_PEOPLE_FILE = PROJECT_LOCATION\
                        + "/data/movies_to_people/movies_to_people.json"
PEOPLE_TO_MOVIE_FILE = PROJECT_LOCATION\
                       + "/data/people_to_movie/people_to_movie.json"
ID_TO_PEOPLE_FILE = PROJECT_LOCATION\
                       + "/data/id_to_people/id_to_people.json"
ID_TO_MOVIE_FILE = PROJECT_LOCATION\
                       + "/data/id_to_movie/id_to_movie.json"
'''
Add in data to person - cast or director
This would go in movies_to_people

Read in the following files:
    * people_to_movie.json
        This is the primary file
    * id_to_movie.json
    * id_to_people.json

Design ideas:
    * Each movie is an object

movies = list[Movies(movie_id)]
actors = {actor_id: Actor(actor_id)}

Actor:
    actor_id = int
    movie_scores = [[]] # list of list. Each movie
        contributes a value to the list. This is summed
        to get the actor score for each round
   actor_score


'''


def create_movie_objs(file_location) -> list:
    movies_to_people = get_data_from_json_file(file_location)
    for movie_id, cast_list in movies_to_people.items():
        movie_objs = [Movie(movie_id, cast_list) for
                      movie_id, cast_list in movies_to_people.items()]
        # movie_objs[movie_id] =
    return movie_objs


def create_all_people_objs(file_location) -> dict:
    people_objs = {}
    all_people = get_data_from_json_file(file_location)
    for person_id, person_name in all_people.items():
        people_objs[int(person_id)] = Person(int(person_id), person_name)
    return people_objs


def initialize_people(people_objs: dict, people_to_movie: dict,
        movie_objs: list):
    for person_id in people_to_movie.keys():
        for _ in people_to_movie[person_id]:
            people_objs[int(person_id)].add_point_to_person_scores(1)

        people_objs[int(person_id)].update_person_score()
        people_objs[int(person_id)].start_new_round()


def initialize_movies(movie_objs: list, people_objs: dict):
    '''Add value from person.get_person_score() to movie
    for each actor in the movie.
    :param movie_objs: list of Movie objects.
    :param people_objs: dict of people objects. Key = person_id,
    value = Person.'''
    for movie in movie_objs:
        for person in movie.cast:
            movie.receive_points_from_person(
                    people_objs[person].get_person_score())
        movie.update_movie_score()


def get_mean_movie_score(movie_objs: list) -> float:
    scores = []
    for movie in movie_objs:
        scores.append(movie.get_movie_score())
    return mean(scores)


def main():
    '''
    Rounds start at 0

    Plan
    1. Initial
    '''
    movie_objs: list[Movie] = create_movie_objs(MOVIES_TO_PEOPLE_FILE)
    people_objs: dict[int, Person] = create_all_people_objs(ID_TO_PEOPLE_FILE)

    people_to_movie: dict[int, list[int]] =\
        get_data_from_json_file(PEOPLE_TO_MOVIE_FILE)

    id_to_movie: dict[int, str] = get_data_from_json_file(ID_TO_MOVIE_FILE)

    initialize_people(people_objs, people_to_movie)
    initialize_movies(movie_objs, people_objs)

    for movie in movie_objs:
        print(id_to_movie[movie.get_movie_id()])
        print(movie.get_movie_score())
        for person in movie.get_cast():
            print('\t',
                  people_objs[person].get_person_name(),
                  people_objs[person].get_person_score())
    print(get_mean_movie_score(movie_objs))
    # for person in people_objs.values():
    #     print(person.get_person_name(), person.get_person_score())
    # for movie in movie_objs:
    #    print(movie.get_movie_id(), id_to_movie[movie.get_movie_id()])

    # for movie, people in people_to_movie.items():
    #     print(movie, people)




if __name__ == '__main__':
    main()
