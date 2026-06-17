import re

with open('k40_gui.py', 'r', encoding='utf-8') as f:
    original_code = f.read()

# Split into variables, widgets, menu, master_configure
parts = original_code.split('# make a Status Bar')
part1 = parts[0] # up to status bar

parts2 = parts[1].split('# Make Menu Bar')
part2 = '# make a Status Bar' + parts2[0] # widgets
part3 = '# Make Menu Bar' + parts2[1].split('    def Master_Configure')[0] # menus

master_configure_old = '    def Master_Configure' + parts2[1].split('    def Master_Configure')[1]

# 1. Modify part2 to use ttk and LeftPanel parent
part2_new = part2.replace('Label(self.master', 'ttk.Label(self.master')
part2_new = part2_new.replace('Button(self.master', 'ttk.Button(self.LeftPanel')
part2_new = part2_new.replace('Entry(self.master', 'ttk.Entry(self.LeftPanel')
part2_new = part2_new.replace('Checkbutton(self.master', 'ttk.Checkbutton(self.LeftPanel')
part2_new = part2_new.replace('Radiobutton(self.master', 'ttk.Radiobutton(self.LeftPanel')

# The canvas stays in self.master
part2_new = part2_new.replace('self.PreviewCanvas_frame = lbframe', 'self.PreviewCanvas_frame = ttk.Frame(self.master)')
part2_new = part2_new.replace('Canvas(lbframe', 'Canvas(self.PreviewCanvas_frame')

# Add LeftPanel creation at the start of part2
left_panel_init = """
        # --- UI LAYOUT REWRITE ---
        self.LeftPanel = ttk.Frame(self.master, padding=10)
        self.LeftPanel.pack(side=LEFT, fill=Y)
        
        self.PreviewCanvas_frame = ttk.Frame(self.master)
        self.PreviewCanvas_frame.pack(side=LEFT, fill=BOTH, expand=True)
        # -------------------------
"""
part2_new = left_panel_init + part2_new

# Inject new Master_Configure
new_master_configure = """    def Master_Configure(self, event, update=0):
        if event.widget != self.master:
            return
            
        x = int(self.master.winfo_x())
        y = int(self.master.winfo_y())
        w = int(self.master.winfo_width())
        h = int(self.master.winfo_height())
        if (self.x, self.y) == (-1,-1):
            self.x, self.y = x,y
            
        # Re-layout the widgets using grid inside LeftPanel
        
        row = 0
        self.Initialize_Button.grid(row=row, column=0, columnspan=2, sticky="ew", pady=5)
        self.Initialize_Button.configure(bootstyle=PRIMARY)
        
        row += 1
        self.Open_Button.grid(row=row, column=0, sticky="ew", padx=(0,2))
        self.Reload_Button.grid(row=row, column=1, sticky="ew", padx=(2,0))
        
        row += 1
        pos_frame = ttk.LabelFrame(self.LeftPanel, text="Position Controls", padding=5)
        pos_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.Home_Button.grid(in_=pos_frame, row=0, column=0, sticky="ew", padx=2)
        self.UnLock_Button.grid(in_=pos_frame, row=0, column=1, sticky="ew", padx=2)
        
        self.Label_Step.grid(in_=pos_frame, row=1, column=0, pady=5)
        self.Entry_Step.grid(in_=pos_frame, row=1, column=1, pady=5)
        
        dpad_frame = ttk.Frame(pos_frame)
        dpad_frame.grid(row=2, column=0, columnspan=2, pady=5)
        self.Up_Button.grid(in_=dpad_frame, row=0, column=1)
        self.Left_Button.grid(in_=dpad_frame, row=1, column=0)
        self.CC_Button.grid(in_=dpad_frame, row=1, column=1)
        self.Right_Button.grid(in_=dpad_frame, row=1, column=2)
        self.Down_Button.grid(in_=dpad_frame, row=2, column=1)
        
        self.GoTo_Button.grid(in_=pos_frame, row=3, column=0, columnspan=2, sticky="ew", pady=5)
        
        row += 1
        eng_frame = ttk.LabelFrame(self.LeftPanel, text="Engraving & Cutting Parameters", padding=5)
        eng_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.Reng_Button.grid(in_=eng_frame, row=0, column=0, sticky="ew", pady=2)
        self.Entry_Reng_feed.grid(in_=eng_frame, row=0, column=1, pady=2, padx=2)
        
        self.Veng_Button.grid(in_=eng_frame, row=1, column=0, sticky="ew", pady=2)
        self.Entry_Veng_feed.grid(in_=eng_frame, row=1, column=1, pady=2, padx=2)
        
        self.Vcut_Button.grid(in_=eng_frame, row=2, column=0, sticky="ew", pady=2)
        self.Entry_Vcut_feed.grid(in_=eng_frame, row=2, column=1, pady=2, padx=2)
        
        row += 1
        self.Stop_Button.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        self.Stop_Button.configure(bootstyle=DANGER)
"""

with open('k40_gui.py', 'w', encoding='utf-8') as f:
    f.write(part1)
    f.write(part2_new)
    f.write(part3)
    f.write(new_master_configure)

print("GUI patched successfully.")
