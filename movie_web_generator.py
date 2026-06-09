"""
This module is for showing the movies inside movies.db on a webpage.
It acts as a generator using _static/index_template.html as a base template.
"""

BASE_TEMPLATE_PATH = '_static/'
BASE_TEMPLATE = 'index_template.html'
BASE_TITLE = 'My Favorite Movies'

def load_html_template(template_filename) -> str:
    """ Loads an HTML template file """
    with open(BASE_TEMPLATE_PATH + template_filename, 'r', encoding='utf-8') as template_file:
        return template_file.read()

def generate_final_html(html_string: str) -> None:
    """ Generates | overwrites final HTML file 'index.html' """
    with open("./index.html", "w", encoding='utf-8') as file:
        file.write(html_string)

def populate_movie_cards(movies):
    """ Populates recursively movie cards iterating through movies """
    result = ''
    # load movie_card_template.html
    card_template = load_html_template('movie_card_template.html')
    for movie, infos in movies.items():
        poster_filled = card_template.replace("__poster__", infos['poster'])
        title_filled = poster_filled.replace("__title__", movie)
        card_filled = title_filled.replace("__year__", str(infos['year']))
        result += card_filled + '\n'
    return result

def populate_main_page(movies):
    """ Populates main page template's Title and Movie cards grid """
    # load template file
    template = load_html_template(BASE_TEMPLATE)
    # Set the Webpage Title
    title_filled = template.replace('__TEMPLATE_TITLE__', BASE_TITLE)
    # load movie cards
    movie_cards = populate_movie_cards(movies)
    template_filled = title_filled.replace('__TEMPLATE_MOVIE_GRID__', movie_cards)
    return template_filled

def generate_movie_webpage(movies):
    """
    Generates | overwrites final HTML file 'index.html'
    by populating the main page template with a set Title and several movie_cards
    according movie inside 'movies' parameter.
    :param movies: Dictionary of movie information
    :return: success string message
    """
    generated_html = populate_main_page(movies)
    generate_final_html(generated_html)
    return "Website was generated successfully."
