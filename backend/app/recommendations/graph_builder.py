import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from time import perf_counter
from datetime import timedelta

from .jaccard import jaccard_similarity


# Graphe chargé au démarrage de l'application
graphe_charge = {}


def construire_graphe(livres: dict[int, set[str]], seuil: float = 0.3) -> dict:
<<<<<<< Updated upstream
    """Construit un graphe pondéré à partir des similarités Jaccard."""
=======
    """Construit un graphe pondéré à partir des similarités de Jaccard."""
>>>>>>> Stashed changes

    if not 0 <= seuil <= 1:
        raise ValueError("Le seuil doit être compris entre 0 et 1")

    # Conserver tous les livres, même ceux sans voisins
    graphe = {id_livre: {} for id_livre in livres}

    # Index inversé temporaire : mot -> livres contenant ce mot
    index = defaultdict(list)

    for id_livre, mots in livres.items():
        for mot in mots:
            index[mot].append(id_livre)

    # Position de chaque livre pour éviter les doublons
    ids = list(livres)
    positions = {
        id_livre: i
        for i, id_livre in enumerate(ids)
    }

<<<<<<< Updated upstream
=======
    # Précalcul des tailles des vocabulaires
>>>>>>> Stashed changes
    tailles = {
        id_livre: len(mots)
        for id_livre, mots in livres.items()
    }

<<<<<<< Updated upstream
    # Comparer uniquement les livres partageant des mots
    for id1 in ids:
        mots1 = livres[id1]
        taille1 = tailles[id1]

        candidats = set()

        for mot in mots1:
            for id2 in index[mot]:
                if positions[id2] > positions[id1]:
                    candidats.add(id2)

        for id2 in candidats:
            taille2 = tailles[id2]

            # Jaccard ne peut pas dépasser min/max
            taille_min = min(taille1, taille2)
            taille_max = max(taille1, taille2)

            if taille_max > 0 and taille_min / taille_max < seuil:
                continue

            similarite = jaccard_similarity(mots1, livres[id2])

            if similarite > 0 and similarite >= seuil:
                graphe[id1][id2] = similarite
                graphe[id2][id1] = similarite
=======
    n = len(ids)
    total = n * (n - 1) // 2

    traitees = 0
    ignorees = 0
    calculees = 0
    aretes = 0

    debut = perf_counter()
    dernier_affichage = debut

    print(f"Nombre total de paires : {total:,}", flush=True)

    for i, id1 in enumerate(ids):
        mots1 = livres[id1]
        taille1 = tailles[id1]

        for id2 in ids[i + 1:]:
            taille2 = tailles[id2]
            traitees += 1

            minimum = min(taille1, taille2)
            maximum = max(taille1, taille2)

            # Éliminer les paires qui ne peuvent pas atteindre
            # le seuil de similarité demandé
            if maximum > 0 and (
                    minimum == 0 or minimum / maximum < seuil
            ):
                ignorees += 1

            else:
                similarite = jaccard_similarity(
                    mots1, livres[id2]
                )
                calculees += 1

                # Conserver uniquement les liens assez similaires
                if 0 < similarite and similarite >= seuil:
                    graphe[id1][id2] = similarite
                    graphe[id2][id1] = similarite
                    aretes += 1

            # Vérifier périodiquement la progression
            if traitees % 1000 == 0:
                maintenant = perf_counter()

                if maintenant - dernier_affichage >= 5:
                    ecoule = maintenant - debut
                    progression = traitees / total * 100

                    restant = (
                                      ecoule / traitees
                              ) * (total - traitees)

                    print(
                        f"Progression : {progression:.2f}% | "
                        f"Paires : {traitees:,}/{total:,} | "
                        f"Ignorées : {ignorees:,} | "
                        f"Arêtes : {aretes:,} | "
                        f"Temps écoulé : "
                        f"{timedelta(seconds=int(ecoule))} | "
                        f"Temps restant estimé : "
                        f"{timedelta(seconds=int(restant))}",
                        flush=True
                    )

                    dernier_affichage = maintenant

    duree = perf_counter() - debut

    print("\nConstruction du graphe terminée.", flush=True)
    print(f"Paires examinées : {traitees:,}", flush=True)
    print(f"Paires ignorées : {ignorees:,}", flush=True)
    print(f"Calculs Jaccard : {calculees:,}", flush=True)
    print(f"Nombre d'arêtes : {aretes:,}", flush=True)
    print(f"Temps de construction : {duree:.2f} secondes", flush=True)
>>>>>>> Stashed changes

    # Deux ensembles vides ont une similarité de 1
    # conformément à jaccard_similarity()
    livres_vides = [
        id_livre
        for id_livre, taille in tailles.items()
        if taille == 0
    ]

    for id1, id2 in combinations(livres_vides, 2):
        graphe[id1][id2] = 1.0
        graphe[id2][id1] = 1.0

    return graphe


def load_graph(directory: Path) -> dict:
    """Charge le graphe depuis graph.json."""

    global graphe_charge

    chemin = Path(directory) / "graph.json"

<<<<<<< Updated upstream
    with chemin.open("r", encoding="utf-8") as fichier:
        donnees = json.load(fichier)

=======
    # Lecture du graphe enregistré par build_graph.py
    with chemin.open("r", encoding="utf-8") as fichier:
        donnees = json.load(fichier)

    # Conversion des clés JSON en entiers
>>>>>>> Stashed changes
    graphe_charge = {
        int(livre): {
            int(voisin): float(poids)
            for voisin, poids in voisins.items()
        }
        for livre, voisins in donnees.items()
    }

    return graphe_charge