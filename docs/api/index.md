# API reference

This reference documents the public Python interfaces exposed by the engine and
game packages.

Domain pages are generated during each MkDocs build from public package entry
points and their docstrings. A domain is included when its package
`__init__.py` defines a non-empty `__all__`.

The API reference explains available contracts and signatures. The architecture
pages remain the authoritative source for responsibilities, relationships,
design decisions, and change risks.

## Engine domains

- [Application](application.md)
- [Assets](assets.md)
- [Collisions](collisions.md)
- [Graphics](graphics.md)
- [Input](input.md)
- [Scenes](scenes.md)
- [World](world.md)
- [Persistence](persistence.md)

## Game domains

- [Events](game-events.md)
- [Input](game-input.md)
- [Levels](game-levels.md)
- [Scenes](game-scenes.md)
- [Scoring](game-scoring.md)
- [Statistics](game-statistics.md)
- [Progression](game-progression.md)
- [Profile](game-profile.md)
