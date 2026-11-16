
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
