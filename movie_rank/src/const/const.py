import os
import sys
sys.path.append('..')
sys.path.append('.')


def get_key() -> str:
    with open(f"{PROJECT_LOCATION}/src/const/api.key", 'r') as key_in:
        key = key_in.read().strip('\n')
    return key


PROJECT_LOCATION = '/home/john/git/whm/movie_rank'
API_URL_BASE = 'https://api.themoviedb.org/3'
API_MOVIE_SEARCH = f"{API_URL_BASE}/search/movie?api_key={get_key()}&query="
API_GET_CREDITS = f'''{API_URL_BASE}/movie/@/credits?api_key={get_key()}&language=en-US'''
MAX_CAST_SIZE = 75
