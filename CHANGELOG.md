# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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