"""Nettoyage des textes avant l'indexation."""

import unicodedata


def nettoyer_texte(texte: str) -> str:
    """Met le texte en minuscules et retire les caracteres inutiles."""

    # On garde les accents et on met en minuscules
    texte = unicodedata.normalize("NFC", texte).lower()

    caracteres = []

    # On garde les lettres et on remplace le reste par des espaces
    for caractere in texte:
        if caractere.isalpha():
            caracteres.append(caractere)
        else:
            caracteres.append(" ")

    # On rassemble le texte et on retire les espaces en trop
    texte = "".join(caracteres)
    return " ".join(texte.split())


def decouper_mots(texte: str) -> list[str]:
    """Renvoie la liste des mots nettoyes."""

    return nettoyer_texte(texte).split()
