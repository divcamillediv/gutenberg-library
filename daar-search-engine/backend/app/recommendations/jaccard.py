"""Similarité et distance de Jaccard — RESPONSABLE : NADINE (feature/graph-ranking).

Contrat commun : J(A, B) = |A ∩ B| / |A ∪ B| sur les ensembles de termes
normalisés (book_terms fourni par Kenza) ; distance d = 1 - J.
"""
from __future__ import annotations


def jaccard_similarity(terms_a: set[str], terms_b: set[str]) -> float:
    """Similarité de Jaccard dans [0, 1].

    TODO (Nadine) : implémenter, y compris le cas des ensembles vides (convention
                    à fixer et à documenter).
    TODO (Nadine) : tests dans tests/test_jaccard.py (cas connus, symétrie, bornes).
    """
    raise NotImplementedError("TODO Nadine : similarité de Jaccard")


def jaccard_distance(terms_a: set[str], terms_b: set[str]) -> float:
    """Distance de Jaccard d = 1 - J.

    TODO (Nadine)
    """
    raise NotImplementedError("TODO Nadine : distance de Jaccard")
