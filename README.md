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
- use the arrow keys to move the player.

## Development checks

Check formatting:

```powershell
python -m ruff format --check .
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

Implemented foundations include:

- a reusable `engine` and game-specific `game` package structure;
- application lifecycle, frame timing, and window configuration;
- explicit scene management and game-owned navigation;
- action-based input with pressed, held, and released states;
- normalized directional movement;
- package-based image and font caches;
- minimal engine text rendering and game-owned rectangle presentation;
- immutable floating-point collision bounds;
- lightweight spatial entities and deterministic world storage;
- axis-separated movement against solid obstacles;
- a game-owned Python-authored demo map;
- automated tests, Ruff checks, strict documentation builds, package builds,
  and GitHub Actions CI.

Persistence, scoring, profiles, localization, combat, and interaction systems
have not been implemented yet.

## Documentation

The documentation site combines manually maintained architecture pages with an
API reference generated from public Python interfaces and docstrings.

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