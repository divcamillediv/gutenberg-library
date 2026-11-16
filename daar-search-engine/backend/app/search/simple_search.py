"""Recherche simple par mot-clé — RESPONSABLE : KENZA (feature/data-search).

Signature convenue avec Camille (voir docs/api_contract.md, « Fonctions internes »).
Tant que cette fonction lève NotImplementedError, l'API répond avec le moteur
simulé de app/mocks.py.
"""
from __future__ import annotations


def search(query: str) -> dict[int, int]:
    """Retourne {book_id: occurrences} pour tous les livres dont l'index contient `query`.

    TODO (Kenza) : normaliser la requête avec inverted_index.normalize().
    TODO (Kenza) : interroger l'index chargé en mémoire (jamais de reconstruction).
    TODO (Kenza) : requête vide ou terme inconnu -> {} (pas d'exception).
    TODO (Kenza) : définir le comportement pour plusieurs mots (ET / OU) et le documenter.
    TODO (Kenza) : tests dans tests/test_search.py (terme connu, absent, vide ;
                   mot présent uniquement dans le corps d'un livre).
    """
    raise NotImplementedError("TODO Kenza : recherche simple sur l'index inversé")
