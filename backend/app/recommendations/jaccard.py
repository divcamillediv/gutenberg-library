def jaccard_similarity(a: set[str], b: set[str]) -> float:
    """Calcule la similarité de Jaccard entre deux ensembles."""

    if not a and not b:
        return 1.0

    # Calculer uniquement l'intersection
    intersection = len(a.intersection(b))

    # Pas besoin de construire l'ensemble union
    union = len(a) + len(b) - intersection

    return intersection / union


def jaccard_distance(a: set[str], b: set[str]) -> float:
    """Calcule la distance de Jaccard."""
    return 1.0 - jaccard_similarity(a, b)
