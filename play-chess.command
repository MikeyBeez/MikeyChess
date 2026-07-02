#!/bin/bash
# Serve MikeyChess over http so the Lichess opening book can connect.
# (Browsers block the cross-origin Lichess request from file:// pages.)
cd "$(dirname "$0")"
PORT=8787
URL="http://localhost:$PORT/chess.html"
echo "Serving MikeyChess at $URL"
echo "Keep this window open while you play. Press Ctrl-C here to stop."
( sleep 1; open "$URL" ) &
exec python3 -m http.server "$PORT"
