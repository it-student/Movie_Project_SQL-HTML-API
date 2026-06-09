"""
This module is for data visualization exports like Diagrams, Graphs, etc.
It currently features only Histogram-like exports of movies inside given Dataset ordered by rating.
created file type will be '.png'
"""
import matplotlib.pyplot as plt

def save_histogram(movie_database):
    """
    Fetch every movie's rating, put it into an array and create a histogram.
    In order for the user to find it, ask the user for the filename (without extension).
    """
    movie_info_array = list(movie_database.values())
    movie_rating_array = [movie['rating'] for movie in movie_info_array]
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
    plt.savefig(fname=f"./_static/{file_name}.png", dpi='figure', format='png')
    return f"Histogram saved as '{file_name}' to your 'static' working directory!"
