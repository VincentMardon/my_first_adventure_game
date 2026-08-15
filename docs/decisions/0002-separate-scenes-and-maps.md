# 0002 — Separate scenes from maps

- Status: Accepted
- Date: 2026-08-05

## Context

A top-down adventure game contains both global application states and spatial
areas.

Global states include title, gameplay, pause, results, and profile screens.

Spatial areas include rooms, fields, dungeons, and other maps traversed during
gameplay.

Treating every map as a scene would mix application navigation with world
navigation and make it difficult to preserve gameplay session state across map
changes.

## Decision

A scene represents a global application state.

A map represents spatial content owned by a gameplay scene.

Changing maps does not automatically change scenes.

`SceneManager` manages the active scene. `GameplayScene` manages the current
map-owned spatial roles and replaces them explicitly through `change_map()`.

Concrete `MapExit` values identify a destination map and arrival position.
`game.main` resolves the current game's destinations, updates the shared
player position, and asks the existing gameplay scene to change maps.

## Consequences

### Positive

- One gameplay scene can preserve session state across several maps.
- Pause and results remain distinct from world navigation.
- Scene transitions stay small and explicit.
- Map loading does not require rebuilding the entire application state.
- Future overworld, dungeon, and room structures can share one gameplay scene.

### Negative

- The gameplay scene coordinates the spatial roles belonging to the active
  map.
- The composition root must resolve concrete destination identifiers.
- Developers must understand two different kinds of navigation.

## Alternatives considered

### Represent every map as a scene

Rejected because it couples spatial transitions to application state and risks
duplicating gameplay services between scenes.

### Use one scene for the entire application

Rejected because title, pause, results, and profile states have different
lifecycles and responsibilities.

### Introduce a universal state machine

Rejected because the current requirements need only explicit scene replacement
and do not justify a more general abstraction.

## Revisit when

Reconsider this decision only if a concrete game requires map transitions that
also replace the complete gameplay session and its services.

Such behavior should remain an explicit game rule rather than becoming the
default engine model.
