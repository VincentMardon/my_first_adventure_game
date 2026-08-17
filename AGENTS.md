# AGENTS.md

## Purpose

This file gives human and AI contributors the minimum operational guidance
required before modifying My First Adventure Game.

The project builds:

1. a small reusable Pygame engine for top-down 2D adventure games;
2. a concrete game that validates the engine through real requirements.

The engine is internal to this repository and is not a universal game engine.

## Required reading

Before proposing or making an architectural change:

1. read [`docs/index.md`](docs/index.md);
2. read the
   [architecture overview](docs/architecture/overview.md);
3. read the
   [architectural boundaries](docs/architecture/boundaries.md);
4. read the page for the affected domain;
5. read the relevant records in [`docs/decisions`](docs/decisions);
6. inspect the current code and tests before relying on documentation alone.

Documentation explains intent. Code and tests provide evidence of current
behavior. A disagreement must be investigated, not silently ignored.

## Collaboration mode

The repository owner is using this project to learn game programming.

Unless the owner explicitly changes this rule:

- agents remain read-only for source code, tests, configuration, workflows, and
  other non-Markdown files;
- agents inspect the repository and propose focused changes;
- the owner rewrites and applies proposed code, tests, and configuration;
- agents review the resulting implementation;
- after the owner confirms that the code portion of an increment is complete,
  agents may create, edit, or remove the Markdown files required to document
  that increment;
- this Markdown authorization includes architecture pages, API reference
  pages, `README.md`, `CHANGELOG.md`, and `AGENTS.md`;
- agents report the Markdown files they changed and explain any deletion;
- the owner reviews all documentation changes before committing them;
- agents do not stage changes, commit, push, or create pull requests;
- agents may run non-mutating checks;
- commands that generate files are left for the owner to run.

Communicate with the owner in French.

Write code, documentation, identifiers, and commit messages in English.

## Architectural boundaries

The primary dependency direction is:

```text
game → engine
```

The engine must never import the game.

The engine owns reusable mechanisms.

The game owns concrete rules, content, presentation, and composition.

`game.main` is the composition root.

A scene is a global application state. A map is spatial content managed by a
gameplay scene.

The engine must not know concrete:

- game actions;
- scenes;
- colors or themes;
- entities or levels;
- scoring or progression rules;
- profiles or statistics;
- localization content;
- combat, quest, or achievement rules.

See
[`docs/architecture/boundaries.md`](docs/architecture/boundaries.md)
for the normative rules.

## Genericity review

Before placing a capability in `engine`, determine:

1. whether it is a reusable mechanism or a game rule;
2. which accepted requirement or roadmap item needs it;
3. which concrete or planned component will consume it;
4. whether it can be tested without concrete game content;
5. what a cloned Zelda-like, action RPG, or traditional RPG would replace;
6. whether a smaller game-owned solution is sufficient.

When an idea risks excessive coupling, explain:

- the immediate impact;
- the cloning risk;
- the recommended layer;
- the smallest acceptable solution.

Do not introduce an abstraction solely for hypothetical future games.

## Prohibited premature systems

Do not introduce without a demonstrated requirement:

- an entity-component system;
- realistic physics;
- polygonal collisions;
- a universal event bus;
- a dependency injection framework;
- a custom map editor;
- a general scripting language;
- a standalone engine package;
- runtime metadata used only for documentation.

## Development workflow

Work in small, coherent increments.

For each increment:

1. inspect the current working tree;
2. define the intended responsibility and layer;
3. identify the behavior and invariants to protect;
4. propose the smallest implementation;
5. add or update focused tests;
6. let the owner write the change;
7. review the actual implementation;
8. after the owner confirms that the code is complete, update the required
   Markdown documentation;
9. run the relevant quality checks;
10. inspect the complete diff;
11. report the documentation changes and propose one Conventional Commit
   message with a scope;
12. let the owner review, commit, and push;
13. verify the remote CI when requested.

Do not mix unrelated cleanup with the current increment.

## Code conventions

The project targets Python 3.13 and Pygame.

Use:

- the `src/` package layout;
- type annotations;
- explicit constructor injection;
- immutable configuration when appropriate;
- public exports through package `__init__.py` and `__all__`;
- pure functions for deterministic calculations;
- focused pytest tests;
- Ruff formatting and linting.

Prefer public domain imports from package entry points.

Internal modules may use direct sibling imports when needed to avoid circular
package initialization.

Do not add validation or abstraction without a concrete invariant or
requirement.

## Input conventions

Game code depends on actions, not raw device state.

The engine never defines concrete game actions.

Directional screen coordinates use:

- left: negative horizontal;
- right: positive horizontal;
- up: negative vertical;
- down: positive vertical.

Diagonal movement remains normalized.

## Scene conventions

Every scene implements:

- `handle_event(event)`;
- `update(delta_time)`;
- `draw(surface)`.

Transitions use `SceneManager.change_scene()` explicitly.

There are currently no scene lifecycle hooks and no scene stack.

Do not add them without a concrete requirement and tests defining their
semantics.

## Documentation conventions

Public components should receive concise docstrings describing their contract.

Architecture pages explain:

- responsibilities;
- relationships;
- invariants;
- extension points;
- change risks.

Architectural decision records explain:

- context;
- decisions;
- consequences;
- rejected alternatives;
- conditions for reconsideration.

Do not document planned components as implemented.

Update:

- the affected architecture page when responsibilities or relationships change;
- an ADR when an accepted architectural decision changes;
- `CHANGELOG.md` at the end of a milestone;
- `README.md` when the project status or developer workflow changes.

Generated documentation must not become the only source of architectural
reasoning.

MkDocs provides the documentation site. Mkdocs-gen-files discovers public
domains and creates their virtual API pages during each build, while
mkdocstrings renders the public interfaces and docstrings.

`scripts/generate_api_pages.py` discovers two-level package entry points whose
`__init__.py` defines a non-empty `__all__`. Generated domain pages do not exist
as physical files under `docs/api`; `docs/api/index.md` remains manually
maintained.

Mdformat enforces consistent Markdown structure, list indentation, tables, and
line endings. Keep its versions pinned and preserve the validated MkDocs and
GFM extensions.

When adding or changing a public domain:

- update its architecture page;
- expose its public contracts through a non-empty `__all__`;
- update `docs/api/index.md`, `docs/index.md`, and the `mkdocs.yml` navigation
  when the domain itself is new;
- keep architecture-to-API links valid;
- run the strict documentation build.

Generated API pages describe available contracts. They must not become the only
source of responsibilities, design intent, invariants, or change risks.

## Commit convention

Use Conventional Commits with a scope:

```text
<type>(<scope>): <description>
```

Examples:

```text
feat(input): track per-frame action states
refactor(application): integrate action input lifecycle
docs(architecture): document engine boundaries
test(scenes): cover explicit scene transitions
```

Descriptions are written in English, lowercase, imperative style, without a
trailing period.

## Verification commands

Activate the project virtual environment and use `python`, not the Windows
`py` launcher:

```powershell
.\.venv\Scripts\Activate.ps1
python -m ruff format --check .
python -m mdformat --check README.md CHANGELOG.md AGENTS.md docs
python -m ruff check .
python -m pytest
python -m mkdocs build --strict
python -m build
```

`python -m mkdocs build --strict` and `python -m build` create files and are run
by the owner.

The CI must reproduce Python and Markdown formatting, lint, tests, strict
documentation, and package build checks.

## Current implemented foundations

Implemented engine domains:

- application lifecycle and window configuration;
- scenes and explicit transitions;
- action-based keyboard input;
- per-frame action states;
- normalized directional movement axes.
- package-based image and font loading with instance-local caches;
- minimal game-independent text rendering;
- floating-point AABB geometry and overlap detection;
- lightweight spatial entities, deterministic lookup and AABB movement;
- normalized target-directed movement with capped travel distance;
- UTF-8 JSON loading and atomic file replacement;

Implemented game foundations:

- concrete title and gameplay scenes;
- Python-authored demo and clearing maps with concrete gameplay roles;
- bidirectional spatial exits that preserve one gameplay scene and session
  player;
- a session-local four-state Guide collection objective;
- factual collection, destruction, enemy defeat, and player defeat events;
- session-local score and activity statistics;
- victory and defeat summaries with fresh state for each new game.
- a versioned persistent player profile with cross-session score and activity
  statistics.
- a profile scene that presents accumulated statistics without owning storage.
- optional NPC target movement demonstrated by the clearing Caretaker without
  pathfinding.

Reserved but not implemented:

- localization.

Do not infer behavior from reserved package names.
