"""Nettoyage des textes — RESPONSABLE : KENZA (feature/data-search).

Sortie attendue : data/processed/*.txt, métadonnées mises à jour
Le script doit être relançable et ne jamais être exécuté pendant une requête
de l'API : le backend ne fait que charger les fichiers produits.

    python scripts/clean_books.py
"""
from __future__ import annotations


def main() -> None:
    # TODO (Kenza) : retirer les en-têtes et pieds de page Gutenberg.
    # TODO (Kenza) : écrire les textes nettoyés et lisibles dans data/processed/{id}.txt (affichés par l'application).
    # TODO (Kenza) : calculer word_count (avant filtrage des stopwords) et exclure les livres < 10 000 mots.
    # TODO (Kenza) : afficher le contrôle final : nombre total de livres, minimum de mots, exclusions.
    raise NotImplementedError("TODO Kenza : scripts/clean_books.py")


if __name__ == "__main__":
    main()
