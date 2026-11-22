# DAAR — Bibliothèque Gutenberg

**Projet 2 — DAAR, Master Informatique**  
**Réalisé par Kenza, Nadine et Camille**

Application web permettant de rechercher des livres du Projet Gutenberg, de lire leur texte et d'obtenir des recommandations de livres similaires.

**Application en ligne :** http://56.228.24.64/  
**Dépôt GitHub :** https://github.com/divcamillediv/gutenberg-library

## 1. Comment lancer et tester l'application ?

Deux méthodes sont possibles :

| Méthode | Accès | Données disponibles |
|---|---|---|
| **1. Site en ligne (AWS)** | http://56.228.24.64/ | Corpus réel, 1 697 livres chargés lors de notre dernière vérification |
| **2. Docker Compose (local)** | http://localhost:8080/ | 10 livres d'exemple si le corpus complet est absent |

**Nous recommandons le site AWS pour tester les algorithmes sur le corpus réel.** Le lancement avec Docker permet de vérifier le fonctionnement de l'application sur un ordinateur local.

### Méthode 1 — Utiliser directement le site en ligne

L'application est hébergée sur un serveur **AWS EC2 Ubuntu**.

**Adresse : http://56.228.24.64/**

Aucune installation n'est nécessaire.

Pour tester l'application :

1. Ouvrir le site dans un navigateur.
2. Rechercher `whale` dans la barre de recherche.
3. Consulter les résultats classés par pertinence.
4. Ouvrir un livre pour consulter sa fiche et lire son texte.
5. Consulter les suggestions de livres similaires.
6. Aller dans l'onglet **RegEx** et saisir `whal(e|es|ing)`.

Cette version utilise le corpus réel, l'index inversé, le graphe de Jaccard et les scores PageRank.

Nous avons préparé un corpus de **1 700 livres**. Lors de notre dernière vérification, **1 697 livres** étaient chargés par le backend.

Le site est accessible depuis plusieurs ordinateurs ou téléphones disposant d'une connexion Internet, tant que le serveur AWS est disponible.

### Méthode 2 — Lancer le projet en local avec Docker Compose

Cette méthode permet de lancer l'application à partir du ZIP du code source fourni dans notre rendu.

#### Prérequis

- Docker Desktop installé et démarré, avec Docker Compose.
- Une connexion Internet pour télécharger les images et les dépendances au premier lancement.
- Les ports `8080`, `8000` et `5432` disponibles si utilisés par la configuration Docker.

#### Étape 1 — Décompresser le projet

Dans notre dossier de rendu, vous trouverez notamment :

```text
DAAR-Projet2/
├── gutenberg-library-main.zip
├── .env
├── rapport.pdf
└── demonstration.mp4
```

Décompresser le fichier `gutenberg-library-main.zip`.

Le dossier obtenu contient le code source de l'application et le fichier `docker-compose.yml`.

#### Étape 2 — Ajouter le fichier `.env`

Le fichier `.env` est fourni séparément dans notre rendu. Il contient les variables nécessaires au lancement local, notamment la configuration PostgreSQL.

1. Copier le fichier `.env` fourni.
2. Le coller dans le dossier `gutenberg-library-main`, après décompression.
3. Vérifier qu'il se trouve au même niveau que `docker-compose.yml`.

Le dossier doit alors ressembler à ceci :

```text
gutenberg-library-main/
├── .env
├── docker-compose.yml
├── backend/
├── frontend/
├── data/
└── ...
```

**Aucune modification du fichier `.env` n'est nécessaire.** Il est déjà configuré pour le lancement local.

#### Étape 3 — Démarrer Docker Compose

Ouvrir un terminal dans le dossier `gutenberg-library-main`.

Exécuter :

```bash
docker compose up -d --build
```

Cette commande construit les images Docker et démarre les trois services :

- `db` : base de données PostgreSQL ;
- `backend` : API FastAPI et moteur de recherche ;
- `frontend` : interface React servie par Nginx.

Le premier lancement peut prendre quelques minutes.

Vérifier les services :

```bash
docker compose ps
```

Les services doivent être démarrés. Les services `db` et `backend` disposent de contrôles de santé.

#### Étape 4 — Accéder à l'application

Ouvrir les adresses suivantes dans un navigateur :

| Service | Adresse |
|---|---|
| Application web | http://localhost:8080/ |
| État du backend | http://localhost:8000/api/health |
| Documentation de l'API | http://localhost:8000/docs |

Nous avons testé cette procédure à partir d'un ZIP téléchargé depuis GitHub et décompressé dans un nouveau dossier. Les trois conteneurs ont démarré et le site était accessible sur `localhost:8080`.

#### Étape 5 — Tester les fonctionnalités

Depuis le site local :

1. Effectuer une recherche simple avec `whale`.
2. Tester la recherche RegEx.
3. Ouvrir la fiche d'un livre.
4. Tester la lecture et les suggestions.

**Important : fonctionnement avec les données d'exemple**

Le ZIP du code source ne contient pas les textes de l'ensemble du corpus.

Lors de notre test local, le site affichait :

> Mode démonstration : 10 livres simulés, recherche et classement simulés.

Ce fonctionnement est prévu lorsque les données complètes sont absentes.

La version locale permet donc de vérifier le lancement Docker, l'interface et les parcours de navigation, mais elle ne permet pas d'évaluer les résultats réels des algorithmes sur les 1 700 livres.

**Pour tester le moteur complet, utiliser directement le site AWS : http://56.228.24.64/**

#### Vérifier les données chargées

Ouvrir :

http://localhost:8000/api/health

Cette route indique la source des métadonnées (`postgres`, `corpus` ou `sample`) et l'état des modules (`real` ou `mock`).

#### Arrêter l'application

Depuis le dossier du projet :

```bash
docker compose down
```

Cette commande arrête les conteneurs sans supprimer les volumes PostgreSQL.

Pour consulter les journaux en cas de problème :

```bash
docker compose logs --tail=80 backend
docker compose logs --tail=80 frontend
docker compose logs --tail=80 db
```

## 2. Fonctionnalités

Notre application propose :

- **Recherche simple :** rechercher les livres contenant un mot-clé.
- **Recherche avancée RegEx :** rechercher plusieurs formes de mots à partir d'une expression régulière.
- **Classement par pertinence :** combiner les occurrences des mots et les scores PageRank.
- **Recommandations :** proposer des livres similaires grâce au graphe de Jaccard.
- **Lecture :** consulter les informations et le texte des livres.
- **Interface web :** accéder à l'application depuis un ordinateur ou un téléphone.

### Exemples de recherches

| Recherche | Fonction |
|---|---|
| `whale` | Recherche simple |
| `ship` | Recherche simple |
| `alice` | Recherche simple |
| `whal(e\|es\|ing)` | Recherche RegEx |
| `([a-z` | Vérification de la gestion d'une RegEx invalide |

## 3. Architecture technique

| Technologie | Utilisation |
|---|---|
| React / Vite | Interface web |
| FastAPI / Python | API et moteur de recherche |
| PostgreSQL | Stockage des métadonnées |
| Docker / Docker Compose | Exécution des services |
| AWS EC2 | Hébergement de l'application |
| GitHub Actions | Automatisation du déploiement |
| GitHub Container Registry (GHCR) | Stockage des images Docker |

L'application est composée de trois services : `frontend`, `backend` et `db`.

Les calculs de l'index inversé, du graphe de Jaccard et du PageRank sont réalisés hors ligne. Le backend charge ensuite les fichiers pré-calculés au démarrage.

## 4. Corpus et algorithmes

### Corpus

Nous avons préparé un corpus de **1 700 livres en anglais**, issus du Projet Gutenberg via le jeu de données Hugging Face `sedthh/gutenberg_english`.

Les livres sélectionnés contiennent au moins 10 000 mots.

### Index inversé

L'index inversé associe chaque mot aux livres qui le contiennent, avec son nombre d'occurrences.

Il permet d'effectuer les recherches simples et les recherches RegEx sur les termes indexés.

### Graphe de Jaccard

Chaque livre correspond à un sommet du graphe.

Deux livres sont reliés lorsque leur similarité de Jaccard est supérieure ou égale au seuil de **0,3**.

Ce graphe est utilisé pour trouver les livres proches et produire des recommandations.

### PageRank

Nous calculons le PageRank sur le graphe de similarité pour estimer l'importance des livres dans le réseau.

Le classement combine les occurrences des termes recherchés et les scores PageRank.

### Organisation des données

| Données | Emplacement |
|---|---|
| Textes des livres | `data/raw/` |
| Métadonnées | PostgreSQL ou `data/metadata/` |
| Index inversé | `data/indexes/index_complet.json` |
| Graphe de Jaccard | `data/graphs/graph.json` |
| Scores PageRank | `data/graphs/pagerank.json` |
| Données d'exemple | `data/sample/` |

Les fichiers volumineux du corpus ne sont pas inclus dans le ZIP du code source.

## 5. Reconstituer le corpus complet en local (facultatif)

Cette procédure permet de reconstruire les données du moteur sur un ordinateur local.

Elle nécessite Python 3.11 ou plus récent, une connexion Internet et du temps pour le téléchargement et les calculs.

**Elle n'est pas nécessaire pour utiliser le site AWS avec le corpus complet.**

Depuis la racine du projet, installer les dépendances :

```bash
python -m pip install -r backend/requirements.txt
python -m pip install datasets
```

Télécharger les livres :

```bash
python scripts/telecharger_depuis_huggingface.py
```

Construire l'index inversé :

```bash
python -m scripts.indexer_corpus data/raw data/indexes/index_complet.json
```

Construire le graphe de Jaccard :

```bash
python scripts/build_graph.py --corpus data/raw
```

Calculer le PageRank :

```bash
python scripts/compute_pagerank.py
```

### Importer les métadonnées dans PostgreSQL

Démarrer la base :

```bash
docker compose up -d db
```

Sous Windows PowerShell, depuis la racine du projet :

```powershell
$env:POSTGRES_PASSWORD = (Get-Content .env | Where-Object { $_ -match '^POSTGRES_PASSWORD=' } | Select-Object -First 1) -replace '^POSTGRES_PASSWORD=', ''
python scripts/import_metadata.py
```

Après la préparation des données :

```bash
docker compose restart backend
```

Vérifier ensuite :

http://localhost:8000/api/health

Cette reconstruction complète n'a pas été validée sur un ordinateur vierge. Elle dépend de la disponibilité du corpus et de la configuration locale de PostgreSQL.

## 6. Hébergement AWS et déploiement automatique

Notre application est hébergée sur une instance **AWS EC2 Ubuntu**.

Le frontend, le backend et PostgreSQL fonctionnent dans des conteneurs Docker gérés par Docker Compose.

Nous avons mis en place un déploiement automatique avec **GitHub Actions**.

### Fonctionnement du déploiement

1. Une modification est effectuée dans le code.
2. Un commit et un push sont réalisés sur la branche `main`.
3. GitHub Actions déclenche le workflow de publication.
4. Les images Docker sont construites et publiées dans **GHCR**.
5. Le workflow de déploiement utilise un runner installé sur le serveur AWS EC2.
6. Docker Compose met à jour les conteneurs.
7. La nouvelle version devient accessible sur le site en ligne.

Les workflows sont disponibles dans `.github/workflows/`.

### Démonstration dans notre vidéo

Nous montrons une modification du texte de la page d'accueil, suivie d'un commit et d'un push sur GitHub.

Après l'exécution de GitHub Actions, la modification apparaît directement sur le site :

http://56.228.24.64/

Cette démonstration permet de vérifier le déploiement automatique sans intervention manuelle sur le serveur pour chaque mise à jour.

## 7. Accès depuis plusieurs machines

Le site AWS est accessible depuis plusieurs ordinateurs ou téléphones connectés à Internet :

http://56.228.24.64/

Dans notre vidéo, la première partie de la démonstration est réalisée sur le PC de Camille. La partie consacrée au déploiement est réalisée depuis un autre ordinateur, sur le même site.

Cela montre que l'application est accessible depuis deux machines différentes.

## 8. API

L'API FastAPI propose notamment les routes suivantes :

```text
GET /api/health
GET /api/books?limit=5&offset=0
GET /api/search?q=whale
GET /api/search/advanced?regex=...
GET /api/books/2701
GET /api/books/2701/text?page=1
GET /api/books/2701/similar
```

Documentation interactive de l'API locale :

http://localhost:8000/docs

## 9. Tests et performances

### Tests backend

Depuis la racine du projet, avec Python et les dépendances installées :

```bash
python -m pytest
```

### Tests frontend

```bash
cd frontend
npm ci
npm test
```

### Mesures de performance

Nous avons créé le script `benchmark_gutenberg.py` pour mesurer les temps de réponse des recherches simple et RegEx.

Les requêtes `whale`, `ship` et `alice` ont été exécutées **10 fois chacune** sur l'application en ligne.

Le script calcule les moyennes, les écarts-types et génère un graphique.

Les mesures incluent le temps de communication réseau.

Sur les requêtes testées, la recherche simple était environ **2,5 fois plus rapide** que la recherche RegEx.

Les résultats sont présentés dans notre rapport.

## 10. Organisation du projet

| Dossier / fichier | Rôle |
|---|---|
| `backend/` | API FastAPI, recherche et recommandations |
| `frontend/` | Interface React/Vite |
| `data/sample/` | Livres d'exemple |
| `data/raw/` | Textes du corpus, si présents |
| `data/indexes/` | Index inversé |
| `data/graphs/` | Graphe et PageRank |
| `scripts/` | Préparation du corpus et calculs |
| `tests/` | Tests automatisés |
| `.github/workflows/` | Workflows GitHub Actions |
| `docker-compose.yml` | Configuration Docker Compose |
| `.env` | Configuration locale fournie séparément avec le rendu |
| `docs/` | Documentation complémentaire |

## 11. Dépannage

| Problème | Solution |
|---|---|
| Docker ne démarre pas | Vérifier que Docker Desktop est ouvert |
| Port `5432` déjà utilisé | Arrêter l'ancien conteneur PostgreSQL ou le service qui occupe ce port |
| Port `8080` ou `8000` occupé | Libérer le port concerné |
| Backend non prêt | Consulter `docker compose logs --tail=80 backend` |
| Bandeau « Mode démonstration » | Les données complètes sont absentes ; utiliser le site AWS pour tester le moteur réel |
| PostgreSQL ne contient aucun livre | Vérifier l'import des métadonnées |
| Nouvelles données non chargées | Exécuter `docker compose restart backend` |
| Site AWS inaccessible | Vérifier la connexion Internet et la disponibilité du serveur |

## 12. Contenu du rendu

Notre rendu comprend :

- Le ZIP du code source téléchargé depuis GitHub.
- Le fichier `.env` déjà configuré pour le lancement local.
- Le rapport du projet.
- La vidéo de présentation et de démonstration.
- Les scripts, les tests et la documentation présents dans le dépôt.

Le ZIP du code source ne contient pas les textes volumineux du corpus complet.

**Pour évaluer les fonctionnalités et les algorithmes sur les données réelles, utiliser le site AWS.**

---

**Application en ligne :** http://56.228.24.64/  
**Dépôt GitHub :** https://github.com/divcamillediv/gutenberg-library

**Kenza, Nadine et Camille — Projet 2 DAAR**
