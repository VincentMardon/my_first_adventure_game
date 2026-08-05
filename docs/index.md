# Project documentation

This documentation explains the architecture of My First Adventure Game and the
reasoning behind its design.

It is intended for:

- developers learning or revisiting the project;
- contributors extending the engine or game;
- AI agents preparing to modify the codebase.

## Where to start

1. Read the [architecture overview](architecture/overview.md).
2. Read the architectural boundaries before modifying dependencies.
3. Read the page for the domain being changed.
4. Consult the relevant architectural decision records.
5. Verify assumptions against the current code and tests.

## Documentation layers

The project uses several complementary sources of information:

- source code describes the current implementation;
- tests protect behavior and architectural invariants;
- architecture pages explain responsibilities and relationships;
- architectural decision records explain why important choices were made;
- the changelog summarizes notable project evolution.

If documentation and implementation disagree, treat the code and tests as
evidence of current behavior, then determine whether the implementation or the
documentation must be corrected.

## Agent guidance

AI agents must read the repository-level [AGENTS.md](../AGENTS.md) before
proposing changes.

## Current documentation

### Architecture

- [Overview](architecture/overview.md)
- [Boundaries](architecture/boundaries.md)
- [Application](architecture/application.md)
- [Scenes](architecture/scenes.md)
- [Input](architecture/input.md)
- [Assets](architecture/assets.md)

### Architectural decisions

- [0001 — Separate engine and game code](decisions/0001-separate-engine-and-game.md)
- [0002 — Separate scenes from maps](decisions/0002-separate-scenes-and-maps.md)
- [0003 — Use action-based input](decisions/0003-use-action-based-input.md)

### API reference

Automatic API reference generation is planned for a later milestone. Until
then, public Python APIs remain authoritative in the source code.