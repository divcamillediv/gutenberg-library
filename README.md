# DAAR Projet 2 — Moteur de recherche d'une bibliothèque

Application web de recherche dans une bibliothèque de livres du projet Gutenberg :
recherche par mot-clé, recherche avancée par RegEx, classement par pertinence (occurrences
et PageRank sur le graphe de Jaccard), suggestions de livres voisins, lecture du texte.

Équipe : Kenza (corpus, index, recherche), Nadine (graphe, PageRank, classement,
suggestions), Camille (API, interface, intégration web).

## État du projet

| Partie | Responsable | État |
|---|---|---|
| API FastAPI, contrat JSON, lecture des livres | Camille | Fait |
| Interface React (recherche, résultats, RegEx, catalogue, lecture) | Camille | Fait |
| Tests de l'API et du parcours frontend, README | Camille | Fait |
| Docker Compose | Collectif | Écrit, à lancer sur une machine avec Docker |
| Corpus de 1 664 livres, nettoyage, validation, index inversé | Kenza | **TODO** |
| Recherche simple et RegEx sur l'index | Kenza | **TODO** |
| Jaccard, graphe, seuil, PageRank | Nadine | **TODO** |
| Classement combiné et suggestions | Nadine | **TODO** |

Tant que les modules en TODO ne sont pas livrés, l'application fonctionne en **mode
démonstration** sur 10 livres simulés (`data/sample/`) : courts textes de remplacement,
PageRank et similarités fictifs. Un bandeau l'indique dans l'interface et `/api/health`
détaille l'état de chaque module. Chercher `TODO (Kenza)` et `TODO (Nadine)` dans le code
pour la liste des tâches.

## Installation et démarrage

### Avec Docker

Prérequis : Docker et Docker Compose.

```bash
docker compose up --build
```

- Application : <http://localhost:8080>
- Documentation de l'API : <http://localhost:8000/docs>

Pour changer les ports, copier `.env.example` en `.env`.

### Sans Docker (développement)

Prérequis : Python 3.11 ou plus récent, Node.js 20 ou plus récent.

```bash
# Terminal 1 — backend
cd backend
python -m venv .venv && source .venv/bin/activate    # Windows : .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 — frontend
cd frontend
npm install
npm run dev
```

Application : <http://localhost:5173>. Le serveur Vite relaie `/api` vers le backend.

## Utilisation depuis plusieurs machines

1. Connecter le serveur et les clients au même réseau (Wi-Fi ou partage de connexion).
2. Trouver l'adresse IP du serveur : `ipconfig` (Windows), `ipconfig getifaddr en0` (macOS),
   `hostname -I` (Linux).
3. Sur chaque client (PC, téléphone), ouvrir `http://<IP-du-serveur>:8080` (Docker) ou
   `http://<IP-du-serveur>:5173` (développement).

## Préparation du corpus

Le dépôt ne contient que le jeu d'exemple. Le corpus complet se reconstruit hors ligne, avant
la démonstration (aucun téléchargement pendant la vidéo) :

```bash
./scripts/rebuild_all.sh
```

| Étape | Script | Sortie | Responsable |
|---|---|---|---|
| 1 | `download_books.py` | `data/raw/`, `data/metadata/books.json` | Kenza (TODO) |
| 2 | `clean_books.py` | `data/processed/` | Kenza (TODO) |
| 3 | `validate_corpus.py` | Rapport JSON : ≥ 1 664 livres de ≥ 10 000 mots | Kenza (TODO) |
| 4 | `build_index.py` | `data/indexes/` | Kenza (TODO) |
| 5 | `build_graph.py` | `data/graphs/` (arêtes, voisins, statistiques) | Nadine (TODO) |
| 6 | `compute_pagerank.py` | `data/graphs/pagerank.*` | Nadine (TODO) |

Puis redémarrer le backend. L'API bascule sur les vraies données sans modification de code :
dès que `data/metadata/books.json` existe, le catalogue réel est chargé ; dès qu'une fonction
(`search`, `regex_search`, `rank_results`, `recommend`) ne lève plus `NotImplementedError`,
elle remplace la simulation. Vérifier sur `/api/health` que `data_source` vaut `corpus` et
que les quatre modules valent `real`.

Le jeu d'exemple se régénère avec `python scripts/make_sample_data.py`.

## Exemples de requêtes

Dans l'interface : saisir un mot-clé sur l'accueil, ou une expression régulière dans
l'onglet RegEx. Directement sur l'API (jeu d'exemple) :

```bash
curl "http://localhost:8000/api/health"
curl "http://localhost:8000/api/books?limit=5&offset=0"
curl "http://localhost:8000/api/books/2701"
curl "http://localhost:8000/api/books/2701/text?page=1"
curl "http://localhost:8000/api/books/2701/similar"
curl "http://localhost:8000/api/search?q=whale"
curl -G "http://localhost:8000/api/search/advanced" --data-urlencode "regex=whal(e|es|ing)"
```

| Requête | Résultat attendu sur le jeu d'exemple |
|---|---|
| `q=harpooner` | Un seul livre, *Moby Dick* : le mot n'apparaît dans aucun titre |
| `q=ship` | Plusieurs livres classés par score décroissant, avec suggestions |
| `q=zzzz` | `total: 0`, listes vides |
| `q=` (vide) | Erreur `400` |
| `regex=sea.*` | Livres contenant un mot commençant par `sea` |
| `regex=(bad` | Erreur `400` avec le motif de l'erreur |

Le format complet des réponses est dans [docs/api_contract.md](docs/api_contract.md).

## Tests

```bash
pip install -r backend/requirements.txt
pytest                      # API ; les tests de Kenza et Nadine sont marqués « skipped » (TODO)

cd frontend
npm test                    # client de l'API + parcours recherche → résultats → lecture → suggestions
```

## Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| « Le serveur est injoignable » dans l'interface | Backend arrêté | Lancer `uvicorn` (ou `docker compose up`) et ouvrir `/api/health` |
| Bandeau « Mode démonstration » alors que le corpus est prêt | `data/metadata/books.json` absent, ou module encore en TODO | Consulter `/api/health` ; relancer `./scripts/rebuild_all.sh` ; redémarrer le backend |
| « Le texte du livre n'est pas disponible » | `file_path` ne pointe pas vers un fichier de `data/` | Vérifier `data/processed/{id}.txt` et le chemin relatif dans les métadonnées |
| La page ne s'ouvre pas depuis un autre appareil | Pare-feu, ou réseau qui isole les appareils (eduroam, Wi-Fi invité) | Autoriser le port 8080 (ou 5173) ; passer par un partage de connexion |
| `address already in use` | Port 8000, 8080 ou 5173 occupé | Arrêter l'autre programme, ou changer les ports dans `.env` / `--port` |
| `ModuleNotFoundError: app` | `uvicorn` lancé hors de `backend/` | `cd backend` avant `uvicorn app.main:app` ; pour `pytest`, se placer à la racine |
| Données non prises en compte dans Docker | Le backend charge les fichiers au démarrage | `docker compose restart backend` |
| Page blanche après une mise à jour du frontend | Ancien build dans l'image | `docker compose up --build` |

## Organisation du dépôt

```
backend/app/
  main.py                     point d'entrée FastAPI
  config/settings.py          configuration
  books/                      routes.py, schemas.py, service.py
  search/                     routes.py + index et recherches (Kenza)
  ranking/                    PageRank et classement (Nadine)
  recommendations/            Jaccard, graphe, suggestions (Nadine)
  integration.py, mocks.py    branchement des modules et moteur simulé
frontend/src/
  pages/                      Home, Results, AdvancedSearch, BookDetails, Library
  components/                 SearchBar, ResultsList, BookCard, SuggestionsList, ...
  services/api.js             appels FastAPI
data/                         raw/, processed/, metadata/, indexes/, graphs/ (hors Git), sample/
scripts/                      préparation hors ligne + rebuild_all.sh
tests/                        tests pytest
docs/                         instructions, architecture, contrat de l'API, algorithmes, expériences, vidéo
```

Fichiers ajoutés par rapport à la structure de référence : `integration.py`, `mocks.py` et
`errors.py` (mode simulé et bascule vers les vrais modules), la page `Library`,
`scripts/make_sample_data.py`, et une CI minimale dans `.github/workflows/`.

## Préparer l'archive de rendu

Depuis le dossier parent, sans corpus brut, caches ni dépendances (remplacer les noms) :

```bash
zip -r daar-projet2-NOM1-NOM2-NOM3.zip daar-search-engine \
  -x "*/node_modules/*" "*/dist/*" "*/.venv/*" "*/__pycache__/*" "*/.pytest_cache/*" "*/.git/*" \
     "*/data/raw/*" "*/data/processed/*" "*/data/indexes/*" "*/data/graphs/*" "*/data/metadata/*"
```

Ajouter le rapport et la vidéo, puis vérifier le poids de l'archive (viser 30 Mo au plus).
