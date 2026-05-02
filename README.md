# Backlog de Jeux Vidéo - API REST

Projet réalisé dans le cadre de la SAE **Développement & Déploiement d'une Application Web RESTful Conteneurisée** (Sup-Galilée).

---

## Contexte du projet

Cette application est une **API REST** permettant à des utilisateurs de gérer leur **backlog personnel de jeux vidéo**.

Le problème résolu : les joueurs ont souvent une quantité importante de jeux qu'ils possèdent mais n'ont pas encore joués, ou des jeux en cours qu'ils oublient de finir. Cette API leur permet de :

- Lister les jeux qu'ils veulent jouer (statut "à jouer")
- Suivre les jeux en cours
- Marquer les jeux finis avec une note et un avis personnel
- Indiquer les jeux abandonnés
- Catégoriser les jeux avec des tags (RPG, Indie, Soulslike...)
- Consulter des statistiques sur leur progression

L'API est conçue pour être consommée par n'importe quel client (application web, mobile, script...).

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Python 3.12 + Flask |
| ORM | SQLAlchemy (via Flask-SQLAlchemy) |
| Base de données | PostgreSQL 15 |
| Documentation API | Swagger (Flasgger) |
| Tests | Pytest |
| Conteneurisation | Docker + Docker Compose |

---

## Architecture du projet

```
Projet-PrincipeProg/
├── docker-compose.yml       # Orchestration des conteneurs (API + BDD)
├── Dockerfile               # Image Docker de l'API Flask
├── requirements.txt         # Dépendances Python
├── init.sql                 # Jeu de données de test (chargement manuel)
├── README.md                # Documentation du projet
│
├── app/                     # Code source de l'API
│   ├── app.py               # Point d'entrée Flask + config Swagger
│   ├── database.py          # Configuration SQLAlchemy
│   ├── models.py            # Modèles ORM (User, Profile, Game, Tag, BacklogEntry)
│   └── routes/              # Routes organisées en Blueprints
│       ├── __init__.py
│       ├── users.py         # Routes /users + gestion du profil (1-1)
│       ├── games.py         # Routes /games + association N-N avec tags
│       ├── tags.py          # Routes /tags
│       └── backlog.py       # Routes /backlog + statistiques
│
└── tests/                   # Tests automatisés (pytest)
    ├── __init__.py
    ├── conftest.py          # Configuration partagée (fixture client)
    ├── test_users.py        # Tests des routes utilisateurs
    ├── test_games.py        # Tests des routes jeux + N-N
    └── test_backlog.py      # Tests du backlog + 1-N
```

### Choix d'architecture

- **Séparation des responsabilités** : les modèles, les routes et la configuration sont dans des fichiers séparés.
- **Blueprints Flask** : chaque "thème" de l'API a son fichier de routes, ce qui rend le code modulaire et facile à maintenir.
- **ORM SQLAlchemy** : permet de manipuler la base de données via des objets Python plutôt que d'écrire du SQL à la main.
- **PATCH vs PUT** : on utilise PATCH pour les mises à jour partielles (modifier juste le statut d'une entrée du backlog par exemple).

---

## Modélisation et relations

Le projet implémente les **3 types de relations** demandées par le sujet :

| Type | Relation | Implémentation |
|------|----------|----------------|
| **One-to-One** | `User` ↔ `Profile` | FK avec `unique=True` + `uselist=False` |
| **One-to-Many** | `User` → `BacklogEntry` et `Game` → `BacklogEntry` | FK simple + `db.relationship` |
| **Many-to-Many** | `Game` ↔ `Tag` | Table d'association `game_tags` |

### Schéma simplifié de la BDD

```
users (id, email, username, created_at)
   │ 1-1
   └── profiles (id, user_id [unique], avatar_url, favorite_platform, bio)
   │ 1-N
   └── backlog_entries (id, user_id, game_id, status, rating, review, added_at)
                                        │ N-1
                                        └── games (id, title, developer, release_year)
                                                       │ N-N
                                                       └── game_tags (game_id, tag_id)
                                                                      │
                                                                      └── tags (id, name)
```

---

## Lancer l'application

### Prérequis

- Docker Desktop installé et lancé
- Git (pour cloner le projet)

### Étape 1 : Cloner le projet

```bash
git clone https://github.com/karimht/Projet-PrincipeProg.git
cd Projet-PrincipeProg
```

### Étape 2 : Lancer l'application

```bash
docker compose up --build
```

Cette commande :
- Construit l'image Docker de l'API
- Télécharge l'image PostgreSQL
- Lance les deux conteneurs et les met en réseau
- Crée automatiquement les tables au premier démarrage (via `db.create_all()`)

L'API est ensuite accessible sur **http://localhost:5000**
PostgreSQL est exposé sur le port **5432**.

### Étape 3 : Charger les données de test (optionnel mais recommandé)

Une fois les conteneurs lancés, dans un nouveau terminal :

```bash
docker compose cp init.sql db:/tmp/init.sql
docker compose exec db psql -U user_backlog -d backlog_jeux -f /tmp/init.sql
```

### Étape 4 : Tester

- **Page d'accueil de l'API** : http://localhost:5000
- **Documentation Swagger interactive** : http://localhost:5000/apidocs
- **Liste des jeux** : http://localhost:5000/games
- **Liste des utilisateurs** : http://localhost:5000/users

### Arrêter l'application

```bash
docker compose down
```

Pour aussi supprimer le volume de données (réinitialiser la BDD) :

```bash
docker compose down -v
```

---

## Routes de l'API REST

### Utilisateurs

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/users` | Lister tous les utilisateurs |
| GET | `/users/{id}` | Détails d'un utilisateur (avec son profil) |
| POST | `/users` | Créer un utilisateur |
| PUT | `/users/{id}` | Modifier un utilisateur |
| DELETE | `/users/{id}` | Supprimer un utilisateur (cascade sur profil et backlog) |
| PUT | `/users/{id}/profile` | Créer ou mettre à jour le profil (relation 1-1) |

### Jeux

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/games` | Lister tous les jeux (avec leurs tags) |
| GET | `/games/{id}` | Détails d'un jeu |
| POST | `/games` | Ajouter un jeu |
| PUT | `/games/{id}` | Modifier un jeu |
| DELETE | `/games/{id}` | Supprimer un jeu |
| POST | `/games/{game_id}/tags/{tag_id}` | Associer un tag à un jeu (N-N) |
| DELETE | `/games/{game_id}/tags/{tag_id}` | Dissocier un tag d'un jeu |

### Tags

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/tags` | Lister tous les tags |
| GET | `/tags/{id}` | Détails d'un tag |
| POST | `/tags` | Créer un tag |
| DELETE | `/tags/{id}` | Supprimer un tag |

### Backlog

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/users/{user_id}/backlog` | Backlog d'un utilisateur |
| GET | `/users/{user_id}/backlog?status=playing` | Backlog filtré par statut |
| POST | `/users/{user_id}/backlog` | Ajouter un jeu au backlog |
| PATCH | `/backlog/{id}` | Modifier une entrée (statut, note, avis) |
| DELETE | `/backlog/{id}` | Retirer une entrée du backlog |
| GET | `/users/{user_id}/stats` | Statistiques (nb de jeux par statut) |

---

## Exemples de requêtes

### Créer un utilisateur

**Requête :**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@test.com", "username": "alice_gamer"}'
```

**Réponse (201 Created) :**
```json
{
  "id": 1,
  "email": "alice@test.com",
  "username": "alice_gamer",
  "created_at": "2026-04-22T10:30:00",
  "profile": null
}
```

### Mettre à jour le profil (relation 1-1)

**Requête :**
```bash
curl -X PUT http://localhost:5000/users/1/profile \
  -H "Content-Type: application/json" \
  -d '{"favorite_platform": "PC", "bio": "Fan de metroidvanias"}'
```

**Réponse (200 OK) :**
```json
{
  "id": 1,
  "user_id": 1,
  "avatar_url": null,
  "favorite_platform": "PC",
  "bio": "Fan de metroidvanias"
}
```

### Créer un jeu et lui associer un tag (N-N)

```bash
# Créer le jeu
curl -X POST http://localhost:5000/games \
  -H "Content-Type: application/json" \
  -d '{"title": "Hollow Knight", "developer": "Team Cherry", "release_year": 2017}'

# Créer le tag
curl -X POST http://localhost:5000/tags \
  -H "Content-Type: application/json" \
  -d '{"name": "Metroidvania"}'

# Associer le tag au jeu
curl -X POST http://localhost:5000/games/1/tags/1
```

### Ajouter un jeu au backlog (relation 1-N)

**Requête :**
```bash
curl -X POST http://localhost:5000/users/1/backlog \
  -H "Content-Type: application/json" \
  -d '{"game_id": 1, "status": "playing", "rating": 9, "review": "Excellent jeu"}'
```

**Réponse (201 Created) :**
```json
{
  "id": 1,
  "user_id": 1,
  "game_id": 1,
  "game_title": "Hollow Knight",
  "status": "playing",
  "rating": 9,
  "review": "Excellent jeu",
  "added_at": "2026-04-22T10:35:00"
}
```

### Modifier le statut d'une entrée

```bash
curl -X PATCH http://localhost:5000/backlog/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "finished", "rating": 10}'
```

### Récupérer les statistiques d'un utilisateur

**Requête :**
```bash
curl http://localhost:5000/users/1/stats
```

**Réponse :**
```json
{
  "to_play": 3,
  "playing": 1,
  "finished": 5,
  "dropped": 0,
  "total": 9
}
```

---

## Documentation Swagger interactive

Une fois l'API lancée, ouvrez **http://localhost:5000/apidocs** dans votre navigateur.

Vous pourrez :
- Voir toutes les routes disponibles, triées par tags
- Consulter les paramètres et les schémas de chaque route
- **Tester l'API directement depuis l'interface** (bouton "Try it out")

---

## Tests automatisés

Le projet contient une suite de tests automatisés couvrant les principales fonctionnalités et les 3 relations.

### Lancer les tests

```bash
docker compose run --rm api pytest /tests -v
```

### Couverture des tests

- CRUD des utilisateurs (création, lecture, mise à jour, suppression)
- Validation des champs obligatoires
- Gestion des erreurs 404
- Création et mise à jour du profil (relation 1-1)
- CRUD des jeux
- Association/dissociation de tags (relation N-N)
- Ajout au backlog et filtrage par statut (relation 1-N)
- Statistiques utilisateur

---

## Données de test

Le fichier `init.sql` contient un jeu de données de test :

**Utilisateurs :**
- `alice_gamer` (PC, fan de jeux indés et metroidvanias)
- `bob_player` (PS5, joueur de RPG)
- `karim47` (Switch, jeux en coop)

**Jeux :**
- Hollow Knight (Team Cherry, 2017) — Indie, Metroidvania
- Elden Ring (FromSoftware, 2022) — RPG, Soulslike, Open World
- Stardew Valley (ConcernedApe, 2016) — Indie
- Hades (Supergiant Games, 2020) — Indie, Rogue-like
- Celeste (Maddy Makes Games, 2018) — Indie, Platformer
- The Witcher 3 (CD Projekt Red, 2015) — RPG, Open World

**Tags :** Indie, RPG, Metroidvania, Rogue-like, Soulslike, Platformer, Open World

**Backlog pré-rempli** avec différents statuts pour montrer toutes les fonctionnalités.

---

## Image Docker Hub

L'image Docker de l'API est publiée sur Docker Hub :

- **Image** : `karimht/backlog-jeux-api:latest`
- **Lien** : https://hub.docker.com/r/karimht/backlog-jeux-api

### Lancer depuis Docker Hub

```bash
docker pull karimht/backlog-jeux-api:latest
```

Pour lancer l'image avec une BDD PostgreSQL, on utilise le `docker-compose.yml` du dépôt qui orchestre les deux conteneurs.

### Volume Docker

Un volume nommé `postgres_data` est utilisé pour persister les données de PostgreSQL. Cela garantit que les données ne sont pas perdues si le conteneur est supprimé ou redémarré.

---

## Points clés du projet

- API REST complète avec les 4 méthodes HTTP (GET, POST, PUT/PATCH, DELETE)
- Persistance dans PostgreSQL via SQLAlchemy (ORM)
- Les 3 relations (1-1, 1-N, N-N) modélisées dans le code et la BDD
- Conteneurisation complète (API + BDD)
- Orchestration via Docker Compose
- Documentation interactive avec Swagger
- Tests automatisés avec pytest
- Gestion des erreurs (try/except, handlers globaux 404/500)
- Volume Docker pour la persistance
- Code modulaire organisé en Blueprints

---

## Auteur

Projet SAE — Sup-Galilée
Karim — [@karimht](https://github.com/karimht)
