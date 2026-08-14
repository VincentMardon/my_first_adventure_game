# Architecture overview

## Purpose

My First Adventure Game has two related goals:

1. build a small reusable engine for top-down 2D games with Pygame;
2. build a complete game that exercises the engine through real requirements.

The engine is internal to the repository. It is specialized for small adventure
games and is not intended to be a universal game engine.

## Fundamental separation

The source code is divided into two main areas:

### `engine`

Provides reusable technical capabilities independent of game rules and
content.

The engine must not know:

- concrete game actions;
- player profiles or statistics;
- scoring rules;
- game text or localization keys;
- game colors or artistic direction;
- concrete levels, entities, or combat rules.

### `game`

Defines the concrete application assembled from engine capabilities.

The game owns:

- concrete actions and default controls;
- scenes specific to the game;
- visual presentation;
- entities and levels;
- scoring and progression;
- localization;
- profile data and gameplay rules.

The dependency direction is always:

```text
game → engine
```

The engine must never import the game.

## Implemented domains

### Application

Owns the Pygame lifecycle, window creation, frame timing, event dispatch, scene
updates, rendering, and shutdown.

### Scenes

Defines the scene contract and manages the active scene.

A scene represents a global application state, such as a title screen,
gameplay, pause, results, or profile.

A map represents spatial content loaded by a gameplay scene. A map is not a
scene.

### Input

Converts device events into game-independent action states.

The engine tracks whether an action was pressed, held, or released during the
current frame. Concrete action names and default keys belong to the game.

### Assets

Loads and caches Pygame images and fonts stored in Python packages.

The engine owns package-based loading and caching. Concrete resource files,
paths, sizes, themes, and presentation decisions belong to the game.

### Graphics

Provides small tested drawing operations without owning game presentation
rules.

The current implementation renders centered antialiased text, returns its
destination rectangle, and advances looping or one-shot image-frame animations
using elapsed time.

### Collisions

Provides immutable floating-point axis-aligned bounds and positive-area overlap
detection.

The engine reports geometric overlap. The game decides its consequences.

### World

Provides lightweight entities with stable identity, floating-point geometry,
active state, deterministic lookup, and axis-separated movement against
immutable collision bounds.

Concrete entity types, solid obstacle selection, and behavior belong to the
game.

## Implemented game foundations

### Entities

Defines concrete gameplay objects that compose reusable engine entities.

The current `Enemy` and `Player` own mutable integer health, apply positive
damage, deactivate their spatial entities on the fatal hit, and report whether
that hit caused the defeat. `NPC` composes the same reusable spatial state with
a game-owned display name and ordered dialogue lines.

### Events

Defines immutable facts produced by concrete gameplay behavior.

The current `ItemCollected`, `ObstacleDestroyed`, `EnemyDefeated`, and
`PlayerDefeated` events identify concrete gameplay facts without deciding their
consequences.

### Scoring

Defines concrete game-owned point rules and the mutable score for the current
session.

An item collection currently awards 100 points. `game.main` converts each
`ItemCollected` fact into points, accumulates them in `SessionScore`, and shares
that score with `GameplayScene` for display.

### Progression

Owns the session-local state and status text of the Guide's concrete collection
objective.

The objective starts before activation, becomes active after the first Guide
interaction, becomes ready after every requested item is collected, and is
completed when the player returns to the Guide. The transitions remain
game-owned: `GuideObjective` records them, while `game.main` decides when they
occur and what they change in the world. `GameplayScene` only reads the current
status for display. This is not a generic engine quest system.

### Scenes

Provides the concrete title, gameplay, pause, dialogue, defeat, and victory
scenes.

The title scene requests an explicit transition to gameplay when the
confirmation action is pressed.

The gameplay scene converts game actions into player movement, selects active
walls, enemies, and NPCs as solid obstacles, opens dialogue for a nearby active
NPC when interaction is requested, deactivates collectibles overlapping the
player, destroys nearby destructible obstacles and defeats nearby enemies when
attacking, emits factual events,
prioritizes one-shot collection and attack animations over movement and idle
presentation, applies contact damage with temporary player invulnerability,
and displays the current session score and player health.

The defeat scene displays the final session score after player defeat and
requests an explicit return to the title when confirmation is pressed. Starting
again constructs a fresh session rather than resetting the previous objects.

The victory scene displays the final session score after every enemy on the
current map is inactive and provides the same explicit return to the title.

The opaque pause scene temporarily replaces gameplay when Escape is pressed.
Because only the active scene is updated, gameplay time and animation stop. A
second press explicitly restores the same gameplay scene and session state.

The opaque dialogue scene presents the selected NPC's name and ordered lines
one at a time inside a game-owned bordered panel. Long content is measured with
the selected font, wrapped at word boundaries, and given additional panel
height without changing the original NPC line. Confirmation advances the
dialogue, then explicitly restores the same gameplay scene and session state
after the final line.

### Levels

Defines the first Python-authored game map.

`GameMap` groups the reusable world representation with the concrete player,
wall, enemy, NPC, destructible obstacle, and collectible roles owned by the
game.
`create_demo_map()` defines their initial geometry and registration order.

## Reserved domains

The package skeleton also reserves locations for capabilities that have not yet
been implemented:

- persistence;
- profiles;
- localization.

Reserved packages communicate intended organization, not completed features.

## Runtime composition

The game entry point creates the concrete objects and connects them together.
The composition is split below into three focused views so that each diagram
answers one architectural question.

### Application and scene composition

```mermaid
flowchart TD
    GameMain["game.main"]
    Application["Application"]
    WindowConfig["WindowConfig"]
    InputProcessor["InputProcessor"]
    InputState["InputState"]
    KeyboardBindings["KeyboardBindings"]
    SceneManager["SceneManager"]
    Scene["Scene"]
    TitleScene["TitleScene"]
    GameplayScene["GameplayScene"]
    PauseScene["PauseScene"]
    DialogueScene["DialogueScene"]
    DefeatScene["DefeatScene"]
    VictoryScene["VictoryScene"]

    GameMain --> Application
    GameMain --> InputState
    GameMain --> SceneManager
    GameMain -->|"injects transition callback"| TitleScene
    GameMain -->|"creates per session"| GameplayScene
    GameMain -->|"creates per session"| PauseScene
    GameMain -->|"creates on interaction"| DialogueScene
    GameMain -->|"creates per session"| DefeatScene
    GameMain -->|"creates per session"| VictoryScene

    Application --> WindowConfig
    Application --> InputProcessor
    Application --> SceneManager

    TitleScene --> InputState
    GameplayScene -->|"requests pause"| PauseScene
    PauseScene --> InputState
    PauseScene -->|"requests resume"| GameplayScene
    GameplayScene -->|"requests dialogue"| DialogueScene
    DialogueScene --> InputState
    DialogueScene -->|"requests resume"| GameplayScene
    DefeatScene --> InputState
    DefeatScene -->|"requests return"| TitleScene
    VictoryScene --> InputState
    VictoryScene -->|"requests return"| TitleScene

    InputState -. "implements structurally" .-> InputProcessor
    InputState --> KeyboardBindings
    SceneManager --> Scene
    TitleScene -. "implements" .-> Scene
    GameplayScene -. "implements" .-> Scene
    PauseScene -. "implements" .-> Scene
    DialogueScene -. "implements" .-> Scene
    DefeatScene -. "implements" .-> Scene
    VictoryScene -. "implements" .-> Scene
```

### Gameplay map composition

```mermaid
flowchart LR
    GameMain["game.main"] --> DemoMap["create_demo_map"]
    DemoMap --> GameMap["GameMap"]
    GameMap --> World["World"]
    GameMap --> Player["Player"]
    GameMap --> Enemy["Enemy"]
    GameMap --> NPC["NPC"]
    Player -->|"composes"| Entity["Entity"]
    Enemy -->|"composes"| Entity
    NPC -->|"composes"| Entity
    World -->|"stores"| Entity
    GameMain -->|"injects map roles"| GameplayScene["GameplayScene"]
```

### Gameplay collaborators and facts

```mermaid
flowchart LR
    GameMain["game.main"] --> GameplayScene["GameplayScene"]

    InputState["InputState"] --> GameplayScene
    SessionScore["SessionScore"] --> GameplayScene
    GuideObjective["GuideObjective"] -->|"provides status text"| GameplayScene
    Animation["Animation"] --> GameplayScene
    FontCache["FontCache"] --> GameplayScene
    GameplayScene --> DrawText["draw_text"]

    GameplayScene --> ItemCollected["ItemCollected"]
    GameplayScene --> ObstacleDestroyed["ObstacleDestroyed"]
    GameplayScene --> EnemyDefeated["EnemyDefeated"]
    GameplayScene --> PlayerDefeated["PlayerDefeated"]
    PlayerDefeated --> DefeatScene["DefeatScene"]
    EnemyDefeated -->|"when all enemies are inactive"| VictoryScene["VictoryScene"]

    ItemCollected --> ItemCollectionPoints["item_collection_points"]
    ItemCollectionPoints --> SessionScore
    ItemCollected --> GuideObjectiveState["GuideObjectiveState"]
    GuideObjectiveState -->|"selects Guide dialogue"| DialogueScene["DialogueScene"]
```

`game.main` creates the demo map, current `SessionScore`, temporary two-frame
idle, movement, collection, and attack animations, and a `GuideObjective` only
after the title scene requests a new game, then composes
`GameplayScene` from its gameplay entities, shared rendering services, score,
objective, animations, and explicit collection and destruction handlers.
`GameplayScene`
selects idle or
movement presentation from directional intent, gives one-shot collection
presentation priority until completion, advances and renders the selected
animation, and delivers an `ItemCollected` fact when an active collectible is
collected. A newly pressed attack deactivates a nearby active destructible
obstacle, removes it from later collision and rendering, and delivers an
`ObstacleDestroyed` fact. The same input starts a one-shot attack presentation
that has priority over movement and idle animation. An active enemy within the
same attack reach takes one point of damage. The current enemy survives the
first hit and briefly flashes with a game-owned feedback color. The second hit
deactivates its spatial entity, removes it from later collision and rendering,
and reports an `EnemyDefeated` fact.

The enemy defeat handler inspects the remaining map enemies after each factual
event. It explicitly replaces gameplay with `VictoryScene` only when all of
them are inactive. This completion rule belongs to the concrete game and may be
replaced by a different objective in a cloned project.

Contact with an active enemy removes one point of player health and starts a
short invulnerability period that prevents immediate repeated damage. Fatal
contact deactivates the player, stops later gameplay updates, and reports a
`PlayerDefeated` fact. The injected handler explicitly replaces gameplay with
`DefeatScene`, which displays the final value of the shared `SessionScore`.

When `INTERACT` is newly pressed, `GameplayScene` searches a small game-owned
area around the player for the first active NPC. A match stops the rest of that
gameplay update and passes the selected NPC to the composition root. The root
creates a fresh `DialogueScene` from its name and ordered lines. The name
remains visible as the speaker while confirmation advances one line at a time
and restores the same gameplay scene after the final line. Reopening the
dialogue starts again from the first line because the temporary index belongs
to the scene instance. This remains a concrete linear interaction flow, not an
engine dialogue system.

Confirmation on `DefeatScene` explicitly returns to the existing title scene.
The next start request constructs a new map, session score, animation set,
gameplay scene, pause scene, defeat scene, victory scene, and session-local
callbacks. Shared application services such as input state, font cache, and
scene manager remain alive.

The collection handler converts that fact through `item_collection_points()`
and adds the result to the same `SessionScore` displayed by `GameplayScene`.
It also advances the session-local Guide objective from active to ready once
every collectible is inactive.

Objective collectibles initially remain inactive. The first Guide interaction
activates them and presents the NPC's introductory lines. Further interactions
before collection finishes use a game-owned reminder. Returning after every
item is collected selects a completion message and makes the completed result
stable for later interactions. This is a concrete progression rule assembled
in `game.main`, not a reusable quest or dialogue-condition system.
The gameplay HUD reads the same objective instance and displays its current
game-owned status text without owning any transition rule.

`game.main` also injects a callback into `TitleScene` that explicitly replaces
the active scene when confirmation is pressed. It configures the shared
`FontCache` with Pygame's resource package, and both concrete scenes load their
selected fonts lazily during drawing after Pygame initialization.

## Main frame flow

For every frame, the application:

1. calculates delta time in seconds;
2. clears transient input states;
3. processes Pygame events;
4. updates the input processor before forwarding ordinary events to the scene;
5. updates the active scene;
6. asks the active scene to draw;
7. presents the completed frame.

The application handles the system-level quit event itself. It does not
interpret game actions.

## Design principle

The engine provides capabilities and reports facts. The game defines meaning
and consequences.

Current example:

- the engine reports that an action is held;
- the game decides whether that action should move a player, navigate a menu,
  or trigger another behavior.

As future domains are implemented, the same principle will apply:

- the engine will detect a collision;
- the game will decide whether it blocks movement, causes damage, or triggers
  an interaction;
- the engine will provide generic storage capabilities;
- the game will define profile schemas, statistics, and migration rules.
