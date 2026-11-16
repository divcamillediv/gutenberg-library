"""Calcul du PageRank — RESPONSABLE : NADINE (feature/graph-ranking) — étape N5.

Sortie attendue : data/graphs/pagerank.* (book_id -> pagerank).

Le script doit être relançable et ne jamais être exécuté pendant une requête
de l'API : le backend ne fait que charger le fichier produit.

    python scripts/compute_pagerank.py
"""
from __future__ import annotations


def main() -> None:
    # TODO (Nadine) : charger le graphe de data/graphs/ (edges ou neighbors).
    # TODO (Nadine) : appeler app.ranking.pagerank.compute_pagerank().
    # TODO (Nadine) : documenter amortissement, convergence, traitement des isolés et
    #                 normalisation ; contrôler que la somme des scores vaut 1.
    # TODO (Nadine) : écrire data/graphs/pagerank.* et mesurer le temps de calcul.
    raise NotImplementedError("TODO Nadine : scripts/compute_pagerank.py")


if __name__ == "__main__":
    main()
