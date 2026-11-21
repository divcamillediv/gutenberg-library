"""Intégration de la recherche simple dans le backend FastAPI."""
from . import inverted_index
from .recherche import rechercher_livres


def search(query: str) -> dict[int, int]:
    """Recherche les livres correspondant à une requête."""

    # On vérifie que l'index est chargé
    if inverted_index.index_charge is None:
        raise NotImplementedError("Index inversé non chargé.")

    # On utilise notre algorithme de recherche existant
    resultats = rechercher_livres(
        inverted_index.index_charge,
        query
    )

    # On convertit les identifiants en entiers pour le backend
    return {
        int(livre_id): occurrences
        for livre_id, occurrences in resultats.items()
    }