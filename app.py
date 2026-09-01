from flask import Flask, jsonify, request, redirect,  render_template
import sqlite3


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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
    conn.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, author TEXT NOT NULL, year INTEGER NOT NULL, genre_id INTEGER NOT NULL, status TEXT NOT NULL, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_books (id), FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()



#création de la table "films"
def create_movies_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, director TEXT NOT NULL, year INTEGER NOT NULL, genre_id INTEGER NOT NULL, duration INTEGER NOT NULL, status TEXT NOT NULL, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_movies (id), FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()


#création de la table "serie"
def create_show_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS show (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, creator TEXT NOT NULL, start_year INTEGER NOT NULL, end_year INTEGER, genre_id INTEGER NOT NULL, duration INTEGER NOT NULL, nb_seasons INTEGER NOT NULL, actual_season INTEGER, actual_episode INTEGER, status TEXT NOT NULL, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_show (id), FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()


#création de la table "jeux vidéos"
def create_games_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, developer TEXT NOT NULL, editor TEXT NOT NULL, year INTEGER NOT NULL, genre_id INTEGER NOT NULL, platform TEXT NOT NULL, status TEXT NOT NULL, hours_played INTEGER, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_games (id), FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()


#création de la table "musiques"
def create_music_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS music (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, artist TEXT NOT NULL, album TEXT NOT NULL, year INTEGER NOT NULL, genre_id INTEGER NOT NULL, playlist_mood TEXT NOT NULL, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_music (id), FOREIGN KEY (user_id) REFERENCES users (id))')
    conn.commit()
    conn.close()


#création de la table "mangas"
def create_manga_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS manga (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, author TEXT NOT NULL, year INTEGER NOT NULL, genre_id INTEGER NOT NULL, status TEXT NOT NULL, nb_chapters INTEGER NOT NULL, actual_chapter INTEGER NOT NULL, nb_volumes INTEGER NOT NULL, actual_volume INTEGER, rating REAL NOT NULL, review TEXT NOT NULL, added DATE NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genres_manga (id), FOREIGN KEY (user_id) REFERENCES users (id))')
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



# ========== LES ROUTES ==========


#LIVRES
@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO books (title, description, author, year, genre_id, status, rating, review, added, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (data['title'], data['description'], data['author'], data['year'], data['genre_id'], data['status'], data['rating'], data['review'], data['added'], data['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livre ajouté !'})

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE books SET title=?, description=?, author=?, year=?, genre_id=?, status=?, rating=?, review=? WHERE id=?',
                 (data['title'], data['description'], data['author'], data['year'], data['genre_id'], data['status'], data['rating'], data['review'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livre modifié !'})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livre supprimé !'})



#FILMS
@app.route('/movies', methods=['GET'])
def get_movies():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return jsonify([dict(movie) for movie in movies])

@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO movies (title, description, director, year, genre_id, duration, status, rating, review, added, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (data['title'], data['description'], data['director'], data['year'], data['genre_id'], data['duration'], data['status'], data['rating'], data['review'], data['added'], data['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Film ajouté !'})

@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE movies SET title=?, description=?, director=?, year=?, genre_id=?, duration=?, status=?, rating=?, review=? WHERE id=?',
                 (data['title'], data['description'], data['director'], data['year'], data['genre_id'], data['duration'], data['status'], data['rating'], data['review'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Film modifié !'})

@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM movies WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Film supprimé !'})


#SÉRIES
@app.route('/shows', methods=['GET'])
def get_shows():
    conn = get_db_connection()
    shows = conn.execute('SELECT * FROM show').fetchall()
    conn.close()
    return jsonify([dict(show) for show in shows])

@app.route('/shows', methods=['POST'])
def add_show():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO show (title, description, creator, start_year, end_year, genre_id, duration, nb_seasons, actual_season, actual_episode, status, rating, review, added, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (data['title'], data['description'], data['creator'], data['start_year'], data.get('end_year'), data['genre_id'], data['duration'], data['nb_seasons'], data.get('actual_season'), data.get('actual_episode'), data['status'], data['rating'], data['review'], data['added'], data['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Série ajoutée !'})

@app.route('/shows/<int:id>', methods=['PUT'])
def update_show(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE show SET title=?, description=?, creator=?, start_year=?, end_year=?, genre_id=?, duration=?, nb_seasons=?, actual_season=?, actual_episode=?, status=?, rating=?, review=? WHERE id=?',
                 (data['title'], data['description'], data['creator'], data['start_year'], data.get('end_year'), data['genre_id'], data['duration'], data['nb_seasons'], data.get('actual_season'), data.get('actual_episode'), data['status'], data['rating'], data['review'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Série modifiée !'})

@app.route('/shows/<int:id>', methods=['DELETE'])
def delete_show(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM show WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Série supprimée !'})


#JEUX VIDÉOS
@app.route('/games', methods=['GET'])
def get_games():
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM games').fetchall()
    conn.close()
    return jsonify([dict(game) for game in games])

@app.route('/games', methods=['POST'])
def add_game():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO games (title, description, developer, editor, year, genre_id, platform, status, hours_played, rating, review, added, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (data['title'], data['description'], data['developer'], data['editor'], data['year'], data['genre_id'], data['platform'], data['status'], data.get('hours_played'), data['rating'], data['review'], data['added'], data['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Jeu ajouté !'})

@app.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE games SET title=?, description=?, developer=?, editor=?, year=?, genre_id=?, platform=?, status=?, hours_played=?, rating=?, review=? WHERE id=?',
                 (data['title'], data['description'], data['developer'], data['editor'], data['year'], data['genre_id'], data['platform'], data['status'], data.get('hours_played'), data['rating'], data['review'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Jeu modifié !'})

@app.route('/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM games WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Jeu supprimé !'})


#MUSIQUES
@app.route('/music', methods=['GET'])
def get_music():
    conn = get_db_connection()
    music = conn.execute('SELECT * FROM music').fetchall()
    conn.close()
    return jsonify([dict(m) for m in music])

@app.route('/music', methods=['POST'])
def add_music():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO music (title, description, artist, album, year, genre_id, playlist_mood, rating, review, added, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (data['title'], data['description'], data['artist'], data['album'], data['year'], data['genre_id'], data['playlist_mood'], data['rating'], data['review'], data['added'], data['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Musique ajoutée !'})

@app.route('/music/<int:id>', methods=['PUT'])
def update_music(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE music SET title=?, description=?, artist=?, album=?, year=?, genre_id=?, playlist_mood=?, rating=?, review=? WHERE id=?',
                 (data['title'], data['description'], data['artist'], data['album'], data['year'], data['genre_id'], data['playlist_mood'], data['rating'], data['review'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Musique modifiée !'})

@app.route('/music/<int:id>', methods=['DELETE'])
def delete_music(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM music WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Musique supprimée !'})


#MANGAS
@app.route('/manga', methods=['GET'])
def get_manga():
    conn = get_db_connection()
    manga = conn.execute('SELECT * FROM manga').fetchall()
    conn.close()
    return jsonify([dict(m) for m in manga])

@app.route('/manga', methods=['POST'])
def add_manga():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO manga (title, description, author, year, genre_id, status, nb_chapters, actual_chapter, nb_volumes, actual_volume, rating, review, added, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (data['title'], data['description'], data['author'], data['year'], data['genre_id'], data['status'], data['nb_chapters'], data['actual_chapter'], data['nb_volumes'], data.get('actual_volume'), data['rating'], data['review'], data['added'], data['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Manga ajouté !'})

@app.route('/manga/<int:id>', methods=['PUT'])
def update_manga(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE manga SET title=?, description=?, author=?, year=?, genre_id=?, status=?, nb_chapters=?, actual_chapter=?, nb_volumes=?, actual_volume=?, rating=?, review=? WHERE id=?',
                 (data['title'], data['description'], data['author'], data['year'], data['genre_id'], data['status'], data['nb_chapters'], data['actual_chapter'], data['nb_volumes'], data.get('actual_volume'), data['rating'], data['review'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Manga modifié !'})

@app.route('/manga/<int:id>', methods=['DELETE'])
def delete_manga(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM manga WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Manga supprimé !'})


# ========== INITIALISATION ==========

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
    
    # Créer l'utilisateur "Kety"
    conn = get_db_connection()
    conn.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", 
                 ("Kety", "ketsia.kouadio@iit.ci"))
    conn.commit()
    conn.close()
    
    print("✅ Base de données initialisée !")


# Appeler au démarrage
if __name__ == '__main__':
    init_db()
    app.run(debug=True)