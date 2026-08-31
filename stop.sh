#!/usr/bin/env bash
# Stop any local portal server started by ./start.sh (python http.server in this folder).
set -euo pipefail
cd "$(dirname "$0")"
HERE="$(pwd)"

# match: python(3) -m http.server ... --directory <this folder>   (or launched from here)
PIDS="$(pgrep -f "http\.server" || true)"
KILLED=0
for pid in $PIDS; do
  cwd="$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p' | head -1 || true)"
  args="$(ps -o command= -p "$pid" 2>/dev/null || true)"
  if [ "${cwd:-}" = "$HERE" ] || printf '%s' "$args" | grep -qF "$HERE"; then
    kill "$pid" 2>/dev/null && { echo "stopped portal server (pid $pid)"; KILLED=1; }
  fi
done
[ "$KILLED" -eq 0 ] && echo "no portal server found for $HERE"
exit 0
