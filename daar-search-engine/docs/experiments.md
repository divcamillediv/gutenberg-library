# Expériences et mesures — DAAR Projet 2

Privilégier courbes et diagrammes en bâtons (moyenne + écart type) plutôt que des colonnes
de chiffres. Citer la provenance des fichiers sources.

## 1. Corpus — TODO Kenza

- TODO (Kenza) : provenance (Gutenberg / Gutendex), nombre de livres, minimum de mots, exclusions.

## 2. Filtrage du vocabulaire — TODO Kenza

- TODO (Kenza) : tableau avant/après (stopwords, fréquence documentaire maximale, stemming) + justification.

## 3. Index et recherche — TODO Kenza

- TODO (Kenza) : durée de construction, taille de l'index, temps de recherche simple et RegEx
  sur 10 / 100 / 500 / 1664 livres.

## 4. Graphe de Jaccard — TODO Nadine

- TODO (Nadine) : comparaison des seuils (densité, degrés, sommets isolés), seuil retenu.
- TODO (Nadine) : exemples de paires similaires et non similaires ; temps de construction.

## 5. PageRank, classement, suggestions — TODO Nadine

- TODO (Nadine) : distribution des scores, comparaison avec le score textuel seul,
  temps de recommandation, appréciation qualitative.

## 6. API et application — Camille

Mesures à relever sur le corpus complet, une fois les modules branchés :

- TODO (Camille) : temps de réponse de `/api/search`, `/api/search/advanced` et
  `/api/books/{id}/text` (moyenne + écart type sur 100 requêtes).
- TODO (Camille) : charge légère avec deux clients simultanés ; temps de démarrage du backend
  (chargement de l'index et du graphe).
- TODO (Camille) : captures de la démonstration sur deux machines clientes.

État actuel (jeu d'exemple de 10 livres simulés) : `tests/test_api.py` vérifie qu'une
recherche répond en moins d'une seconde ; ce n'est pas une mesure de performance du rendu.
