"""Recherche de livres à partir d'une phrase."""

from backend.app.search.nettoyage import decouper_mots, supprimer_stopwords
from backend.app.search.stopwords import STOPWORDS_ANGLAIS
from backend.app.search.inverted_index import chercher_plusieurs_mots


def rechercher_livres(
        index: dict[str, dict[str, int]],
        requete: str
) -> dict[str, int]:
    """Recherche les livres contenant tous les mots utiles de la requête."""

    # On nettoie la phrase et on la découpe en mots
    mots = decouper_mots(requete)

    # On retire les mots courants anglais
    mots = supprimer_stopwords(mots, STOPWORDS_ANGLAIS)

    # On recherche les livres contenant tous les mots
    return chercher_plusieurs_mots(index, mots)
