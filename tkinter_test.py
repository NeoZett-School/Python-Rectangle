import tkinter as tk
from Rectangle import tkinter as rtngle_tk
from Rectangle import Rect

root = tk.Tk()
adapter = rtngle_tk.RectGridAdapter(root)
matrix = rtngle_tk.RootMatrix()

layout = rtngle_tk.GridLayout(matrix, rows=3, cols=3, spacing=6)

# Header

header_root = rtngle_tk.CanvasRoot(root, Rect(0, 0, 200, 60))
header = rtngle_tk.RectBox().prepare(header_root)

title = tk.Label(header_root.canvas, text="Rectangle UI Demo", font=("Arial", 16))
header_root.place_widget(title, Rect(10, 10, 180, 40))

# Content

content_root = rtngle_tk.CanvasRoot(root, Rect(0, 0, 200, 200))
content = rtngle_tk.RectBox().prepare(content_root)

content_layout = rtngle_tk.RowLayout(content_root.matrix) # This is the nested layout

btn1 = rtngle_tk.RectBox().prepare(tk.Button(content_root.canvas, text="Button A")) # We cannot really specify size here no longer?
btn2 = rtngle_tk.RectBox().prepare(tk.Button(content_root.canvas, text="Button B"))

content_layout.add(btn1,1)
content_layout.add(btn2,1)

content_root.set_layout(content_layout)

# Footer

footer_root = rtngle_tk.CanvasRoot(root, Rect(0, 0, 200, 40))
footer = rtngle_tk.RectBox().prepare(footer_root)

close_button = tk.Button(footer_root.canvas, text="Close", command=root.quit)
footer_root.place_widget(close_button, Rect(10, 5, 80, 3))

# Layout

layout.add(header, 0, 0, colspan=3)
layout.add(content, 1, 0, colspan=3)
layout.add(footer, 2, 0, colspan=3)

layout.set_row_weight(1, 4)   # Content expands more
layout.set_row_weight(0, 1)
layout.set_row_weight(2, 1)

# Binding

rtngle_tk.bind_responsive(root, matrix, layout, adapter) # We must resize the window to work as it should if we specify size in RootMatrix!

root.mainloop()