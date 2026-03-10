from typing import Dict
import pygame

class Keybinds:
    def __init__(self, mapping: Dict[str, int]) -> None:
        self.mapping = mapping
    def sort_pressed(self, pressed_keys: pygame.key.ScancodeWrapper) -> Dict[str, bool]:
        result = {}
        for name, key in self.mapping.items():
            result[name] = pressed_keys[key]
        return result