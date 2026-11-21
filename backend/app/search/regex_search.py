"""Intégration de la recherche avancée dans le backend FastAPI."""
import re

from ..errors import InvalidRegexError
from . import inverted_index


def regex_search(pattern: str) -> dict[int, int]:
    """Recherche les livres correspondant à une expression régulière."""

    # On vérifie que l'index est chargé
    if inverted_index.index_charge is None:
        raise NotImplementedError("Index inversé non chargé.")

    try:
        # On vérifie que l'expression régulière est valide
        re.compile(pattern)

        # On utilise notre algorithme de recherche Regex existant
        resultats = inverted_index.chercher_regex(
            inverted_index.index_charge,
            pattern
        )

    except (re.error, ValueError) as exc:
        raise InvalidRegexError(
            f"Expression régulière invalide : {exc}"
        ) from exc

    # On convertit les identifiants en entiers pour le backend
    return {
        int(livre_id): occurrences
        for livre_id, occurrences in resultats.items()
    }