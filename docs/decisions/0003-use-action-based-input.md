# 0003 — Use action-based input

- Status: Accepted
- Date: 2026-08-05

## Context

Game entities should not query keyboard keys directly.

Direct key queries would couple gameplay behavior to Pygame, prevent clean
remapping, complicate testing, and require entity changes when supporting new
devices.

The project also needs frame-specific pressed, held, and released semantics and
normalized movement in eight directions.

## Decision

The engine represents input through generic action identifiers.

The engine provides:

- generic keyboard bindings;
- per-frame pressed, held, and released state;
- an input lifecycle protocol used by the application;
- normalized directional movement axes.

The game defines:

- concrete `GameAction` members;
- default keyboard bindings;
- the meaning and consequences of each action.

`Application` advances the input lifecycle and forwards ordinary events. It
does not inspect concrete actions.

Future entities will query actions rather than Pygame device state.

## Consequences

### Positive

- Gameplay logic remains independent from concrete keys.
- Bindings can be changed without modifying entities.
- Input transitions are deterministic and testable.
- Multiple keys can represent one action.
- Future devices can preserve action-oriented gameplay APIs.
- Diagonal movement has consistent speed.

### Negative

- Input requires explicit frame lifecycle management.
- Concrete actions and engine bindings require composition in the game.
- Controller and analog support are not automatically solved.
- A future read-only action-state contract may be needed for consumers.

## Alternatives considered

### Query `pygame.key.get_pressed()` from entities

Rejected because it couples entities to keyboard state and makes isolated tests
more difficult.

### Define concrete movement actions in the engine

Rejected because action names and meanings belong to the game.

### Build a universal multi-device input system immediately

Rejected because keyboard input is the only current requirement and additional
devices have not yet supplied concrete constraints.

## Revisit when

Reconsider the input architecture when implementing a real controller or analog
movement requirement.

Any revision should preserve action-oriented game code and avoid requiring
changes to player behavior solely because the physical device changed.