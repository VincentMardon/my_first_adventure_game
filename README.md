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

Install the project and its development dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
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

Build the package:

```powershell
python -m build
```

## Current status

The project has completed its application and scene foundations. It provides:

- a reusable `engine` and game-specific `game` package structure;
- immutable window configuration;
- a generic Pygame application loop with delta-time calculation;
- a decoupled scene contract and scene manager;
- explicit, testable scene transitions;
- a minimal title scene integrated with the application;
- automated quality checks and package builds.

Input handling, world simulation, collisions, and gameplay systems have not been
implemented yet.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.