"""Téléchargement du corpus Gutenberg — RESPONSABLE : KENZA (feature/data-search).

Sortie attendue : data/raw/*.txt, data/metadata/books.json
Le script doit être relançable et ne jamais être exécuté pendant une requête
de l'API : le backend ne fait que charger les fichiers produits.

    python scripts/download_books.py
"""
from __future__ import annotations


def main() -> None:
    # TODO (Kenza) : récupérer métadonnées et liens via https://gutendex.com/ (commencer par les 10 livres tests communs).
    # TODO (Kenza) : télécharger les textes bruts dans data/raw/{id}.txt ; relançable sans doublons.
    # TODO (Kenza) : dédoublonner, gérer les erreurs réseau, tenir un journal des exclusions.
    # TODO (Kenza) : écrire data/metadata/books.json au format du contrat (id, title, author, language, word_count, file_path, source_url).
    # TODO (Kenza) : viser >= 1 664 livres distincts de >= 10 000 mots chacun.
    raise NotImplementedError("TODO Kenza : scripts/download_books.py")


if __name__ == "__main__":
    main()
