"""Validation du corpus — RESPONSABLE : KENZA (feature/data-search) — étapes K1, K2.

Preuve attendue : rapport JSON établissant que la bibliothèque contient au moins
1 664 livres distincts d'au moins 10 000 mots chacun.

    python scripts/validate_corpus.py
"""
from __future__ import annotations


def main() -> None:
    # TODO (Kenza) : charger data/metadata/books.json et les textes de data/processed/.
    # TODO (Kenza) : vérifier >= 1 664 livres, identifiants uniques, absence de doublons.
    # TODO (Kenza) : recompter les mots de chaque texte ; refuser tout livre < 10 000 mots.
    # TODO (Kenza) : vérifier que chaque file_path est relatif et que le fichier existe.
    # TODO (Kenza) : écrire le rapport JSON (total, minimum de mots, rejets et motifs,
    #                provenance) ; choisir son emplacement et le documenter.
    # TODO (Kenza) : sortir avec un code d'erreur si une règle n'est pas respectée
    #                (scripts/rebuild_all.sh s'arrête alors).
    raise NotImplementedError("TODO Kenza : scripts/validate_corpus.py")


if __name__ == "__main__":
    main()
