import random                     # for random movie picking
import statistics                 # for movie stats
import matplotlib.pyplot as plt   # for histogram creation
from fuzzy_match import match     # for search string missmatch-matching "fuzzy_match"
from colorama import Fore, Style  # for colored stdout 

def list_movies(movie_database:dict):
  result = ''
  print(Fore.YELLOW + f"{len(movie_database)} movies in total" + Style.RESET_ALL)
  for movie, rating in movie_database.items():
    result += f"{movie}: {rating}\n"
  
  return result

def add_movie(movie_database:dict):
  movie_title = input("Please enter the Title of the movie to add: ")
  movie_rating = float(input("Please enter your rating of this movie (1 - 10): "))
  movie_database[movie_title] = movie_rating
  return f"{movie_title}, {movie_rating} - added to the Movie-Database"


def delete_movie(movie_database:dict):
  movie_to_delete = input("Please enter the title of the movie you want to delete: ")
  if movie_to_delete in movie_database:
    del movie_database[movie_to_delete]
    return f"{movie_to_delete} - deleted"
  else:
    print("The movie you typed in doesn't exist in the Movie-Database")


def update_movie(movie_database:dict):
  movie_to_update = input("Please enter the title of the movie you want to update: ")
  if movie_to_update in movie_database:
    new_rating = float(input("Please enter a new rating to that movie: "))
    movie_database[movie_to_update] = new_rating
    return f"{movie_to_update}'s new rate is: {new_rating}"
  else:
    print("The movie you typed in doesn't exist in the Movie-Database")


def movie_stats(movie_database:dict):
  result = ''
  ratings_list = []
  for rating in movie_database.values():
    ratings_list.append(rating)
  sum_of_ratings = sum(ratings_list)
  result += f"\nAverage rating: {str(round(sum_of_ratings / len(movie_database), 2))}\n"
  result += f"Median rating: {statistics.median(ratings_list)}\n"
  result += f"Best movie: {max(ratings_list)}\n"
  result += f"Worst movie: {min(ratings_list)}\n"
  return result


def random_movie(movie_database:dict):
  picked_movie = random.randrange(0,len(movie_database))
  step = 0
  for movie, rating in movies.items():
    if step == picked_movie:
      return movie, rating
    step += 1

def fuzzy_search(string_to_match, list_of_possible_matching_strings):
  result = ''
  fuzzy_matches = match.extract(string_to_match, list_of_possible_matching_strings, match_type='levenshtein', score_cutoff=0.3)
  for matching in fuzzy_matches:
    result += matching[0]
  return result

def search_movie(movie_database:dict):
  result = ''
  movie_titles = movie_database.keys()
  search_string = input(Fore.BLUE + "Please enter a part of the title you want to search for: " + Style.RESET_ALL)
  findings = f"Enter part of the movie name: {search_string}\n"
  for movie in movie_database.keys():
    if search_string.lower() in movie.lower():
      result += f"{movie}, {movie_database[movie]}\n"
  if result == '':
    print(Fore.RED + f"The movie '{search_string}' does not exist. Did you mean:" + Style.RESET_ALL)
    result += fuzzy_search(search_string, movie_titles)
  return result


def list_by_rating(movie_database:dict):
  result = ''
  list_of_tuples = []
  # insert movie tuples according their rating
  for movie in movie_database.items():
    if len(list_of_tuples) > 0:
      # loop through tuples inside list_of_tuples in order to find the right index to insert the movie
      for i in range(len(list_of_tuples)):
        if i + 1 < len(list_of_tuples):
          if list_of_tuples[i][1] > movie[1]:
            continue
          elif list_of_tuples[i][1] <= movie[1]:
            list_of_tuples.insert(i, movie)
            break
        else:
          if list_of_tuples[i][1] <= movie[1]:
            list_of_tuples.insert(i, movie)
          else:
            list_of_tuples.append(movie)
    else:
      list_of_tuples.append(movie)
  # now put movies being sorted into a string and return that string
  for movie, rating in list_of_tuples:
    result += f"{movie}, {rating}\n"
  return result

def save_histogram(movie_database:dict):
  movie_array = list(movie_database.values())
  xmin = 0.1
  xmax = 10.0
  ymin = 0
  ymax = len(movie_database)
  plt.axis([xmin, xmax, ymin, ymax])
  plt.hist(movie_array)
  font1 = {'family':'serif','color':'blue','size':20}
  font2 = {'family':'serif','color':'darkred','size':15}
  plt.title("Movie Ratings Histogram", fontdict = font1)
  plt.xlabel("Movie Rating 1 - 10", fontdict = font2)
  plt.ylabel("Quantity of those ratings given", fontdict = font2)
  file_name = input("Please enter the filename under which the histogram should be saved: ")
  plt.savefig(fname = f"./{file_name}.png", dpi='figure', format='png')
  return f"Histogram saved as '{file_name}' to your current working directory!"

def main():
  # Dictionary to store the movies and the rating
  movies = {
    "The Shawshank Redemption": 9.5,
    "Pulp Fiction": 8.8,
    "The Room": 3.6,
    "The Godfather": 9.2,
    "The Godfather: Part II": 9.0,
    "The Dark Knight": 9.0,
    "12 Angry Men": 8.9,
    "Everything Everywhere All At Once": 8.9,
    "Forrest Gump": 8.8,
    "Star Wars: Episode V": 8.7,
  }

  # Your code here
  action_to_take = 9
  while True:
    print(Fore.GREEN + "********** My Movies Database **********")
    print(Style.RESET_ALL)
    print(Fore.CYAN + "Menu:\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n8. Movies sorted by rating\n9. Create Rating Histogram")
    print(Style.RESET_ALL)
    action_to_take = int(input(Fore.BLUE + "\nEnter choice (1-8): " + Style.RESET_ALL))
    if action_to_take == 1:
      print()
      print(Fore.YELLOW + list_movies(movies) + Style.RESET_ALL)
      input(Fore.BLUE + "Press enter to continue" + Style.RESET_ALL)
    elif action_to_take == 2:
      print()
      print(Fore.YELLOW + add_movie(movies) + Style.RESET_ALL)
      input(Fore.BLUE + "Press enter to continue" + Style.RESET_ALL)
    elif action_to_take == 3:
      print()
      print(Fore.YELLOW + delete_movie(movies) + Style.RESET_ALL)
      input(Fore.BLUE + "Press enter to continue" + Style.RESET_ALL)
    elif action_to_take == 4:
      print()
      print(Fore.YELLOW + update_movie(movies) + Style.RESET_ALL)
      input(Fore.BLUE + "Press enter to continue" + Style.RESET_ALL)
    elif action_to_take == 5:
      print()
      print(Fore.YELLOW + movie_stats(movies) + Style.RESET_ALL)
      input(Fore.BLUE + "Press enter to continue" + Style.RESET_ALL)
    elif action_to_take == 6:
      print()
      print(Fore.YELLOW + random_movie(movies) + Style.RESET_ALL)
      input(Fore.BLUE + "Press enter to continue" + Style.RESET_ALL)
    elif action_to_take == 7:
      print()
      print(Fore.YELLOW + search_movie(movies) + Style.RESET_ALL)
      input(Fore.BLUE + "Press enter to continue" + Style.RESET_ALL)
    elif action_to_take == 8:
      print()
      print(Fore.YELLOW + list_by_rating(movies) + Style.RESET_ALL)
      input(Fore.BLUE + "Press enter to continue" + Style.RESET_ALL)
    elif action_to_take == 9:
      print()
      print(Fore.YELLOW + save_histogram(movies) + Style.RESET_ALL)
      input(Fore.BLUE + "Press enter to continue" + Style.RESET_ALL)
    else:
      continue

if __name__ == "__main__":
  main()
