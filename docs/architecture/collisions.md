# Collisions domain

## Responsibility

The collisions domain provides reusable geometric facts for axis-aligned
collision detection.

It currently defines floating-point bounds and overlap detection.

It does not decide whether an overlap blocks movement, causes damage, triggers
an interaction, or changes game state.

## Why this domain exists

`pygame.Rect` stores integer coordinates and would truncate smooth
floating-point movement.

The installed Pygame distribution does not provide `FRect`. The engine
therefore owns a small floating-point representation limited to the geometry
required by top-down movement.

## Public components

### [`AABB`](../api/collisions.md#my_first_adventure_game.engine.collisions.AABB)

Represents immutable axis-aligned bounds using a position and dimensions.

It exposes the left, right, top, and bottom edges and can determine whether two
bounds share a positive area.

## Overlap semantics

- Bounds that share a positive area overlap.
- Bounds that only touch by an edge or corner do not overlap.
- Bounds with zero width or height do not overlap.
- Negative dimensions are invalid.
- Overlap detection is symmetric.

These rules allow an entity to rest against an obstacle without already being
considered inside it.

## Ownership

The engine owns geometric detection.

The game decides the consequence of a detected overlap, such as blocking
movement, collecting an item, taking damage, or triggering an event.

## Dependencies

The collisions domain currently depends only on the Python standard library.

The world domain uses `AABB` values for axis-separated movement resolution.

## Extension points

Additional shapes, realistic physics, polygonal collisions, and a general
physics engine are outside the current scope.

## Change risks

Changing contact or zero-area semantics would alter movement and collision
resolution throughout the engine.

Making bounds mutable would allow cached or shared geometric snapshots to
change unexpectedly.