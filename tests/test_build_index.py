
import json

from scripts.build_index import (
    construire_index_des_livres,
    enregistrer_index,
)


def test_construire_index(tmp_path):
    (tmp_path / "1.txt").write_text("La mer, la mer !", encoding="utf-8")
    (tmp_path / "2.txt").write_text("Le bateau sur la mer.", encoding="utf-8")
    (tmp_path / "3.txt").write_text("Un poisson.", encoding="utf-8")

    index = construire_index_des_livres(
        tmp_path, {"la", "le"}, seuil=0.8
    )

    assert index["mer"] == {"1": 2, "2": 1}
    assert "la" not in index
    assert "le" not in index

def test_filtrer_mots_trop_frequents(tmp_path):
    (tmp_path / "1.txt").write_text("mer bateau", encoding="utf-8")
    (tmp_path / "2.txt").write_text("mer poisson", encoding="utf-8")

    index = construire_index_des_livres(tmp_path, set(), seuil=0.8)

    assert "mer" not in index
    assert "bateau" in index
    assert "poisson" in index


def test_enregistrer_index(tmp_path):
    index = {"mer": {"1": 2}}
    chemin = tmp_path / "index.json"

    enregistrer_index(index, chemin)

    resultat = json.loads(chemin.read_text(encoding="utf-8"))
    assert resultat == index



