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
scripts/build_index.py    ─► data/indexes/ (index inversé, book_terms) (Kenza)
scripts/build_graph.py    ─► data/graphs/ (voisins Jaccard)            (Nadine)
scripts/compute_pagerank.py ─► data/graphs/ (PageRank)                 (Nadine)
```

## Backend

```
main.py            instance FastAPI, CORS, lifespan, /api/health
config.py          chemins et limites, lus dans l'environnement
schemas.py         modèles Pydantic = contrat JSON
errors.py          exceptions partagées (InvalidRegexError)
books/             catalogue en mémoire, lecture paginée, /api/books/*
search/router.py   /api/search et /api/search/advanced
integration.py     appelle les modules de l'équipe, bascule sur la simulation
mocks.py           moteur simulé sur les 10 livres d'exemple
search/, ranking/, recommendations/   modules de Kenza et Nadine (TODO)
```

### Parcours d'une recherche

1. `search/router.py` valide la requête (vide, trop longue → `400`).
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

TODO (collectif) : tableau comparatif des technologies du marché pour le rapport et la vidéo.
