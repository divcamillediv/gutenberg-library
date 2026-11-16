"""Couche d'intégration (responsable : Camille) — étape 6 du plan.

Unique point de contact entre les routeurs FastAPI et les modules de l'équipe :

* Kenza  : app.search.simple_search.search, app.search.regex_search.regex_search
* Nadine : app.ranking.ranking_service.rank_results,
           app.recommendations.recommendation_service.recommend

Tant qu'une de ces fonctions lève NotImplementedError (TODO non réalisé), la
réponse provient du moteur simulé (app/mocks.py). Aucun changement n'est
nécessaire ici lorsque les vrais modules arrivent : il suffit qu'ils cessent
de lever NotImplementedError.
"""
from __future__ import annotations

import logging
from typing import Callable

from app.books.service import book_service
from app.config import settings
from app.mocks import mock_engine
from app.ranking import pagerank, ranking_service
from app.recommendations import graph_builder, recommendation_service
from app.search import inverted_index, regex_search, simple_search

logger = logging.getLogger(__name__)

# Origine des réponses par module : "real" ou "mock" (exposé par /api/health).
module_status: dict[str, str] = {
    "search": "mock",
    "regex": "mock",
    "ranking": "mock",
    "recommendations": "mock",
}


def _call(name: str, real: Callable, mock: Callable, *args, **kwargs):
    """Appelle la fonction réelle ; bascule sur la simulation si elle est en TODO."""
    try:
        result = real(*args, **kwargs)
        module_status[name] = "real"
        return result
    except NotImplementedError:
        module_status[name] = "mock"
        return mock(*args, **kwargs)


# ------------------------------------------------------------------------ démarrage
def startup() -> None:
    """Charge une seule fois les fichiers pré-calculés (index, graphe, PageRank)."""
    mock_engine.reset()
    loaders = [
        ("index inversé (Kenza)", lambda: inverted_index.load_index(settings.indexes_dir)),
        ("graphe de Jaccard (Nadine)", lambda: graph_builder.load_graph(settings.graphs_dir)),
        ("PageRank (Nadine)", lambda: pagerank.load_pagerank(settings.graphs_dir)),
    ]
    for label, loader in loaders:
        try:
            loader()
            logger.info("Chargé : %s", label)
        except NotImplementedError:
            logger.warning("Non implémenté, simulation utilisée : %s", label)

    # Sondes : déterminent dès le démarrage quels modules sont réels.
    _call("search", simple_search.search, mock_engine.search, "probe")
    _call("regex", regex_search.regex_search, mock_engine.regex_search, "probe")
    _call("ranking", ranking_service.rank_results, mock_engine.rank_results, {})
    _call("recommendations", recommendation_service.recommend, mock_engine.recommend, [])
    logger.info("État des modules : %s", module_status)


# ------------------------------------------------------------------------- services
def search_simple(query: str) -> dict[int, int]:
    """Mot-clé -> {book_id: occurrences}."""
    return _call("search", simple_search.search, mock_engine.search, query)


def search_regex(pattern: str) -> dict[int, int]:
    """RegEx -> {book_id: occurrences}. Peut lever InvalidRegexError."""
    return _call("regex", regex_search.regex_search, mock_engine.regex_search, pattern)


def rank(results: dict[int, int]) -> list[dict]:
    """{book_id: occurrences} -> [{id, occurrences, pagerank, score}] trié par score décroissant."""
    return _call("ranking", ranking_service.rank_results, mock_engine.rank_results, results)


def suggest(book_ids: list[int], exclude: set[int] | None = None, limit: int = 6) -> list[dict]:
    """Voisins Jaccard enrichis des métadonnées : [{id, title, author, similarity}]."""
    raw = _call(
        "recommendations",
        recommendation_service.recommend,
        mock_engine.recommend,
        book_ids,
        exclude=exclude,
        limit=limit,
    )
    suggestions, seen = [], set()
    for item in raw:
        book = book_service.find(int(item["id"]))
        if book is None or book["id"] in seen:  # identifiant inconnu ou doublon
            continue
        seen.add(book["id"])
        suggestions.append(
            {
                "id": book["id"],
                "title": book["title"],
                "author": book["author"],
                "similarity": round(float(item["similarity"]), 4),
            }
        )
    return suggestions
