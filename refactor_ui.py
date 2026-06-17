import re

with open("k40_whisperer.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update imports
imports_old = """    from tkinter import *
    from tkinter.filedialog import *
    import tkinter.messagebox
    MAXINT = sys.maxsize"""
    
imports_new = """    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    from tkinter import *
    from tkinter.filedialog import *
    import tkinter.messagebox
    MAXINT = sys.maxsize"""
code = code.replace(imports_old, imports_new)

# 2. Update root window
code = code.replace("root = Tk()", "root = ttk.Window(themename='cosmo')")

# 3. Replace Buttons
code = re.sub(r'\bButton\(', 'ttk.Button(', code)

# 4. Handle Button styles
code = code.replace("configure(bg='light coral')", "configure(bootstyle=DANGER)")
code = code.replace("configure(bg='light green')", "configure(bootstyle=SUCCESS)")

# Add PRIMARY style to Initialize Button
code = code.replace(
    'self.Initialize_Button = ttk.Button(self.master,text="Initialize Laser Cutter", command=self.Initialize_Laser)',
    'self.Initialize_Button = ttk.Button(self.master,text="Initialize Laser Cutter", command=self.Initialize_Laser, bootstyle=PRIMARY)'
)

# 5. Fix any Checkbuttons (optional, leaving as is might be safer)
# code = re.sub(r'\bCheckbutton\(', 'ttk.Checkbutton(', code)

with open("k40_whisperer.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Refactor script completed successfully.")
