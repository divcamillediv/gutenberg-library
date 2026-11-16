# Démarrage progressif

## Ce qui existe et ce qui manque

L'arborescence et un jeu synthétique sont créés. Il n'existe encore ni algorithme,
ni corpus réel, ni application exécutable. Les contrats sont proposés, non validés.
Aucun changement Git n'a été effectué.

L'arborescence détaillée initiale fait référence ici : `config/settings.py`,
`books/schemas.py` et `routes.py`. Ne pas ajouter en parallèle `config.py` ou
`router.py`, qui feraient doublon.

## Décisions collectives avant le premier commit commun

- Isoler le dépôt du projet du dépôt situé dans le dossier utilisateur ;
  choisir le dépôt distant et organiser les trois branches prévues.
- Valider cette arborescence et les responsabilités de chaque module.
- Choisir les versions de Python et Node, les dépendances initiales et la
  gestion de leurs versions. Prévoir pytest comme dépendance de développement.
- Valider les identifiants, les formats de `book_terms` et des occurrences,
  les chemins configurables et l'ordre des identifiants de la matrice.
- Confirmer que les contrats de `api_contract.md` sont provisoires et décider
  comment communiquer leurs évolutions sans bloquer les autres modules.
- Vérifier les exclusions Git et la livraison séparée des données volumineuses.

Le seuil du graphe et le coefficient du classement ne doivent pas être figés
sans expériences. Ils ne bloquent pas le commit du squelette.
La règle pour deux ensembles vides doit être fixée avant de coder Jaccard.
La normalisation doit être commune à l'index et aux requêtes avant intégration.

## Ordre de développement du module graphe et classement

| Étape | Fichiers principaux | Fonctions proposées | Validation attendue |
|---|---|---|---|
| 1 | `backend/app/recommendations/jaccard.py`, `tests/test_jaccard.py` | `jaccard_similarity`, `jaccard_distance` | Identiques, disjoints, intersection partielle, vides, symétrie, bornes |
| 2 | `backend/app/recommendations/graph_builder.py`, `tests/test_graph.py` | `build_similarity_matrix` | Ordre des IDs, dimensions, symétrie, diagonale |
| 3 | Même module, `scripts/build_graph.py` | `build_graph`, `graph_statistics` | Seuil exact, poids, sommets isolés, export/relecture |
| 4 | `backend/app/ranking/pagerank.py`, `scripts/compute_pagerank.py`, `tests/test_pagerank.py` | `compute_pagerank` | Petits graphes connus, poids, sommets pendants, somme, convergence |
| 5 | `backend/app/ranking/ranking_service.py`, `tests/test_ranking.py` | `rank_results` | Normalisation, vrais effets du PageRank, stratégies, égalités |
| 6 | `backend/app/recommendations/recommendation_service.py`, `tests/test_recommendations.py` | `recommend` | Exclusions, dédoublonnage, ordre, limite |
| 7 | Scripts, `tests/test_performance.py`, `docs/experiments.md` | Exécution hors ligne reproductible | Dix vrais livres, corpus complet, mesures et intégration API |

Les recommandations dépendent du graphe mais pas du classement ni de PageRank :
elles peuvent avancer après l'étape 3 pour débloquer l'interface.

Après chaque incrément : exécuter les tests ciblés, lire les résultats, puis
faire un commit seulement lorsque le comportement attendu est vérifié.
Supprimer le `pytest.skip` du fichier concerné en écrivant ses vrais tests.
La collecte actuelle ne contient aucun test exécutable ; elle ne doit pas servir
de preuve de validation ni de pipeline CI « vert ».

## Première action concrète

Ouvrir `data/sample/book_terms.json` et vérifier à la main :

```text
A = {island, sea, ship}
B = {sea, ship, whale}
intersection = {sea, ship}             -> 2 termes
union = {island, sea, ship, whale}     -> 4 termes
J(A, B) = 2/4 = 0,5 ; distance = 0,5
```

Ce calcul deviendra le premier test de Jaccard. Pour l'étape suivante, décider
explicitement si `J(vide, vide) = 1`, convention recommandée pour conserver une
distance nulle entre ensembles identiques, puis implémenter seulement les deux
fonctions de Jaccard et leurs tests.

Après installation et configuration validées de pytest, la commande ciblée
prévue depuis la racine du projet sera :

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_jaccard.py -q
```

Cette commande n'est pas une validation disponible aujourd'hui :
le fichier est encore un squelette et pytest n'est pas déclaré comme dépendance.

## Commits et intégration

Une fois le dépôt correctement isolé, le squelette commun doit être partagé
avant les développements indépendants. Message possible :
`chore: préparer la structure du moteur de recherche`.

Le premier incrément personnel se fera sur `feature/graph-ranking`, avec par
exemple `feat: ajouter la similarité et la distance de Jaccard`.
Ouvrir une Pull Request vers `main`, décrire les contrats et les tests exécutés,
obtenir une revue et intégrer progressivement. Ne pas attendre la fin du projet.

## Priorités

Obligatoires : corpus conforme, recherche sur le texte, Jaccard, matrice, graphe,
centralité, classement, suggestions, lecture, tests, rapport et démonstration.
Docker est recommandé pour la reproductibilité. Oracle reste conditionnel aux
ressources disponibles. Kubernetes est optionnel et ne doit bloquer aucun livrable.
Les limites exactes de dépôt et de vidéo restent à vérifier sur Moodle.
