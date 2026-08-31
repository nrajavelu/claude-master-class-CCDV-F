#!/usr/bin/env bash
# ============================================================================
# Aizentify CDF-F Bootcamp — start the local portal
#
#   ./start.sh              serve on localhost, open the portal in your browser
#   ./start.sh --lan        also bind 0.0.0.0 so candidates on your Wi-Fi can reach it
#   ./start.sh 9000         use a specific port
#   PORT=9000 ./start.sh    same, via env
#
# Serves this folder over http (so portal/view.html can fetch the .md files),
# then opens  http://localhost:<port>/portal/  . Ctrl+C to stop.
# ============================================================================
set -euo pipefail

cd "$(dirname "$0")"

# ---- args ----
BIND="127.0.0.1"
SHARE=0
PORT="${PORT:-8000}"
for a in "$@"; do
  case "$a" in
    --lan|--share) BIND="0.0.0.0"; SHARE=1 ;;
    ''|*[!0-9]*)   : ;;                       # ignore non-numeric
    *)             PORT="$a" ;;
  esac
done

# ---- python ----
PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
  echo "error: python3 (or python) not found on PATH." >&2
  echo "install Python 3.11+ — see logistics/00-environment-setup.md" >&2
  exit 1
fi

# ---- find a free port (try PORT .. PORT+20) ----
# returns 0 (success) when nothing is listening on the port
port_free() { "$PY" -c "import socket,sys; s=socket.socket(); s.settimeout(0.3); sys.exit(1 if s.connect_ex(('127.0.0.1', int('$1')))==0 else 0)" 2>/dev/null; }
tries=0
while ! port_free "$PORT"; do
  PORT=$((PORT + 1)); tries=$((tries + 1))
  if [ "$tries" -gt 20 ]; then echo "error: no free port near ${PORT}." >&2; exit 1; fi
done

URL="http://localhost:${PORT}/portal/"

# ---- start server ----
"$PY" -m http.server "$PORT" --bind "$BIND" --directory "$(pwd)" >/dev/null 2>&1 &
SRV=$!
trap 'echo; echo "stopping portal (pid $SRV)"; kill "$SRV" 2>/dev/null || true' INT TERM EXIT

# wait for it to answer
for _ in $(seq 1 20); do
  if "$PY" -c "import urllib.request,sys
try: urllib.request.urlopen('http://127.0.0.1:${PORT}/portal/index.html', timeout=0.5); sys.exit(0)
except Exception: sys.exit(1)" 2>/dev/null; then break; fi
  sleep 0.25
done

# ---- banner ----
echo
echo "  Aizentify CDF-F portal is running."
echo "  ─────────────────────────────────────────────"
echo "  Portal        $URL"
echo "  Trainer       ${URL}trainer.html"
echo "  Practice      ${URL}practice.html"
if [ "$SHARE" -eq 1 ]; then
  LAN="$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null \
        || hostname -I 2>/dev/null | awk '{print $1}' || true)"
  if [ -n "${LAN:-}" ]; then
    echo "  Share (LAN)   http://${LAN}:${PORT}/portal/"
    echo "                ^ paste this as the base URL in trainer.html to make candidate links"
  fi
fi
echo "  ─────────────────────────────────────────────"
echo "  Ctrl+C to stop."
echo

# ---- open browser ----
if command -v open        >/dev/null 2>&1; then open "$URL"
elif command -v xdg-open  >/dev/null 2>&1; then xdg-open "$URL" >/dev/null 2>&1 || true
elif command -v explorer.exe >/dev/null 2>&1; then explorer.exe "$URL" >/dev/null 2>&1 || true
else echo "  (open $URL manually)"; fi

wait "$SRV"
