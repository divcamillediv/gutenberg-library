import argparse
import json
import sys
import unicodedata
from pathlib import Path
from time import perf_counter

racine = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(racine))

from backend.app.recommendations.graph_builder import construire_graphe


def nettoyer_mots(texte: str) -> set[str]:
    """Nettoie le texte comme pour l'indexation des livres."""

    texte = unicodedata.normalize("NFC", texte).lower()

    caracteres = []
    for caractere in texte:
        if caractere.isalpha():
            caracteres.append(caractere)
        else:
            caracteres.append(" ")

    return set("".join(caracteres).split())


def charger_livres(dossier: Path) -> dict[str, set[str]]:
    """Lit les livres et récupère leurs mots distincts."""

    livres = {}

    for fichier in sorted(dossier.glob("*.txt")):
        identifiant = fichier.stem
        texte = fichier.read_text(encoding="utf-8-sig", errors="replace")

        livres[identifiant] = nettoyer_mots(texte)

    return livres


def enregistrer_graphe(graphe: dict, destination: Path) -> None:
    """Enregistre le graphe dans un fichier JSON."""

    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", encoding="utf-8") as fichier:
        json.dump(graphe, fichier, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/graphs/graph.json")
    )
    parser.add_argument("--seuil", type=float, default=0.3)

    args = parser.parse_args()

    if not args.corpus.is_dir():
        parser.error("Le dossier du corpus est introuvable")

    debut = perf_counter()

    livres = charger_livres(args.corpus)
    print(f"Livres chargés : {len(livres)}")

    graphe = construire_graphe(livres, seuil=args.seuil)

    duree = perf_counter() - debut
    enregistrer_graphe(graphe, args.output)

    nombre_aretes = sum(len(voisins) for voisins in graphe.values()) // 2

    print(f"Sommets : {len(graphe)}")
    print(f"Arêtes : {nombre_aretes}")
    print(f"Temps total : {duree:.2f} secondes")
    print(f"Graphe enregistré dans : {args.output}")


if __name__ == "__main__":
    main()
