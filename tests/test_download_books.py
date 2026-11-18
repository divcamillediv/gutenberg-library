from pathlib import Path
from unittest.mock import patch

from scripts.download_books import telecharger_plusieurs_livres


def test_telecharger_plusieurs_livres(tmp_path):
    def faux_telechargement(identifiant, dossier):
        chemin = dossier / f"{identifiant}.txt"
        chemin.write_text("Texte du livre", encoding="utf-8")
        return chemin

    with patch(
            "scripts.download_books.telecharger_livre",
            side_effect=faux_telechargement
    ):
        resultat = telecharger_plusieurs_livres([11, 84], tmp_path)

    assert set(resultat) == {11, 84}
    assert all(chemin.exists() for chemin in resultat.values())

def test_continuer_apres_erreur(tmp_path):
    def faux_telechargement(identifiant, dossier):
        if identifiant == 84:
            raise OSError("Site indisponible")

        chemin = dossier / f"{identifiant}.txt"
        chemin.write_text("Texte du livre", encoding="utf-8")
        return chemin

    with patch(
            "scripts.download_books.telecharger_livre",
            side_effect=faux_telechargement
    ):
        resultat = telecharger_plusieurs_livres([11, 84, 1342], tmp_path)

    assert set(resultat) == {11, 1342}
    assert 84 not in resultat

