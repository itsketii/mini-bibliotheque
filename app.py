from flask import Flask, jsonify, request, redirect
import sqlite3


app = Flask(__name__)


#connection à la base de données
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


#création de la table "users"
def create_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE)')
    conn.commit()
    conn.close()


#création de la table "livres"
def create_books_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, author TEXT NOT NULL, year INTEGER NOT NULL, genre_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_books (id), status TEXT NOT NULL, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()



#création de la table "films"
def create_movies_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, director TEXT NOT NULL, year INTEGER NOT NULL, genre_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_movies (id), duration INTEGER NOT NULL, status TEXT NOT NULL,rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()


#création de la table "serie"
def create_show_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS show (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, creator TEXT NOT NULL, start_year INTEGER NOT NULL, end_year INTEGER, genre_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_show (id), duration INTEGER NOT NULL, nb_seasons INTEGER NOT NULL, actual_season INTEGER, actual_episode INTEGER, status TEXT NOT NULL, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()


#création de la table "jeux vidéos"
def create_games_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, developer TEXT NOT NULL, editor TEXT NOT NULL, year INTEGER NOT NULL, genre_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_games (id), platform TEXT NOT NULL, status TEXT NOT NULL, hours_played INTEGER, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()


#création de la table "musiques"
def create_music_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS music (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, artist TEXT NOT NULL, album TEXT NOT NULL, year INTEGER NOT NULL, genre_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_music (id), playlist_mood TEXT NOT NULL, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()


#création de la table "mangas"
def create_manga_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS manga (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, author TEXT NOT NULL, year INTEGER NOT NULL, genre_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_manga (id), status TEXT NOT NULL, nb_chapters INTEGER NOT NULL, actual_chapter INTEGER NOT NULL, nb_volumes INTEGER NOT NULL, actual_volume INTEGER, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()


#création de la table "genres" pour les livres
def create_genres_books_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS genres_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')
    conn.commit()
    conn.close()


#création de la table "genres" pour les films
def create_genres_movies_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS genres_movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')
    conn.commit()
    conn.close()


#création de la table "genres" pour les séries
def create_genres_show_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS genres_show (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')
    conn.commit()
    conn.close()


#création de la table "genres" pour les jeux vidéos
def create_genres_games_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS genres_games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')
    conn.commit()
    conn.close()


#création de la table "genres" pour les musiques
def create_genres_music_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS genres_music (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')
    conn.commit()
    conn.close()


#création de la table "genres" pour les mangas
def create_genres_manga_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS genres_manga (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')
    conn.commit()
    conn.close()        


#ajout des genres
def populate_genres():
    conn = get_db_connection()
    
    # Genres pour les livres
    genres_books = ["Fantasie", "Science-Fiction", "Romance", "Thriller", "Policier", "Horreur", "Historique", "Biographie", "Poésie", "Essai"]
    for genre in genres_books:
        conn.execute("INSERT OR IGNORE INTO genres_books (name) VALUES (?)", (genre,))
    
    # Genres pour les mangas
    genres_manga = ["Shonen", "Shojo", "Seinen", "Shoujo"]
    for genre in genres_manga:
        conn.execute("INSERT OR IGNORE INTO genres_manga (name) VALUES (?)", (genre,))

    # Genres pour les films
    genres_movies = ["Action", "Comedie", "Drame", "Horreur", "Science-Fiction", "Romance", "Thriller", "Animation", "Documentaire", "Aventure"]
    for genre in genres_movies:
        conn.execute("INSERT OR IGNORE INTO genres_movies (name) VALUES (?)", (genre,))

    # Genres pour les séries
    genres_show = ["Action", "Comedie", "Drame", "Horreur", "Science-Fiction", "Romance", "Thriller", "Animation", "Documentaire", "Aventure"]
    for genre in genres_show:
        conn.execute("INSERT OR IGNORE INTO genres_show (name) VALUES (?)", (genre,))

    # Genres pour les jeux vidéos
    genres_games = ["Action", "Aventure", "RPG", "Simulation", "Stratégie", "Sports", "Course", "Puzzle", "Combat", "Horreur"]
    for genre in genres_games:
        conn.execute("INSERT OR IGNORE INTO genres_games (name) VALUES (?)", (genre,))

    # Genres pour les musiques
    genres_music = ["Pop", "Rock", "Jazz", "Classique", "Hip-Hop", "Electronique", "Reggae", "Blues", "Country", "Folk"]
    for genre in genres_music:
        conn.execute("INSERT OR IGNORE INTO genres_music (name) VALUES (?)", (genre,))

    conn.commit()
    conn.close()    



# Initialiser la base de données
def init_db():
    # Tables users et genres d'abord
    create_table()
    create_genres_books_table()
    create_genres_movies_table()
    create_genres_show_table()
    create_genres_games_table()
    create_genres_music_table()
    create_genres_manga_table()
    
    # Tables de contenu après
    create_books_table()
    create_movies_table()
    create_show_table()
    create_games_table()
    create_music_table()
    create_manga_table()
    
    # Remplir les genres
    populate_genres()
    print("✅ Base de données initialisée !")

# Appeler au démarrage
if __name__ == '__main__':
    init_db()
    app.run(debug=True)