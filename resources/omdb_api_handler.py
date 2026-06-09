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
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env", verbose=True)
# required for this module to work
os.getenv('OMDB_API_KEY')
BASE = os.getenv('BASE_URL')

# res = requests.get(BASE, params={'apikey': KEY, 't': "The Beekeeper"})

def is_connection_healthy(response):
    """
    This function is for checking the connection with omdbApi given the response.status_code.
    Returns True if the connection is healthy, False otherwise with a print of the response-error.
    :param response:
    :return Boolean:
    """
    if response.status_code != 200:
        print(f"Error getting movie infos: {response.status_code}: {response.json().get('Response')}")
        return False
    else:
        return True

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
    res = requests.get(BASE, params={'apikey': KEY, 't': movie_title})
    if not is_connection_healthy(res):
        pass
    else:
        response_json = res.json()
        if response_json.get('Response'):
            found_title = response_json.get('Title')
            if found_title == movie_title:
                found_year = response_json.get('Year')
                if response_json.get('imdbRating') is not None:
                    if response_json.get('imdbRating') != 'N/A':
                        found_rating = response_json.get('imdbRating')
                    else:
                        found_rating = -1
                else:
                    found_rating = -1
                found_poster = response_json.get('Poster')
                found_movie_infos = {'year': int(found_year),
                                    'rating': float(found_rating),
                                    'poster': found_poster}
            else:
                print(f"Error getting movie infos, found title: '{found_title}' doesn't \
match searched title: '{movie_title}'")
        else:
            print(f"Error getting movie infos: {response_json.get('Error')}")
    return found_movie_infos