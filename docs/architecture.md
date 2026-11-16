# Architecture — DAAR Projet 2

> Responsable de ce document : Camille (architecture, API, frontend, Docker).

## Vue d'ensemble

```
 Clients (PC, téléphone)                Machine serveur
 ┌───────────────────┐        ┌──────────────────────────────────────────────┐
 │ Navigateur        │  HTTP  │ frontend (nginx)        backend (FastAPI)    │
 │ React (SPA)       ├───────►│  :8080                   :8000               │
 └───────────────────┘        │  ├─ fichiers statiques   ├─ /api/books       │
                              │  └─ /api  ──────────────►├─ /api/search      │
                              │                          └─ /api/health      │
                              │                               │ lecture seule│
                              │                          volume ./data       │
                              └──────────────────────────────────────────────┘
```

- **Deux conteneurs permanents** : le frontend (React compilé, servi par nginx) et le
  backend (FastAPI + uvicorn). Pas de conteneur par algorithme, pas de base de données
  obligatoire.
- **Une seule origine pour le client** : nginx relaie `/api` vers le backend. Un téléphone
  n'a besoin que de l'adresse `http://<IP-du-serveur>:8080`.
- **Données en fichiers persistants**, montées en lecture seule dans le backend.

## Trois couches

| Couche | Contenu | Responsable |
|---|---|---|
| Data | `data/` + `scripts/` : corpus, textes nettoyés, index inversé, graphe de Jaccard, PageRank | Kenza, Nadine |
| Serveur | `backend/app/` : API FastAPI, recherche, classement, suggestions | Camille (API), Kenza, Nadine |
| Client | `frontend/` : application React/Vite | Camille |

## Hors ligne / en ligne

Tout ce qui est coûteux est calculé **hors ligne** par les scripts, puis **chargé une seule
fois** au démarrage du backend (`lifespan` de `main.py`). Une requête ne fait que des
lectures en mémoire, plus la lecture d'un fichier texte pour l'affichage d'un livre.

```
scripts/download_books.py ─► data/raw/ + data/metadata/books.json      (Kenza)
scripts/clean_books.py    ─► data/processed/                           (Kenza)
scripts/validate_corpus.py ─► rapport JSON de validation               (Kenza)
scripts/build_index.py    ─► data/indexes/ (inverted_index, book_terms,
                             original_to_normalized)                   (Kenza)
scripts/build_graph.py    ─► data/graphs/ (edges, neighbors, stats)    (Nadine)
scripts/compute_pagerank.py ─► data/graphs/pagerank                    (Nadine)
```

`scripts/rebuild_all.sh` enchaîne ces étapes dans l'ordre et s'arrête à la première erreur.

## Backend

```
main.py              instance FastAPI, CORS, lifespan, /api/health
config/settings.py   chemins et limites, lus dans l'environnement
books/schemas.py     modèles Pydantic = contrat JSON
books/routes.py      /api/books/*
books/service.py     catalogue en mémoire, lecture paginée des textes
search/routes.py     /api/search et /api/search/advanced
integration.py       appelle les modules de l'équipe, bascule sur la simulation
mocks.py             moteur simulé sur les 10 livres d'exemple
errors.py            exceptions partagées (InvalidRegexError)
search/, ranking/, recommendations/   modules de Kenza et Nadine (TODO)
```

### Parcours d'une recherche

1. `search/routes.py` valide la requête (vide, trop longue → `400`).
2. `integration.search_simple()` ou `search_regex()` → `{book_id: occurrences}`.
3. `integration.rank()` → liste triée `{id, occurrences, pagerank, score}`.
4. Pagination, puis ajout du titre et de l'auteur depuis le catalogue.
5. `integration.suggest()` sur les 3 meilleurs résultats → voisins Jaccard, hors livres affichés.

### Simulation et bascule

`integration.py` appelle d'abord la fonction réelle. Si elle lève `NotImplementedError`
(module encore en TODO), il appelle l'équivalent de `mocks.py`. `/api/health` indique, module
par module, `"real"` ou `"mock"`, et l'interface affiche un bandeau « mode démonstration »
tant qu'une simulation est active. Brancher un vrai module ne demande aucune modification de
l'API ni du frontend.

## Frontend

| Vue | Route | Rôle |
|---|---|---|
| Accueil | `/` | Recherche par mot-clé |
| Résultats | `/search?q=&page=` | Résultats classés (rang, occurrences, PageRank, score) + suggestions |
| Recherche avancée | `/advanced?regex=&page=` | Saisie d'une RegEx, exemples, limites, résultats |
| Catalogue | `/books?page=` | Liste paginée des livres |
| Livre | `/books/:id?page=` | Métadonnées, texte intégral paginé, livres similaires |

Fichiers : `pages/Home.jsx`, `Results.jsx`, `AdvancedSearch.jsx`, `Library.jsx`,
`BookDetails.jsx` ; composants `SearchBar`, `ResultsList`, `BookCard`, `SuggestionsList`,
`Pagination`, `StatusMessage`, `Layout`.

L'état de recherche (requête, page) est dans l'URL : une page de résultats se partage et le
bouton retour fonctionne. `services/api.js` est le seul fichier qui connaît les routes de
l'API. Chaque vue gère chargement, erreur (backend injoignable, `4xx`, `5xx`) et résultat vide.
La mise en page passe sur une colonne en dessous de 760 px.

## Choix techniques

| Besoin | Choix | Raison |
|---|---|---|
| API | FastAPI | Validation et documentation `/docs` automatiques, même langage que les scripts de données |
| Client | React + Vite | Application monopage, rechargement à chaud, build statique léger |
| Stockage | Fichiers (JSON, texte) | Données en lecture seule, calculées hors ligne ; pas de serveur de base à administrer |
| Déploiement | Docker Compose | Démarrage en une commande sur la machine de démonstration |

### Comparatif des technologies courantes

Base de discussion pour le rapport (section de Camille) ; à relire en équipe.

| Backend | Atouts | Limites pour ce projet | Retenu |
|---|---|---|---|
| FastAPI (Python) | Validation Pydantic, `/docs` généré, même langage que l'indexation et le graphe | Pas d'ORM ni d'administration intégrés (inutiles ici) | Oui |
| Django REST Framework (Python) | ORM, administration, écosystème complet | Lourd pour une API en lecture seule sur des fichiers pré-calculés | Non |
| Flask (Python) | Minimal, très répandu | Validation et documentation à ajouter à la main | Non |
| Express (Node.js) | Même langage que le client | Algorithmes à réécrire ou à appeler dans un autre processus | Non |
| Spring Boot (Java) | Robuste, typé | Mise en place plus longue pour une échéance d'une semaine | Non |

| Client | Atouts | Limites pour ce projet | Retenu |
|---|---|---|---|
| React + Vite | Composants, routage côté client, build statique léger | Bibliothèque de routage à ajouter | Oui |
| Vue | Prise en main rapide | Moins pratiqué par l'équipe | Non |
| Angular | Cadre complet et typé | Surdimensionné pour cinq vues | Non |
| Application native (Android / iOS) | Intégration au téléphone | Deux développements ; le navigateur suffit pour la démo multi-client | Non |

| Stockage | Atouts | Limites pour ce projet | Retenu |
|---|---|---|---|
| Fichiers JSON / texte | Aucun service à administrer, chargés une fois en mémoire | Pas de mise à jour incrémentale | Oui |
| SQLite | Requêtes SQL, un seul fichier | Peu utile pour un index déjà en mémoire | Facultatif |
| Elasticsearch | Moteur de recherche complet | Remplacerait les algorithmes que le projet demande d'implémenter | Non |
