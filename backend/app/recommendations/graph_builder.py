from .jaccard import jaccard_similarity


def construire_graphe(livres: dict[int, set[str]], seuil: float = 0.3) -> dict:
    if not 0 <= seuil <= 1:
        raise ValueError("Le seuil doit être compris entre 0 et 1")

    ids = list(livres)
    graphe = {id_livre: {} for id_livre in ids}

    for i, id1 in enumerate(ids):
        for id2 in ids[i + 1:]:
            similarite = jaccard_similarity(livres[id1], livres[id2])

            # On garde uniquement les liens assez similaires
            if 0 < similarite and similarite >= seuil:
                graphe[id1][id2] = similarite
                graphe[id2][id1] = similarite

    return graphe