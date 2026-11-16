"""Calcul du PageRank — RESPONSABLE : NADINE (feature/graph-ranking).

Sortie attendue : data/graphs/pagerank (book_id -> pagerank)
Le script doit être relançable et ne jamais être exécuté pendant une requête
de l'API : le backend ne fait que charger les fichiers produits.

    python scripts/compute_pagerank.py
"""
from __future__ import annotations


def main() -> None:
    # TODO (Nadine) : charger le graphe de data/graphs/.
    # TODO (Nadine) : appeler app.ranking.pagerank.compute_pagerank() ; traiter les sommets isolés.
    # TODO (Nadine) : contrôler les scores (somme = 1) et écrire book_id -> pagerank dans data/graphs/.
    # TODO (Nadine) : illustrer le résultat sur quelques livres du corpus pour le rapport.
    raise NotImplementedError("TODO Nadine : scripts/compute_pagerank.py")


if __name__ == "__main__":
    main()
