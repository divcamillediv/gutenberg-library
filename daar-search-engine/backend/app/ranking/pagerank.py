"""PageRank sur le graphe de Jaccard — RESPONSABLE : NADINE (feature/graph-ranking).

Le PageRank est calculé hors ligne par scripts/compute_pagerank.py puis chargé
UNE fois au démarrage du backend (app/integration.py appelle load_pagerank).
"""
from __future__ import annotations

from pathlib import Path


def compute_pagerank(
    neighbors: dict[int, dict[int, float]],
    damping: float = 0.85,
    max_iterations: int = 100,
    tolerance: float = 1e-8,
) -> dict[int, float]:
    """Calcule book_id -> pagerank à partir du graphe pondéré {u: {v: poids}}.

    TODO (Nadine) : itération de puissance, graphe pondéré non orienté.
    TODO (Nadine) : traiter les sommets isolés / sans voisin (redistribution).
    TODO (Nadine) : contrôler que la somme des scores vaut 1 et documenter la
                    définition et le calcul dans docs/algorithms.md.
    """
    raise NotImplementedError("TODO Nadine : calcul du PageRank")


def load_pagerank(graphs_dir: Path) -> None:
    """Charge en mémoire le fichier book_id -> pagerank de `graphs_dir` (data/graphs/).

    TODO (Nadine)
    """
    raise NotImplementedError("TODO Nadine : chargement du PageRank pré-calculé")


def get_pagerank(book_id: int) -> float:
    """Retourne le PageRank pré-calculé d'un livre.

    TODO (Nadine)
    """
    raise NotImplementedError("TODO Nadine : accès au PageRank d'un livre")
