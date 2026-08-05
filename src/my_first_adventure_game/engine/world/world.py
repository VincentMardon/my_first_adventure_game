from my_first_adventure_game.engine.world.entity import Entity


class World:
    """Own entities and provide deterministic lookup by stable identifier."""

    __slots__ = ("_entities",)

    def __init__(self) -> None:
        self._entities: dict[str, Entity] = {}

    @property
    def entities(self) -> tuple[Entity, ...]:
        """Return an ordered snapshot of the registered entities."""
        return tuple(self._entities.values())

    def get(self, entity_id: str) -> Entity | None:
        """Return the entity registered with an identifier, if any."""
        return self._entities.get(entity_id)

    def add(self, entity: Entity) -> None:
        """Register an entity without replacing an existing identifier."""
        if entity.entity_id in self._entities:
            raise ValueError(f"Entity identifier already exists: {entity.entity_id}")

        self._entities[entity.entity_id] = entity
