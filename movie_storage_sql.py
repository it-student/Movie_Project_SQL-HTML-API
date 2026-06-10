from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT NOT NULL,
            CONSTRAINT fk_user
            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
    """))
    connection.commit()
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL
        )
    """))
    connection.commit()

def list_users():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT username FROM users")).fetchall()

    return [row[0] for row in result]

def add_user(username):
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO users (username) VALUES (:username)"),
                               {"username": username})
            connection.commit()
            print(f"User '{username}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def get_user_id_from_username(username):
    with engine.connect() as connection:
        try:
            user_id = connection.execute(text("SELECT id FROM users WHERE username = :username"),
                               {"username": username}).fetchall()
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        return {'user_id': row[0] for row in user_id}

def list_movies(username):
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies \
JOIN users ON users.id = movies.user_id WHERE users.username = :username"),
                                    {"username": username})
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}

def add_movie(title, year, rating, poster, user_id):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies (title, year, rating, poster, user_id) \
VALUES (:title, :year, :rating, :poster, :user_id)"),
        {"title": title, "year": year, "rating": rating, "poster": poster, "user_id": user_id})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def delete_movie(title, username):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"),
                               {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :rating  WHERE title = :title"),
                               {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully with rating {rating}.")
        except Exception as e:
            print(f"Error: {e}")