# Graphics domain

## Responsibility

The graphics domain provides small reusable drawing and frame-animation
operations built on Pygame.

It does not define themes, colors, text content, fonts, screen layouts, or
artistic direction.

## Why this domain exists

Repeated low-level rendering operations should have one tested implementation
without forcing game presentation rules into the engine.

The domain remains intentionally small. A drawing helper is added only when a
concrete game-owned presentation need demonstrates its usefulness.

## Public components

### [`draw_text`](../api/graphics.md#my_first_adventure_game.engine.graphics.draw_text)

Renders antialiased text with a supplied font and RGB color.

The rendered text is centered on the supplied position, drawn onto the target
surface, and its destination rectangle is returned.

Returning the rectangle allows callers to position later elements or inspect
the occupied area without rendering the text again.

### [`Animation`](../api/graphics.md#my_first_adventure_game.engine.graphics.Animation)

Advances a non-empty sequence of Pygame surfaces at a fixed positive frame
duration.

The animation starts on its first frame, preserves partial elapsed time between
updates, advances across every frame covered by a long update, and loops after
its final frame. Resetting it restores both the first frame and the initial
timing state.

## Ownership

The engine owns:

- rendering the text surface;
- centering its rectangle;
- drawing it onto the target surface.
- frame timing and selection for a looping animation.

The game owns:

- text content;
- fonts and font sizes;
- colors;
- positions;
- layout and visual hierarchy.
- concrete animation frames and speeds;
- visual state names and the rules that switch between animations.

## Invariants

- Text rendering uses antialiasing.
- The supplied center determines the destination rectangle.
- The returned rectangle is the rectangle used for drawing.
- The helper does not read global theme or application state.
- An animation contains at least one frame.
- Frame duration is strictly positive.
- Partial elapsed time is preserved between updates.
- Looping remains correct when one update spans multiple frames.
- Resetting clears both the selected frame and accumulated time.

## Extension points

Future requirements may justify additional alignment, opacity, wrapping, or
layout helpers. Concrete consumers may also justify non-looping animations,
per-frame durations, or completion reporting.

These capabilities must not be added until a concrete consumer defines their
semantics.

## Change risks

Changing alignment or return semantics would affect every caller's layout.

Adding game-owned presentation defaults would couple cloned games to the
current artistic direction.

Adding animation state names or transition rules to the engine would couple
the mechanism to concrete game behavior. Changing elapsed-time handling could
make animation speed depend on frame rate or discard timing information after
a slow frame.
