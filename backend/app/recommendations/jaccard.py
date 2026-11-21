def jaccard_similarity(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0

    intersection = a & b
    union = a | b

    return len(intersection) / len(union)