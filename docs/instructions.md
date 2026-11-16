# Instructions communes — résumé du plan final

Résumé du « Plan final fusionné » (16 novembre 2026), document unique de référence de
l'équipe. Le PDF d'origine fait foi.

## Échéance et rendu

Dépôt Moodle le **22 novembre 2026 à 23 h 59** : archive `daar-projet2-NOM1-NOM2-NOM3.zip`
contenant le rapport (10 à 15 pages, 12 recommandées), le code commenté et la vidéo pitch
d'environ 5 minutes avec démonstration. Taille : environ 30 Mo selon la consigne écrite ;
vidéo < 50 Mo à confirmer sur Moodle ; appliquer la limite la plus stricte en cas de doute.

Barème annoncé : environ 30 % réalisation, 40 % rapport, 30 % présentation.

## Exigences

- Au moins 1 664 livres distincts de 10 000 mots minimum ; provenance, contrôles et
  exclusions documentés.
- Index inversé sur le contenu ; recherche simple et RegEx sur le vocabulaire indexé,
  limites expliquées.
- Classement utilisant réellement PageRank ; graphe de similarité Jaccard et recommandations.
- Interface : recherche, classement, suggestions, ouverture du texte des livres.
- Démonstration sur deux machines clientes.

## Répartition

| Membre | Branche | Responsabilité | Preuve attendue |
|---|---|---|---|
| Kenza | `feature/data-search` | Corpus, nettoyage, index inversé, recherche simple et RegEx | Corpus validé, index et fonctions testées, couverture et latences |
| Nadine | `feature/graph-ranking` | Jaccard, distances, graphe, seuil, PageRank, classement, suggestions | Statistiques de graphe, classement A/B/C, voisins pertinents, mesures |
| Camille | `feature/web-app` | FastAPI, contrat JSON, React, lecture, erreurs, intégration web | Parcours navigateur complet, API testée, deux clients |

Collectif : architecture et contrats, GitHub et CI, Docker et Compose, intégration, rapport
et vidéo. Optionnel : Oracle Cloud. Bonus après socle et Docker validés : Kubernetes / K3s.

## Tâches de Camille

| Tâche | Contenu | État |
|---|---|---|
| C1 | FastAPI (routeurs, schémas, `/api/health`) et React/Vite | Fait |
| C2 | Routes livres, détail, texte, recherche, RegEx, suggestions ; pagination et erreurs | Fait |
| C3 | Pages accueil, résultats, recherche avancée, détail/lecture, suggestions ; chargement, erreur, vide | Fait |
| C4 | Réponses simulées sur 10 livres, puis fonctions réelles de Kenza et Nadine | Simulation faite ; branchement en attente des modules |
| C5 | Docker : deux services, volumes, réseau, variables d'environnement | Écrit ; à lancer sur une machine avec Docker |
| C6 | Test sur deux machines clientes ; séquence de démonstration sans téléchargement | À faire |
| C7 | README : installation, démarrage, corpus, requêtes, dépannage | Fait |

Les tâches de Kenza (K1 à K7) et de Nadine (N1 à N7) sont reportées en `TODO (Kenza)` et
`TODO (Nadine)` dans leurs fichiers.

## Contrats communs

- `book_id` stable et identique dans métadonnées, index, graphe et API.
- Métadonnées : `id`, `title`, `author`, `language`, `word_count`, `source_url`, `file_path`.
- Index : terme normalisé → `{book_id: fréquence}` ; plus `book_terms` et le lien formes
  originales → termes normalisés.
- Graphe : nœud = `book_id` ; similarité Jaccard ; distance = 1 − Jaccard ; arêtes pondérées
  au-dessus d'un seuil justifié.
- API : voir `docs/api_contract.md` ; changement uniquement après accord des trois.
- Même jeu de 10 livres pour commencer.

## Règles quotidiennes

- Un push minimum par jour ; mini-point de 15 minutes : terminé / prochain objectif / blocage.
- Pull Request relue par au moins une autre personne avant fusion sur `main`.
- Chaque livraison = code + tests + entrées/sorties documentées + chiffres ou figures.
- Données volumineuses hors Git ; échantillon et scripts de reconstruction versionnés.
- Point de charge chaque soir.

Terminé = code poussé, tests exécutés, données et IDs compatibles, documentation présente,
fonction démontrée sur données réelles, PR fusionnée après revue.

## Trois modes d'utilisation

- **Démo** : corpus complet, index et graphe déjà présents sur la machine ; aucun
  téléchargement pendant la vidéo.
- **Reconstruction** : `scripts/rebuild_all.sh`, dépendances figées, provenance documentée.
- **Correcteur** : petit corpus d'exemple dans l'archive (`data/sample/`) pour un test immédiat.

## Planning

| Date | Individuel | Jalon collectif |
|---|---|---|
| 16 nov. | Kenza : 10 livres + mini-index. Nadine : Jaccard test. Camille : FastAPI/React + mocks | Dépôt, branches, contrats, CI minimale |
| 17–18 nov. | Kenza : corpus, index, RegEx. Nadine : graphe, PageRank, suggestions. Camille : routes et écrans | Première recherche + lecture via React |
| 19 nov. | Modules terminés et testés ; artefacts livrés | Intégration de bout en bout + Docker Compose |
| 20 nov. | Benchmarks et corrections | 1 664 livres, deux clients, courbes |
| 21 nov. | Sections et figures | Rapport ~12 pages, vidéo ~5 min |
| 22 nov. | Derniers tests | Clone/ZIP propre, nom, poids ; dépôt avant 23 h 59 |

Si l'application ne fonctionne pas de bout en bout le 19 novembre : suspendre Oracle et
Kubernetes.

## Rapport (cible 12 pages)

| Partie | Responsable |
|---|---|
| Objectifs, architecture, choix techniques (1–2 p.) | Camille |
| Corpus, nettoyage, index, RegEx (2–3 p.) | Kenza |
| Jaccard, graphe, seuil, PageRank (2–3 p.) | Nadine |
| Classement et recommandations (1–2 p.) | Nadine + Kenza |
| Tests, performance, limites (~2 p.) | Toutes |
| Conclusion, références, relecture (~1 p.) | Toutes |

## Validation avant dépôt

- [ ] 1 664 livres valides et provenance prouvée ; index couvrant tous les IDs et le contenu.
- [ ] Recherche simple, RegEx et cas limites testés ; lecture du texte depuis l'interface.
- [ ] Similarité Jaccard cohérente ; seuil justifié ; PageRank calculé et utilisé ; classements comparés.
- [ ] Suggestions pertinentes sans doublons ; exemples documentés.
- [ ] Application accessible depuis deux clients ; Docker Compose opérationnel.
- [ ] Mesures et figures disponibles : temps, tailles, isolés, densité, pertinence.
- [ ] README reproductible, petit jeu de test, corpus complet prêt pour la démo.
- [ ] Rapport et vidéo avec démonstration ; taille et nom d'archive conformes ; dépôt à temps.
