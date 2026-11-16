# Architecture de départ

## Principes retenus

Backend Python/FastAPI, frontend React/Vite, fichiers persistants, préparation
hors ligne et tests automatisés. Pas de migration vers Django.

```text
Textes + métadonnées
    -> nettoyage et normalisation
    -> index inversé + termes par livre
         -> recherche simple / RegEx -> occurrences des candidats
         -> matrice Jaccard + ordre des identifiants
              -> graphe pondéré -> PageRank persisté
              -> voisins -> recommandations
Occurrences + PageRank -> classement -> API -> interface
```

## Indépendance des modules

Le module Jaccard n'a besoin que de `book_id -> ensemble de termes normalisés`.
Il n'a pas besoin de FastAPI, des titres, des textes ou du téléchargement.
Le jeu synthétique permet de commencer sans attendre le corpus.

Le classement nécessite les occurrences renvoyées par la recherche et les scores
PageRank. Les recommandations nécessitent les voisins pondérés. Ces fonctions
renvoient des IDs et des scores ; la couche web enrichit avec les métadonnées.
Ne pas importer FastAPI dans les algorithmes.

La couche web pourra utiliser des services simulés explicitement signalés en
développement. Aucun faux résultat ne doit remplacer silencieusement une erreur
ou un artefact absent en fonctionnement réel.

## Artefacts prévus, non encore générés

| Emplacement | Contenu |
|---|---|
| `data/metadata/books.json` | Métadonnées et sources |
| `data/indexes/inverted_index.json` | Terme vers fréquences par livre |
| `data/indexes/book_terms.json` | Termes normalisés uniques par livre |
| `data/indexes/original_to_normalized.json` | Correspondance optionnelle selon la stratégie RegEx |
| `data/graphs/` | Matrice et ordre des IDs, format à confirmer |
| `data/graphs/edges.json` | Une occurrence de chaque arête non orientée |
| `data/graphs/neighbors.json` | Adjacence pondérée incluant les sommets isolés |
| `data/graphs/pagerank.json` | Scores pour tous les sommets |

Ces fichiers ne sont pas créés vides : un fichier vide pourrait être pris à tort
pour un artefact valide. Seuls leurs répertoires sont préparés.
À terme, un manifeste devra relier les artefacts à la même version du corpus et
de la normalisation pour éviter les mélanges d'index, de graphe et de scores.

Les scripts orchestrent les calculs ; ils ne dupliquent pas les algorithmes
de `backend/app`. Le frontend consomme uniquement l'API.
