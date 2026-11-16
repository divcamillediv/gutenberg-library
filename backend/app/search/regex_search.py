"""Recherche avancée par RegEx — RESPONSABLE : KENZA (feature/data-search).

Choix d'équipe : la RegEx est appliquée aux TERMES de l'index (et non au texte
brut). C'est simple et rapide, mais limité aux motifs portant sur un seul terme
normalisé : les limites doivent être expliquées dans le rapport.

Signature convenue avec Camille (voir docs/api_contract.md, « Fonctions internes »).
Tant que cette fonction lève NotImplementedError, l'API répond avec le moteur
simulé de app/mocks.py.
"""
from __future__ import annotations

from app.errors import InvalidRegexError  # noqa: F401  (à lever pour un motif invalide)


def regex_search(pattern: str) -> dict[int, int]:
    """Retourne {book_id: occurrences cumulées} des livres dont un terme vérifie `pattern`.

    TODO (Kenza) : compiler le motif ; lever InvalidRegexError si invalide (-> HTTP 400).
    TODO (Kenza) : parcourir inverted_index.vocabulary() et cumuler les fréquences
                   des termes qui vérifient le motif.
    TODO (Kenza) : limiter la taille/complexité du motif et prévoir un timeout
                   (motifs coûteux du type (a+)+$) ; lever InvalidRegexError.
    TODO (Kenza) : décider si le motif porte sur les termes normalisés ou sur les formes
                   originales (inverted_index.original_forms()) ; traiter les limites
                   liées à la normalisation (running/run, mots filtrés) et les expliquer.
    TODO (Kenza) : éventuellement brancher l'automate du projet 1 (Aho-Ullman) et
                   comparer avec la bibliothèque standard dans le rapport.
    TODO (Kenza) : tests dans tests/test_regex.py (valide, invalide, sans
                   correspondance, coûteux).
    """
    raise NotImplementedError("TODO Kenza : recherche RegEx sur les termes indexés")
