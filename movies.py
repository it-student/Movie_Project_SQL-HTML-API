import random  # for random movie picking
import statistics  # for movie stats
import matplotlib.pyplot as plt  # for histogram creation
from fuzzy_match import match  # for search string missmatch-matching "fuzzy_match"
from colorama import Fore, Style  # for colored stdout
from movie_storage import get_movies, save_movies, add_movie, update_movie, delete_movie

##########         INPUT HELPER FUNCTIONS START          ##########
def get_movie_from_title(movie_database : dict):
    """
    Asks for a title (or a fragment of it at least),
    matches it against titles given from movie_database,
    if no direct match exists, it gives back matching titles according levenshtein to choose from.
    Calls fuzzy_search().
    """
    movie_titles = list(movie_database.keys())
    lower_movie_titles = [title.lower() for title in movie_titles]
    movie_title = input("Please enter the title of the movie: ")
    while not movie_title in movie_database:
        print("The movie you typed in doesn't exist in the Movie-Database")
        print(Fore.RED + f"'{movie_title}'? Did you mean:" \
        + Style.RESET_ALL)
        for fuzzy_matching_index in fuzzy_search(movie_title.lower(), lower_movie_titles):
            print(movie_titles[fuzzy_matching_index])
        movie_title = input("Please enter the title of the movie you want to delete: ")
    return movie_title


def is_valid_rating(movie_rating):
    """Rating must be between 1.0 and 10.0 including"""
    return 0.9 < movie_rating <= 10.0

def is_valid_input(string_to_check):
    """Check whether string_to_check is not empty as well as not only consistent of whitespace"""
    return len(string_to_check) > 0 and not string_to_check.isspace()


def get_valid_rating_from_user(optional_pre_input = ""):
    """
    Asks user for rating 1-10 until input form user is correct.
    Calls is_valid_rating().
    """
    is_valid = False
    while not is_valid:
        try:
            movie_rating = float(input("Please enter your rating of this movie (1 - 10): ")) if optional_pre_input == "" else float(optional_pre_input)
        except ValueError as e:
            print(f"Invalid rating input! \n {e}")
            continue
        is_valid = is_valid_rating(movie_rating)
    return movie_rating


def get_valid_release_from_user(optional_pre_input = ""):
    """Asks user for year of release until input from user is in correct from."""
    is_valid = False
    while not is_valid:
        try:
            release_input = int(input("Please enter the release date of this movie (1900-2026): "))  if optional_pre_input == "" else int(optional_pre_input)
        except ValueError as e:
            print(f"Input must be numeric! \n {e}")
            continue
        is_valid = 1900 <= release_input < 2027
    return release_input


def get_user_listing_order_choice():
    user_choice = input("Do you want to see the latest movies listet 'f'irst or 'l'ast (f or l): ")
    is_f_or_l = False
    while not is_f_or_l:
        if "f" in user_choice:
            order = -1
            is_f_or_l = True
        elif "l" in user_choice:
            order = 1
            is_f_or_l = True
        else:
            print("couldn't understand your input, please try again")
            user_choice = input("Do you want to see the latest movies listet 'f'irst or 'l'ast (f or l): ")
    return order
##########         INPUT HELPER FUNCTIONS END          ##########

##########         MOVIE PROJECT FUNCTIONS START          ##########
def list_movies(movie_database: dict):
    """List all movies in the Movie-Database by looping through the dictionary"""
    result = ''
    print(Fore.YELLOW + f"{len(movie_database)} movies in total" + Style.RESET_ALL)
    for title, movie_info in movie_database.items():
        result += f"{title}: {movie_info['rating']} ({movie_info['year']})\n"
    return result


def add_title(movie_database: dict):
    """
    asking the user for the movies title, rating and year of release
    and save it to the movie_database.
    Calls get_valid_rating_from_user().
    Calls get_valid_release_from_user().
    """
    available_titles = [title.lower() for title in movie_database.keys()]
    movie_title = input("Please enter the Title of the movie to add: ")
    is_valid = is_valid_input(movie_title)
    while not is_valid:
        if movie_title.lower() in available_titles:
            print(f"Movie {movie_title} already exist!")
        movie_title = input("Please enter the Title of the movie to add: ")
        is_valid = is_valid_input(movie_title)
    movie_rating = get_valid_rating_from_user()
    movie_release = get_valid_release_from_user()
    added_title, added_infos = add_movie( title = movie_title,
                                          rating = movie_rating,
                                          year = movie_release )
    return f"{added_title}, {added_infos['rating']} ({added_infos['year']})- added to the Movie-Database"


def delete_title(movie_database: dict):
    """
    Asking the user for the title of the movie to delete and
    delete it from movie_database if title exists in movie_database.
    Calls get_movie_from_title(movie_database)
    Calls delete_movie().
    """
    movie_title = get_movie_from_title(movie_database)
    movie_infos = delete_movie(movie_title)
    result = f"{movie_title}, {movie_infos['rating']} ({movie_infos['year']}) - deleted"
    return result


def update_movie_rating(movie_database: dict):
    """
    Asking the user for the title of the movie to update,
    then ask for the new ranking and save the new ranking
    to the movie_database if a movie with the title exists in movie_database.
    Calls get_movie_from_title(movie_database)
    Calls update_movie().
    """
    movie_title = get_movie_from_title(movie_database)
    new_rating = float(input("Please enter a new rating to that movie: "))
    updated_title, movie_infos = update_movie(movie_title, new_rating)
    result = f"{updated_title}'s new rate is: {movie_infos['rating']}"
    return result


def movie_stats(movie_database: dict):
    """
    loop through the movie_database to fetch every movies rating, append it to a new list
    and do the calculations, finally present them to the user.
    """
    result = ''
    ratings_list = []
    for movie_info in movie_database.values():
        ratings_list.append(movie_info["rating"])
    sum_of_ratings = sum(ratings_list)
    result += f"\nAverage rating: {str(round(sum_of_ratings / len(movie_database), 2))}\n"
    result += f"Median rating: {statistics.median(ratings_list)}\n"
    result += f"Best movie: {max(ratings_list)}\n"
    result += f"Worst movie: {min(ratings_list)}\n"
    return result


def random_movie(movie_database: dict):
    """
    get a random number between 0 and number of movies in movie_database,
    select the movie according the random number generated and return it to the user.
    """
    picked_movie = random.randrange(0, len(movie_database))
    movies_enumerated_list = list(enumerate(movie_database.items()))
    title = movies_enumerated_list[picked_movie][1][0]
    movie_info = movies_enumerated_list[picked_movie][1][1]
    return f"{title}, {movie_info['rating']} ({movie_info['year']})"



def fuzzy_search(string_to_match, list_of_possible_matching_strings):
    """implementation of fuzzy match according levenshtein's match type"""
    result = []
    fuzzy_matches = match.extract(string_to_match,
                                  list_of_possible_matching_strings,
                                  match_type='levenshtein',
                                  score_cutoff=0.3)
    for matching in fuzzy_matches:
        result.append(list_of_possible_matching_strings.index(matching[0]))
    return result


def search_movie(movie_database: dict):
    """
    Asks the user for (at least a part of) the title, searches the movie_database
    for it and returns all finds from the movie_database.
    calls fuzzy_match().
    """
    result = ''
    movie_titles = list(movie_database.keys())
    lower_movie_titles = [title.lower() for title in movie_titles]
    search_string = input(Fore.BLUE + \
    "Please enter a part of the title you want to search for: " + Style.RESET_ALL)
    if len(search_string) > 0:
        lowered_search_string = search_string.lower()
        if lowered_search_string in lower_movie_titles:
            movie_infos = movie_database[movie_titles[lower_movie_titles.index(lowered_search_string)]]
            result += f"{search_string}, {movie_infos['rating']} ({movie_infos['year']})"
        else:
            for fuzzy_matching_index in fuzzy_search(lowered_search_string, lower_movie_titles):
                result += movie_titles[fuzzy_matching_index] + "\n"
            print(Fore.RED + f"'{search_string}'? Did you mean:" \
            + Style.RESET_ALL)
    else:
        result += "No Title typed in to search..."
    return result


def list_by_rating(movie_database: dict):
    """Reorder the movies inside movie_database by sorting according their rating and return them."""
    result = ''
    for title, movie_info in sorted(movie_database.items(), key = lambda x : x[1]['rating'])[::-1]:
        result += f"{title}, {movie_info['rating']} ({movie_info['year']})\n"
    return result


def list_by_release(movie_database: dict):
    """Reorder the movies inside movie_database by sorting according their release and return them."""
    result = ''
    order = get_user_listing_order_choice()
    #This loop is just a little helper, because the movies given in the dict didnt have a year of release.
    for title, movie_info in movie_database.items():
        if movie_info['year'] == "":
            movie_info['year'] = "0"

    for title, movie_info in sorted(movie_database.items(), key = lambda x : int(x[1]['year']))[::order]:
        result += f"{title}, {movie_info['rating']} ({movie_info['year']})\n"
    return result


def filter_movies(movie_database : dict):
    """
    Asks user of min_rating, min_year, as well as max_year as filter criterias.
    No input is allowed and will be treatet as not a criteria to filter.
    """
    result = ''
    rating_input = input("Enter minimum rating (leave blank for no minimum rating): ")
    min_rating = get_valid_rating_from_user(rating_input) if len(rating_input) > 0 else 1.0

    min_year_input = input("Enter start year (leave blank for no start year): ")
    min_year = get_valid_release_from_user(min_year_input) if len(min_year_input) > 0 else 0

    max_year_input = input("Enter end year (leave blank for no end year): ")
    max_year = get_valid_release_from_user(max_year_input) if len(max_year_input) > 0 else 2026

    #This loop is just a little helper, because the movies given in the dict didnt have a year of release.
    for title, movie_info in movie_database.items():
        if movie_info['year'] == "":
            movie_info['year'] = "0"

    filtered_movies = sorted(movie_database.items(), key = lambda x : x[1]['rating'])[::-1]
    for title, movie_info in filtered_movies:
        result += f"{title} ({movie_info['year']}): {movie_info['rating']}\n" if \
        min_year <= int(movie_info['year']) < max_year + 1 and \
        movie_info['rating'] >= min_rating else ""

    return "Filtered Movies:\n" + result


def save_histogram(movie_database: dict):
    """
    Fetch every movie's rating, put it into an array and create a histogram.
    In order for the user to find it, ask the user for the filename (without extension).
    """
    movie_info_array = list(movie_database.values())
    movie_rating_array = []
    for movie_info in movie_info_array:
        movie_rating_array.append(movie_info['rating'])
    xmin = 0.1
    xmax = 10.0
    ymin = 0.0
    ymax = float(len(movie_database))
    plt.axis((xmin, xmax, ymin, ymax))
    plt.hist(movie_rating_array)
    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}
    plt.title("Movie Ratings Histogram", fontdict=font1)
    plt.xlabel("Movie Rating 1 - 10", fontdict=font2)
    plt.ylabel("Quantity of those ratings given", fontdict=font2)
    file_name = input("Please enter the filename (without extension, i.e. NO '.png'): ")
    plt.savefig(fname=f"./{file_name}.png", dpi='figure', format='png')
    return f"Histogram saved as '{file_name}' to your current working directory!"


def quit_program(movie_database):
    """
    Saves the Database for persistency.
    Calls save_movies().
    returns the string thats matching the break condition in main()
    """
    ready_to_quit = save_movies(movie_database)
    if ready_to_quit:
        result = 'Bye!'
    else:
        result = 'Something went wrong during the saving process :('
    return result


AVAILABLE_ACTIONS = {
  0 : quit_program,
  1 : list_movies,
  2 : add_title,
  3 : delete_title,
  4 : update_movie_rating,
  5 : movie_stats,
  6 : random_movie,
  7 : search_movie,
  8 : list_by_rating,
  9 : list_by_release,
  10 : filter_movies,
  11 : save_histogram,
}


def show_menu():
    print(Fore.GREEN + "********** My Movies Database **********")
    print(Style.RESET_ALL)
    print(Fore.CYAN + "Menu:")
    for action_index, action_name in AVAILABLE_ACTIONS.items():
        action_name = str(action_name)[10:str(action_name).find(' at ')]
        print(f"{str(action_index)}. {action_name}")
    print(Style.RESET_ALL)


def main():
    """Main function logik"""
    # Your code here
    while True:
        movies = get_movies()
        show_menu()
        try:
            action_to_take = int(input(Fore.BLUE + "\nEnter choice (0-9): " + Style.RESET_ALL))
        except ValueError:
            print(f"Given input needs to be a number, not a text please! Try again...")
            continue
        print()
        return_val = AVAILABLE_ACTIONS[action_to_take](movies)
        print(Fore.YELLOW + return_val + Style.RESET_ALL)
        if return_val != 'Bye!':
            input(Fore.BLUE + "Press enter to continue" + Style.RESET_ALL)
        else:
            break


if __name__ == "__main__":
    main()
