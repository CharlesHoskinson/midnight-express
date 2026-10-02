#!/usr/bin/env bash
# Make the evidence tree read-only for a design round, or restore it.
#   design/guard.sh lock | unlock | snapshot
# Locked: catalog notes reviews pdfs graphify-out graph/text design/evidence + the top-level dirs
# (so no new files can be created next to them). design/rounds, graph/out and graph/chunks stay writable.
set -uo pipefail
R=/home/charl/privateEvents
FILES=(catalog notes reviews pdfs graphify-out graph/text design/evidence scripts)
DIRS=("$R" "$R/design" "$R/graph")
case "${1:-}" in
  lock)
    for d in "${FILES[@]}"; do [ -e "$R/$d" ] && chmod -R a-w "$R/$d"; done
    for f in CHARTER.md roles.json; do chmod a-w "$R/design/$f"; done
    for d in "${DIRS[@]}"; do chmod a-w "$d"; done
    echo locked ;;
  unlock)
    for d in "${DIRS[@]}"; do chmod u+w "$d"; done
    for f in CHARTER.md roles.json; do chmod u+w "$R/design/$f"; done
    for d in "${FILES[@]}"; do [ -e "$R/$d" ] && chmod -R u+w "$R/$d"; done
    echo unlocked ;;
  snapshot)
    cd "$R" && find catalog notes reviews graphify-out design/evidence design/CHARTER.md -type f -print0 2>/dev/null | sort -z | xargs -0 sha256sum | sha256sum | cut -c1-16
    ls pdfs | wc -l ;;
  *) echo "usage: $0 lock|unlock|snapshot"; exit 2 ;;
esac
