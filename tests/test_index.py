
"""Tests de l'index inverse."""

import pytest

from backend.app.search.inverted_index import chercher_mot, creer_index


def test_creer_index():
    # On verifie le nombre d'occurrences dans chaque livre
    livres = {
        "1": ["mer", "bateau", "mer"],
        "2": ["mer", "ile"],
    }

    assert creer_index(livres) == {
        "mer": {"1": 2, "2": 1},
        "bateau": {"1": 1},
        "ile": {"2": 1},
    }


def test_livres_vides():
    # Un corpus vide doit donner un index vide
    assert creer_index({}) == {}
    assert creer_index({"1": [], "2": []}) == {}


def test_livre_vide_et_livre_rempli():
    # Un livre vide ne doit pas apparaitre dans l'index
    assert creer_index({"1": [], "2": ["mer"]}) == {"mer": {"2": 1}}


def test_identifiant_vide():
    # On refuse un livre sans identifiant
    with pytest.raises(ValueError, match="identifiant"):
        creer_index({"": []})


def test_mot_vide_dans_livre():
    # On refuse les mots vides
    with pytest.raises(ValueError, match="mot vide"):
        creer_index({"1": ["mer", ""]})


def test_livres_non_modifies():
    # La creation de l'index ne doit pas modifier les livres
    livres = {"1": ["mer", "bateau", "mer"]}

    creer_index(livres)

    assert livres == {"1": ["mer", "bateau", "mer"]}


def test_chercher_mot():
    # On cherche un mot present dans plusieurs livres
    index = creer_index({"1": ["mer", "mer"], "2": ["mer", "ile"]})

    assert chercher_mot(index, "mer") == {"1": 2, "2": 1}


def test_mot_absent():
    # Un mot absent doit retourner un dictionnaire vide
    index = creer_index({"1": ["mer"]})

    assert chercher_mot(index, "montagne") == {}
    assert index == {"mer": {"1": 1}}
    assert chercher_mot({}, "mer") == {}


def test_recherche_vide():
    # On refuse une recherche vide
    with pytest.raises(ValueError, match="mot recherche"):
        chercher_mot({}, "")


def test_resultat_independant():
    # Modifier le resultat ne doit pas changer l'index
    index = creer_index({"1": ["mer", "mer"]})

    resultat = chercher_mot(index, "mer")
    resultat["1"] = 99
    resultat["2"] = 1

    assert index == {"mer": {"1": 2}}


def test_pas_de_nettoyage_implicite():
    # Les majuscules et minuscules restent differentes
    index = creer_index({"1": ["Mer", "mer"]})

    assert index == {"Mer": {"1": 1}, "mer": {"1": 1}}
    assert chercher_mot(index, "MER") == {}
