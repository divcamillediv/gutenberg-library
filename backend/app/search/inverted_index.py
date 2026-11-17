
"""Index inverse construit a partir des mots nettoyes des livres."""


def creer_index(livres: dict[str, list[str]]) -> dict[str, dict[str, int]]:
    """Construit un index avec les mots et leurs occurrences dans chaque livre."""

    index: dict[str, dict[str, int]] = {}

    # On parcourt tous les livres
    for livre_id, mots in livres.items():

        # On verifie que le livre a un identifiant
        if not livre_id:
            raise ValueError("L'identifiant du livre ne doit pas etre vide.")

        # On parcourt les mots du livre
        for mot in mots:

            # On refuse les mots vides
            if not mot or not mot.strip():
                raise ValueError(f"Le livre {livre_id} contient un mot vide.")

            # Si le mot n'existe pas encore, on l'ajoute a l'index
            if mot not in index:
                index[mot] = {}

            # On initialise le compteur pour ce livre
            if livre_id not in index[mot]:
                index[mot][livre_id] = 0

            # On compte chaque apparition du mot
            index[mot][livre_id] += 1

    return index


def chercher_mot(index: dict[str, dict[str, int]], mot: str) -> dict[str, int]:
    """Cherche un mot et renvoie les livres qui le contiennent."""

    # On verifie que le mot recherche n'est pas vide
    if not mot or not mot.strip():
        raise ValueError("Le mot recherche ne doit pas etre vide.")

    # On retourne les livres trouves et leurs frequences
    return index.get(mot, {}).copy()


def retirer_mots_presents_dans_trop_de_livres(
        index: dict[str, dict[str, int]],
        nombre_total_livres: int,
        seuil: float = 0.8
) -> dict[str, dict[str, int]]:
    """Allège l'index inversé en retirant les mots présents dans presque
    tous les livres, car ils sont souvent moins utiles pour la recherche.
    """

    # On vérifie que le nombre de livres et le seuil sont valides
    if nombre_total_livres <= 0:
        raise ValueError("Le nombre de livres doit être positif.")

    if not 0 < seuil <= 1:
        raise ValueError("Le seuil doit être entre 0 et 1.")

    # On crée un nouvel index pour garder l'original
    index_filtre = {}

    # On parcourt chaque mot et les livres où il apparaît
    for mot, livres_contenant_mot in index.items():

        # On calcule dans quelle proportion des livres le mot apparaît
        proportion = len(livres_contenant_mot) / nombre_total_livres

        # On garde seulement les mots présents dans moins de livres que le seuil
        if proportion < seuil:
            index_filtre[mot] = livres_contenant_mot.copy()

    return index_filtre
