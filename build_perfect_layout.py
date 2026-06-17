import re

with open('k40_gui.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Find the start and end of the static layout block
start_marker = "# --- STATIC LAYOUT ---"
end_marker = "def Master_Configure("

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find layout block markers.")
    exit(1)

new_layout = """# --- STATIC LAYOUT ---
        # Ensure LeftPanel has some padding to match the mockup sidebar
        self.LeftPanel.configure(padding=15)
        
        row = 0
        # Main Initialize Button
        self.Initialize_Button.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipadx=10, ipady=10)
        self.Initialize_Button.configure(bootstyle="primary")
        
        row += 1
        # File operations
        file_frame = ttk.Frame(self.LeftPanel)
        file_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        file_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(1, weight=1)
        self.Open_Button.grid(in_=file_frame, row=0, column=0, sticky="ew", padx=(0,5), ipady=5)
        self.Reload_Button.grid(in_=file_frame, row=0, column=1, sticky="ew", padx=(5,0), ipady=5)
        
        row += 1
        # Position Controls
        self.pos_frame = ttk.Labelframe(self.LeftPanel, text=" Position Controls ")
        self.pos_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipadx=10, ipady=10)
        self.pos_frame.columnconfigure(0, weight=1)
        self.pos_frame.columnconfigure(1, weight=1)
        
        self.Home_Button.grid(in_=self.pos_frame, row=0, column=0, sticky="ew", padx=(0,5), pady=(0,10), ipady=5)
        self.UnLock_Button.grid(in_=self.pos_frame, row=0, column=1, sticky="ew", padx=(5,0), pady=(0,10), ipady=5)
        
        # Jog Step
        step_frame = ttk.Frame(self.pos_frame)
        step_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0,10))
        self.Label_Step.grid(in_=step_frame, row=0, column=0, sticky="w", padx=(0,10))
        self.Entry_Step.grid(in_=step_frame, row=0, column=1, sticky="ew")
        self.Entry_Step.configure(width=8)
        ttk.Label(step_frame, text="mm").grid(row=0, column=2, sticky="w", padx=(5,0))
        step_frame.columnconfigure(1, weight=1)
        
        # D-Pad
        self.dpad_frame = ttk.Frame(self.pos_frame)
        self.dpad_frame.grid(row=2, column=0, columnspan=2, pady=(10,15))
        self.Up_Button.grid(in_=self.dpad_frame, row=0, column=1, pady=(0,2))
        self.Left_Button.grid(in_=self.dpad_frame, row=1, column=0, padx=(0,2))
        self.CC_Button.grid(in_=self.dpad_frame, row=1, column=1)
        self.Right_Button.grid(in_=self.dpad_frame, row=1, column=2, padx=(2,0))
        self.Down_Button.grid(in_=self.dpad_frame, row=2, column=1, pady=(2,0))
        
        # Move To
        goto_frame = ttk.Frame(self.pos_frame)
        goto_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.GoTo_Button.grid(in_=goto_frame, row=0, column=0, sticky="w", padx=(0,10))
        ttk.Label(goto_frame, text="X:").grid(row=0, column=1)
        self.Entry_GoToX.grid(in_=goto_frame, row=0, column=2, padx=2)
        self.Entry_GoToX.configure(width=6)
        ttk.Label(goto_frame, text="Y:").grid(row=0, column=3)
        self.Entry_GoToY.grid(in_=goto_frame, row=0, column=4, padx=2)
        self.Entry_GoToY.configure(width=6)
        
        row += 1
        # Engraving & Cutting Parameters
        self.eng_frame = ttk.Labelframe(self.LeftPanel, text=" Engraving & Cutting Parameters ")
        self.eng_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipadx=10, ipady=10)
        self.eng_frame.columnconfigure(0, weight=1)
        
        self.Reng_Button.grid(in_=self.eng_frame, row=0, column=0, sticky="ew", pady=2)
        self.Entry_Reng_feed.grid(in_=self.eng_frame, row=0, column=1, pady=2, padx=(10,5))
        self.Entry_Reng_feed.configure(width=6)
        ttk.Label(self.eng_frame, text="mm/s").grid(row=0, column=2)
        
        self.Veng_Button.grid(in_=self.eng_frame, row=1, column=0, sticky="ew", pady=2)
        self.Entry_Veng_feed.grid(in_=self.eng_frame, row=1, column=1, pady=2, padx=(10,5))
        self.Entry_Veng_feed.configure(width=6)
        ttk.Label(self.eng_frame, text="mm/s").grid(row=1, column=2)
        
        self.Vcut_Button.grid(in_=self.eng_frame, row=2, column=0, sticky="ew", pady=2)
        self.Entry_Vcut_feed.grid(in_=self.eng_frame, row=2, column=1, pady=2, padx=(10,5))
        self.Entry_Vcut_feed.configure(width=6)
        ttk.Label(self.eng_frame, text="mm/s").grid(row=2, column=2)
        
        row += 1
        self.Stop_Button.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(10, 0), ipady=10)
        self.Stop_Button.configure(bootstyle="danger")
        
        # Lift all re-parented widgets
        self.Open_Button.lift()
        self.Reload_Button.lift()
        self.Home_Button.lift()
        self.UnLock_Button.lift()
        self.Label_Step.lift()
        self.Entry_Step.lift()
        self.dpad_frame.lift()
        self.Up_Button.lift()
        self.Left_Button.lift()
        self.CC_Button.lift()
        self.Right_Button.lift()
        self.Down_Button.lift()
        self.GoTo_Button.lift()
        self.Entry_GoToX.lift()
        self.Entry_GoToY.lift()
        
        self.Reng_Button.lift()
        self.Entry_Reng_feed.lift()
        self.Veng_Button.lift()
        self.Entry_Veng_feed.lift()
        self.Vcut_Button.lift()
        self.Entry_Vcut_feed.lift()

    """

text = text[:start_idx] + new_layout + text[end_idx:]

with open('k40_gui.py', 'w', encoding='utf-8') as f:
    f.write(text)
