import customtkinter as ctk
import tkinter as tk

# Initialize CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class SidebarTest(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter Sidebar Test")
        self.geometry("400x700")

        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        
        # --- Initialize Button ---
        self.btn_initialize = ctk.CTkButton(self.sidebar_frame, text="Initialize Laser Cutter", height=40, font=("Helvetica", 14, "bold"))
        self.btn_initialize.pack(padx=20, pady=(20, 10), fill="x")

        # --- File Buttons ---
        self.file_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.file_frame.pack(padx=20, pady=10, fill="x")
        self.file_frame.columnconfigure(0, weight=1)
        self.file_frame.columnconfigure(1, weight=1)

        self.btn_open = ctk.CTkButton(self.file_frame, text="Open\nDesign File")
        self.btn_open.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.btn_reload = ctk.CTkButton(self.file_frame, text="Reload\nDesign File")
        self.btn_reload.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # --- Position Controls ---
        self.pos_frame = ctk.CTkFrame(self.sidebar_frame)
        self.pos_frame.pack(padx=20, pady=10, fill="x")
        
        self.pos_label = ctk.CTkLabel(self.pos_frame, text="Position Controls", font=("Helvetica", 12, "bold"))
        self.pos_label.pack(pady=(10, 5))

        self.btn_home = ctk.CTkButton(self.pos_frame, text="Home")
        self.btn_home.pack(padx=10, pady=5, fill="x")
        
        self.btn_unlock = ctk.CTkButton(self.pos_frame, text="Unlock Rail")
        self.btn_unlock.pack(padx=10, pady=5, fill="x")

        self.jog_frame = ctk.CTkFrame(self.pos_frame, fg_color="transparent")
        self.jog_frame.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(self.jog_frame, text="Jog Step:").pack(side="left", padx=5)
        self.entry_step = ctk.CTkEntry(self.jog_frame, width=50)
        self.entry_step.pack(side="left", padx=5)
        self.entry_step.insert(0, "10.0")
        ctk.CTkLabel(self.jog_frame, text="mm").pack(side="left", padx=5)

        # D-pad mock
        self.dpad_frame = ctk.CTkFrame(self.pos_frame, fg_color="transparent")
        self.dpad_frame.pack(pady=10)
        
        self.btn_up = ctk.CTkButton(self.dpad_frame, text="▲", width=30, height=30)
        self.btn_up.grid(row=0, column=1, pady=2)
        
        self.btn_left = ctk.CTkButton(self.dpad_frame, text="◀", width=30, height=30)
        self.btn_left.grid(row=1, column=0, padx=2)
        
        self.btn_cc = ctk.CTkButton(self.dpad_frame, text="●", width=30, height=30, fg_color="gray")
        self.btn_cc.grid(row=1, column=1)
        
        self.btn_right = ctk.CTkButton(self.dpad_frame, text="▶", width=30, height=30)
        self.btn_right.grid(row=1, column=2, padx=2)
        
        self.btn_down = ctk.CTkButton(self.dpad_frame, text="▼", width=30, height=30)
        self.btn_down.grid(row=2, column=1, pady=2)

        # --- Parameters ---
        self.param_frame = ctk.CTkFrame(self.sidebar_frame)
        self.param_frame.pack(padx=20, pady=10, fill="x")
        
        self.param_label = ctk.CTkLabel(self.param_frame, text="Parameters", font=("Helvetica", 12, "bold"))
        self.param_label.pack(pady=(10, 5))

        self.btn_raster = ctk.CTkButton(self.param_frame, text="Raster Engrave")
        self.btn_raster.pack(padx=10, pady=5, fill="x")
        
        self.btn_vector_eng = ctk.CTkButton(self.param_frame, text="Vector Engrave", fg_color="#1f538d")
        self.btn_vector_eng.pack(padx=10, pady=5, fill="x")
        
        self.btn_vector_cut = ctk.CTkButton(self.param_frame, text="Vector Cut", fg_color="#c83232", hover_color="#a02828")
        self.btn_vector_cut.pack(padx=10, pady=5, fill="x")

        # --- Stop Button ---
        self.btn_stop = ctk.CTkButton(self.sidebar_frame, text="Pause/Stop", height=50, font=("Helvetica", 16, "bold"), fg_color="#c83232", hover_color="#a02828")
        self.btn_stop.pack(padx=20, pady=(20, 20), fill="x", side="bottom")

if __name__ == "__main__":
    app = SidebarTest()
    app.mainloop()
