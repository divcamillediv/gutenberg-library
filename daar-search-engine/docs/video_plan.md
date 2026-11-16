# Plan de la vidéo pitch (≈ 5 minutes) — collectif

La démonstration est obligatoire : une vidéo sans démonstration est pénalisée. Des schémas
clairs valent mieux qu'une visite du code.

| Durée | Séquence | Contenu | Qui |
|---|---|---|---|
| 45 s | Contexte | Équipe, objectif, corpus (≥ 1 664 livres de ≥ 10 000 mots) | TODO |
| 60 s | Architecture et index | Schéma 3 couches, pipeline hors ligne, index inversé | TODO (Kenza, Camille) |
| 60 s | Graphe et classement | Jaccard, seuil, PageRank, score combiné | TODO (Nadine) |
| 105 s | Démonstration | Voir le scénario ci-dessous | TODO (Camille) |
| 30 s | Conclusion | Résultats, limites, perspectives | TODO |

## Scénario de démonstration (deux clients)

1. Montrer le serveur (`docker compose up`) et deux clients : un PC et un téléphone.
2. PC : recherche d'un mot présent seulement dans le corps d'un livre ; lire le classement.
3. PC : ouvrir un résultat, lire le texte, changer de page.
4. Téléphone, en même temps : recherche RegEx, puis clic sur une suggestion.
5. Montrer un cas d'erreur géré (RegEx invalide) et une recherche sans résultat.

## À vérifier avant l'envoi

- TODO : son, lisibilité des écrans, durée.
- TODO : poids de la vidéo (consigne orale < 50 Mo, archive ≈ 30 Mo selon l'énoncé : vérifier Moodle,
  retenir la limite la plus stricte).
