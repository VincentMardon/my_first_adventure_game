# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A searchable MkDocs documentation site with Material navigation and Mermaid
  diagram rendering.
- A generated public API reference backed by mkdocstrings and source docstrings.
- Direct links between architectural component descriptions and generated API
  contracts.
- Strict documentation builds in the local verification workflow and GitHub
  Actions CI.
- Consistent Markdown formatting enforced locally and in GitHub Actions CI.
- Automatic API page discovery and generation from public package entry points.
- Floating-point AABB geometry with positive-area overlap detection.
- Lightweight spatial entities with stable identifiers and mutable geometry.
- Deterministic world registration and entity lookup.
- Axis-separated movement that prevents crossing solid AABB obstacles.
- A concrete gameplay scene with normalized player movement and collision-aware
  wall handling.
- A game-owned Python-authored demo map with concrete player, wall, and
  collectible roles.
- Collectible objects that disappear when the player overlaps them.
- Immutable `ItemCollected` facts delivered once through an explicit gameplay
  callback.
- A game-owned rule awarding 100 points for each collected item.
- A mutable session score accumulated through the collection event handler.
- A gameplay score display using the shared font cache and text renderer.
- Reusable looping and one-shot frame animations driven by elapsed time.
- Game-owned temporary idle and movement animations selected from directional
  input.
- A one-shot player collection animation with priority over idle and movement
  presentation.
- A game-owned attack action bound to Space.
- A destructible obstacle removed by a proximity attack and excluded from later
  collision and rendering.
- Immutable `ObstacleDestroyed` facts delivered once through an explicit
  gameplay callback.
- A one-shot player attack animation with priority over idle and movement
  presentation.
- A stationary game-owned enemy that blocks movement while active and is
  defeated by a nearby attack.
- Immutable `EnemyDefeated` facts delivered once through an explicit gameplay
  callback.
- A game-owned `Enemy` that composes reusable spatial state with validated,
  mutable health.
- One-point player attack damage requiring two hits to defeat the demo enemy.
- Brief color feedback after non-fatal enemy damage.
- A game-owned `Player` that composes reusable spatial state with validated,
  mutable health.
- Enemy contact damage with temporary player invulnerability between hits.
- A gameplay health display and an inactive player state after fatal damage.
- Immutable `PlayerDefeated` facts delivered once through an explicit gameplay
  callback.
- A game-owned defeat scene displaying the final score after an explicit
  `PlayerDefeated` transition.
- Confirmation-driven navigation from defeat back to the title.
- Fresh map, score, animation, gameplay, and defeat state for every new game.
- A game-owned victory scene displayed after every enemy on the current map is
  defeated.
- Final score display and confirmation-driven return to the title after
  victory.
- A game-owned pause action bound to Escape.
- An opaque pause scene that suspends gameplay and explicitly resumes the same
  session without a scene stack.
- A confirmation action bound to Enter.
- An explicit title-to-gameplay transition composed in `game.main`.
- Architecture documentation for collisions, world representation, game levels,
  and the playable runtime composition.
- Package-based image and font loading through `importlib.resources`.
- Instance-local image caching and size-aware font caching.
- Minimal centered and antialiased text rendering.
- Title screen rendering with a cached Pygame font.
- Public API docstrings for the existing engine and game foundations.
- Architecture documentation, decision records, and guidance for AI agents.
- Initial Python project structure with separate `engine` and `game` packages.
- Pygame application entry point and immutable window configuration.
- Generic application loop with delta-time calculation.
- Decoupled scene contract and scene manager with explicit transitions.
- Minimal game-owned title scene.
- Generic action-to-key bindings independent of concrete game actions.
- Per-frame pressed, held, and released action states.
- Support for multiple keys per action and multiple actions per key.
- Normalized directional movement axes.
- Default directional game actions bound to the arrow keys.
- Automated tests, Ruff quality checks, package builds, and GitHub Actions CI.
