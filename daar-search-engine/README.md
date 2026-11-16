# DAAR Projet 2 — Moteur de recherche d'une bibliothèque

Application web de recherche dans une bibliothèque de livres du projet Gutenberg :
recherche par mot-clé, recherche avancée par RegEx, classement par pertinence (occurrences
et PageRank sur le graphe de Jaccard), suggestions de livres voisins, lecture du texte.

Équipe : Kenza (données, index, recherche), Nadine (graphe, PageRank, classement,
suggestions), Camille (API, interface, Docker, intégration).

## État du projet

| Partie | Responsable | État |
|---|---|---|
| API FastAPI, contrat JSON, lecture des livres | Camille | Fait |
| Interface React (recherche, résultats, RegEx, catalogue, lecture) | Camille | Fait |
| Docker Compose, README, tests de l'API | Camille | Fait |
| Corpus de 1 664 livres, nettoyage, index inversé | Kenza | **TODO** |
| Recherche simple et RegEx sur l'index | Kenza | **TODO** |
| Jaccard, graphe, PageRank | Nadine | **TODO** |
| Classement combiné et suggestions | Nadine | **TODO** |

Tant que les modules en TODO ne sont pas livrés, l'application fonctionne en **mode
démonstration** sur 10 livres simulés (`data/sample/`) : courts textes de remplacement,
PageRank et similarités fictifs. Un bandeau l'indique dans l'interface et `/api/health`
détaille l'état de chaque module. Chercher `TODO (Kenza)` et `TODO (Nadine)` dans le code
pour la liste des tâches.

## Démarrage avec Docker

Prérequis : Docker et Docker Compose.

```bash
docker compose up --build
```

- Application : <http://localhost:8080>
- Documentation de l'API : <http://localhost:8000/docs>

Pour changer les ports, copier `.env.example` en `.env`.

## Démonstration sur plusieurs machines

1. Connecter le serveur et les clients au même réseau (Wi-Fi ou partage de connexion).
2. Trouver l'adresse IP du serveur : `ipconfig` (Windows), `ipconfig getifaddr en0` (macOS),
   `hostname -I` (Linux).
3. Sur chaque client (PC, téléphone), ouvrir `http://<IP-du-serveur>:8080`.

Si la page ne s'ouvre pas, autoriser le port 8080 dans le pare-feu du serveur. Certains
réseaux (eduroam, Wi-Fi invités) isolent les appareils : utiliser alors un partage de connexion.

## Démarrage en développement

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

Application : <http://localhost:5173> (ou `http://<IP-du-serveur>:5173` depuis un autre
appareil). Le serveur Vite relaie `/api` vers le backend.

## Tests

```bash
pip install -r backend/requirements.txt
pytest                      # API ; les tests de Kenza et Nadine sont marqués « skipped » (TODO)

cd frontend && npm test     # client de l'API
```

## Passer au corpus réel

L'API bascule sur les vraies données sans modification de code :

1. Kenza : `scripts/download_books.py`, `clean_books.py`, `build_index.py` produisent
   `data/metadata/books.json`, `data/processed/` et `data/indexes/`.
2. Nadine : `scripts/build_graph.py`, `compute_pagerank.py` produisent `data/graphs/`.
3. Redémarrer le backend. Dès que `data/metadata/books.json` existe, le catalogue réel est
   chargé ; dès qu'une fonction (`search`, `regex_search`, `rank_results`, `recommend`) ne
   lève plus `NotImplementedError`, elle remplace la simulation correspondante.
4. Vérifier `http://localhost:8000/api/health` : `data_source` vaut `corpus` et les quatre
   modules valent `real`.

Le jeu d'exemple se régénère avec `python scripts/make_sample_data.py`.

## Organisation du dépôt

```
backend/app/     API FastAPI : main, config, schemas, books/, search/, ranking/, recommendations/
frontend/        Application React/Vite, servie par nginx dans Docker
data/            raw/, processed/, indexes/, graphs/, metadata/ (hors Git) et sample/ (versionné)
scripts/         Construction du corpus, de l'index, du graphe et du PageRank
tests/           Tests pytest
docs/            instructions, architecture, algorithmes, expériences, contrat de l'API, plan vidéo
```

Documents : [contrat de l'API](docs/api_contract.md) · [architecture](docs/architecture.md) ·
[algorithmes](docs/algorithms.md) · [expériences](docs/experiments.md) ·
[plan de la vidéo](docs/video_plan.md) · [instructions](docs/instructions.md)

## Préparer l'archive de rendu

Depuis le dossier parent, sans corpus brut, caches ni dépendances (remplacer les noms) :

```bash
zip -r daar-projet2-NOM1-NOM2-NOM3.zip daar-search-engine \
  -x "*/node_modules/*" "*/dist/*" "*/.venv/*" "*/__pycache__/*" "*/.pytest_cache/*" "*/.git/*" \
     "*/data/raw/*" "*/data/processed/*" "*/data/indexes/*" "*/data/graphs/*" "*/data/metadata/*"
```

Ajouter le rapport et la vidéo, puis vérifier que l'archive reste sous 30 Mo.
