# DAAR — Bibliothèque Gutenberg

Application web de recherche et de lecture de livres du Projet Gutenberg, réalisée par **Kenza, Nadine et Camille** dans le cadre du projet 2 de DAAR.

**Application en ligne :** http://56.228.24.64/  
**Dépôt GitHub :** https://github.com/divcamillediv/gutenberg-library

## Fonctionnalités

- Recherche simple par mot-clé et recherche avancée par expression régulière (RegEx).
- Classement des résultats selon les occurrences des mots et le PageRank.
- Recommandations de livres à partir d'un graphe de similarité de Jaccard.
- Consultation des informations des livres et lecture de leur texte dans le navigateur.
- Interface accessible depuis un ordinateur ou un téléphone.

Le corpus préparé contient **1 700 livres**. Lors de notre dernière vérification, **1 697 livres** étaient chargés sur l'application en ligne.

## 1. Tester directement l'application en ligne

L'application est déjà déployée sur un serveur **AWS EC2** et accessible depuis Internet :

**http://56.228.24.64/**

Aucune installation n'est nécessaire. Il suffit d'ouvrir cette adresse dans un navigateur.

Quelques fonctionnalités à tester :

1. Rechercher `whale` dans la barre de recherche.
2. Ouvrir la recherche avancée et saisir `whal(e|es|ing)`.
3. Consulter les résultats classés par pertinence.
4. Ouvrir un livre pour lire son texte.
5. Consulter les suggestions de livres similaires.

Cette version utilise les données réelles du corpus. Elle nécessite une connexion Internet et la disponibilité du serveur AWS.

Le même site peut être ouvert depuis plusieurs ordinateurs différents. C'est notamment ce que nous montrons dans notre vidéo de démonstration.

## 2. Architecture et technologies

Notre application utilise les technologies suivantes :

| Technologie | Utilisation |
|---|---|
| React / Vite | Interface web |
| FastAPI / Python | API, recherche et algorithmes |
| PostgreSQL | Stockage des métadonnées des livres |
| Docker / Docker Compose | Conteneurisation et lancement des services |
| AWS EC2 | Hébergement de l'application |
| GitHub Actions | Intégration et déploiement automatiques |
| GitHub Container Registry (GHCR) | Stockage des images Docker |

L'application est organisée autour de trois services Docker :

- **frontend** : interface React servie par Nginx ;
- **backend** : API FastAPI et moteur de recherche ;
- **db** : base de données PostgreSQL.

Docker Compose permet de gérer ces trois services ensemble.

Les calculs de l'index inversé, du graphe de Jaccard et du PageRank sont réalisés hors ligne. Les résultats sont enregistrés dans des fichiers que le backend charge au démarrage.

## 3. Déploiement sur AWS et GitHub Actions

Notre application est hébergée sur une instance **AWS EC2 Ubuntu**.

Les services frontend, backend et PostgreSQL sont exécutés dans des conteneurs Docker. Docker Compose permet de les démarrer et de les maintenir ensemble sur le serveur.

Nous avons également mis en place un déploiement automatique avec **GitHub Actions**.

### Fonctionnement du déploiement

1. Une modification est effectuée dans le code du projet.
2. Le code est envoyé sur la branche `main` avec `git push`.
3. GitHub Actions déclenche le workflow de publication.
4. Les images Docker sont construites et publiées dans **GHCR**.
5. Le workflow de déploiement utilise un runner installé sur notre serveur AWS EC2.
6. Les conteneurs sont mis à jour avec Docker Compose.
7. La nouvelle version devient accessible sur le même site, sans déploiement manuel.

Les workflows se trouvent dans le dossier `.github/workflows/` du dépôt.

### Démonstration du déploiement automatique

Dans notre vidéo, nous montrons un exemple concret :

- modification d'un texte sur la page d'accueil ;
- commit et push sur la branche `main` ;
- exécution de GitHub Actions ;
- actualisation du site pour constater la modification.

Cela permet de vérifier que le code publié sur GitHub peut être déployé automatiquement sur notre serveur.

**Adresse de l'application déployée :** http://56.228.24.64/

## 4. Lancer l'application en local avec Docker Compose

Cette méthode permet de lancer le projet sur un ordinateur disposant de Docker.

### Prérequis

- Docker Desktop installé et démarré, avec Docker Compose.
- Une connexion Internet pour le premier démarrage.
- Les ports **8080** et **8000** disponibles.

### Sous Windows (PowerShell)

Décompresser le ZIP, puis ouvrir PowerShell dans le dossier contenant `docker-compose.yml`.

**Étape 1 — Préparer la configuration**

```powershell
Copy-Item .env.example .env
notepad .env
```

Dans le fichier `.env`, remplacer `POSTGRES_PASSWORD=change-me` par un mot de passe local, puis enregistrer.

**Étape 2 — Démarrer les services**

```powershell
docker compose up -d --build
```

**Étape 3 — Vérifier que les conteneurs fonctionnent**

```powershell
docker compose ps
```

**Étape 4 — Ouvrir l'application**

- Interface web : http://localhost:8080/
- État du backend : http://localhost:8000/api/health
- Documentation de l'API : http://localhost:8000/docs

Le premier démarrage peut prendre quelques minutes.

### Sous Linux / macOS

Depuis le dossier du projet :

```bash
cp .env.example .env
```

Modifier `POSTGRES_PASSWORD` dans `.env`, puis exécuter :

```bash
docker compose up -d --build
docker compose ps
```

Ouvrir ensuite http://localhost:8080/.

### Arrêter l'application

```bash
docker compose down
```

Pour consulter les journaux en cas de problème :

```bash
docker compose logs --tail=80 backend
docker compose logs --tail=80 frontend
```

**Remarque :** ne pas utiliser `docker compose down -v` si vous souhaitez conserver les données PostgreSQL.

## 5. Données du corpus et mode démonstration

Le projet utilise plusieurs fichiers préparés à l'avance :

| Données | Emplacement |
|---|---|
| Textes des livres | `data/raw/` |
| Métadonnées | PostgreSQL ou `data/metadata/` |
| Index inversé | `data/indexes/index_complet.json` |
| Graphe de Jaccard | `data/graphs/graph.json` |
| PageRank | `data/graphs/pagerank.json` |

Au démarrage, le backend charge les fichiers disponibles.

Si certains fichiers sont absents, l'application peut utiliser les données d'exemple et les modules simulés. Un bandeau **« Mode démonstration »** apparaît alors dans l'interface.

Pour vérifier les données réellement chargées :

http://localhost:8000/api/health

Cette route indique la source des métadonnées (`postgres`, `corpus` ou `sample`) ainsi que l'état des modules (`real` ou `mock`).

**Important :** les fichiers volumineux du corpus complet ne sont pas nécessairement inclus dans l'archive ZIP. Un lancement local sans ces fichiers ne reproduit donc pas automatiquement les résultats obtenus avec les 1 700 livres.

Pour tester directement toutes les fonctionnalités sur le corpus réel, utiliser notre application en ligne :

http://56.228.24.64/

## 6. Reconstituer les données complètes (facultatif)

Cette étape nécessite Python 3.11 ou plus récent et les dépendances Python. Elle n'est pas nécessaire pour consulter le site en ligne.

Depuis la racine du projet :

```powershell
python -m pip install -r backend/requirements.txt
python -m pip install datasets
```

Télécharger et préparer le corpus :

```powershell
python scripts/telecharger_depuis_huggingface.py
```

Construire l'index inversé :

```powershell
python -m scripts.indexer_corpus data/raw data/indexes/index_complet.json
```

Construire le graphe de Jaccard :

```powershell
python scripts/build_graph.py --corpus data/raw
```

Calculer le PageRank :

```powershell
python scripts/compute_pagerank.py
```

Pour importer les métadonnées dans PostgreSQL, démarrer la base :

```powershell
docker compose up -d db
```

Puis, sous PowerShell :

```powershell
$env:POSTGRES_PASSWORD = (Get-Content .env | Where-Object { $_ -match '^POSTGRES_PASSWORD=' } | Select-Object -First 1) -replace '^POSTGRES_PASSWORD=', ''
python scripts/import_metadata.py
```

Redémarrer ensuite le backend :

```powershell
docker compose restart backend
```

Vérifier le résultat sur http://localhost:8000/api/health.

La reconstruction complète peut prendre du temps et dépend de la disponibilité de la source du corpus. Elle n'a pas été vérifiée ici sur un ordinateur vierge.

## 7. Exemples d'utilisation de l'API

Une fois le backend démarré, les routes suivantes peuvent être testées :

```text
GET http://localhost:8000/api/health
GET http://localhost:8000/api/books?limit=5&offset=0
GET http://localhost:8000/api/search?q=whale
GET http://localhost:8000/api/books/2701
GET http://localhost:8000/api/books/2701/text?page=1
GET http://localhost:8000/api/books/2701/similar
```

Pour la recherche RegEx, utiliser l'interface de recherche avancée ou la route :

```text
GET /api/search/advanced?regex=...
```

Exemples de recherches :

| Recherche | Objectif |
|---|---|
| `whale` | Recherche simple |
| `ship` | Recherche d'un mot présent dans plusieurs livres |
| `whal(e\|es\|ing)` | Recherche RegEx |
| `([a-z` | Vérification de la gestion d'une RegEx invalide |

## 8. Tests et performances

### Tests backend

Depuis la racine du projet, avec Python et les dépendances installées :

```powershell
python -m pytest
```

### Tests frontend

```powershell
cd frontend
npm ci
npm test
```

### Mesures de performance

Nous avons également créé le script `benchmark_gutenberg.py` pour comparer les temps de réponse de la recherche simple et de la recherche RegEx.

Les requêtes `whale`, `ship` et `alice` ont été exécutées 10 fois chacune sur l'application en ligne.

Le script calcule les moyennes et les écarts-types et génère un graphique. Les mesures incluent le temps de communication réseau.

Les résultats sont présentés dans notre rapport, avec les fichiers CSV et le graphique.

## 9. Organisation du projet

| Dossier / fichier | Rôle |
|---|---|
| `backend/` | API FastAPI, recherche, classement et recommandations |
| `frontend/` | Interface React/Vite |
| `data/sample/` | Données d'exemple |
| `data/raw/` | Textes du corpus, si présents |
| `data/indexes/` | Index inversé |
| `data/graphs/` | Graphe et PageRank |
| `scripts/` | Téléchargement, indexation, graphe, PageRank et import |
| `tests/` | Tests automatisés |
| `.github/workflows/` | Workflows GitHub Actions |
| `docker-compose.yml` | Configuration des services Docker |
| `docs/` | Documentation complémentaire |

## 10. Dépannage

| Problème | Solution |
|---|---|
| Docker ne démarre pas | Vérifier que Docker Desktop est lancé |
| Port 8080 ou 8000 déjà utilisé | Libérer le port ou adapter la configuration |
| Backend non prêt | Consulter `docker compose logs --tail=80 backend` |
| Bandeau « Mode démonstration » | Vérifier les données disponibles et `/api/health` |
| Aucun livre dans PostgreSQL | Vérifier l'import des métadonnées |
| Modification des données non visible | Exécuter `docker compose restart backend` |
| Le site AWS est inaccessible | Vérifier la connexion Internet et la disponibilité du serveur |

## 11. Contenu du rendu

Le rendu comprend :

- Le code source de l'application.
- Les fichiers Docker et Docker Compose.
- Les scripts de préparation du corpus et des algorithmes.
- Les tests et les mesures de performance.
- Le README et la documentation.
- Le rapport du projet.
- La vidéo de présentation et de démonstration.

Le corpus complet pouvant dépasser la taille autorisée pour l'archive, la version déployée sur AWS permet de tester l'application avec les données réelles.

**Application :** http://56.228.24.64/  
**Code source :** https://github.com/divcamillediv/gutenberg-library

**Projet réalisé par Kenza, Nadine et Camille — Master Informatique, DAAR, Projet 2.**
