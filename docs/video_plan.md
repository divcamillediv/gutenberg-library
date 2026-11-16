# Plan de la vidéo pitch (5 minutes) — collectif

La démonstration est obligatoire : une vidéo sans démonstration est pénalisée. Schémas
lisibles et vraie démonstration plutôt qu'une visite du code.

| Temps | Contenu | Pilote |
|---|---|---|
| 0:00–0:35 | Problème, objectif, équipe | Camille |
| 0:35–1:20 | Architecture FastAPI/React, corpus et index | Kenza + Camille |
| 1:20–2:10 | Jaccard, graphe, PageRank, seuil | Nadine |
| 2:10–4:30 | Démo : recherche, RegEx, lecture, classement, suggestions, deux clients | Toutes |
| 4:30–5:00 | Résultats chiffrés, limites, conclusion | Toutes |

## Scénario de démonstration (2:10–4:30)

Corpus complet, index et graphe déjà présents sur la machine serveur : aucun téléchargement
pendant l'enregistrement.

1. Montrer le serveur (`docker compose up`) et deux clients : un PC et un téléphone.
2. PC : recherche d'un mot présent seulement dans le corps d'un livre ; commenter le
   classement (occurrences, PageRank, score).
3. PC : ouvrir un résultat, lire le texte, changer de page.
4. Téléphone, en même temps : recherche RegEx, puis clic sur une suggestion.
5. Montrer un cas d'erreur géré (RegEx invalide) et une recherche sans résultat.

TODO (toutes) : choisir les requêtes de la démo une fois le corpus complet indexé, et les
répéter avant le tournage.

## À vérifier avant l'envoi

- TODO : son, lisibilité des écrans, durée.
- TODO : exporter en résolution SD si nécessaire pour limiter le poids.
- TODO : poids de la vidéo (information partagée < 50 Mo, archive ≈ 30 Mo selon la consigne
  écrite : vérifier Moodle, appliquer la limite la plus stricte).
