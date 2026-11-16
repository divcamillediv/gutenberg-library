# Instructions communes — résumé

Résumé du document d'équipe « Instructions communes et répartition finale » et du « Plan
d'action révisé » (16 novembre 2026). Les PDF d'origine font foi.

## Échéance

Dépôt Moodle le **22 novembre 2026 à 23 h 59** : archive `daar-projet2-NOM1-NOM2-NOM3.zip`
(viser ≤ 30 Mo) contenant rapport (cible 12 pages, 15 maximum), code commenté et vidéo pitch
d'environ 5 minutes avec démonstration.

## Obligatoire

- Bibliothèque d'au moins 1 664 livres d'au moins 10 000 mots chacun.
- Recherche par mot-clé sur un index du **contenu** des livres.
- Recherche avancée par RegEx (choix : sur les termes indexés).
- Classement utilisant une centralité (choix : PageRank sur le graphe de Jaccard).
- Suggestions (choix : voisins Jaccard des 2-3 meilleurs résultats).
- Lecture du texte d'un livre ; démonstration sur au moins deux machines clientes.

## Répartition

| Personne | Branche | Périmètre |
|---|---|---|
| Kenza | `feature/data-search` | `data/`, `scripts/download_books.py`, `clean_books.py`, `build_index.py`, `backend/app/search/` |
| Nadine | `feature/graph-ranking` | `backend/app/ranking/`, `backend/app/recommendations/`, `scripts/build_graph.py`, `compute_pagerank.py` |
| Camille | `feature/web-docker` | `backend/app/main.py`, `books/`, `schemas.py`, `frontend/`, Dockerfiles, `docker-compose.yml`, `docs/api_contract.md` |

Collectif : contrats communs, GitHub et CI, Docker, intégration, mesures transversales,
rapport, vidéo. Bonus seulement si le socle fonctionne le 19 novembre : Oracle Cloud, Kubernetes.

## Règles de travail

- Mêmes 10 livres tests et identifiants stables dès le départ.
- Contrat dans `docs/api_contract.md` ; aucune modification unilatérale.
- Un push par jour, point quotidien de 15 minutes, Pull Request relue avant fusion dans `main`.
- Données volumineuses hors Git ; scripts de reconstruction et données d'exemple versionnés.
- Un module est terminé si : code poussé, tests exécutés, entrées/sorties documentées,
  intégration vérifiée.

## Tests minimaux avant livraison

- [ ] ≥ 1 664 livres distincts, chacun ≥ 10 000 mots ; sources identifiables.
- [ ] Un mot du texte (absent du titre) retrouve le bon livre.
- [ ] Recherche simple : terme connu, terme absent, requête vide.
- [ ] RegEx : motif valide, invalide, sans correspondance, coûteux.
- [ ] Matrice Jaccard : diagonale 1, symétrie, valeurs entre 0 et 1.
- [ ] Graphe : voisins et seuil cohérents ; PageRank enregistré et réellement utilisé.
- [ ] Suggestions : voisins liés au contenu ; pas de doublons.
- [ ] Page détail : texte du livre consultable.
- [ ] Deux navigateurs sur deux machines distinctes utilisent l'application.
- [ ] Docker Compose et README testés.
- [ ] Rapport : méthodes, justification du filtrage, sources, résultats, graphiques, limites.
- [ ] Vidéo d'environ 5 minutes avec démonstration ; archive dans la limite de taille.
