# Graphics domain

## Responsibility

The graphics domain provides small reusable drawing operations built on
Pygame.

It does not define themes, colors, text content, fonts, screen layouts, or
artistic direction.

## Why this domain exists

Repeated low-level rendering operations should have one tested implementation
without forcing game presentation rules into the engine.

The domain remains intentionally small. A drawing helper is added only when a
concrete game-owned presentation need demonstrates its usefulness.

## Public components

### `draw_text`

Renders antialiased text with a supplied font and RGB color.

The rendered text is centered on the supplied position, drawn onto the target
surface, and its destination rectangle is returned.

Returning the rectangle allows callers to position later elements or inspect
the occupied area without rendering the text again.

## Ownership

The engine owns:

- rendering the text surface;
- centering its rectangle;
- drawing it onto the target surface.

The game owns:

- text content;
- fonts and font sizes;
- colors;
- positions;
- layout and visual hierarchy.

## Invariants

- Text rendering uses antialiasing.
- The supplied center determines the destination rectangle.
- The returned rectangle is the rectangle used for drawing.
- The helper does not read global theme or application state.

## Extension points

Future requirements may justify additional alignment, opacity, wrapping, or
layout helpers.

These capabilities must not be added until a concrete consumer defines their
semantics.

## Change risks

Changing alignment or return semantics would affect every caller's layout.

Adding game-owned presentation defaults would couple cloned games to the
current artistic direction.