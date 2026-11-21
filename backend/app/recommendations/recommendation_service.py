
def recommend(
    book_ids: list[int],
    neighbors: dict[int, dict[int, float]],
    *,
    exclude_ids=None,
    limit: int = 3
) -> list[int]:

    if limit < 0:
        raise ValueError("La limite ne peut pas être negative")

    if limit == 0 or not book_ids:
        return []

    # On exclut les livres de départ et ceux déjà affichés
    exclus = set(book_ids)

    if exclude_ids is not None:
        exclus.update(exclude_ids)

    scores = {}

    for livre in book_ids:
        # On récupère les voisins de chaque livre
        for voisin, similarite in neighbors.get(livre, {}).items():

            if voisin in exclus:
                continue

            # On garde la meilleure similarité pour chaque voisin
            if voisin not in scores or similarite > scores[voisin]:
                scores[voisin] = similarite

    # Les livres les plus similaires arrivent en premier
    recommandations = sorted(
        scores,
        key=lambda livre: (-scores[livre], livre)
    )

    return recommandations[:limit]
