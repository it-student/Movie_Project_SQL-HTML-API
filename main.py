"""
This is the main module for the Movie Project SQL+HTML+API
It runs the CLI logic (Prompt loops, associated function calls, etc.)
imports random,
imports statistics,
imports visualization_export,
imports fuzzy_match,
imports colorama,
imports movie_storage_sql,
"""
import random  # for random movie picking
import statistics  # for movie stats
from fuzzy_match import match  # for search string missmatch-matching "fuzzy_match"
from colorama import Fore, Style  # for colored stdout
from visualization_export import save_histogram
from resources import omdb_api_handler as omdb
from movie_web_generator import generate_movie_webpage
# from movie_storage import get_movies, save_movies, add_movie, update_movie, delete_movie
import movie_storage_sql as storage

##########         INPUT HELPER FUNCTIONS START          ##########
def get_movie_from_title(user):
    """
    Asks for a title (or a fragment of it at least),
    matches it against titles given from movie_database,
    if no direct match exists, it gives back matching titles according levenshtein to choose from.
    Calls fuzzy_search().
    """
    movie_database = storage.list_movies(user)
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


def is_valid_rating(movie_rating):
    """Rating must be between 1.0 and 10.0 including"""
    return 0.9 < movie_rating <= 10.0

def is_valid_input(string_to_check):
    """Check whether string_to_check is not empty as well as not only consistent of whitespace"""
    return len(string_to_check) > 0 and not string_to_check.isspace()


def get_valid_rating_from_user(opt_pre_input = ""):
    """
    Asks user for rating 1-10 until input form user is correct.
    Calls is_valid_rating().
    """
    is_valid = False
    while not is_valid:
        try:
            input_msg = "Please enter your rating of this movie (1 - 10): "
            movie_rating = float(input(input_msg)) if opt_pre_input == "" else float(opt_pre_input)
        except ValueError as e:
            print(f"Invalid rating input! \n {e}")
            continue
        is_valid = is_valid_rating(movie_rating)
    return movie_rating


def get_valid_release_from_user(opt_pre_input = ""):
    """Asks user for year of release until input from user is in correct from."""
    is_valid = False
    while not is_valid:
        try:
            input_msg = "Please enter the release date of this movie (1900-2026): "
            release_input = int(input(input_msg))  if opt_pre_input == "" else int(opt_pre_input)
        except ValueError as e:
            print(f"Input must be numeric! \n {e}")
            continue
        is_valid = 1900 <= release_input < 2027
    return release_input


def get_user_listing_order_choice():
    """
    Prompts the user to choose how to list movies latest first or latest last.
    calls itself if user input does not equal 'f' or 'l'.
    :return order:
    """
    order = -1
    user_choice = input("Do you want to see the latest movies 'f'irst or 'l'ast (f/l): ")
    if "f" == user_choice.lower():
        pass
    elif "l" == user_choice.lower():
        order = 1
    else:
        print("couldn't understand your input, please try again")
        get_user_listing_order_choice()
    return order
##########         INPUT HELPER FUNCTIONS END          ##########

##########         MOVIE PROJECT FUNCTIONS START          ##########
def command_list_movies(user):
    """List all movies in the Movie-Database by looping through the dictionary"""
    result = ''
    movie_database = storage.list_movies(user)
    print(Fore.YELLOW + f"{len(movie_database)} movies in total \n" + Style.RESET_ALL)
    for title, movie_info in movie_database.items():
        result += f"{title} ({movie_info['year']}): {movie_info['rating']}\n"
    return result


def command_add_title(user):
    """
    asking the user for the movies title,
    collecting movie infos from omdbApi given user input of title to add,
    save it to the movie_database if API request was successful.
    """
    movie_database = storage.list_movies(user)
    available_titles = [title.lower() for title in movie_database.keys()]
    movie_title = input("Please enter the Title of the movie to add: ")
    is_valid = is_valid_input(movie_title)
    while not is_valid:
        if movie_title.lower() in available_titles:
            print(f"Movie {movie_title} already exist!")
        movie_title = input("Please enter the Title of the movie to add: ")
        is_valid = is_valid_input(movie_title)
    # movie_rating = get_valid_rating_from_user() - DEPRECATED
    # movie_release = get_valid_release_from_user() - DEPRECATED
    found_on_omdb = omdb.get_movie_infos(movie_title)
    if found_on_omdb:
        user_id = storage.get_user_id_from_username(user)
        storage.add_movie( title = movie_title,
                            rating = found_on_omdb["rating"],
                            year = found_on_omdb["year"],
                            poster = found_on_omdb["poster"],
                            user_id = user_id['user_id'])
    return ''


def command_delete_title(user):
    """
    Asking the user for the title of the movie to delete and
    delete it from movie_database if title exists in movie_database.
    Calls get_movie_from_title(movie_database)
    Calls delete_movie().
    """
    movie_title = get_movie_from_title(user)
    storage.delete_movie(movie_title, user)
    return ''


def command_update_movie_rating(user):
    """
    Asking the user for the title of the movie to update,
    then ask for the new ranking and save the new ranking
    to the movie_database if a movie with the title exists in movie_database.
    Calls get_movie_from_title(movie_database)
    Calls update_movie().
    """
    movie_title = get_movie_from_title(user)
    new_rating = float(input("Please enter a new rating to that movie: "))
    storage.update_movie(title=movie_title, rating=new_rating)
    return ''


def command_movie_stats(user):
    """
    loop through the movie_database to fetch every movies rating, append it to a new list
    and do the calculations, finally present them to the user.
    """
    result = ''
    ratings_list = [(title, info['rating']) for title, info in storage.list_movies(user).items()]
    all_ratings = [movie[1] for movie in ratings_list]
    result += f"\nAverage rating: {str(round(sum(all_ratings) / len(ratings_list), 2))}\n"
    result += f"Median rating: {statistics.median(all_ratings)}\n"
    result += f"Best movie: \
        {[movie for movie in ratings_list if movie[1] == max(all_ratings)].pop()}\n"
    result += f"Worst movie: \
        {[movie for movie in ratings_list if movie[1] == min(all_ratings)].pop()}\n"
    return result


def command_random_movie(user):
    """
    get a random number between 0 and number of movies in movie_database,
    select the movie according the random number generated and return it to the user.
    """
    movie_database = storage.list_movies(user)
    picked_movie = random.randrange(0, len(movie_database))
    movies_enumerated_list = list(enumerate(movie_database.items()))
    title = movies_enumerated_list[picked_movie][1][0]
    movie_info = movies_enumerated_list[picked_movie][1][1]
    return f"{title} ({movie_info['year']}): {movie_info['rating']}"


def command_search_movie(user):
    """
    Asks the user for (at least a part of) the title, searches the movie_database
    for it and returns all finds from the movie_database.
    calls fuzzy_match().
    """
    result = ''
    movie_database = storage.list_movies(user)
    movie_titles = list(movie_database.keys())
    lower_movie_titles = [title.lower() for title in movie_titles]
    search_string = input(Fore.BLUE + \
    "Please enter a part of the title you want to search for: " + Style.RESET_ALL)
    if len(search_string) > 0:
        lowered_search_str = search_string.lower()
        if lowered_search_str in lower_movie_titles:
            movie_infos = movie_database[movie_titles[lower_movie_titles.index(lowered_search_str)]]
            result += f"{search_string}, {movie_infos['rating']} ({movie_infos['year']})"
        else:
            for fuzzy_matching_index in fuzzy_search(lowered_search_str, lower_movie_titles):
                result += movie_titles[fuzzy_matching_index] + "\n"
            print(Fore.RED + f"'{search_string}'? Did you mean:" \
            + Style.RESET_ALL)
    else:
        result += "No Title typed in to search..."
    return result


def command_list_by_rating(user):
    """Reorder the movies inside movie_database by their rating and return them."""
    result = ''
    movie_database = storage.list_movies(user)
    for title, movie_info in sorted(movie_database.items(), key = lambda x : x[1]['rating'])[::-1]:
        result += f"{title} ({movie_info['year']}): {movie_info['rating']}\n"
    return result


def command_list_by_release(user):
    """Reorder the movies inside movie_database by their release and return them."""
    result = ''
    movie_database = storage.list_movies(user)
    order = get_user_listing_order_choice()
    #This loop is just a little helper, because the movies don't always have a year of release.
    for title, movie_info in movie_database.items():
        if movie_info['year'] == "":
            movie_info['year'] = "0"

    for title, movie_info in sorted(movie_database.items(),
                                    key = lambda x : int(x[1]['year']))[::order]:
        result += f"{title} ({movie_info['year']}): {movie_info['rating']}\n"
    return result


def command_filter_movies(user):
    """
    Asks user of min_rating, min_year, as well as max_year as filter criteria.
    No input is allowed and will be treated as not a criteria to filter.
    """
    result = ''
    movie_database = storage.list_movies(user)
    rating_input = input("Enter minimum rating (leave blank for no minimum rating): ")
    min_rating = get_valid_rating_from_user(rating_input) if len(rating_input) > 0 else 1.0

    min_year_input = input("Enter start year (leave blank for no start year): ")
    min_year = get_valid_release_from_user(min_year_input) if len(min_year_input) > 0 else 0

    max_year_input = input("Enter end year (leave blank for no end year): ")
    max_year = get_valid_release_from_user(max_year_input) if len(max_year_input) > 0 else 2026

    #This loop is just a little helper, because the movies don't always have a year of release.
    for title, movie_info in movie_database.items():
        if movie_info['year'] == "":
            movie_info['year'] = "0"

    filtered_movies = sorted(movie_database.items(), key = lambda x : x[1]['rating'])[::-1]
    for title, movie_info in filtered_movies:
        result += f"{title} ({movie_info['year']}): {movie_info['rating']}\n" if \
        min_year <= int(movie_info['year']) < max_year + 1 and \
        movie_info['rating'] >= min_rating else ""

    return "Filtered Movies:\n" + result


def command_save_histogram(user):
    """
    Fetch every movie's rating, put it into an array and create a histogram.
    In order for the user to find it, ask the user for the filename (without extension).
    """
    movie_database = storage.list_movies(user)
    return save_histogram(movie_database)

def command_generate_webpage(user):
    """
    dynamically generate a webpage for with each movie in the database shown.
    :return success_msg: A simple str with a message of the webpage being generated.
    """
    movies = storage.list_movies(user)
    return generate_movie_webpage(movies)

def command_switch_current_user(_):
    """show list of users and prompt for choice, if is valid choice, return choice."""
    next_user = pick_a_user_or_create()
    print("Switched to user:", next_user)
    return next_user


def command_quit_program(_):
    """
    returns the string that's matching the break condition in main()
    """
    return 'Bye!'


AVAILABLE_ACTIONS = {
  0 : command_quit_program,
  1 : command_list_movies,
  2 : command_add_title,
  3 : command_delete_title,
  4 : command_movie_stats,
  5 : command_random_movie,
  6 : command_search_movie,
  7 : command_list_by_rating,
  8 : command_list_by_release,
  9 : command_filter_movies,
  10 : command_save_histogram,
  11 : command_generate_webpage,
  12 : command_switch_current_user
}

def show_menu(user):
    """
    Prompts the user to choose an action from AVAILABLE_ACTIONS and calls it.
    calls function dispatch hooked functions within AVAILABLE_ACTIONS.
    """
    print(Fore.GREEN + "********** My Movies Database **********")
    print(f"Welcome back, {user}! 🎬" + Style.RESET_ALL)
    print(Fore.CYAN + "Menu:")
    for action_index, action_name in AVAILABLE_ACTIONS.items():
        action_name = str(action_name)[10:str(action_name).find(' at ')]
        print(f"{str(action_index)}. {action_name}")
    print(Style.RESET_ALL)
    return

def show_user_list():
    """List all users in the Movie-Database by looping through the dictionary"""
    user_database = storage.list_users()
    print(Fore.CYAN + f"{len(user_database)} users in total \n")
    for index in range(len(user_database)):
        print(f"{index} : {user_database[index]}")
    return user_database

def pick_a_user_or_create():
    curr_usr = None
    while curr_usr is None:
        users = show_user_list()
        if len(users) > 0:
            print(f"{len(users)} : Create new User\n")
            try:
                user_chosen = int(input(Fore.BLUE + f"Enter choice (0-{len(users)}): " + Style.RESET_ALL))
                if valid_user_pick(user_chosen):
                    curr_usr = users[user_chosen]
                elif user_chosen == len(users):
                    storage.add_user(input(Fore.BLUE + "Add username of new user: " + Style.RESET_ALL))
                else:
                    print("Invalid choice. Try again...")
                    continue
            except ValueError:
                print(f"Given input needs to be a number, not a text please! Try again...")
            except IndexError:
                print(f"Number to type in must be within Range of 0-{len(users)}. Try again...")
        else:
            storage.add_user(input(Fore.BLUE + "Add username of new user: " + Style.RESET_ALL))
    return curr_usr


def valid_user_pick(user_chosen):
    """ Get all users from database and check whether given choice is within valid range"""
    users = storage.list_users()
    return 0 <= user_chosen < len(users)

def main():
    users = storage.list_users()
    """Main function logik"""
    # First let's choose a user or create one
    print(Fore.CYAN + "********** WELCOME to My Movies Database **********" + Style.RESET_ALL)
    chosen_user = pick_a_user_or_create()
    curr_usr = chosen_user
    # Main Movie Project loop
    while True:
        show_menu(curr_usr)
        try:
            action_to_take = int(input(Fore.BLUE + "\nEnter choice (0-12): " + Style.RESET_ALL))
        except ValueError:
            print("Given input needs to be a number, not a text please! Try again...")
            continue
        print()
        return_val = AVAILABLE_ACTIONS[action_to_take](curr_usr)
        print(Fore.YELLOW + return_val + Style.RESET_ALL)
        if return_val != 'Bye!':
            input(Fore.BLUE + f"Press enter to continue, {curr_usr}" + Style.RESET_ALL)
            if return_val in users:
                curr_usr = return_val
        else:
            break


if __name__ == "__main__":
    main()
