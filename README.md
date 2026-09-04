
# 📚 Mini-Bibliothèque - Résumé Complet

## 🔧 BACKEND (app.py)

### 1️⃣ Structure BD (SQLite)

#### **6 Tables de Contenu**

- `books` (livres)
- `movies` (films)
- `show` (séries)
- `games` (jeux vidéo)
- `music` (musiques)
- `manga` (mangas)

**Chaque table contient :**

- `id` (clé primaire)
- Champs spécifiques :
  - **books** : `title`, `author`, `year`, `genre_id`, `status`, `rating`, `review`, `added`, `user_id`, `description`
  - **movies** : `title`, `director`, `year`, `genre_id`, `duration`, `status`, `rating`, `review`, `added`, `user_id`, `description`
  - **show** : `title`, `creator`, `start_year`, `end_year`, `genre_id`, `nb_seasons`, `actual_season`, `actual_episode`, `status`, `rating`, `review`, `added`, `user_id`, `description`
  - **games** : `title`, `developer`, `editor`, `year`, `genre_id`, `platform`, `hours_played`, `status`, `rating`, `review`, `added`, `user_id`, `description`
  - **music** : `title`, `artist`, `album`, `year`, `genre_id`, `playlist_mood`, `status`, `rating`, `review`, `added`, `user_id`, `description`
  - **manga** : `title`, `author`, `year`, `genre_id`, `nb_chapters`, `actual_chapter`, `nb_volumes`, `actual_volume`, `status`, `rating`, `review`, `added`, `user_id`, `description`

**Champs communs :**

- `genre_id` → Référence à la table de genres correspondante
- `status` → À lire, En cours, Terminé, Vu, Écouté, etc.
- `rating` → Note sur 10
- `review` → Description/Avis
- `added` → Date d'ajout (YYYY-MM-DD)
- `user_id` → ID utilisateur (1 = Kety)

---

#### **6 Tables de Genres**

- `genres_books` - Genres des livres (Fantasy, Science-Fiction, Romance, etc.)
- `genres_movies` - Genres des films (Action, Comédie, Drame, etc.)
- `genres_show` - Genres des séries
- `genres_games` - Genres des jeux (RPG, FPS, Stratégie, etc.)
- `genres_music` - Genres musicaux (Pop, Rock, Jazz, etc.)
- `genres_manga` - Genres de manga (Shonen, Shojo, Seinen, etc.)

**Structure de chaque table de genres :**

```sql
id INTEGER PRIMARY KEY
name TEXT NOT NULL UNIQUE
```

---

#### **Table Users**

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE
)
```

**Au démarrage :** Kety est créée automatiquement (id=1, email=ketsia.kouadio@iit.ci)

---

### 2️⃣ Routes Flask (API REST)

#### **Routes CRUD - Livres (/books)**

```
GET    /books                    Récupère tous les livres
POST   /books                    Ajoute un livre
PUT    /books/<int:id>           Modifie un livre
DELETE /books/<int:id>           Supprime un livre
```

#### **Routes CRUD - Films (/movies)**

```
GET    /movies                   Récupère tous les films
POST   /movies                   Ajoute un film
PUT    /movies/<int:id>          Modifie un film
DELETE /movies/<int:id>          Supprime un film
```

#### **Routes CRUD - Séries (/shows)**

```
GET    /shows                    Récupère toutes les séries
POST   /shows                    Ajoute une série
PUT    /shows/<int:id>           Modifie une série
DELETE /shows/<int:id>           Supprime une série
```

#### **Routes CRUD - Jeux (/games)**

```
GET    /games                    Récupère tous les jeux
POST   /games                    Ajoute un jeu
PUT    /games/<int:id>           Modifie un jeu
DELETE /games/<int:id>           Supprime un jeu
```

#### **Routes CRUD - Musiques (/music)**

```
GET    /music                    Récupère toutes les musiques
POST   /music                    Ajoute une musique
PUT    /music/<int:id>           Modifie une musique
DELETE /music/<int:id>           Supprime une musique
```

#### **Routes CRUD - Mangas (/manga)**

```
GET    /manga                    Récupère tous les mangas
POST   /manga                    Ajoute un manga
PUT    /manga/<int:id>           Modifie un manga
DELETE /manga/<int:id>           Supprime un manga
```

#### **Routes Spéciales**

```
GET    /                         Serve le fichier index.html
GET    /genres                   Récupère TOUS les genres (pour les dropdowns)
```

---

### 3️⃣ Fonctionnement des Routes

#### **Ajout (POST)**

```
1. Frontend envoie : POST /books avec JSON
   {
     "title": "Harry Potter",
     "author": "J.K. Rowling",
     "year": 1997,
     "genre_id": 1,
     "status": "Lu",
     "rating": 9,
     "review": "Incroyable !",
     "added": "2024-09-04",
     "user_id": 1,
     "description": "..."
   }

2. Backend (app.py) :
   - Récupère le JSON
   - INSERT INTO books (...)
   - Retourne : {"message": "Livre ajouté !"}

3. Frontend :
   - Ajoute le nouvel élément à S.data['books']
   - Ferme le modal
   - Appelle render() → Affiche le nouvel élément
```

#### **Modification (PUT)**

```
1. Frontend envoie : PUT /books/3 avec JSON modifié

2. Backend :
   - UPDATE books SET ... WHERE id=3
   - Retourne : {"message": "Livre modifié !"}

3. Frontend :
   - Remplace l'élément local dans S.data['books']
   - Appelle render() → Affiche la modification
```

#### **Suppression (DELETE)**

```
1. Frontend envoie : DELETE /books/3

2. Backend :
   - DELETE FROM books WHERE id=3
   - Retourne : {"message": "Livre supprimé !"}

3. Frontend :
   - Enlève l'élément de S.data['books']
   - Appelle render() → Affiche la liste mise à jour
```

---

## 🎨 FRONTEND (app.js)

### 1️⃣ État Global (S)

```javascript
const S = {
  view: "home",                                    // Onglet actif (home, books, movies, etc.)
  data: {                                          // Données cachées en mémoire locale
    books: [],
    movies: [],
    shows: [],
    games: [],
    music: [],
    manga: []
  },
  genres: {},                                      // Genres depuis GET /genres
  search: "",                                      // Terme de recherche actif
  filter: "Tous",                                  // Filtre par statut (À lire, En cours, etc.)
  formNote: 0,                                     // Note actuellement sélectionnée dans le formulaire
};
```

---

### 2️⃣ Flux de Données au Démarrage

```
Au chargement de la page :
    ↓
  renderThemeOptions()     → Affiche les boutons de thème
  applyTheme()             → Applique le thème sauvegardé
    ↓
  loadGenres()             → GET /genres → Remplit S.genres
    ↓
  loadAllData()            → Fait 6 GET (un par type)
                           → Remplit S.data[books], S.data[movies], etc.
    ↓
  render()                 → Affiche la page d'accueil avec les données
```

---

### 3️⃣ Catégories (CATS)

```javascript
const CATS = [
  { key: "books",  label: "Livres",   icon: "📚", endpoint: "/books",  authorField: "author",    authorLabel: "Auteur" },
  { key: "movies", label: "Films",    icon: "🎬", endpoint: "/movies", authorField: "director",  authorLabel: "Réalisateur" },
  { key: "shows",  label: "Séries",   icon: "📺", endpoint: "/shows",  authorField: "creator",   authorLabel: "Créateur" },
  { key: "games",  label: "Jeux",     icon: "🎮", endpoint: "/games",  authorField: "developer", authorLabel: "Développeur" },
  { key: "music",  label: "Musiques", icon: "🎵", endpoint: "/music",  authorField: "artist",    authorLabel: "Artiste" },
  { key: "manga",  label: "Manga",    icon: "📖", endpoint: "/manga",  authorField: "author",    authorLabel: "Auteur" },
];
```

---

### 4️⃣ Fonctions Principales

| Fonction                         | Rôle                                                   |
| -------------------------------- | ------------------------------------------------------- |
| `loadGenres()`                 | Fetch GET /genres → Rempli S.genres pour les dropdowns |
| `loadAllData()`                | Fetch GET pour chaque endpoint → Charge tout           |
| `buildNav()`                   | Construit la navigation latérale avec les compteurs    |
| `navigateTo(view)`             | Navigue vers une catégorie ou l'accueil                |
| `render()`                     | Affiche la page selon S.view                            |
| `renderHome()`                 | Affiche l'accueil avec stats et récentes entrées      |
| `renderCatView()`              | Affiche les cartes de la catégorie actuelle            |
| `renderFilters()`              | Affiche les filtres (statut)                            |
| `setFilter(f)`                 | Filtre par statut et réaffiche                         |
| `openAdd(cat)`                 | Ouvre le modal d'ajout                                  |
| `openEdit(id, cat)`            | Ouvre le modal de modification                          |
| `openDelete(id, cat)`          | Ouvre la confirmation de suppression                    |
| `handleFormSubmit(e, cat, id)` | Traite l'envoi du formulaire                            |
| `apiAdd(item, cat)`            | Fetch POST → Ajoute en BD                              |
| `apiEdit(item, cat)`           | Fetch PUT → Modifie en BD                              |
| `confirmDelete(id, cat)`       | Fetch DELETE → Supprime en BD                          |
| `openModal(title, html)`       | Ouvre un modal                                          |
| `closeModal()`                 | Ferme le modal                                          |

---

### 5️⃣ Architecture des Formulaires

#### **Ajout/Modification**

```
Utilisateur clique "+ Ajouter"
    ↓
openAdd(cat) → Ouvre modal
    ↓
formHTML(cat, null) → Génère le formulaire vide
    ↓
Utilisateur remplit :
  - Titre (obligatoire)
  - Auteur/Réalisateur/Artiste
  - Année
  - Genre (dropdown depuis S.genres)
  - Statut (dropdown options spécifiques au type)
  - Champs spécifiques (durée, heures, chapitres, etc.)
  - Note (5 étoiles cliquables)
  - Description/Avis (textarea)
    ↓
Clique "Ajouter" → handleFormSubmit()
    ↓
Collecte toutes les données
Génère un objet JavaScript
    ↓
apiAdd(item, cat) → Fetch POST
    ↓
Ajoute à S.data[cat]
closeModal()
render()
    ↓
L'élément apparaît dans la liste ✨
```

#### **Modification**

```
Utilisateur clique l'icône ✏️ sur une carte
    ↓
openEdit(id, cat) → Ouvre modal
    ↓
formHTML(cat, item) → Génère le formulaire PRÉ-REMPLI
    ↓
Utilisateur modifie les champs
    ↓
Clique "Enregistrer" → handleFormSubmit()
    ↓
apiEdit(item, cat) → Fetch PUT /endpoint/id
    ↓
Met à jour S.data[cat]
closeModal()
render()
    ↓
La carte mise à jour réapparaît ✨
```

#### **Suppression**

```
Utilisateur clique l'icône 🗑️ sur une carte
    ↓
openDelete(id, cat) → Ouvre confirmation
    ↓
Affiche : "Supprimer [titre] ? Irréversible."
    ↓
Clique "Supprimer" → confirmDelete(id, cat)
    ↓
confirmDelete() → Fetch DELETE /endpoint/id
    ↓
Enlève de S.data[cat]
closeModal()
render()
    ↓
La carte disparaît de la liste ✨
```

---

### 6️⃣ Utilitaires

```javascript
esc(s)                    Échappe les caractères HTML
statusBadge(s)            Retourne un badge coloré pour le statut
starsView(n)              Retourne n étoiles (affichage)
starsInput(n)             Retourne n boutons étoiles (cliquables)
getAuthorField(cat)       Retourne le champ auteur selon la catégorie
getAuthorLabel(cat)       Retourne le label auteur selon la catégorie
getGenreName(cat, id)     Retourne le nom du genre
cardHTML(item, cat)       Génère le HTML d'une carte
renderCatContent()        Raffraîchit l'affichage de la catégorie
setFormNote(n)            Change la note du formulaire à n
```

---

### 7️⃣ Gestion de la Recherche et des Filtres

```javascript
// Recherche
document.getElementById("search-input").addEventListener("input", e => {
  S.search = e.target.value;
  renderCatContent();  // Raffraîchit avec la recherche
});

// Filtre
function setFilter(f) {
  S.filter = f;
  renderCatContent();  // Raffraîchit avec le filtre
}

// Dans renderCatView() :
const filtered = items.filter(i => {
  const matchSearch = !q || Object.values(i).some(v => 
    String(v).toLowerCase().includes(q)
  );
  const matchStatus = S.filter === "Tous" || i.status === S.filter;
  return matchSearch && matchStatus;
});
```

---

## 🔗 Communication Backend ↔️ Frontend

### **Flow Général**

```
Frontend (JavaScript/HTML)
    ↓
fetch(API + endpoint, {method, headers, body})
    ↓
Envoie requête HTTP au Backend
    ↓
Backend (Flask/Python)
    ↓
Reçoit requête
Traite les données
Modifie la BD
    ↓
Retourne réponse JSON
    ↓
Frontend reçoit
Traite la réponse
Met à jour S.data
Appelle render()
    ↓
Page mise à jour, utilisateur voit les changements
```

---

### **Exemple Concret : Ajout d'un Livre**

**Frontend (JavaScript) :**

```javascript
await fetch("http://localhost:5000/books", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    title: "Harry Potter",
    author: "J.K. Rowling",
    year: 1997,
    genre_id: 1,
    status: "Lu",
    rating: 9,
    review: "Incroyable !",
    added: "2024-09-04",
    user_id: 1,
    description: "L'histoire de Harry Potter à Poudlard"
  })
})
```

**Backend (Python/Flask) :**

```python
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''INSERT INTO books 
                    (title, author, year, genre_id, status, rating, review, added, user_id, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (data['title'], data['author'], data['year'], data['genre_id'],
                  data['status'], data['rating'], data['review'], data['added'],
                  data['user_id'], data['description']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livre ajouté !'})
```

**Frontend reçoit la réponse :**

```javascript
S.data['books'].push(newItem);
closeModal();
render();  // Réaffiche la page avec le nouveau livre
```

---

## 📊 Flux Complet d'une Ajout

```
┌─────────────────────────────────────────────────────────────┐
│ Utilisateur tape "Harry Potter"                             │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Clique "+ Ajouter"                                          │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ openAdd('books') → Modal formulaire s'ouvre                 │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Remplit les champs :                                        │
│ - Titre                                                      │
│ - Auteur                                                     │
│ - Année                                                      │
│ - Genre (dropdown S.genres['books'])                         │
│ - Statut (dropdown options spécifiques)                      │
│ - Note (clic sur les étoiles)                               │
│ - Avis/Description                                          │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Clique "Ajouter"                                            │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ handleFormSubmit() collecte les données                      │
│ Génère objet : {title, author, year, genre_id, ...}        │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ apiAdd() → Fetch POST /books + JSON                         │
└────────────────┬────────────────────────────────────────────┘
                 ↓
        ╔════════════════════╗
        ║  BACKEND (Flask)   ║
        ║                    ║
        ║ INSERT INTO books  ║
        ║ WHERE ...          ║
        ║                    ║
        ╚════════════════════╝
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Backend retourne JSON avec l'ID du nouvel élément            │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Frontend :                                                   │
│ - Ajoute à S.data['books']                                  │
│ - closeModal()                                              │
│ - render() → Raffraîchit tout                               │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ ✨ "Harry Potter" apparaît dans la section Livres ✨         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Résumé en Une Phrase

**Backend** = Base de données + Routes API qui modifient les données
**Frontend** = Interface + Logique qui communique avec le backend via fetch
**Ensemble** = App complète et fonctionnelle 🚀

---

## 📁 Structure Finale du Projet

```
mini-bibliotheque/
├── venv/                              # Environnement virtuel
├── app.py                             # Backend Flask
├── database.db                        # BD SQLite (créée au démarrage)
├── requirements.txt                   # Dépendances Python
├── templates/
│   └── index.html                     # Page HTML principale
├── static/
│   ├── css/
│   │   └── style.css                  # Tous les styles
│   └── js/
│       └── app.js                     # Toute la logique JavaScript
└── RESUME_PROJET.md                   # Ce fichier
```

---

## ✨ Statut du Projet

✅ **COMPLET ET FONCTIONNEL**

- ✅ Backend : Routes CRUD complètes
- ✅ BD : 6 tables de contenu + 6 de genres
- ✅ Frontend : Interface responsive
- ✅ Fetch API : Tous les CRUD implémentés
- ✅ Recherche et filtres : Fonctionnels
- ✅ Thème : 4 thèmes switchables
- ✅ Formulaires : Tous les champs par type
