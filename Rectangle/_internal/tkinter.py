from typing import Union, Optional, Self
from .core import Rect, RectLike
import tkinter as tk

class Grid(Rect):
    def __init__(self, row: int, column: int, rowspan: int = 1, columnspan: int = 1) -> None:
        Rect.__init__(self, column, row, columnspan, rowspan)

class CanvasRoot:
    __slots__ = ("canvas", "rect", "matrix", "layout")
    def __init__(self, parent: tk.Widget, rect: Rect) -> None:
        self.rect = rect
        self.canvas = tk.Canvas(parent, highlightthickness=0)
        self.canvas.place(
            x=rect.x,
            y=rect.y,
            width=rect.width,
            height=rect.height
        )
        self.matrix = RootMatrix(rect.width, rect.height)
        self.layout = None
    @property
    def widget(self) -> tk.Canvas:
        return self.canvas
    def place_widget(self, widget: tk.Widget, rect: Rect) -> None:
        self.canvas.create_window(
            rect.x,
            rect.y,
            anchor="nw",
            width=rect.width,
            height=rect.height,
            window=widget
        )
    def set_layout(self, layout: Union["RowLayout", "ColumnLayout", "GridLayout"]) -> None:
        self.layout = layout
    def update(self) -> None:
        if not self.layout:
            return
        self.matrix.rect = Rect(0, 0, self.rect.width, self.rect.height)
        self.layout.compute()
        # remove previous widgets
        self.canvas.delete("all")
        if isinstance(self.layout, GridLayout):
            boxes = self.layout.cells.keys()
        elif isinstance(self.layout, (RowLayout, ColumnLayout)):
            boxes = [child[0] for child in self.layout.children]
        else:
            raise RuntimeError(f"Unsupported layout: {type(self.layout).__qualname__}")
        for box in boxes:
            widget = box.widget
            if widget is None:
                continue
            self.canvas.create_window(
                box.rect.x,
                box.rect.y,
                anchor="nw",
                width=box.rect.width,
                height=box.rect.height,
                window=widget.widget if isinstance(widget, CanvasRoot) else widget
            )
            if isinstance(widget, CanvasRoot):
                widget.rect = box.rect
                widget.update()

class RectGridAdapter:
    """Adapts the package Rect system to Tkinter's grid layout."""

    __all__ = ("parent",)
    def __init__(self, parent: tk.Widget) -> None:
        self.parent = parent
    def place(
        self,
        widget: tk.Widget,
        rect: Union[Rect, RectLike],
        padx: int = 0,
        pady: int = 0,
        sticky: str = "nsew"
    ) -> None:
        rect = Rect(rect)
        widget.grid(
            row=max(0, int(rect.y)),
            column=max(0, int(rect.x)),
            rowspan=max(1, int(rect.height)),
            columnspan=max(1, int(rect.width)),
            padx=padx,
            pady=pady,
            sticky=sticky
        )
    def configure_grid(self, rect: Union[Rect, RectLike], weight: int = 1) -> None:
        rect = Rect(rect)
        for r in range(int(rect.y), int(rect.y + rect.height)):
            self.parent.rowconfigure(r, weight=weight)
        for c in range(int(rect.x), int(rect.x + rect.width)):
            self.parent.columnconfigure(c, weight=weight)

class RectBox:
    __slots__ = ("rect", "widget")
    def __init__(self, row: int = 0, column: int = 0, rowspan: int = 0, columnspan: int = 0) -> None:
        self.rect = Rect(column, row, columnspan, rowspan)
        self.widget: Optional[Union[tk.Widget, CanvasRoot]] = None
    def prepare(self, widget: Union[tk.Widget, CanvasRoot]) -> Self:
        self.widget = widget
        return self

class RootMatrix:
    __slots__ = ("rect",)
    def __init__(self, width: int = 0, height: int = 0) -> None:
        self.rect = Rect(0, 0, width, height)

class RowLayout:
    __slots__ = ("matrix", "spacing", "children")
    def __init__(self, matrix: Union[RootMatrix, RectBox], spacing: int = 0) -> None:
        self.matrix = matrix
        self.spacing = spacing
        self.children = []
    def add(self, child: RectBox, weight: int = 1) -> None:
        self.children.append((child, weight))
    def compute(self) -> None:
        total_weight = sum(w for _, w in self.children)
        x, y = self.matrix.rect.topleft
        w, h = self.matrix.rect.size
        cursor = x
        for child, weight in self.children:
            width = int(w * (weight / total_weight))
            child.rect = Rect(cursor, y, width, h)
            cursor += width + self.spacing

class ColumnLayout:
    __slots__ = ("matrix", "spacing", "children")
    def __init__(self, matrix: Union[RootMatrix, RectBox], spacing: int = 0) -> None:
        self.matrix = matrix
        self.spacing = spacing
        self.children = []
    def add(self, child: RectBox, weight: int = 1) -> None:
        self.children.append((child, weight))
    def compute(self) -> None:
        total_weight = sum(w for _, w in self.children)
        x, y = self.matrix.rect.topleft
        w, h = self.matrix.rect.size
        cursor = y
        for child, weight in self.children:
            height = int(h * (weight / total_weight))
            child.rect = Rect(x, cursor, w, height)
            cursor += height + self.spacing

class GridLayout:
    __slots__ = (
        "matrix", "rows", "cols", "spacing", 
        "row_weights", "col_weights", 
        "cells"
    )
    def __init__(self, matrix: Union[RootMatrix, RectBox], rows: int, cols: int, spacing: int = 0) -> None:
        self.matrix = matrix
        self.rows = rows
        self.cols = cols
        self.spacing = spacing
        self.row_weights = [1] * rows
        self.col_weights = [1] * cols
        self.cells = {}
    def set_row_weight(self, row: int, weight: int) -> None:
        self.row_weights[row] = weight
    def set_col_weight(self, col: int, weight: int) -> None:
        self.col_weights[col] = weight
    def add(self, rectbox: RectBox, row: int, col: int, rowspan: int = 1, colspan: int = 1) -> None:
        self.cells[rectbox] = (row, col, rowspan, colspan)
    def compute(self) -> None:
        x, y = self.matrix.rect.topleft
        w, h = self.matrix.rect.size
        total_row_weight = sum(self.row_weights)
        total_col_weight = sum(self.col_weights)
        row_heights = [
            int(h * weight / total_row_weight)
            for weight in self.row_weights
        ]
        col_widths = [
            int(w * weight / total_col_weight)
            for weight in self.col_weights
        ]
        row_positions = []
        col_positions = []
        cursor = y
        for rh in row_heights:
            row_positions.append(cursor)
            cursor += rh + self.spacing
        cursor = x
        for cw in col_widths:
            col_positions.append(cursor)
            cursor += cw + self.spacing
        for box, (row, col, rowspan, colspan) in self.cells.items():
            bx = col_positions[col]
            by = row_positions[row]
            bw = sum(col_widths[col:col+colspan])
            bh = sum(row_heights[row:row+rowspan])
            box.rect = Rect(bx, by, bw, bh)

def bind_responsive(root: tk.Widget, root_matrix: RootMatrix, layout: Union[RowLayout, ColumnLayout, GridLayout], adapter: RectGridAdapter) -> None:
    def on_resize(event=None):
        # If event is None, we are calling this manually; get size from root
        root.update_idletasks() # Force tkinter to calculate sizes
        w, h = root.winfo_width(), root.winfo_height()
        if int(w) == int(root_matrix.rect.width) and int(h) == int(root_matrix.rect.height):
            return
        root_matrix.rect = Rect(0, 0, w, h)
        layout.compute()
        if isinstance(layout, (RowLayout, ColumnLayout)):
            for child in layout.children:
                box = child[0]
                widget = box.widget
                if widget is None:
                    continue
                if isinstance(widget, CanvasRoot):
                    widget.rect = box.rect
                    widget.canvas.place(
                        x=box.rect.x,
                        y=box.rect.y,
                        width=box.rect.width,
                        height=box.rect.height
                    )
                    widget.update()  # important
                else:
                    adapter.place(widget, box.rect)
        elif isinstance(layout, GridLayout):
            for box in layout.cells:
                widget = box.widget
                if box.widget is None:
                    continue
                if isinstance(widget, CanvasRoot):
                    widget.rect = box.rect
                    widget.canvas.place(
                        x=box.rect.x,
                        y=box.rect.y,
                        width=box.rect.width,
                        height=box.rect.height
                    )
                    widget.update()  # important
                else:
                    adapter.place(widget, box.rect)
        else:
            raise RuntimeError(f"Unknown layout: '{type(layout).__qualname__}'")
    root.bind("<Configure>", on_resize)

    if root_matrix.rect.width != 0 and root_matrix.rect.height != 0:
        root.geometry(f"{int(root_matrix.rect.width)}x{int(root_matrix.rect.height)}+{int(root_matrix.rect.x)}+{int(root_matrix.rect.y)}")