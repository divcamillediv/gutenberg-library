"""Graphe de Jaccard — RESPONSABLE : NADINE (feature/graph-ranking).

Le graphe est construit hors ligne par scripts/build_graph.py, puis chargé UNE
fois au démarrage du backend (app/integration.py appelle load_graph).
"""
from __future__ import annotations

from pathlib import Path


def build_graph(book_terms: dict[int, set[str]], threshold: float) -> dict[int, dict[int, float]]:
    """Construit le graphe pondéré {book_id: {voisin_id: similarité}}.

    TODO (Nadine) : calculer la matrice de similarité (1 664² cellules) ; contrôler
                    diagonale, symétrie et bornes.
    TODO (Nadine) : préciser si le seuil est en similarité (J >= seuil) ou en
                    distance (d <= seuil).
    TODO (Nadine) : comparer plusieurs seuils (densité, degrés, sommets isolés) et
                    justifier le seuil retenu dans docs/experiments.md.
    """
    raise NotImplementedError("TODO Nadine : construction du graphe de Jaccard")


def load_graph(graphs_dir: Path) -> None:
    """Charge en mémoire les listes de voisins stockées dans `graphs_dir` (data/graphs/).

    TODO (Nadine) : choisir et documenter le format (liste d'arêtes / voisins filtrés).
    """
    raise NotImplementedError("TODO Nadine : chargement du graphe pré-calculé")


def get_neighbors(book_id: int) -> dict[int, float]:
    """Retourne {voisin_id: similarité} pour un livre ({} si isolé ou inconnu).

    TODO (Nadine)
    """
    raise NotImplementedError("TODO Nadine : accès aux voisins d'un livre")
