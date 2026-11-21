from .similarity_matrix import construire_matrice_similarite

def construire_graphe(livres: dict[int, set[str]], seuil: float = 0.3) -> dict:
    if not 0 <= seuil <= 1:
        raise ValueError("Le seuil doit être compris entre 0 et 1")

    matrice = construire_matrice_similarite(livres)

    # Chaque livre est un sommet, même s'il n'a aucun voisin
    graphe = {id_livre: {} for id_livre in livres}

    for id1 in livres:
        for id2 in livres:
            # On évite les liens vers soi-même et les doublons
            if id1 >= id2:
                continue

            similarite = matrice[id1][id2]

            if similarite >= seuil and similarite > 0:
                # Le lien fonctionne dans les deux sens
                graphe[id1][id2] = similarite
                graphe[id2][id1] = similarite

    return graphe