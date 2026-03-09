# Rectangle: A Python Module for Rectangles, Colors, and Rendering Systems

Rectangle is a versatile Python module designed for managing rectangles, colors, and rendering systems. It provides high-level abstractions for working with graphical elements in both **Pygame** and **Tkinter**, making it suitable for a variety of use cases, such as physics simulations, UI layouts, and more.

---

## Features

- **Pygame Integration**:
  - Create and render rectangles with physics properties.
  - Premade physics-enabled boxes for rapid prototyping.
  - High-performance rendering with optional detailed surfaces.

- **Tkinter Integration**:
  - Responsive layouts with grid, row, and column systems.
  - Canvas-based rendering for custom widgets.
  - Easy-to-use adapters for integrating with Tkinter's grid layout.

- **Core Utilities**:
  - Flexible `Rect` and `Color` classes for managing geometry and colors.
  - Support for vector operations, collision detection, and transformations.

---

## Installation

To use this module, clone the repository and ensure you have Python 3.10 or higher installed. Install the required dependencies:

```bash
pip install pygame
```

---

## Usage

### Pygame Example

```python
from Rectangle import pygame_phys_premade as rtngle_phys_premade
from Rectangle import Rect, Color
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = Color(255, 255, 255)
ORANGE = Color(255, 125, 0)

box = rtngle_phys_premade.Box(
    surface=screen, 
    rect=Rect(10, 10, 50, 50), 
    color=ORANGE, 
    use_detail=False
)

active = True
while active:
    dt = clock.tick(60.0) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        box.handle_event(event)
    pressed_keys = pygame.key.get_pressed()
    screen.fill(WHITE)

    box.update(pressed_keys, dt)
    box.render()

    pygame.display.flip()

pygame.quit()
sys.exit()
```

### Tkinter Example

```python
import tkinter as tk
from Rectangle import tkinter as rtngle_tk
from Rectangle import Rect

root = tk.Tk()
adapter = rtngle_tk.RectGridAdapter(root)
matrix = rtngle_tk.RootMatrix()

layout = rtngle_tk.GridLayout(matrix, rows=3, cols=3, spacing=6)

header_root = rtngle_tk.CanvasRoot(root, Rect(0, 0, 200, 60))
header = rtngle_tk.RectBox().prepare(header_root)

title = tk.Label(header_root.canvas, text="Rectangle UI Demo", font=("Arial", 16))
header_root.place_widget(title, Rect(10, 10, 180, 40))

layout.add(header, 0, 0, colspan=3)

rtngle_tk.bind_responsive(root, matrix, layout, adapter)
root.mainloop()
```

---

## Project Structure

```text
Rectangle/
├── __init__.py
├── core.py
├── prefab.py
├── spatial_grid.py
├── pygame.py
├── pygame_phys.py
├── pygame_phys_premade.py
├── tkinter.py
├── tkinter_pref.py
├── tkinter_surf.py
└── _internal/
    ├── core.py
    ├── prefab.py
    ├── spatial_grid.py
    ├── pygame.py
    ├── pygame_phys.py
    ├── pygame_phys_premade.py
    ├── tkinter.py
    ├── tkinter_perf.py
    └── tkinter_surf.py
```

---

## License

This project is licensed under the MIT License.

---

## Author

**Neo Zetterberg**  
Feel free to reach out for any questions or contributions!

---

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

---

## Acknowledgments

- **Pygame**: For providing a powerful library for game development.
- **Tkinter**: For enabling GUI development in Python.