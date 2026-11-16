"""Construction de l'index inversé — RESPONSABLE : KENZA (feature/data-search).

Sortie attendue : data/indexes/ (index inversé, vocabulaire, book_terms)
Le script doit être relançable et ne jamais être exécuté pendant une requête
de l'API : le backend ne fait que charger les fichiers produits.

    python scripts/build_index.py
"""
from __future__ import annotations


def main() -> None:
    # TODO (Kenza) : tokeniser et normaliser avec app.search.inverted_index.normalize().
    # TODO (Kenza) : choisir stopwords, fréquence documentaire maximale (ex. > 99 %), stemming éventuel ; mesurer la réduction du vocabulaire.
    # TODO (Kenza) : construire terme -> {book_id: fréquence} sur le texte intégral ; l'écrire dans data/indexes/.
    # TODO (Kenza) : exporter book_terms (book_id -> ensemble de termes) pour Nadine.
    # TODO (Kenza) : mesurer durée de construction et taille de l'index sur 10/100/500/1664 livres (docs/experiments.md).
    raise NotImplementedError("TODO Kenza : scripts/build_index.py")


if __name__ == "__main__":
    main()
