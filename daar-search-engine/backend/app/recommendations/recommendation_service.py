"""Suggestions de livres similaires — RESPONSABLE : NADINE (feature/graph-ranking).

Stratégie retenue par l'équipe : voisins, dans le graphe de Jaccard, des 2 ou 3
résultats les plus pertinents.

Signature convenue avec Camille (voir docs/api_contract.md, « Fonctions internes »).
Tant que cette fonction lève NotImplementedError, l'API répond avec les
suggestions fictives de app/mocks.py.
"""
from __future__ import annotations


def recommend(book_ids: list[int], exclude: set[int] | None = None, limit: int = 6) -> list[dict]:
    """Suggère les voisins Jaccard des livres `book_ids`.

    Retour attendu, trié par similarité décroissante, sans doublon :
        [{"id": 456, "similarity": 0.71}, ...]

    TODO (Nadine) : réunir les voisins de chaque livre via graph_builder.get_neighbors().
    TODO (Nadine) : dédoublonner (garder la meilleure similarité), exclure
                    `book_ids` et `exclude` (livres déjà affichés).
    TODO (Nadine) : `book_ids` vide -> [] (pas d'exception).
    TODO (Nadine) : mesurer le temps de recommandation et la qualité qualitative.
    """
    raise NotImplementedError("TODO Nadine : suggestions par voisinage Jaccard")
