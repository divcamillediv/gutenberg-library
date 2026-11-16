# Expériences — protocole à compléter

**Aucune mesure n'a encore été effectuée.** Ne pas présenter les exemples
synthétiques comme des résultats sur le corpus réel.

Pour chaque campagne, conserver : version du code, corpus et nombre de livres,
normalisation, taille du vocabulaire, matériel, versions logicielles, paramètres,
nombre de répétitions et distinction entre chargement et calcul.

## Similarité et graphe

Mesurer séparément le chargement, le calcul de la matrice, l'export et la
construction du graphe. Étudier plusieurs seuils sur une même matrice.
Conserver nombre de sommets, arêtes uniques, isolés, degrés et densité.
Pour un graphe simple non orienté de n >= 2 sommets et m arêtes :
`densité = 2m / (n(n - 1))`. Traiter explicitement n < 2.

## PageRank et recommandations

Relever durée, paramètres, nombre d'itérations et résidu de convergence.
Mesurer les recommandations indépendamment du calcul hors ligne.
Présenter des exemples pertinents et des contre-exemples avec leurs poids Jaccard.

## Classements

Comparer occurrences seules, PageRank seul et combinaison pour les mêmes
requêtes et candidats. Définir les jugements de pertinence avant la comparaison.
Ne pas assimiler un score PageRank élevé à une preuve de pertinence textuelle.

## Montée en charge

Commencer sur le jeu synthétique pour la correction, puis dix vrais livres
pour l'intégration, puis le corpus conforme pour les performances.
Ne pas extrapoler une performance sur 1 664 livres à partir de dix documents.
Les seuils d'acceptation des temps de réponse restent à convenir.
