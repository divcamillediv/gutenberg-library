
from backend.app.recommendations.jaccard import jaccard_similarity


def test_livres_partiellement_similaires():
    livre1 = {"mer", "bateau", "voyage"}
    livre2 = {"mer", "bateau", "pirate"}

    assert jaccard_similarity(livre1, livre2) == 0.5


def test_livres_identiques_et_differents():
    livre1 = {"mer", "bateau"}
    livre2 = {"montagne", "foret"}

    assert jaccard_similarity(livre1, livre1) == 1.0
    assert jaccard_similarity(livre1, livre2) == 0.0


def test_ensembles_vides():
    assert jaccard_similarity(set(), set()) == 1.0
    assert jaccard_similarity({"mer"}, set()) == 0.0