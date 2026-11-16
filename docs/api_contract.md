# Contrat de l'API — DAAR Projet 2

> Responsable : Camille. **Proposition à valider par l'équipe** ; ensuite, aucune
> modification unilatérale. Les modèles Pydantic de `backend/app/books/schemas.py` sont la
> référence exécutable, et la documentation interactive est générée sur `/docs`.

Toutes les routes sont en `GET`, renvoient du JSON et sont préfixées par `/api`.

## 1. Routes

| Route | Rôle |
|---|---|
| `GET /api/health` | État du backend |
| `GET /api/books?limit=20&offset=0` | Livres paginés (triés par titre) |
| `GET /api/books/{book_id}` | Métadonnées d'un livre |
| `GET /api/books/{book_id}/text?page=1&page_size=4000` | Texte intégral, lecture paginée |
| `GET /api/books/{book_id}/similar?limit=6` | Voisins recommandés |
| `GET /api/search?q=...&limit=10&offset=0` | Recherche par mot-clé, résultats classés + suggestions |
| `GET /api/search/advanced?regex=...&limit=10&offset=0` | Recherche RegEx, résultats classés + suggestions |

### Paramètres

| Paramètre | Routes | Contraintes | Défaut |
|---|---|---|---|
| `limit` | books, search | 1 à 100 | 20 (books), 10 (search) |
| `offset` | books, search | ≥ 0 | 0 |
| `page` | text | ≥ 1 | 1 |
| `page_size` | text | 500 à 20 000 caractères | 4000 |
| `q` | search | non vide, ≤ 200 caractères | — |
| `regex` | search/advanced | non vide, ≤ 100 caractères | — |

## 2. Réponses

### Métadonnées d'un livre

```json
{"id": 123, "title": "Example", "author": "Author", "language": "en",
 "word_count": 15200, "file_path": "data/processed/123.txt",
 "source_url": "https://example.org/book"}
```

- `id` : entier unique et stable, identique dans tous les fichiers (métadonnées, index, graphe).
- `word_count` : nombre de mots avant filtrage des stopwords ; ≥ 10 000 pour chaque livre retenu.
- `file_path` : chemin relatif à la racine du projet, jamais absolu.

### `GET /api/books`

```json
{"total": 1664, "limit": 20, "offset": 0, "books": [ { "...métadonnées..." } ]}
```

### `GET /api/books/{book_id}/text`

```json
{"id": 123, "title": "Example", "page": 1, "page_size": 4000, "total_pages": 42, "text": "..."}
```

Les pages sont découpées sur un saut de ligne ou une espace : aucun mot n'est coupé, et la
concaténation de toutes les pages redonne exactement le texte nettoyé.

### `GET /api/search` et `GET /api/search/advanced`

```json
{
  "query": "ship",
  "mode": "simple",
  "total": 2,
  "limit": 10,
  "offset": 0,
  "results": [
    {"id": 123, "title": "Example", "author": "Author", "occurrences": 5, "pagerank": 0.002, "score": 0.84}
  ],
  "suggestions": [
    {"id": 456, "title": "Another book", "author": "Author", "similarity": 0.71}
  ]
}
```

- `mode` : `"simple"` ou `"regex"` ; `query` contient le mot-clé ou le motif.
- `total` : nombre total de livres correspondants (toutes pages confondues).
- `results` : triés par `score` décroissant ; `score` est normalisé dans [0, 1].
- `suggestions` : voisins Jaccard des 3 meilleurs résultats, sans doublon, sans les livres
  affichés sur la page ; triés par `similarity` décroissante (au plus 6).
- Aucun résultat : `200` avec `total: 0`, `results: []`, `suggestions: []`.

Ajouts par rapport à l'exemple des instructions, **à valider** : `mode`, `limit`, `offset`,
et `author` dans les suggestions.

### `GET /api/books/{book_id}/similar`

```json
{"book_id": 123, "suggestions": [{"id": 456, "title": "Another book", "author": "Author", "similarity": 0.71}]}
```

### `GET /api/health`

```json
{"status": "ok", "books_loaded": 10, "data_source": "sample",
 "modules": {"search": "mock", "regex": "mock", "ranking": "mock", "recommendations": "mock"}}
```

`data_source` vaut `"corpus"` dès que `data/metadata/books.json` existe. Chaque module vaut
`"real"` quand la fonction de l'équipe est implémentée, `"mock"` tant qu'elle est en TODO.

## 3. Erreurs

Format unique : `{"detail": "message lisible"}` (pour un `422`, `detail` est la liste
d'erreurs de validation de FastAPI).

| Code | Cas |
|---|---|
| `400` | Requête vide ou trop longue ; RegEx vide, trop longue, invalide ou trop coûteuse |
| `404` | Livre inconnu ; texte indisponible ; page au-delà de la dernière |
| `422` | Paramètre hors bornes ou mal typé (`limit=0`, `page=0`, `book_id` non entier) |

## 4. Fonctions internes (signatures à valider)

Appelées uniquement depuis `backend/app/integration.py`.

| Fonction | Responsable | Signature |
|---|---|---|
| `app.search.simple_search.search` | Kenza | `search(query: str) -> dict[int, int]` — `book_id -> occurrences` |
| `app.search.regex_search.regex_search` | Kenza | `regex_search(pattern: str) -> dict[int, int]` — lève `app.errors.InvalidRegexError` |
| `app.ranking.ranking_service.rank_results` | Nadine | `rank_results(results: dict[int, int]) -> list[dict]` — `[{id, occurrences, pagerank, score}]`, trié |
| `app.recommendations.recommendation_service.recommend` | Nadine | `recommend(book_ids: list[int], exclude: set[int] \| None = None, limit: int = 6) -> list[dict]` — `[{id, similarity}]`, trié |

Chargement au démarrage (une seule fois, jamais par requête) :
`inverted_index.load_index(indexes_dir)`, `graph_builder.load_graph(graphs_dir)`,
`pagerank.load_pagerank(graphs_dir)`.

**Règle de bascule** : tant qu'une fonction lève `NotImplementedError`, l'API répond avec le
moteur simulé (`app/mocks.py`). Requête vide ou sans correspondance : renvoyer `{}` ou `[]`,
jamais d'exception.

## 5. Fichiers pré-calculés attendus

| Fichier | Producteur | Contenu |
|---|---|---|
| `data/metadata/books.json` | Kenza | Liste JSON des métadonnées (format ci-dessus) |
| `data/processed/{id}.txt` | Kenza | Texte nettoyé et lisible, UTF-8 |
| `data/indexes/inverted_index.*` | Kenza | Terme normalisé → `{book_id: fréquence}` |
| `data/indexes/book_terms.*` | Kenza | `book_id` → ensemble des termes normalisés (entrée de Jaccard) |
| `data/indexes/original_to_normalized.*` | Kenza | Forme originale → terme normalisé (pour la RegEx) |
| `data/graphs/edges.*` | Nadine | Arêtes pondérées : similarité Jaccard au-dessus du seuil |
| `data/graphs/neighbors.*` | Nadine | `book_id` → voisins et poids |
| `data/graphs/pagerank.*` | Nadine | `book_id` → score PageRank |
| `data/graphs/stats.*` | Nadine | Mesures du graphe (arêtes, densité, isolés, composantes) |

Les noms sont ceux du plan final ; l'extension et le format interne restent à préciser par
Kenza et Nadine (TODO). L'API n'en dépend pas : elle n'appelle que les fonctions de la
section 4.

Jeu d'exemple versionné (10 livres simulés) : `data/sample/books.json`,
`data/sample/texts/{id}.txt`, `data/sample/neighbors.json`, `data/sample/pagerank.json`.
