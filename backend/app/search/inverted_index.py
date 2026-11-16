"""Index inversé du contenu des livres — RESPONSABLE : KENZA (feature/data-search).

Contrat commun (section 3 des instructions) :
    data/indexes/inverted_index.*          terme_normalisé -> {book_id: fréquence}
    data/indexes/book_terms.*              book_id -> ensemble des termes normalisés (pour Nadine)
    data/indexes/original_to_normalized.*  forme originale -> terme normalisé (pour la RegEx)

L'index est construit hors ligne par scripts/build_index.py, puis chargé UNE
fois au démarrage du backend (app/integration.py appelle load_index).
"""
from __future__ import annotations

from pathlib import Path


def normalize(text: str) -> list[str]:
    """Transforme un texte (ou une requête) en liste de termes normalisés.

    TODO (Kenza) : casse, ponctuation, tokenisation, stopwords, stemming éventuel.
    TODO (Kenza) : utiliser EXACTEMENT ce pipeline pour l'index, la recherche et
                   book_terms (Nadine s'appuie dessus pour Jaccard).
    """
    raise NotImplementedError("TODO Kenza : pipeline de normalisation")


def load_index(index_dir: Path) -> None:
    """Charge en mémoire l'index inversé stocké dans `index_dir` (data/indexes/).

    TODO (Kenza) : choisir le format de stockage (JSON compressé, SQLite, ...) et
                   le documenter dans docs/algorithms.md.
    TODO (Kenza) : garder l'index dans une variable de module pour get_postings().
    """
    raise NotImplementedError("TODO Kenza : chargement de l'index inversé")


def get_postings(term: str) -> dict[int, int]:
    """Retourne {book_id: fréquence} pour un terme déjà normalisé ({} si absent).

    TODO (Kenza)
    """
    raise NotImplementedError("TODO Kenza : accès aux postings d'un terme")


def vocabulary() -> list[str]:
    """Retourne tous les termes indexés (utilisé par la recherche RegEx).

    TODO (Kenza)
    """
    raise NotImplementedError("TODO Kenza : vocabulaire de l'index")


def original_forms() -> dict[str, str]:
    """Retourne le mapping forme originale -> terme normalisé (original_to_normalized).

    TODO (Kenza) : charger ce mapping dans load_index() ; il permet à la RegEx de
                   porter sur les mots tels qu'ils apparaissent dans les livres.
    """
    raise NotImplementedError("TODO Kenza : mapping formes originales -> termes normalisés")
