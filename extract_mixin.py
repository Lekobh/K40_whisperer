import os

with open('k40_whisperer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Create k40_gui.py
header = """import sys
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import *
from embedded_images import K40_Whisperer_Images

# To allow type hints or fallback if needed
# We assume ttkbootstrap is installed and K40_Whisperer_Images is available

def toplevel_dummy(): pass # we might need to mock this if it's missing, but actually it's just self.master

class K40_GUI_Mixin:
"""

# Extract methods
create_widgets_lines = lines[148:897]
master_configure_lines = lines[4330:4763]

with open('k40_gui.py', 'w', encoding='utf-8') as f:
    f.write(header)
    f.writelines(create_widgets_lines)
    f.write("\n")
    f.writelines(master_configure_lines)

# 2. Modify k40_whisperer.py
# Remove the lines (reverse order to not mess up indices)
del lines[4330:4763]
del lines[148:897]

# Inject inheritance and import
for i, l in enumerate(lines):
    if l.startswith('class Application(Frame):'):
        lines[i] = 'class Application(Frame, K40_GUI_Mixin):\n'
        break

# Inject import at the top after standard imports
for i, l in enumerate(lines):
    if l.startswith('from embedded_images import'):
        lines.insert(i + 1, 'from k40_gui import K40_GUI_Mixin\n')
        break

with open('k40_whisperer.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Extraction successful.")
