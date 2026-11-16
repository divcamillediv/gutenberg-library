# Algorithmes — notes préparatoires

Aucun des algorithmes ci-dessous n'est encore implémenté.

## Jaccard

Pour deux ensembles de termes A et B, lorsque leur union n'est pas vide :

```text
J(A, B) = taille(A intersection B) / taille(A union B)
d(A, B) = 1 - J(A, B)
```

Les fréquences sont volontairement ignorées. La convention pour deux ensembles
vides reste à valider ; proposer une similarité de 1 conserve une distance nulle
entre ensembles identiques. Cela ne justifie pas automatiquement de relier des
livres sans termes : la politique du graphe doit être distincte.

## Matrice et graphe

La matrice complète conserve un ordre explicite des identifiants. À 1 664 livres,
elle contient 2 768 896 valeurs, avec 1 383 616 paires distinctes hors diagonale.
Une représentation numérique dense float64 demande environ 21,1 Mio pour les
valeurs seules ; une liste Python ou du JSON a un surcoût nettement supérieur.
Le coût réel du calcul dépend également de la taille des ensembles de termes.

Exploiter la symétrie évite de calculer deux fois chaque paire. Le graphe pondéré
est construit après le calcul des similarités, selon un seuil étudié.
La matrice est un livrable distinct : les seules arêtes conservées par seuil
ne permettent pas de reconstituer les similarités supprimées.

## PageRank pondéré

Chaque sommet répartit sa masse entre ses voisins proportionnellement aux poids.
La téléportation et la redistribution de la masse des sommets sans voisins
doivent être explicites. Contrôler convergence, non-négativité et somme des scores.
Une absence de convergence doit être signalée, pas présentée comme un résultat final.

## Classement et recommandations

Ne classer que les candidats renvoyés par la recherche. Normaliser les signaux
avant combinaison et comparer aux deux stratégies de référence.
Les recommandations exploitent les poids Jaccard et non le seul PageRank.
Les formules précises restent des propositions dans `api_contract.md`.
