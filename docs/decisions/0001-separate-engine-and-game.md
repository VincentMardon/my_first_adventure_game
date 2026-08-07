# 0001 — Separate engine and game code

- Status: Accepted
- Date: 2026-08-05

## Context

The project has two related goals:

1. build reusable technical foundations for top-down 2D adventure games;
2. build a concrete game that validates those foundations.

The previous Beat the Maths project combined reusable Pygame ideas with
quiz-specific application behavior. Copying that project and progressively
removing quiz code would preserve unwanted coupling.

The new project needs a clear boundary between reusable mechanisms and concrete
game rules.

## Decision

Source code is separated into two top-level domains inside the project package:

- `engine` contains reusable technical mechanisms;
- `game` contains concrete rules, content, presentation, and composition.

The dependency direction is:

```text
game → engine
```

The engine never imports the game.

The engine remains internal to this repository. It is not published as a
standalone library.

`game.main` acts as the composition root and connects concrete game objects to
engine capabilities.

## Consequences

### Positive

- Game-specific concepts cannot silently become engine dependencies.
- Engine components can be tested independently from game content.
- Future games can replace `game` while preserving useful engine foundations.
- The composition of the application remains visible in one location.
- Architectural coupling becomes easier to inspect.

### Negative

- Some concepts require an engine mechanism and a game-owned configuration.
- More constructor injection and explicit wiring may be necessary.
- Deciding where a feature belongs requires ongoing architectural review.
- Premature engine abstractions remain possible if the boundary is applied
  mechanically rather than thoughtfully.

## Alternatives considered

### Clone Beat the Maths and remove quiz features

Rejected because quiz-specific dependencies would be difficult to identify and
would shape the new architecture accidentally.

### Publish the engine as a separate package immediately

Rejected because the engine API is not yet stable and has only one real game
consumer.

### Keep all code in one game package

Rejected because reusable mechanisms and game rules would become harder to
distinguish as the project grows.

## Revisit when

Reconsider extracting the engine only when:

- several real games consume substantially the same API;
- the engine has a stable release and compatibility policy;
- repository separation solves a demonstrated maintenance problem.
