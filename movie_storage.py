import json


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open("data.json", "r") as fileobj:
       data = json.loads(fileobj.read())

    return data
      

def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    json_string = json.dumps(movies)
    with open("data.json", "w") as fileobj:
      fileobj.write(json_string)
    return True


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title] = { "rating" : rating, "year" : year }
    save_movies(movies)
    return title, movies[title]


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    del_movie = movies.pop(title)
    save_movies(movies)
    return del_movie



def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movie_to_update = movies[title]
    movie_to_update['rating'] = rating
    save_movies(movies)
    return title, movies[title]
  