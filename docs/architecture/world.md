# World domain

## Responsibility

The world domain provides the minimal spatial state shared by entities in a
top-down game world.

It currently defines a lightweight entity representation and a deterministic
entity container.

It does not yet provide movement resolution, maps, or gameplay behavior.

## Why this domain exists

World objects need a common spatial representation before collision detection
and movement can operate independently from concrete player, enemy, item, or
obstacle classes.

This representation remains deliberately smaller than an entity-component
system.

## Public components

### `Entity`

Stores:

- a stable string identifier;
- a floating-point position;
- a floating-point size;
- an active state.

Position and size are copied during construction so the entity does not share
the caller's mutable vectors.

The identifier is exposed without a public setter. Position, size, and active
state remain mutable.

### `Entity.bounds`

Creates an immutable `AABB` snapshot from the current position and size.

Later changes to the entity do not mutate bounds returned previously.

### `World`

Owns entities indexed by stable identifier.

It provides:

- registration without silent replacement;
- optional lookup by identifier;
- an ordered tuple snapshot of registered entities.

Entity order follows registration order. Requesting an unknown identifier
returns `None`.

## Ownership

The engine owns common spatial state.

The game owns:

- concrete player, enemy, item, and obstacle types;
- entity behavior;
- rendering and animation;
- combat and interaction rules;
- reasons for activating or deactivating an entity.

## Dependencies

The world domain depends on:

- Pygame for floating-point vectors;
- the collisions domain for immutable bounds.

The dependency direction is:

`world` depends on `collisions`.

The collisions domain must not import the world domain.

## Invariants

- Entity identifiers cannot be reassigned through the public API.
- Initial position and size vectors are copied.
- Bounds reflect the current entity geometry.
- Bounds are immutable snapshots.
- Entity state contains no game-specific behavior.
- Registered entity identifiers are unique.
- Duplicate registration leaves the original entity unchanged.
- Entity snapshots cannot mutate the world's internal registry.
- Entity iteration follows registration order.

## Extension points

The accepted roadmap includes:

- movement against solid obstacles.

Component registries, dynamic component attachment, and general-purpose ECS
queries are outside the current scope.

## Change risks

Making identifiers mutable would break stable lookup in `World`.

Sharing input vectors would allow external code to move or resize an entity
without going through its owned state.

Adding concrete behavior would couple the engine to the current game.