from __future__ import annotations
import numpy as np
from obj.movie import Movie
from obj.person import Person
from utils.utils import get_data_from_json_file # noqa
from const.const import PROJECT_LOCATION # noqa
from const.const import MAX_CAST_SIZE # noqa

MOVIES_TO_PEOPLE_FILE = PROJECT_LOCATION\
                        + "/data/movies_to_people/movies_to_people.json"
PEOPLE_TO_MOVIE_FILE = PROJECT_LOCATION\
                       + "/data/people_to_movie/people_to_movie.json"
ID_TO_PEOPLE_FILE = PROJECT_LOCATION\
                       + "/data/id_to_people/id_to_people.json"
ID_TO_MOVIE_FILE = PROJECT_LOCATION\
                       + "/data/id_to_movie/id_to_movie.json"


def create_movie_objs(file_location, id_to_movie: dict) -> dict:
    '''Loop through all movies and create a dict.
    Key: movie_id, value: Movie object.
    Movie initialized with: movie_id, cast_list and movie_name.
    Note: movie name is from the file list and is not official. Would
    need to grab this from another file if needed.
    :param file_location: location of json file'''
    movies_to_people = get_data_from_json_file(file_location)
    movie_objs: dict[int, Movie] = {}
    for movie_id, cast_list in movies_to_people.items():
        movie_objs[movie_id] = Movie(movie_id, cast_list,
                                     id_to_movie[movie_id])
    return movie_objs


def create_all_people_objs(file_location: str) -> dict:
    '''Loop through all people and create a dict.
    Key: person_id, value: Person_object.
    Person initialized with person_id and person_name
    :param file_location: location of json file'''
    people_objs = {}
    all_people = get_data_from_json_file(file_location)
    for person_id, person_name in all_people.items():
        people_objs[int(person_id)] = Person(int(person_id), person_name)
    return people_objs


def add_movies_to_people_objs(people_objs: dict, movie_objs: dict) -> None:
    '''Helps initialize people objects by adding a movie_id to their
    person_movies if it does not exist already.
    :param people_objs: dict of people_ids to Person objects.
    :param movie_objs: dict of movie_ids to Movie objects.'''
    for movie_id, movie in movie_objs.items():
        for individual_id in movie.get_cast():
            if individual_id not in people_objs[individual_id].\
                    get_person_movies():
                people_objs[individual_id].update_person_movies(movie_id)


def add_points_to_people_from_movie(people_objs: dict, movie_objs: dict,
                                    round_num: int) -> None:
    '''Grab cast list for all movies and give points to person.
    For the first round the below formula is used to make sure the same
    total points are awarded to all movies. This prevents movies with small
    casts from being penalized. Each person gets a larger % of the total points
    available. After that, the movie z_score is used.
    :param people_objs: dict of people_ids to Person objects.
    :param movie_objs: dict of movie_ids to Movie objects.
    :param round_num: int to track the round.'''
    for movie in movie_objs.values():
        if round_num == 0:
            points = (1/len(movie.get_cast()) * MAX_CAST_SIZE)
        else:
            points = movie.get_z_score()
        for person_id in movie.get_cast():
            people_objs[person_id].add_point_to_person_scores(points)


def person_new_round_processesing(people_objs: dict) -> None:
    '''update_person_score() sums all movie points awarded
    from previous round.
    start_new_round() appends new empty list to the movie score
    lists for the current rounds of scores to go to.
    :param people_objs: key: person_id, value: Person object'''
    for person_id in people_objs.keys():
        people_objs[int(person_id)].update_person_score()
        people_objs[int(person_id)].start_new_round()


def update_movie_scores(movie_objs: dict, people_objs: dict):
    '''Add value from person.get_person_score() to movie
    for each actor in the movie.
    :param movie_objs: dict of Movie objects.
    :param people_objs: dict of people objects. Key = person_id,
    value = Person.'''
    for movie in movie_objs.values():
        for person in movie.cast:
            movie.receive_points_from_person(
                    people_objs[person].get_person_score())
        movie.update_movie_score()


def get_movie_score_stats(movie_objs: list) -> tuple[float, float]:
    '''Calculate the average movie score and the standard deviation of
    movie scores.'''
    scores = []
    for movie in movie_objs.values():
        scores.append(movie.get_movie_score())
    return np.mean(scores), np.std(scores)


def update_movie_z_scores(movie_objs: dict, mean_movie_score: float,
                          std_movie_score: float):
    '''Loop through all movie objects and update the z_score based on
    the current mean_movie_score and std_movie_score.
    :param movie_objs: dict[movie_ids, Movie].
    :param mean_movie_score: current average movie score.
    :param std_movie_score: standard deviation of movie score.
    '''
    for movie in movie_objs.values():
        movie.update_z_score(mean_movie_score, std_movie_score)


def check_if_futher_analysis_needed(movie_objs: dict) -> bool:
    '''Loop through all movies to see if further analysis is needed.
    This checks if the current z_score is within a certain % of the previous
    rounds' z_score. If any movie requires more calculation, it returns True
    and stops checking.
    :param: movie_objs dict[movie_id, Movie]'''
    for movie in movie_objs.values():
        if movie.needs_further_analysis():
            return True
    return False


def rank_movies(movie_objs) -> list:
    ranked_movies = sorted(movie_objs.values(),
                           key=lambda: movie_objs.values().get_movie_score())
    for movie in ranked_movies:
        print(movie.get_movie_name(), movie.get_movie_score())


def get_all_movie_scores_for_person(person_id: int,
                                    people_objs: dict,
                                    id_to_movie: dict,
                                    movie_objs: dict) -> None:
    '''Tool to help view all movies associated with a given person
    and the score of those movies.'''
    for movie_id in people_objs[person_id].get_person_movies():
        print(movie_id,
              id_to_movie[movie_id],
              movie_objs[movie_id].get_z_score())


def get_person_details_for_movie(movie: Movie, people_objs: dict):
    '''Tool to help view all people associated with a given movie
    and their current person scores.'''
    for person in movie.get_cast():
        print('\t', people_objs[person].get_person_name(),
              '\n\t\t', people_objs[person].get_person_score())


def console_reporting(movie_objs: dict, people_objs: dict) -> None:
    '''Tool to print out each movie with the score.
    If a movie is a "top movie" then additional information
    is displayed.
    :param movie_objs: dict[movie_id, Movie].
    :param people_objs: dict[people_id, Person].'''
    for movie in movie_objs.values():
        print(movie.get_movie_name(), '\n\t\t', movie.get_z_score())
        if movie.get_z_score() > 1:
            print("********TOP MOVIE********")
            get_person_details_for_movie(movie, people_objs)
    print("ROUND STOP")
    print("********************************************")
    print("********************************************")
    print("********************************************")
    print("********************************************")
    print("********************************************")


def main():
    id_to_movie: dict[int, str] = get_data_from_json_file(ID_TO_MOVIE_FILE)

    movie_objs: dict[int, Movie] = create_movie_objs(MOVIES_TO_PEOPLE_FILE,
                                                     id_to_movie)
    people_objs: dict[int, Person] = create_all_people_objs(ID_TO_PEOPLE_FILE)

    add_movies_to_people_objs(people_objs, movie_objs)

    further_analysis_needed = True
    round_num = 0
    while further_analysis_needed:
        # print(f"*********ROUND {round_num}*********")

        add_points_to_people_from_movie(people_objs, movie_objs, round_num)
        person_new_round_processesing(people_objs)
        update_movie_scores(movie_objs, people_objs)

        mean_movie_score, std_movie_score = get_movie_score_stats(movie_objs)
        update_movie_z_scores(movie_objs, mean_movie_score, std_movie_score)
        needs_further_analysis = check_if_futher_analysis_needed(movie_objs)

        # console_reporting(movie_objs, people_objs)

        if not needs_further_analysis:
            print("NO FURTHER ANALYSIS NEEDED")
            break

        round_num += 1

    movies = [movie for movie in movie_objs.values()]
    movies.sort(key=lambda movie: movie.get_z_score())
    for movie in movies:
        print(movie.get_movie_name(), movie.get_z_score())
        # if movie.get_z_score() > 1:
        get_person_details_for_movie(movie, people_objs)


if __name__ == '__main__':
    main()
