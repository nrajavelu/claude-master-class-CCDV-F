#!/usr/bin/env bash
# Serve the CDF-F Bootcamp portal locally and print the direct URLs.
#   ./start.sh            # port 8070
#   ./start.sh 8010       # pick a port
#   ./start.sh --lan      # also bind 0.0.0.0 for other devices on your network
set -eu
cd "$(dirname "$0")"

BIND=127.0.0.1 HOST=localhost
PORT=8070          # distinct per course so browser-cached pages never collide with another course
for a in "$@"; do
  case "$a" in
    --lan|--share) BIND=0.0.0.0 ;;
    *[!0-9]*|'') : ;;
    *) PORT="$a" ;;
  esac
done

PY=python3; command -v python3 >/dev/null || PY=python

# find a free port: PORT .. PORT+15
for p in $(seq "$PORT" $((PORT+15))); do
  if "$PY" -c "import socket,sys; s=socket.socket(); sys.exit(0 if s.connect_ex(('127.0.0.1',$p))==0 else 1)"; then
    continue                     # in use -> next
  else
    PORT="$p"; break
  fi
done

if [ "$BIND" = 0.0.0.0 ]; then
  HOST=$("$PY" -c "import socket; print(socket.gethostbyname(socket.gethostname()))" 2>/dev/null || echo localhost)
fi
BASE="http://$HOST:$PORT"

cat <<TXT

  Aizentify CDF-F Bootcamp  —  serving from $(pwd)
  ------------------------------------------------------------------
  Portal (start here)   $BASE/portal/index.html
  Candidate portal      $BASE/portal/candidate.html
  Trainer console       $BASE/portal/trainer.html
  Practice              $BASE/portal/practice.html
  Video player          $BASE/portal/watch.html
  Decks                 $BASE/portal/decks.html
  Study                 $BASE/portal/study.html
  Cookbooks             $BASE/portal/cookbooks.html
  Worked examples       $BASE/portal/examples.html
  Resources             $BASE/portal/resources.html
  ------------------------------------------------------------------
  Ctrl+C to stop.

TXT

( sleep 1; command -v open >/dev/null && open "$BASE/portal/index.html" >/dev/null 2>&1 || true ) &
exec "$PY" -m http.server "$PORT" --bind "$BIND"
