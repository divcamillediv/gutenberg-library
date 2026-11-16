#!/usr/bin/env bash
# Reconstruit toutes les données, dans l'ordre, depuis un clone propre (collectif).
#
#   ./scripts/rebuild_all.sh
#
# Chaque étape s'arrête à la première erreur. À lancer AVANT la démonstration :
# aucun téléchargement ne doit avoir lieu pendant la vidéo.
# Les étapes de Kenza et Nadine sont encore en TODO : le script s'arrête à la
# première étape non implémentée.
set -euo pipefail

cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"
# Les scripts importent le paquet `app` du backend (normalisation, PageRank).
export PYTHONPATH="backend${PYTHONPATH:+:$PYTHONPATH}"

STEPS=(
  download_books     # Kenza  : data/raw/ + data/metadata/books.json
  clean_books        # Kenza  : data/processed/
  validate_corpus    # Kenza  : >= 1 664 livres de >= 10 000 mots, rapport JSON
  build_index        # Kenza  : data/indexes/
  build_graph        # Nadine : data/graphs/ (edges, neighbors, stats)
  compute_pagerank   # Nadine : data/graphs/pagerank
)

for step in "${STEPS[@]}"; do
  echo "==> scripts/${step}.py"
  "$PYTHON" "scripts/${step}.py"
done

echo "Données reconstruites. Redémarrer le backend pour les charger."
