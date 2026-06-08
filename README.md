# MikeyChess

A single-file chess app you can run in your browser — play against Stockfish at
eight difficulty levels and get full post-game analysis. No account, no sign-up,
no server. Just open the file.

Built because the free online sites started rate-limiting heavy use. This runs
entirely on your own machine.

## Run it

Download `chess.html` and double-click it (or open it in any modern browser).
The first load needs an internet connection once, to pull the engine from a CDN;
after that the gameplay runs locally in your browser.

## Features

- **Play vs Stockfish, levels 1–8** — strength curve modeled on lichess's levels,
  from roughly 800 Elo up to 2400+. Level 4 is the default and is remembered
  between sessions.
- **Full board interaction** — click to move, legal-move dots, last-move and
  check highlighting, pawn promotion picker, board flip.
- **Game management** — play as White, Black, or random; takeback; resign; copy
  the game as PGN.
- **Move navigation** — step through the game with the on-screen buttons or the
  arrow keys.
- **Post-game analysis** — runs full-strength Stockfish over every position and
  gives you:
  - an evaluation graph across the whole game,
  - per-move inaccuracy / mistake / blunder marks (`?!`, `?`, `??`) in the move list,
  - average centipawn loss for each side,
  - the engine's best move shown for any move you click.

## How it works

The whole app is one HTML file. It loads two libraries at runtime from
[cdnjs](https://cdnjs.com):

- [chess.js](https://github.com/jhlywa/chess.js) — move generation and rules (BSD license)
- [stockfish.js](https://github.com/nmrugg/stockfish.js) — the Stockfish engine
  compiled to WebAssembly/asm.js (GPL v3)

Because these are loaded from a CDN rather than bundled, this repository contains
only original code, released under the MIT license below. If you ever vendor
`stockfish.js` into the repo to make it fully offline, note that Stockfish is
GPL v3 and those terms would then apply to the distribution.

## License

MIT — see [LICENSE](LICENSE). Stockfish and chess.js remain under their own
licenses (GPL v3 and BSD respectively).
