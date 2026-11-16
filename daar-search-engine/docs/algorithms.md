# Algorithmes — DAAR Projet 2

Pour chaque algorithme, le rapport attend : définition du problème et structure de données,
présentation théorique, critique argumentée, puis tests et performances.

## 1. Normalisation et index inversé — TODO Kenza

- TODO (Kenza) : pipeline de normalisation (casse, ponctuation, tokenisation, stopwords, stemming).
- TODO (Kenza) : structure de l'index `terme -> {book_id: fréquence}` et format de stockage.
- TODO (Kenza) : complexité de construction et d'interrogation.

## 2. Recherche simple — TODO Kenza

- TODO (Kenza) : traitement d'un mot, de plusieurs mots, d'une requête vide ou inconnue.

## 3. Recherche RegEx sur les termes indexés — TODO Kenza

- TODO (Kenza) : algorithme utilisé (bibliothèque standard, automate Aho-Ullman du projet 1, KMP).
- TODO (Kenza) : limites de la recherche sur termes plutôt que sur texte brut ; motifs coûteux.

## 4. Similarité de Jaccard et graphe — TODO Nadine

- TODO (Nadine) : définition `J(A,B) = |A ∩ B| / |A ∪ B|`, distance `1 - J`, ensembles vides.
- TODO (Nadine) : construction du graphe, sens et valeur du seuil.

## 5. PageRank — TODO Nadine

- TODO (Nadine) : définition, calcul (itération de puissance, facteur d'amortissement), sommets isolés.
- TODO (Nadine) : résultat sur des extraits pertinents de quelques livres du corpus.

## 6. Classement combiné — TODO Nadine

- TODO (Nadine) : formule du score (occurrences + PageRank), normalisation, exemple chiffré.

## 7. Suggestions — TODO Nadine

- TODO (Nadine) : voisins des 2-3 meilleurs résultats, dédoublonnage, exclusions.

## Annexe : moteur simulé (Camille)

`backend/app/mocks.py` sert uniquement au développement de l'interface. Il compte les mots
des 10 textes d'exemple en mémoire, applique `re.fullmatch` aux mots pour la RegEx, et classe
avec `0,7 × occurrences/max + 0,3 × PageRank/max` sur des PageRank fictifs. Il ne doit pas
être décrit comme un algorithme du projet dans le rapport.
