with open('k40_gui.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

create_widgets_end = 0
for i, l in enumerate(lines):
    if 'def Master_Configure' in l:
        create_widgets_end = i - 1
        break

layout_code = """
        # --- STATIC LAYOUT ---
        row = 0
        self.Initialize_Button.grid(row=row, column=0, columnspan=2, sticky="ew", pady=5)
        self.Initialize_Button.configure(bootstyle=PRIMARY)
        
        row += 1
        self.Open_Button.grid(row=row, column=0, sticky="ew", padx=(0,2))
        self.Reload_Button.grid(row=row, column=1, sticky="ew", padx=(2,0))
        
        row += 1
        self.pos_frame = ttk.Labelframe(self.LeftPanel, text="Position Controls")
        self.pos_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10, ipadx=5, ipady=5)
        
        self.Home_Button.grid(in_=self.pos_frame, row=0, column=0, sticky="ew", padx=2)
        self.UnLock_Button.grid(in_=self.pos_frame, row=0, column=1, sticky="ew", padx=2)
        
        self.Label_Step.grid(in_=self.pos_frame, row=1, column=0, pady=5)
        self.Entry_Step.grid(in_=self.pos_frame, row=1, column=1, pady=5)
        
        self.dpad_frame = ttk.Frame(self.pos_frame)
        self.dpad_frame.grid(row=2, column=0, columnspan=2, pady=5)
        self.Up_Button.grid(in_=self.dpad_frame, row=0, column=1)
        self.Left_Button.grid(in_=self.dpad_frame, row=1, column=0)
        self.CC_Button.grid(in_=self.dpad_frame, row=1, column=1)
        self.Right_Button.grid(in_=self.dpad_frame, row=1, column=2)
        self.Down_Button.grid(in_=self.dpad_frame, row=2, column=1)
        
        self.GoTo_Button.grid(in_=self.pos_frame, row=3, column=0, columnspan=2, sticky="ew", pady=5)
        
        row += 1
        self.eng_frame = ttk.Labelframe(self.LeftPanel, text="Engraving & Cutting Parameters")
        self.eng_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10, ipadx=5, ipady=5)
        
        self.Reng_Button.grid(in_=self.eng_frame, row=0, column=0, sticky="ew", pady=2)
        self.Entry_Reng_feed.grid(in_=self.eng_frame, row=0, column=1, pady=2, padx=2)
        
        self.Veng_Button.grid(in_=self.eng_frame, row=1, column=0, sticky="ew", pady=2)
        self.Entry_Veng_feed.grid(in_=self.eng_frame, row=1, column=1, pady=2, padx=2)
        
        self.Vcut_Button.grid(in_=self.eng_frame, row=2, column=0, sticky="ew", pady=2)
        self.Entry_Vcut_feed.grid(in_=self.eng_frame, row=2, column=1, pady=2, padx=2)
        
        row += 1
        self.Stop_Button.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        self.Stop_Button.configure(bootstyle=DANGER)
"""

# Now we need to remove the layout code from Master_Configure
new_master_configure = """    def Master_Configure(self, event, update=0):
        if getattr(self, 'master', None) and event.widget != self.master:
            return
            
        x = int(self.master.winfo_x())
        y = int(self.master.winfo_y())
        if (self.x, self.y) == (-1,-1):
            self.x, self.y = x,y
"""

lines.insert(create_widgets_end, layout_code)

# Remove the old Master_Configure lines
master_conf_start = -1
for i, l in enumerate(lines):
    if 'def Master_Configure' in l:
        master_conf_start = i
        break

if master_conf_start != -1:
    del lines[master_conf_start:]
    lines.append(new_master_configure)

with open('k40_gui.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
