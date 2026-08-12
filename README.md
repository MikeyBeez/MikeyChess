# MikeyChess

A single-file chess app that runs in your browser — play against Stockfish at
eight difficulty levels, get full post-game analysis, and (optionally) turn on a
**talking coach** powered by a local LLM that narrates openings, offers your book
options, chats about the position, and remembers what it has taught you.
No account, no sign-up.

Built because the free online sites started rate-limiting heavy use. Everything
runs on your own machines.

## Run it (game only)

Download `chess.html` and double-click it (or open it in any modern browser:
Chrome, Firefox, Safari, or Edge). The chess engine and rules library are
embedded directly inside the file, so the game itself is fully playable offline.
Two features use the network when available: the live Lichess opening-book panel
(falls back to a built-in book offline) and the coach (below).

## Features

- **Play vs Stockfish, levels 1–8** — strength curve modeled on lichess's levels,
  from roughly 800 Elo up to 2400+. Level 4 is the default and is remembered
  between sessions.
- **Click or drag** — move pieces by clicking (with legal-move dots) or by
  dragging them to the target square. Last-move and check highlighting, pawn
  promotion picker, board flip.
- **Appearance** — choose from 8 board color themes and 5 piece styles (three
  embedded vector sets plus unicode symbols and letters). Your choice is
  remembered between sessions.
- **Game management** — play as White, Black, or random; takeback; resign; copy
  the move list or the full PGN to your clipboard.
- **Opening detection** — the opening name (Ruy López, Sicilian Najdorf, etc.)
  is shown and updated as you play.
- **Opening book panel** — live Lichess explorer stats (with win/draw/loss bars,
  click a book move to play it), falling back to a built-in book offline.
- **Talking coach** (optional, via [reachi](https://github.com/MikeyBeez/reachi)) —
  spoken opening narration, book options each turn, move grading outside theory,
  position chat, hints, and a persistent lesson memory. See "The coach" below.
- **Move navigation** — step through the game with the on-screen buttons or the
  arrow keys.
- **Post-game analysis** — runs Stockfish over every position and gives you:
  - a win-probability **Accuracy %** for each side (the same style of metric
    lichess reports), plus average centipawn loss,
  - an evaluation graph across the whole game,
  - per-move inaccuracy / mistake / blunder marks (`?!`, `?`, `??`) in the move list,
  - the engine's best move shown for any move you click.

## The coach (optional)

The coach is the teaching layer: it announces openings by name ("That's the
Sicilian Defense, main line"), lists your 3–4 book options each turn, grades
your moves after you leave theory (never criticizing book moves or checkmates),
chats about the position, speaks aloud, and keeps a lesson memory — it knows
which openings it has already shown you and reminds you when you repeat a
mistake it has flagged before.

Most of the coach needs **no extra software at all**: opening narration, book
options, move grading, hints, and the (browser) voice are built into the page.
Only the free-form chat needs an LLM — and the page can talk to one directly.

### Setup — the simple way (any machine)

1. Install [Ollama](https://ollama.com) and pull any instruct model:

   ```bash
   ollama pull llama3.1:8b
   ```

2. Serve the page (browsers block LLM calls from `file://`):

   ```bash
   ./play-chess.command        # or: python3 -m http.server 8787
   ```

3. Turn the **Coach** toggle on. In the Coach panel, leave the backend on
   *Ollama*, host blank (local), hit **Apply**, and pick your model from the
   dropdown. Done — the coach chats through your local model, speaks with the
   browser's voice, and keeps its lesson memory in the browser.

   A local [llama.cpp](https://github.com/ggerganov/llama.cpp) `llama-server`
   works too: choose *llama.cpp* as the backend and give its port.

### Setup — with the reachi assistant (optional extra)

[reachi](https://github.com/MikeyBeez/reachi) is a small local assistant server.
Adding it upgrades the coach with a neural (Piper) voice, lesson memory that
follows you across browsers and machines, and cloud foundation-model support
(the API key stays server-side). The page auto-detects it — no configuration.

```bash
git clone https://github.com/MikeyBeez/reachi ~/Code/reachi
cd ~/Code/reachi
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env          # pick your model — see below
./install_api_service.command # macOS always-on service
```

Then open the game at **http://127.0.0.1:8765/** (reachi serves it; set
`REACHI_WEB_ROOT` if your copy lives elsewhere). Opening the page any other
way also works — it finds reachi at `127.0.0.1:8765` automatically.

### Choosing a model

**In the game:** the Coach panel has connection controls — pick a backend
(Ollama, llama.cpp, or a cloud Foundation API), enter the host (blank = this
machine) and port, hit Apply, then choose from the model list that appears.
Your choices are remembered by the browser and re-applied when you return.
For a cloud foundation model, put the API key in reachi's `.env`
(`FOUNDATION_API_KEY=...`) — the key never touches the browser — then select
"Foundation API" and enter the host (e.g. `api.openai.com`).

**In config:** the coach otherwise uses whatever model reachi's **active
persona** points at, set in `~/Code/reachi/.env`:

```env
# The model the coach (and "hey jarvis") uses:
GEMMA_MODEL=llama3.1:8b                  # any model name your server knows
GEMMA_HOST=http://127.0.0.1:11434       # where that server listens
```

Two kinds of model server are supported, **auto-detected** — point `GEMMA_HOST`
at either and reachi figures out the protocol:

- **Ollama** — easiest. `ollama pull llama3.1:8b` (or any instruct model),
  keep the default host above. Model names are meaningful; switch models by
  changing `GEMMA_MODEL`.
- **llama.cpp `llama-server`** — for models you run yourself (OpenAI-style
  API). It serves one model, so `GEMMA_MODEL` is just a display label:

  ```bash
  llama-server --model your-model.gguf --port 8080 ...
  # .env: GEMMA_HOST=http://127.0.0.1:8080
  ```

Any competent instruct model works; 7–8B models give quick, decent coaching,
larger models give noticeably better chess talk. Two practical notes for big
models: raise the timeouts in `.env` (`OLLAMA_TIMEOUT_S=240`,
`OLLAMA_COLD_TIMEOUT_S=360`) so a slow cold load isn't mistaken for a hang,
and keep the model files on an SSD — cold-loading a 20 GB model from a
spinning disk takes minutes.

**Remote GPU box:** run the model server there and forward a local port to it,
then use the forwarded port as `GEMMA_HOST`:

```bash
ssh -N -L 127.0.0.1:11435:127.0.0.1:8080 your-gpu-box   # keep this running
# .env: GEMMA_HOST=http://127.0.0.1:11435
```

The API-serving process can also override the model just for the coach without
touching the voice assistant: set `REACHI_API_MODEL` / `REACHI_API_HOST` in the
service's environment.

### Lesson memory

Without reachi, lessons live in your browser's localStorage. With reachi they
are stored on the machine running the API, in
`~/Library/Application Support/reachi/memory/chess-lessons.json`, so the
coach's memory of you follows you across browsers. The browser keeps a
localStorage copy as an offline cache.

### If the coach won't answer

No reachi: make sure Ollama is running (`ollama serve`) and a model is pulled,
and that you opened the page over http (not `file://`). With reachi: run
`diagnose_coach.command` in the reachi repo — it checks each hop
(API service → model host → full round-trip) and tells you which one is broken.
The usual suspects: the API service isn't running, the tunnel to a remote GPU
box is down, or the model is still cold-loading (first answer after a restart
can take a minute or two; later ones are instant).

## How it works

The whole app is one self-contained HTML file. Two libraries are embedded inside
it (base64-encoded) so nothing is ever fetched from the network:

- [chess.js](https://github.com/jhlywa/chess.js) — move generation and rules (BSD license)
- [Stockfish](https://github.com/nmrugg/stockfish.js) — the Stockfish 10 engine,
  asm.js build, compiled to JavaScript (GPL v3)

The original, un-embedded copies of these libraries are kept in the `build/`
directory, and `build.py`-style assembly is done by the build step described
below.

## Building

`chess.html` is generated by embedding the libraries in `build/` into the source
template. To rebuild after editing:

1. Ensure `build/chess.min.js` and `build/stockfish.asm.js` are present.
2. Re-run the embedding step (base64-encode each file and substitute it into the
   template's `__CHESS_JS_B64__` / `__SF_ASM_B64__` placeholders).

## License

This project bundles the Stockfish engine, which is licensed under the
**GNU General Public License v3**. Because Stockfish is embedded in `chess.html`,
the distributed combination is covered by the **GPL v3** — see
[stockfish.org](https://stockfishchess.org/) and the
[stockfish.js](https://github.com/nmrugg/stockfish.js) project for the engine and
its corresponding source. The complete engine source as distributed here is in
`build/stockfish.asm.js`.

The original application code in this repository (everything other than the
bundled libraries) is additionally made available by the author under the
**MIT License** — see [LICENSE](LICENSE). chess.js is under the BSD license.

The bundled piece sets (Cburnett, Merida, Alpha) come from the
[lichess](https://github.com/lichess-org/lila) project and are used under their
respective free licenses; see lichess's COPYING for details.
