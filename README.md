# My First Adventure Game

My First Adventure Game is a top-down 2D adventure game built with Python and
Pygame.

The project also serves as a learning-oriented foundation for future adventure
games, including Zelda-like games, action RPGs, and traditional RPGs.

## Project goals

The project aims to build:

- a small reusable game engine based on Pygame;
- a complete top-down adventure game using that engine;
- a clear foundation that can be cloned and adapted for future games.

The engine remains internal to the project. It is designed for small 2D
adventure games rather than as a universal game engine.

## Architecture

The source code is divided into two main areas:

- `engine`: reusable technical capabilities independent of game rules;
- `game`: rules, content, presentation, and progression specific to this game.

The engine provides capabilities and reports factual events. The game decides
their meaning and consequences.

## Requirements

- Python 3.13 or later

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project with its development and documentation dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs]"
```

## Running the game

Run the package as a Python module:

```powershell
python -m my_first_adventure_game
```

Alternatively, use the installed command:

```powershell
my-first-adventure-game
```

### Controls

- press Enter on the title screen to start;
- press P on the title screen to view the persistent player profile;
- use the arrow keys to move the player;
- press Space near a destructible obstacle or enemy to attack;
- press E near the non-player character to speak;
- press Escape during gameplay to pause or resume.

## Development checks

Check formatting:

```powershell
python -m ruff format --check .
```

Check Markdown formatting:

```powershell
python -m mdformat --check README.md CHANGELOG.md AGENTS.md docs
```

Run the linter:

```powershell
python -m ruff check .
```

Run the tests:

```powershell
python -m pytest
```

Build the documentation with strict link and configuration checks:

```powershell
python -m mkdocs build --strict
```

Build the package:

```powershell
python -m build
```

## Current status

The project now provides a minimal playable top-down loop:

1. the application opens on a title screen;
2. pressing Enter explicitly transitions to gameplay;
3. the arrow keys move the player through a Python-authored map;
4. axis-aligned collisions prevent the player from crossing walls.
5. speaking to the Guide starts a collection objective and reveals its items;
6. overlapping an active collectible deactivates it and removes it from view.
7. each collected object awards 100 points and updates the displayed session
   score.
8. pressing Space near the destructible obstacle removes it and opens the
   passage it blocked.
9. a stationary enemy blocks movement and survives the first nearby attack;
10. non-fatal damage briefly changes the enemy's color;
11. a second nearby attack defeats it and opens its former position.
12. defeating every enemy contributes to victory but does not bypass the Guide
   objective;
13. touching an active enemy damages the player, with a short invulnerability
   period between hits;
14. reaching zero health transitions to a defeat screen that displays the final
   score.
15. pressing Enter on either result screen returns to the title;
16. starting again creates a fresh map, score, animations, and gameplay state.
17. pressing Escape temporarily replaces gameplay with an opaque pause screen
   and resumes the same session on a second press.
18. pressing E near the non-player character opens an ordered dialogue and
   identifies its speaker as the Guide;
19. pressing Enter advances through its lines, then resumes the same gameplay
   session after the last one.
20. the Guide gives a reminder while collection remains active, validates the
   objective after every item is collected, and preserves that completed state.
21. the current objective status remains visible at the top of the gameplay
   screen and reports collected items against the required total.
22. returning to the Guide after collection awards a one-time 500-point bonus.
23. crossing the demo map's right exit moves the same player into a minimal
   clearing without replacing the gameplay scene;
24. crossing the clearing's left exit returns to the preserved demo map while
   keeping session score and progression.
25. temporary purple markers make both active map exits visible.
26. collision-aware boundary walls give the clearing a minimal enclosed
   layout while leaving its return exit accessible.
27. the clearing's Caretaker provides its own dialogue without starting or
   advancing the Guide objective.
28. the Guide activates a third collectible in the clearing, and collection
   progress and score continue across both maps.
29. victory requires both every demo enemy to be defeated and the Guide
   objective to be completed, in either order.
30. the demo map and clearing use distinct game-owned background colors that
   change with their spatial content.
31. victory and defeat display collected-item, destroyed-obstacle, and
   defeated-enemy totals from the current session.
32. session starts and completed results are saved to a persistent player
   profile in the platform-specific application data directory.
33. pressing P on the title opens the accumulated profile statistics, and
   Enter returns to the title.

Implemented foundations include:

- a reusable `engine` and game-specific `game` package structure;
- application lifecycle, frame timing, and window configuration;
- explicit scene management and game-owned navigation;
- action-based input with pressed, held, and released states;
- normalized directional movement;
- package-based image and font caches;
- minimal engine text rendering and game-owned rectangle presentation;
- reusable elapsed-time-driven looping and one-shot frame animations;
- an animated player with game-owned temporary idle, movement, and one-shot
  collection and attack states;
- immutable floating-point collision bounds;
- lightweight spatial entities and deterministic world storage;
- axis-separated movement against solid obstacles;
- a game-owned Python-authored demo map with collectible objects;
- a minimal second map and bidirectional exits that preserve the same gameplay
  scene and session player;
- map-specific game-owned background colors applied through the same map-change
  path as spatial content;
- a game-owned destructible obstacle removed by a proximity attack;
- a game-owned stationary enemy composed from reusable spatial state and
  mutable health;
- game-owned damage behavior requiring two nearby attacks to defeat the current
  enemy;
- brief game-owned color feedback after non-fatal enemy damage;
- a game-owned player that composes reusable spatial state with validated,
  mutable health;
- enemy contact damage, temporary player invulnerability, and a health display;
- an immutable player defeat fact delivered through an explicit callback;
- a game-owned defeat scene reached through an explicit transition and showing
  the final session score;
- a game-owned victory scene reached only after combat and Guide progression
  are both complete and showing the final session score;
- an explicit return to the title followed by fresh session construction for
  every new game;
- a game-owned pause action and opaque pause scene that suspend gameplay and
  resume the same session explicitly;
- a named game-owned non-player character with ordered dialogue lines, a
  proximity interaction action, and a minimal dialogue scene that displays its
  speaker and advances one line per confirmation before resuming the same
  session explicitly;
- a second map-specific NPC whose static dialogue remains independent from the
  Guide's progression rules;
- a game-owned dialogue panel with a distinct background, border, and balanced
  spacing around the speaker, current line, and continuation instruction;
- word-boundary wrapping based on the selected font's measured width, with a
  dialogue panel whose height adapts to the resulting visual lines;
- a concrete four-state Guide collection objective that activates its items,
  selects reminder and completion dialogue, and resets with each new session;
- a Guide objective whose concrete collectible set spans the demo and clearing
  maps without introducing a generic quest system;
- a gameplay objective display that observes the same session-local objective;
- live collected and required item counts while the Guide objective is active;
- a one-time game-owned score bonus when the Guide validates the objective;
- explicit game-owned progression without a generic quest, condition, or
  dialogue scripting system;
- game-owned collection behavior based on reusable entity overlap detection;
- immutable collection, destruction, and enemy defeat facts delivered through
  explicit callbacks;
- game-owned item collection scoring rules;
- an accumulated session score displayed during gameplay;
- fresh game-owned session statistics updated from factual events and displayed
  on both result screens;
- reusable UTF-8 JSON loading and atomic replacement in the engine persistence
  domain;
- a versioned, validated game-owned player profile that accumulates starts,
  completions, victories, scores, and activity statistics across launches;
- a profile scene accessible from the title that presents every accumulated
  counter without owning storage behavior;
- automated tests, Ruff checks, strict documentation builds, package builds,
  and GitHub Actions CI.

Localization and broader combat and interaction systems have not been
implemented yet.

## Documentation

The documentation site combines manually maintained architecture pages with an
API reference generated during each build from public package entry points and
their docstrings.

Build the site:

```powershell
python -m mkdocs build --strict
```

Preview it locally:

```powershell
python -m mkdocs serve
```

See [docs/index.md](docs/index.md) for the architecture overview, domain
responsibilities, project boundaries, decision records, and API reference.

Generated API documentation complements architectural reasoning. It does not
replace manually maintained architecture pages or decision records.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for notable project changes.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
