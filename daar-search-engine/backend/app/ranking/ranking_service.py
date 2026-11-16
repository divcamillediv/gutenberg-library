"""Classement des résultats — RESPONSABLE : NADINE (feature/graph-ranking).

Signature convenue avec Camille (voir docs/api_contract.md, « Fonctions internes »).
Tant que cette fonction lève NotImplementedError, l'API répond avec le
classement provisoire de app/mocks.py.
"""
from __future__ import annotations


def rank_results(results: dict[int, int]) -> list[dict]:
    """Classe {book_id: occurrences} par pertinence décroissante.

    Retour attendu, trié par `score` décroissant :
        [{"id": 123, "occurrences": 5, "pagerank": 0.002, "score": 0.84}, ...]

    TODO (Nadine) : définir le score combinant occurrences et PageRank, normalisé
                    dans [0, 1] ; justifier les poids par des mesures.
    TODO (Nadine) : `results` vide -> [] (pas d'exception).
    TODO (Nadine) : fournir un exemple chiffré et comparer avec le score textuel
                    seul (docs/experiments.md).
    TODO (Nadine) : tests dans tests/test_pagerank.py.
    """
    raise NotImplementedError("TODO Nadine : classement occurrences + PageRank")
