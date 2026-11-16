"""Construction de l'index inversé — RESPONSABLE : KENZA (feature/data-search) — étapes K3, K4, K7.

Sorties attendues dans data/indexes/ :
    inverted_index.*           terme normalisé -> {book_id: fréquence}
    book_terms.*               book_id -> ensemble des termes normalisés (pour Nadine)
    original_to_normalized.*   forme originale -> terme normalisé (pour la RegEx)

Le script doit être relançable et ne jamais être exécuté pendant une requête
de l'API : le backend ne fait que charger les fichiers produits.

    python scripts/build_index.py
"""
from __future__ import annotations


def main() -> None:
    # TODO (Kenza) : tokeniser et normaliser avec app.search.inverted_index.normalize().
    # TODO (Kenza) : filtrer stopwords et termes trop fréquents (ex. DF > 99 %) ; stemming
    #                seulement si justifié ; mesurer la taille du vocabulaire avant/après.
    # TODO (Kenza) : construire l'index sur le contenu intégral, avec fréquences.
    # TODO (Kenza) : produire vocabulaire, book_terms et le mapping original -> normalisé.
    # TODO (Kenza) : mesurer couverture des 1 664 IDs, taille de l'index et temps de
    #                construction (docs/experiments.md).
    raise NotImplementedError("TODO Kenza : scripts/build_index.py")


if __name__ == "__main__":
    main()
