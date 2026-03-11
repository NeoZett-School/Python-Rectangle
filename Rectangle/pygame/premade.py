"""Premade are physics objects that are already bundled up and provided with physics that would 
be even more customizable or extensible if you made yourself. Thus, premade."""

from .._internal.pygame.premade import default_keybinds, Box

__all__ = (
    "default_keybinds", "Box",
)