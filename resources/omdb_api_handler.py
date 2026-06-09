"""
This module is for the connection of this Application to the omdbApi-Application.
It handles and prepares requests and handles responses according to the API.
Imports requests.
Imports JSON.
Imports dotenv
requires 'OMDB_API_KEY' and 'BASE_URL' environment variables.
"""
import os
import requests
from requests.exceptions import RequestException
from retrying import retry
from dotenv import load_dotenv

# load_dotenv(dotenv_path="../.env", verbose=True)
load_dotenv(verbose=True)
# required for this module to work
KEY = os.getenv('OMDB_API_KEY')
BASE = os.getenv('BASE_URL')

# res = requests.get(BASE, params={'apikey': KEY, 't': "The Beekeeper"})

def is_connection_healthy(response):
    """
    This function is for checking the connection with omdbApi given the response.status_code.
    Returns True if the connection is healthy, False otherwise.
    :param response:
    :return Boolean:
    """
    return response.status_code == 200


@retry(wait_exponential_multiplier=500, stop_max_attempt_number=5)
def call_api(params: dict):
    """
    This function is for calling omdb api using the requests library.
    Within params the API-Key is needed, as well as the OMDB method
    (i.e. 't' for specific title search. 'i' for imdbID search,
    'S' for broader titles matching the query-string).
    :param params:
    :return res:
    """
    res = {}
    try:
        res = requests.get(BASE, params=params, timeout=10.0)
    except RequestException as e:
        print(e)
    return res


def extract_infos_from_api_response(response_json):
    """
    This function is for extracting infos from OMDB API response.
    :param response_json: already mapped into JSON-data
    :return:
    """
    result = {'title': response_json.get('Title'),
              'year': response_json.get('Year'),
              'poster': response_json.get('Poster')}
    if response_json.get('imdbRating') is not None:
        if response_json.get('imdbRating') != 'N/A':
            result['rating'] = response_json.get('imdbRating')
        else:
            result['rating'] = -1
    else:
        result['rating'] = -1
    return result


def get_movie_infos(movie_title):
    """
    This function is for requesting information about a movie from imdbApi given the title.
    Rating, Year of release, poster-img URL will get extracted from the OMDB API response.
    Returns empty dictionary if no information is available.
    found information will get returned as a dictionary.
    :param movie_title:
    :return movie_infos:
    """
    found_movie_infos = {}
    res = call_api({'apikey': KEY, 't': movie_title})
    if res and is_connection_healthy(res):
        response_json = res.json()
        if response_json.get('Response'):
            found_movie_infos = extract_infos_from_api_response(response_json)
            if found_movie_infos['title'] == movie_title:
                pass
            else:
                print(f"Error getting movie infos, found title:\
                 '{found_movie_infos['title']}' doesn't match searched title: '{movie_title}'")
                found_movie_infos = {}
        else:
            print(f"Error getting movie infos: {response_json.get('Error')}")
    else:
        e_msg = res.status_code if res else 'No Connection established'
        print(f"Error getting movie infos: {e_msg}")
    return found_movie_infos
