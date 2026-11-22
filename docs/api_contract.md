# Contrats proposés — à valider collectivement

Ce document est une proposition, pas une API implémentée ni une décision actée.

## Identifiants et termes

Proposition : un identifiant non vide de type `str` partout, y compris dans les
réponses HTTP. Cela évite les conversions implicites entre clés JSON et entiers.
Les IDs réels pourront être les IDs Gutenberg sous forme décimale, sans les
confondre avec les IDs `sample-*` du jeu synthétique.

Sur disque : `book_terms.json` contient `dict[str, list[str]]`, avec termes uniques.
En mémoire : `dict[str, set[str]]`. Les termes sont déjà normalisés par le module
d'indexation ; le module Jaccard ne refait ni stemming ni suppression des stopwords.

Les fréquences ne sont pas utilisées par Jaccard ensembliste. Une liste contenant
deux fois un terme ne doit pas augmenter sa contribution à la similarité.

## Interfaces Python proposées

Les signatures ci-dessous décrivent les futures fonctions, sans les implémenter.
Les structures de sortie devront recevoir des types précis lors de leur création.

```python
jaccard_similarity(a: set[str], b: set[str]) -> float
jaccard_distance(a: set[str], b: set[str]) -> float

build_similarity_matrix(
    book_terms: dict[str, set[str]],
) -> tuple[list[str], list[list[float]]]

build_graph(
    book_ids: list[str],
    matrix: list[list[float]],
    *,
    threshold: float,
) -> dict[str, list[dict]]

graph_statistics(neighbors: dict[str, list[dict]]) -> dict

compute_pagerank(
    neighbors: dict[str, list[dict]],
    *,
    damping: float,
    tolerance: float,
    max_iter: int,
) -> dict[str, float]

rank_results(
    occurrences: dict[str, int],
    pagerank: dict[str, float],
    *,
    strategy: str,
    alpha: float,
) -> list[dict]

recommend(
    book_ids: list[str],
    neighbors: dict[str, list[dict]],
    *,
    exclude_ids: set[str],
    limit: int,
) -> list[dict]
```

Le type numérique de la matrice pourra évoluer vers NumPy après validation des
dépendances. La liste `book_ids` définit explicitement l'ordre des lignes et
colonnes et doit être persistée avec la matrice.

## Formats des échanges

Entrée du classement fournie par la recherche :

```json
{"sample-01": 5, "sample-03": 2}
```

Il s'agit des occurrences agrégées pour chaque candidat, pas d'un score Jaccard.
La règle multi-termes (ET/OU, somme des fréquences, répétitions de requête)
doit être convenue avec le module de recherche.

Graphe d'exemple limité à trois sommets :

```json
{
  "sample-01": [{"id": "sample-03", "similarity": 0.5}],
  "sample-03": [{"id": "sample-01", "similarity": 0.5}],
  "sample-10": []
}
```

Chaque arête non orientée est présente dans les deux listes d'adjacence, mais une
seule fois dans `edges.json`, sous la forme
`{"source": "sample-01", "target": "sample-03", "similarity": 0.5}`.
Tous les IDs doivent apparaître dans les voisins, même sans arête.

PageRank : objet `book_id -> float`, avec un score pour chaque sommet.

Sortie du classement : liste d'objets avec `id`, `occurrences`, `pagerank`, `score`.
Sortie des recommandations : liste d'objets avec `id`, `similarity`.
Les titres et auteurs sont ajoutés par le service de métadonnées, pas par les
algorithmes.

## Règles à valider avant chaque implémentation

| Sujet | Proposition, non encore validée |
|---|---|
| Ensembles vides | `J(vide, vide) = 1`, distance 0 ; un seul ensemble vide donne J = 0 |
| Graphe | Non orienté, sans boucle ; conserver une paire si `J > threshold`, seuil dans [0, 1] |
| Documents sans termes | Les signaler ; décider s'ils restent dans le graphe pour éviter des liens artificiels entre documents vides |
| PageRank | Pondéré, téléportation uniforme et redistribution uniforme de la masse des sommets pendants |
| Convergence | Critère L1 explicite ; erreur si le maximum d'itérations est atteint sans convergence |
| Graphe vide | Refuser le calcul PageRank sans sommet avec une erreur explicite |
| Classement | Comparer occurrences seules, PageRank seul, combinaison |
| Combinaison | `alpha * texte_normalise + (1 - alpha) * pagerank_normalise`, alpha dans [0, 1] |
| Normalisation | Étudier une division par le maximum parmi les candidats ; maximum nul donne un vecteur nul |
| Scores absents | Signaler une incohérence d'artefacts plutôt que remplacer silencieusement par zéro |
| Suggestions | Maximum des similarités aux sources ; exclure les sources et `exclude_ids` |
| Ordre | Score décroissant, puis identifiant pour départager les égalités de façon déterministe |

Pour les suggestions de recherche, l'API choisit les deux ou trois premiers
résultats comme sources. Il reste à décider si `exclude_ids` représente la page
affichée ou tous les résultats de la recherche. Le service ne doit pas le deviner.
Le seuil et alpha seront choisis à partir d'expériences réelles, pas du jeu fictif.

## API HTTP (couche web — Camille)

Implémentée dans `backend/app/books/routes.py` et `backend/app/search/routes.py` ;
les modèles Pydantic de `backend/app/books/schemas.py` sont la référence exécutable
et la documentation interactive est générée sur `/docs`. Toutes les routes sont en
`GET`, renvoient du JSON et sont préfixées par `/api`.

### Routes

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

### Réponses

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
  ],
  "title_matches": [
    {"id": 789, "title": "Ship Stories", "author": "Author"}
  ]
}
```

- `mode` : `"simple"` ou `"regex"` ; `query` contient le mot-clé ou le motif.
- `total` : nombre total de livres correspondants (toutes pages confondues).
- `results` : triés par `score` décroissant ; `score` est normalisé dans [0, 1].
- `suggestions` : voisins Jaccard des 3 meilleurs résultats, sans doublon, sans les livres
  affichés sur la page ; triés par `similarity` décroissante (au plus 6).
- `title_matches` (recherche simple, première page) : jusqu'à 5 livres dont le titre ou
  l'auteur, lus dans la base, contiennent tous les mots utiles de la requête. Complément
  hors classement ; les livres déjà présents dans `results` ne sont pas répétés.
  Toujours `[]` pour la recherche RegEx.
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

`data_source` vaut `"postgres"` si les métadonnées viennent de PostgreSQL (`POSTGRES_PASSWORD`
défini et base joignable), sinon `"corpus"` si `data/metadata/books.json` existe, sinon `"sample"`. Chaque module vaut
`"real"` quand la fonction de l'équipe est implémentée, `"mock"` tant qu'elle est en TODO.

### Erreurs

Format unique : `{"detail": "message lisible"}` (pour un `422`, `detail` est la liste
d'erreurs de validation de FastAPI).

| Code | Cas |
|---|---|
| `400` | Requête vide ou trop longue ; RegEx vide, trop longue, invalide ou trop coûteuse |
| `404` | Livre inconnu ; texte indisponible ; page au-delà de la dernière |
| `422` | Paramètre hors bornes ou mal typé (`limit=0`, `page=0`, `book_id` non entier) |

### Branchement des modules

`backend/app/integration.py` appelle les fonctions des modules de recherche, de
classement et de recommandation. Tant qu'une fonction est absente (squelette) ou
lève `NotImplementedError`, l'API répond avec un moteur simulé sur les 10 livres de
`data/sample/books.json`, et `/api/health` l'indique module par module (`mock` ou
`real`). Les identifiants renvoyés par les modules sont convertis en entiers.

Décisions encore ouvertes entre la couche web et les modules :

| Sujet | Couche web actuelle | Proposition ci-dessus | À trancher |
|---|---|---|---|
| Type des identifiants dans l'API | `int` (instructions communes) | `str` partout | Garder `int` côté HTTP ; les modules peuvent travailler en `str` numériques |
| `rank_results` | `rank_results(occurrences)` | `rank_results(occurrences, pagerank, *, strategy, alpha)` | Si la signature avec `pagerank` est retenue, l'API charge `pagerank.json` et le passe |
| `recommend` | `recommend(book_ids, exclude=None, limit=6)` | `recommend(book_ids, neighbors, *, exclude_ids, limit)` | Si la signature avec `neighbors` est retenue, l'API charge `neighbors.json` et le passe |
| `exclude_ids` des suggestions | livres affichés sur la page courante | à décider | Page courante (proposition de la couche web) |
