"""Construction du graphe de Jaccard — RESPONSABLE : NADINE (feature/graph-ranking).

Sortie attendue : data/graphs/ (graphe, voisins, statistiques)
Le script doit être relançable et ne jamais être exécuté pendant une requête
de l'API : le backend ne fait que charger les fichiers produits.

    python scripts/build_graph.py
"""
from __future__ import annotations


def main() -> None:
    # TODO (Nadine) : charger book_terms (data/indexes/) fourni par Kenza.
    # TODO (Nadine) : calculer la matrice de similarité de Jaccard ; contrôler diagonale, symétrie, bornes.
    # TODO (Nadine) : comparer plusieurs seuils (densité, degrés, sommets isolés) et retenir un seuil justifié.
    # TODO (Nadine) : exporter le graphe pondéré / listes de voisins dans data/graphs/ avec des identifiants stables.
    # TODO (Nadine) : conserver des exemples de paires similaires et non similaires ; mesurer le temps de construction.
    raise NotImplementedError("TODO Nadine : scripts/build_graph.py")


if __name__ == "__main__":
    main()
