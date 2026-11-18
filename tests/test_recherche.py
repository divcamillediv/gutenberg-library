from backend.app.search.recherche import rechercher_livres


def test_rechercher_livres():
    index = {
        "alice": {"11": 3, "84": 1},
        "wonderland": {"11": 2, "74": 1}
    }

    resultat = rechercher_livres(index, "The Alice Wonderland!")

    assert resultat == {"11": 5}


def test_rechercher_livres_requete_vide():
    index = {
        "alice": {"11": 3}
    }

    resultat = rechercher_livres(index, "the and of")

    assert resultat == {}
