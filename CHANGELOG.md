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
- Floating-point AABB geometry with positive-area overlap detection.
- Lightweight spatial entities with stable identifiers and mutable geometry.
- Deterministic world registration and entity lookup.
- Axis-separated movement that prevents crossing solid AABB obstacles.
- A concrete gameplay scene with normalized player movement and collision-aware
  wall handling.
- A game-owned Python-authored demo map with concrete player and wall roles.
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