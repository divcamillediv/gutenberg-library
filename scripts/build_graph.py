"""Construction du graphe de Jaccard — RESPONSABLE : NADINE (feature/graph-ranking) — étapes N1 à N4.

Sorties attendues dans data/graphs/ :
    edges.*       arêtes pondérées (similarité Jaccard au-dessus du seuil)
    neighbors.*   book_id -> voisins et poids
    stats.*       mesures par seuil (arêtes, densité, isolés, composantes, coût)

Le script doit être relançable et ne jamais être exécuté pendant une requête
de l'API : le backend ne fait que charger les fichiers produits.

    python scripts/build_graph.py
"""
from __future__ import annotations


def main() -> None:
    # TODO (Nadine) : lire data/indexes/book_terms.* fourni par Kenza.
    # TODO (Nadine) : calculer la similarité de Jaccard ; vérifier symétrie, diagonale et
    #                 bornes [0, 1].
    # TODO (Nadine) : calculer ou pouvoir reconstituer les distances 1 - Jaccard
    #                 (1 664 livres = 1 383 616 paires uniques ; stockage compact accepté).
    # TODO (Nadine) : tester plusieurs seuils ; mesurer arêtes, densité, isolés,
    #                 composantes et coût ; justifier le seuil retenu.
    # TODO (Nadine) : construire le graphe pondéré et écrire edges, neighbors et stats.
    raise NotImplementedError("TODO Nadine : scripts/build_graph.py")


if __name__ == "__main__":
    main()
