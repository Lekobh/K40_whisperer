import sys
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import *
from embedded_images import K40_Whisperer_Images
from ecoords import ECoord
DEBUG = False

# To allow type hints or fallback if needed
# We assume ttkbootstrap is installed and K40_Whisperer_Images is available

def toplevel_dummy(): pass # we might need to mock this if it's missing, but actually it's just self.master

def trace_variable(variable, callback):
    return variable.trace_add("write", callback)

def trace_delete(variable,callback):
    return variable.trace_remove("write",callback)

class K40_GUI_Mixin:
    def createWidgets(self):
        self.initComplete = 0
        self.stop=[True]
        
        self.k40        = None
        self.run_time   = 0
        self.display_power = False
        self.display_test  = False
        self.pi_mode_height = 625
        
        self.master.bind("<Configure>", self.Master_Configure)
        self.master.bind('<Enter>', self.bindConfigure)
        self.master.bind('<F1>', self.KEY_F1)
        self.master.bind('<F2>', self.KEY_F2)
        self.master.bind('<F3>', self.KEY_F3)
        self.master.bind('<F4>', self.KEY_F4)
        self.master.bind('<F5>', self.KEY_F5)
        self.master.bind('<F6>', self.KEY_F6)
        self.master.bind('<Home>', self.Home)

        #self.master.bind('<Control-R>', self.Raster_Eng)
        #self.master.bind('<Control-V>', self.Vector_Eng)
        #self.master.bind('<Control-C>', self.Vector_Cut)
        #self.master.bind('<Control-G>', self.Gcode_Cut)

        self.master.bind('<Control-Left>'  , self.Move_Left)
        self.master.bind('<Control-Right>' , self.Move_Right)
        self.master.bind('<Control-Up>'    , self.Move_Up)
        self.master.bind('<Control-Down>'  , self.Move_Down)
        
        self.master.bind('<Control-Home>'  , self.Move_UL)
        self.master.bind('<Control-Prior>' , self.Move_UR)
        self.master.bind('<Control-Next>'  , self.Move_LR)
        self.master.bind('<Control-End>'   , self.Move_LL)
        self.master.bind('<Control-Clear>' , self.Move_CC)

        self.master.bind('<Control-Key-4>' , self.Move_Left)
        self.master.bind('<Control-6>'     , self.Move_Right)
        self.master.bind('<Control-8>'     , self.Move_Up)
        self.master.bind('<Control-Key-2>' , self.Move_Down)
        
        self.master.bind('<Control-7>'     , self.Move_UL)
        self.master.bind('<Control-9>'     , self.Move_UR)
        self.master.bind('<Control-Key-3>' , self.Move_LR)
        self.master.bind('<Control-Key-1>' , self.Move_LL)
        self.master.bind('<Control-Key-5>' , self.Move_CC)

        #####

        self.master.bind('<Alt-Control-Left>' , self.Move_Arb_Left)
        self.master.bind('<Alt-Control-Right>', self.Move_Arb_Right)
        self.master.bind('<Alt-Control-Up>'   , self.Move_Arb_Up)
        self.master.bind('<Alt-Control-Down>' , self.Move_Arb_Down)

        self.master.bind('<Alt-Control-Key-4>', self.Move_Arb_Left)
        self.master.bind('<Alt-Control-6>'    , self.Move_Arb_Right)
        self.master.bind('<Alt-Control-8>'    , self.Move_Arb_Up)
        self.master.bind('<Alt-Control-Key-2>', self.Move_Arb_Down)


        self.master.bind('<Alt-Left>' , self.Move_Arb_Left)
        self.master.bind('<Alt-Right>', self.Move_Arb_Right)
        self.master.bind('<Alt-Up>'   , self.Move_Arb_Up)
        self.master.bind('<Alt-Down>' , self.Move_Arb_Down)

        self.master.bind('<Alt-Key-4>', self.Move_Arb_Left)
        self.master.bind('<Alt-6>'    , self.Move_Arb_Right)
        self.master.bind('<Alt-8>'    , self.Move_Arb_Up)
        self.master.bind('<Alt-Key-2>', self.Move_Arb_Down)

        #####
        self.master.bind('<Control-i>' , self.Initialize_Laser)
        self.master.bind('<Control-f>' , self.Unfreeze_Laser)
        self.master.bind('<Control-o>' , self.menu_File_Open_Design)
        self.master.bind('<Control-l>' , self.menu_Reload_Design)
        self.master.bind('<Control-h>' , self.Home)
        self.master.bind('<Control-u>' , self.Unlock)
        self.master.bind('<Escape>'    , self.Stop)
        self.master.bind('<Control-t>' , self.TRACE_Settings_Window)

        self.include_Reng = BooleanVar()
        self.include_Rpth = BooleanVar()
        self.include_Veng = BooleanVar()
        self.include_Vcut = BooleanVar()
        self.include_Gcde = BooleanVar()
        self.include_Time = BooleanVar()

        self.advanced     = BooleanVar()
        self.show_power   = BooleanVar()
        self.show_test    = BooleanVar()
        
        self.halftone     = BooleanVar()
        self.mirror       = BooleanVar()
        self.rotate       = BooleanVar()
        self.negate       = BooleanVar()
        self.inputCSYS    = BooleanVar()
        self.HomeUR       = BooleanVar()
        self.engraveUP    = BooleanVar()
        self.init_home    = BooleanVar()
        self.post_home    = BooleanVar()
        self.post_beep    = BooleanVar()
        self.post_disp    = BooleanVar()
        self.post_exec    = BooleanVar()
        
        self.pre_pr_crc   = BooleanVar()
        self.inside_first = BooleanVar()
        self.rotary       = BooleanVar()
        self.reduced_mem  = BooleanVar()
        self.wait         = BooleanVar()
        

        self.ht_size    = StringVar()
        self.Reng_feed  = StringVar()
        self.Veng_feed  = StringVar()
        self.Vcut_feed  = StringVar()

        self.Reng_power  = StringVar()
        self.Veng_power  = StringVar()
        self.Vcut_power  = StringVar()
        self.Gcode_power = StringVar()
        self.Trace_power = StringVar()
        self.max_power   = StringVar()
        self.test_power  = StringVar()
        self.test_time   = StringVar()

        self.Reng_passes = StringVar()
        self.Veng_passes = StringVar()
        self.Vcut_passes = StringVar()
        self.Gcde_passes = StringVar()
        
        
        self.board_name = StringVar()
        self.units      = StringVar()
        self.jog_step   = StringVar()
        self.rast_step  = StringVar()
        self.funits     = StringVar()
        self.funits_label=StringVar()
        

        self.bezier_M1     = StringVar()
        self.bezier_M2     = StringVar()
        self.bezier_weight = StringVar()

##        self.unsharp_flag = BooleanVar()
##        self.unsharp_r    = StringVar()
##        self.unsharp_p    = StringVar()
##        self.unsharp_t    = StringVar()
##        self.unsharp_flag.set(False)
##        self.unsharp_r.set("40")
##        self.unsharp_p.set("350")
##        self.unsharp_t.set("3")

        self.LaserXsize = StringVar()
        self.LaserYsize = StringVar()

        self.LaserXscale = StringVar()
        self.LaserYscale = StringVar()
        self.LaserRscale = StringVar()

        self.rapid_feed = StringVar()

        self.gotoX = StringVar()
        self.gotoY = StringVar()

        self.n_egv_passes = StringVar()

        self.inkscape_path = StringVar()
        self.batch_path    = StringVar()
        self.ink_timeout   = StringVar()
        
        self.t_timeout  = StringVar()
        self.n_timeouts  = StringVar()
        
        self.Reng_time = StringVar()
        self.Veng_time = StringVar()
        self.Vcut_time = StringVar()
        self.Gcde_time = StringVar()

        self.comb_engrave = BooleanVar()
        self.comb_vector  = BooleanVar()
        self.zoom2image   = BooleanVar()

        self.trace_w_laser  = BooleanVar()
        self.trace_gap      = StringVar()
        self.trace_speed    = StringVar()
        
        ###########################################################################
        #                         INITILIZE VARIABLES                             #
        #    if you want to change a default setting this is the place to do it   #
        ###########################################################################
        self.include_Reng.set(1)
        self.include_Rpth.set(0)
        self.include_Veng.set(1)
        self.include_Vcut.set(1)
        self.include_Gcde.set(1)
        self.include_Time.set(0)
        self.advanced.set(0)
        self.show_power.set(1)
        self.show_test.set(1)
        
        self.halftone.set(1)
        self.mirror.set(0)
        self.rotate.set(0)
        self.negate.set(0)
        self.inputCSYS.set(0)
        self.HomeUR.set(0)
        self.engraveUP.set(0)
        self.init_home.set(1)
        self.post_home.set(0)
        self.post_beep.set(0)
        self.post_disp.set(0)
        self.post_exec.set(0)
        
        self.pre_pr_crc.set(1)
        self.inside_first.set(1)
        self.rotary.set(0)
        self.reduced_mem.set(0)
        self.wait.set(1)
        
        self.ht_size.set(500)

        self.Reng_feed.set("100")
        self.Veng_feed.set("20")
        self.Vcut_feed.set("10")

        self.Reng_power.set("0.5")
        self.Veng_power.set("0.5")
        self.Vcut_power.set("0.5")
        self.Gcode_power.set("0.5")
        self.Trace_power.set("0.5")
        self.max_power.set("30")
        self.test_power.set("0.5")
        self.test_time.set("250")
        
        self.Reng_passes.set("1")
        self.Veng_passes.set("1")
        self.Vcut_passes.set("1")
        self.Gcde_passes.set("1")
        
        
        self.jog_step.set("10.0")
        self.rast_step.set("0.002")
        
        self.bezier_weight.set("3.5")
        self.bezier_M1.set("2.5")
        self.bezier_M2.set("0.50")

        self.bezier_weight_default = float(self.bezier_weight.get())
        self.bezier_M1_default     = float(self.bezier_M1.get())
        self.bezier_M2_default     = float(self.bezier_M2.get())
        
                                        
        self.board_name.set("LASER-M2") # Options are
                                        #    "LASER-M3",
                                        #    "LASER-M2",
                                        #    "LASER-M1",
                                        #    "LASER-M",
                                        #    "LASER-B2",
                                        #    "LASER-B1",
                                        #    "LASER-B",
                                        #    "LASER-A"


        self.units.set("mm")            # Options are "in" and "mm"

        self.ink_timeout.set("3")
        self.t_timeout.set("200")
        self.n_timeouts.set("30")

        self.HOME_DIR    = os.path.expanduser("~")
        
        if not os.path.isdir(self.HOME_DIR):
            self.HOME_DIR = ""

        self.DESIGN_FILE = (self.HOME_DIR+"/None")
        self.EGV_FILE    = None
        
        self.aspect_ratio =  0
        self.segID   = []
        
        self.LaserXsize.set("325")
        self.LaserYsize.set("220")
        
        self.LaserXscale.set("1.000")
        self.LaserYscale.set("1.000")
        self.LaserRscale.set("1.000")

        self.rapid_feed.set("0.0")

        self.gotoX.set("0.0")
        self.gotoY.set("0.0")

        self.n_egv_passes.set("1")

        self.comb_engrave.set(0)
        self.comb_vector.set(0)
        self.zoom2image.set(0)


        self.trace_w_laser.set(0)
        self.trace_gap.set(0)
        self.trace_speed.set(50)
        
        self.laserX    = 0.0
        self.laserY    = 0.0
        self.PlotScale = 1.0
        self.GUI_Disabled = False

        # PAN and ZOOM STUFF
        self.panx = 0
        self.panx = 0
        self.lastx = 0
        self.lasty = 0
        self.move_start_x = 0
        self.move_start_y = 0

        
        self.RengData  = ECoord()
        self.VengData  = ECoord()
        self.VcutData  = ECoord()
        self.GcodeData = ECoord()
        self.SCALE = 1
        self.Design_bounds = (0,0,0,0)
        self.UI_image = None
        self.pos_offset=[0.0,0.0]
        self.inkscape_warning = False
        
        # Derived variables
        if self.units.get() == 'in':
            self.funits.set('in/min')
            self.funits_label.set('Speed\nin/min')
            self.units_scale = 1.0
        else:
            self.units.set('mm')
            self.funits.set('mm/s')
            self.funits_label.set('Speed\nmm/s')
            self.units_scale = 25.4
        
        self.statusMessage = StringVar()
        self.statusMessage.set("Welcome to K40 Whisperer")
        
        
        self.Reng_time.set("0")
        self.Veng_time.set("0")
        self.Vcut_time.set("0")
        self.Gcde_time.set("0")

        self.min_vector_speed = 1.1 #in/min
        self.min_raster_speed = 12  #in/min
        
        ##########################################################################
        ###                     END INITILIZING VARIABLES                      ###
        ##########################################################################

        
        # --- UI LAYOUT REWRITE ---
        self.LeftPanel = ttk.Frame(self.master, padding=10)
        self.LeftPanel.pack(side=LEFT, fill=Y)
        
        self.PreviewCanvas_frame = ttk.Frame(self.master)
        self.PreviewCanvas_frame.pack(side=LEFT, fill=BOTH, expand=True)
        # -------------------------
# make a Status Bar
        self.statusbar = ttk.Label(self.master, textvariable=self.statusMessage, \
                                   bd=1, relief=SUNKEN , height=1)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
        

        # Canvas
        lbframe = Frame( self.master )
        self.PreviewCanvas_frame = ttk.Frame(self.master)
        self.PreviewCanvas = Canvas(self.PreviewCanvas_frame, width=self.w-(220+20), height=self.h-200, background="grey75")
        self.PreviewCanvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.PreviewCanvas_frame.place(x=230, y=10)

        self.PreviewCanvas.tag_bind('LaserTag',"<1>"              , self.mousePanStart)
        self.PreviewCanvas.tag_bind('LaserTag',"<B1-Motion>"      , self.mousePan)
        self.PreviewCanvas.tag_bind('LaserTag',"<ButtonRelease-1>", self.mousePanStop)

        self.PreviewCanvas.tag_bind('LaserDot',"<3>"              , self.right_mousePanStart)
        self.PreviewCanvas.tag_bind('LaserDot',"<B3-Motion>"      , self.right_mousePan)
        self.PreviewCanvas.tag_bind('LaserDot',"<ButtonRelease-3>", self.right_mousePanStop)

        # Left Column #
        self.separator1 = Frame(self.master, height=2, bd=1, relief=SUNKEN)
        self.separator2 = Frame(self.master, height=2, bd=1, relief=SUNKEN)
        self.separator3 = Frame(self.master, height=2, bd=1, relief=SUNKEN)
        self.separator4 = Frame(self.master, height=2, bd=1, relief=SUNKEN)

        #Speed
        self.Label_Reng_feed_u = ttk.Label(self.master,textvariable=self.funits, anchor=W)
        self.Entry_Reng_feed   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Reng_feed.configure(textvariable=self.Reng_feed,justify='center',fg="black")
        trace_variable(self.Reng_feed, self.Entry_Reng_feed_Callback)
        self.NormalColor =  self.Entry_Reng_feed.cget('bg')

        self.Label_Veng_feed_u = ttk.Label(self.master,textvariable=self.funits, anchor=W)
        self.Entry_Veng_feed   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Veng_feed.configure(textvariable=self.Veng_feed,justify='center',fg="blue")
        trace_variable(self.Veng_feed, self.Entry_Veng_feed_Callback)
        self.NormalColor =  self.Entry_Veng_feed.cget('bg')

        self.Label_Vcut_feed_u = ttk.Label(self.master,textvariable=self.funits, anchor=W)
        self.Entry_Vcut_feed   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Vcut_feed.configure(textvariable=self.Vcut_feed,justify='center',fg="red")
        trace_variable(self.Vcut_feed, self.Entry_Vcut_feed_Callback)
        self.NormalColor =  self.Entry_Vcut_feed.cget('bg')

        #Power
        self.Label_feed_u  = ttk.Label(self.master,textvariable=self.funits_label, anchor=CENTER)
        self.Label_power_u = Label(text="Power\nFraction", anchor=CENTER)

        self.Label_time_u  = Label(text="Time\nmSec", anchor=CENTER)
        self.Label_power2_u= Label(text="Power\nFraction", anchor=CENTER)
                        
        
        self.Entry_Reng_power   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Reng_power.configure(textvariable=self.Reng_power,justify='center',fg="black")
        trace_variable(self.Reng_power, self.Entry_Reng_power_Callback)
        self.NormalColor =  self.Entry_Reng_power.cget('bg')

        self.Entry_Veng_power   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Veng_power.configure(textvariable=self.Veng_power,justify='center',fg="blue")
        trace_variable(self.Veng_power, self.Entry_Veng_power_Callback)
        self.NormalColor =  self.Entry_Veng_power.cget('bg')

        self.Entry_Vcut_power   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Vcut_power.configure(textvariable=self.Vcut_power,justify='center',fg="red")
        trace_variable(self.Vcut_power, self.Entry_Vcut_power_Callback)
        self.NormalColor =  self.Entry_Vcut_power.cget('bg')

        self.Entry_Gcode_power   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Gcode_power.configure(textvariable=self.Gcode_power,justify='center',fg="red")
        trace_variable(self.Gcode_power, self.Entry_Gcode_power_Callback)
        self.NormalColor =  self.Entry_Gcode_power.cget('bg')


        ### Test Fire ###
        self.Test_Button  = ttk.Button(self.LeftPanel,text="Test Fire Laser", command=self.Test_Fire)
        self.Label_Test_time_u = ttk.Label(self.master,text="ms", anchor=W)
        self.Entry_Test_time   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Test_time.configure(textvariable=self.test_time,justify='center',fg="black")

        trace_variable(self.test_time, self.Entry_Test_time_Callback)
        self.NormalColor =  self.Entry_Test_time.cget('bg')
        
        self.Entry_Test_power   = ttk.Entry(self.LeftPanel,width="15")
        self.Label_Test_power_u = ttk.Label(self.master,text="%", anchor=W)
        self.Entry_Test_power.configure(textvariable=self.test_power,justify='center',fg="black")
        trace_variable(self.test_power, self.Entry_Test_power_Callback)
        self.NormalColor =  self.Entry_Test_power.cget('bg')

        ##################
                        
        # Buttons
        self.Reng_Button  = ttk.Button(self.LeftPanel,text="Raster Engrave", command=self.Raster_Eng)
        self.Veng_Button  = ttk.Button(self.LeftPanel,text="Vector Engrave", command=self.Vector_Eng)
        self.Vcut_Button  = ttk.Button(self.LeftPanel,text="Vector Cut"    , command=self.Vector_Cut)
        self.Grun_Button  = ttk.Button(self.LeftPanel,text="Run G-Code"    , command=self.Gcode_Cut)


        self.Reng_Veng_Button      = ttk.Button(self.LeftPanel,text="Raster and\nVector Engrave", command=self.Raster_Vector_Eng)
        self.Veng_Vcut_Button      = ttk.Button(self.LeftPanel,text="Vector Engrave\nand Cut", command=self.Vector_Eng_Cut)
        self.Reng_Veng_Vcut_Button = ttk.Button(self.LeftPanel,text="Raster Engrave\nVector Engrave\nand\nVector Cut", command=self.Raster_Vector_Cut)
        
        self.Label_Position_Control = ttk.Label(self.master,text="Position Controls:", anchor=W)
        
        self.Initialize_Button = ttk.Button(self.LeftPanel,text="Initialize Laser Cutter", command=self.Initialize_Laser)

        self.Open_Button       = ttk.Button(self.LeftPanel,text="Open\nDesign File",   command=self.menu_File_Open_Design)
        self.Reload_Button     = ttk.Button(self.LeftPanel,text="Reload\nDesign File", command=self.menu_Reload_Design)
        
        self.Home_Button       = ttk.Button(self.LeftPanel,text="Home",            command=self.Home)
        self.UnLock_Button     = ttk.Button(self.LeftPanel,text="Unlock Rail",     command=self.Unlock)
        self.Stop_Button       = ttk.Button(self.LeftPanel,text="Pause/Stop",      command=self.Stop)

        try:            
            self.left_image  = PhotoImage(data=K40_Whisperer_Images.left_B64,  format='gif')
            self.right_image = PhotoImage(data=K40_Whisperer_Images.right_B64, format='gif')
            self.up_image    = PhotoImage(data=K40_Whisperer_Images.up_B64,    format='gif')
            self.down_image  = PhotoImage(data=K40_Whisperer_Images.down_B64,  format='gif')
            
            self.Right_Button   = ttk.Button(self.LeftPanel,image=self.right_image, command=self.Move_Right)
            self.Left_Button    = ttk.Button(self.LeftPanel,image=self.left_image,  command=self.Move_Left)
            self.Up_Button      = ttk.Button(self.LeftPanel,image=self.up_image,    command=self.Move_Up)
            self.Down_Button    = ttk.Button(self.LeftPanel,image=self.down_image,  command=self.Move_Down)

            self.UL_image  = PhotoImage(data=K40_Whisperer_Images.UL_B64, format='gif')
            self.UR_image  = PhotoImage(data=K40_Whisperer_Images.UR_B64, format='gif')
            self.LR_image  = PhotoImage(data=K40_Whisperer_Images.LR_B64, format='gif')
            self.LL_image  = PhotoImage(data=K40_Whisperer_Images.LL_B64, format='gif')
            self.CC_image  = PhotoImage(data=K40_Whisperer_Images.CC_B64, format='gif')

            self.UL_Button = ttk.Button(self.LeftPanel,image=self.UL_image, command=self.Move_UL)
            self.UR_Button = ttk.Button(self.LeftPanel,image=self.UR_image, command=self.Move_UR)
            self.LR_Button = ttk.Button(self.LeftPanel,image=self.LR_image, command=self.Move_LR)
            self.LL_Button = ttk.Button(self.LeftPanel,image=self.LL_image, command=self.Move_LL)
            self.CC_Button = ttk.Button(self.LeftPanel,image=self.CC_image, command=self.Move_CC)
            
        except:
            self.Right_Button   = ttk.Button(self.LeftPanel,text=">",          command=self.Move_Right)
            self.Left_Button    = ttk.Button(self.LeftPanel,text="<",          command=self.Move_Left)
            self.Up_Button      = ttk.Button(self.LeftPanel,text="^",          command=self.Move_Up)
            self.Down_Button    = ttk.Button(self.LeftPanel,text="v",          command=self.Move_Down)

            self.UL_Button = ttk.Button(self.LeftPanel,text=" ", command=self.Move_UL)
            self.UR_Button = ttk.Button(self.LeftPanel,text=" ", command=self.Move_UR)
            self.LR_Button = ttk.Button(self.LeftPanel,text=" ", command=self.Move_LR)
            self.LL_Button = ttk.Button(self.LeftPanel,text=" ", command=self.Move_LL)
            self.CC_Button = ttk.Button(self.LeftPanel,text=" ", command=self.Move_CC)

        self.Label_Step   = ttk.Label(self.master,text="Jog Step", anchor=CENTER )
        self.Label_Step_u = ttk.Label(self.master,textvariable=self.units, anchor=W)
        self.Entry_Step   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Step.configure(textvariable=self.jog_step, justify='center')
        trace_variable(self.jog_step, self.Entry_Step_Callback)

        ###########################################################################
        self.GoTo_Button    = ttk.Button(self.LeftPanel,text="Move To", command=self.GoTo)
        
        self.Entry_GoToX   = ttk.Entry(self.LeftPanel,width="15",justify='center')
        self.Entry_GoToX.configure(textvariable=self.gotoX)
        trace_variable(self.gotoX, self.Entry_GoToX_Callback)
        self.Entry_GoToY   = ttk.Entry(self.LeftPanel,width="15",justify='center')
        self.Entry_GoToY.configure(textvariable=self.gotoY)
        trace_variable(self.gotoY, self.Entry_GoToY_Callback)
        
        self.Label_GoToX   = ttk.Label(self.master,text="X", anchor=CENTER )
        self.Label_GoToY   = ttk.Label(self.master,text="Y", anchor=CENTER )
        ###########################################################################
        # End Left Column #

        # Advanced Column     #
        self.separator_vert = Frame(self.master, height=2, bd=1, relief=SUNKEN)
        self.Label_Advanced_column = ttk.Label(self.master,text="Advanced Settings",anchor=CENTER)
        self.separator_adv = Frame(self.master, height=2, bd=1, relief=SUNKEN)       

        self.Label_Halftone_adv = ttk.Label(self.master,text="Halftone (Dither)")
        self.Checkbutton_Halftone_adv = ttk.Checkbutton(self.LeftPanel,text=" ", anchor=W)
        self.Checkbutton_Halftone_adv.configure(variable=self.halftone)
        trace_variable(self.halftone, self.View_Refresh_and_Reset_RasterPath) #self.menu_View_Refresh_Callback

        self.Label_Negate_adv = ttk.Label(self.master,text="Invert Raster Color")
        self.Checkbutton_Negate_adv = ttk.Checkbutton(self.LeftPanel,text=" ", anchor=W)
        self.Checkbutton_Negate_adv.configure(variable=self.negate)
        trace_variable(self.negate, self.View_Refresh_and_Reset_RasterPath)

        self.separator_adv2 = Frame(self.master, height=2, bd=1, relief=SUNKEN)  

        self.Label_Mirror_adv = ttk.Label(self.master,text="Mirror Design")
        self.Checkbutton_Mirror_adv = ttk.Checkbutton(self.LeftPanel,text=" ", anchor=W)
        self.Checkbutton_Mirror_adv.configure(variable=self.mirror)
        trace_variable(self.mirror, self.View_Refresh_and_Reset_RasterPath)

        self.Label_Rotate_adv = ttk.Label(self.master,text="Rotate Design")
        self.Checkbutton_Rotate_adv = ttk.Checkbutton(self.LeftPanel,text=" ", anchor=W)
        self.Checkbutton_Rotate_adv.configure(variable=self.rotate)
        trace_variable(self.rotate, self.View_Refresh_and_Reset_RasterPath)

        self.separator_adv3 = Frame(self.master, height=2, bd=1, relief=SUNKEN)
        
        self.Label_inputCSYS_adv = ttk.Label(self.master,text="Use Input CSYS")
        self.Checkbutton_inputCSYS_adv = ttk.Checkbutton(self.LeftPanel,text=" ", anchor=W)
        self.Checkbutton_inputCSYS_adv.configure(variable=self.inputCSYS)
        trace_variable(self.inputCSYS, self.menu_View_inputCSYS_Refresh_Callback)

        self.Label_Inside_First_adv = ttk.Label(self.master,text="Cut Inside First")
        self.Checkbutton_Inside_First_adv = ttk.Checkbutton(self.LeftPanel,text=" ", anchor=W)
        self.Checkbutton_Inside_First_adv.configure(variable=self.inside_first)
        trace_variable(self.inside_first, self.menu_Inside_First_Callback)

        self.Label_Inside_First_adv = ttk.Label(self.master,text="Cut Inside First")
        self.Checkbutton_Inside_First_adv = ttk.Checkbutton(self.LeftPanel,text=" ", anchor=W)
        self.Checkbutton_Inside_First_adv.configure(variable=self.inside_first)

        self.Label_Rotary_Enable_adv = ttk.Label(self.master,text="Use Rotary Settings")
        self.Checkbutton_Rotary_Enable_adv = ttk.Checkbutton(self.LeftPanel,text="")
        self.Checkbutton_Rotary_Enable_adv.configure(variable=self.rotary)
        trace_variable(self.rotary, self.Reset_RasterPath_and_Update_Time)


        #####
        self.separator_comb = Frame(self.master, height=2, bd=1, relief=SUNKEN)  

        self.Label_Comb_Engrave_adv = ttk.Label(self.master,text="Group Engrave Tasks")
        self.Checkbutton_Comb_Engrave_adv = ttk.Checkbutton(self.LeftPanel,text=" ", anchor=W)
        self.Checkbutton_Comb_Engrave_adv.configure(variable=self.comb_engrave)
        trace_variable(self.comb_engrave, self.menu_View_Refresh_Callback)

        self.Label_Comb_Vector_adv = ttk.Label(self.master,text="Group Vector Tasks")
        self.Checkbutton_Comb_Vector_adv = ttk.Checkbutton(self.LeftPanel,text=" ", anchor=W)
        self.Checkbutton_Comb_Vector_adv.configure(variable=self.comb_vector)
        trace_variable(self.comb_vector, self.menu_View_Refresh_Callback) 
        #####
        
        self.Label_Reng_passes = ttk.Label(self.master,text="Raster Eng. Passes")
        self.Entry_Reng_passes   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Reng_passes.configure(textvariable=self.Reng_passes,justify='center',fg="black")
        trace_variable(self.Reng_passes, self.Entry_Reng_passes_Callback)
        self.NormalColor =  self.Entry_Reng_passes.cget('bg')

        self.Label_Veng_passes = ttk.Label(self.master,text="Vector Eng. Passes")
        self.Entry_Veng_passes   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Veng_passes.configure(textvariable=self.Veng_passes,justify='center',fg="blue")
        trace_variable(self.Veng_passes, self.Entry_Veng_passes_Callback)
        self.NormalColor =  self.Entry_Veng_passes.cget('bg')

        self.Label_Vcut_passes = ttk.Label(self.master,text="Vector Cut Passes")
        self.Entry_Vcut_passes   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Vcut_passes.configure(textvariable=self.Vcut_passes,justify='center',fg="red")
        trace_variable(self.Vcut_passes, self.Entry_Vcut_passes_Callback)
        self.NormalColor =  self.Entry_Vcut_passes.cget('bg')

        self.Label_Gcde_passes = ttk.Label(self.master,text="G-Code Passes")
        self.Entry_Gcde_passes   = ttk.Entry(self.LeftPanel,width="15")
        self.Entry_Gcde_passes.configure(textvariable=self.Gcde_passes,justify='center',fg="black")
        trace_variable(self.Gcde_passes, self.Entry_Gcde_passes_Callback)
        self.NormalColor =  self.Entry_Gcde_passes.cget('bg')

        
        self.Hide_Adv_Button = ttk.Button(self.LeftPanel,text="Hide Advanced", command=self.Hide_Advanced)
                
        # End Right Column #
        self.calc_button = ttk.Button(self.LeftPanel,text="Calculate Raster Time", command=self.menu_Calc_Raster_Time)

        #GEN Setting Window Entry initializations
        self.Entry_Sspeed    = Entry()
        self.Entry_BoxGap    = Entry()
        self.Entry_ContAngle = Entry()

        # Make Menu Bar
        self.menuBar = Menu(self.master, relief = "raised", bd=2)

        


        top_File = Menu(self.menuBar, tearoff=0)
        top_File.add("command", label = "Save Settings File", command = self.menu_File_Save)
        top_File.add("command", label = "Read Settings File", command = self.menu_File_Open_Settings_File)

        top_File.add_separator()
        top_File.add("command", label = "Open Design (SVG/DXF/G-Code)"  , command = self.menu_File_Open_Design)
        top_File.add("command", label = "Reload Design"          , command = self.menu_Reload_Design)

        top_File.add_separator()    
        top_File.add("command", label = "Send EGV File to Laser"             , command = self.menu_File_Open_EGV)

        SaveEGVmenu = Menu(self.master, relief = "raised", bd=2, tearoff=0)
        top_File.add_cascade(label="Save EGV File", menu=SaveEGVmenu)        
        SaveEGVmenu.add("command", label = "Raster Engrave"     , command = self.menu_File_Raster_Engrave)
        SaveEGVmenu.add("command", label = "Vector Engrave"     , command = self.menu_File_Vector_Engrave)
        SaveEGVmenu.add("command", label = "Vector Cut"         , command = self.menu_File_Vector_Cut)
        SaveEGVmenu.add("command", label = "G-Code Operations"  , command = self.menu_File_G_Code)
        SaveEGVmenu.add_separator()   
        SaveEGVmenu.add("command", label = "Raster and Vector Engrave"             , command = self.menu_File_Raster_Vector_Engrave)
        SaveEGVmenu.add("command", label = "Vector Engrave and Cut"                , command = self.menu_File_Vector_Engrave_Cut)
        SaveEGVmenu.add("command", label = "Raster, Vector Engrave and Vector Cut" , command = self.menu_File_Raster_Vector_Cut)
        
    
        top_File.add_separator()
        top_File.add("command", label = "Exit"              , command = self.menu_File_Quit)
        
        self.menuBar.add("cascade", label="File", menu=top_File)

        #top_Edit = Menu(self.menuBar, tearoff=0)
        #self.menuBar.add("cascade", label="Edit", menu=top_Edit)

        top_View = Menu(self.menuBar, tearoff=0)
        top_View.add("command", label = "Refresh   <F5>", command = self.menu_View_Refresh)
        top_View.add_separator()
        top_View.add_checkbutton(label = "Show Raster Image"  ,  variable=self.include_Reng ,command= self.menu_View_Refresh)
        if DEBUG:
            top_View.add_checkbutton(label = "Show Raster Paths" ,variable=self.include_Rpth ,command= self.menu_View_Refresh)
        
        top_View.add_checkbutton(label = "Show Vector Engrave",   variable=self.include_Veng ,command= self.menu_View_Refresh)
        top_View.add_checkbutton(label = "Show Vector Cut"    ,   variable=self.include_Vcut ,command= self.menu_View_Refresh)
        top_View.add_checkbutton(label = "Show G-Code Paths"  ,   variable=self.include_Gcde ,command= self.menu_View_Refresh)
        top_View.add_separator()
        top_View.add_checkbutton(label = "Show Time Estimates",   variable=self.include_Time ,command= self.menu_View_Refresh)
        top_View.add_checkbutton(label = "Zoom to Design Size",   variable=self.zoom2image   ,command= self.menu_View_Refresh)

        #top_View.add_separator()
        #top_View.add("command", label = "computeAccurateReng",command= self.computeAccurateReng)
        #top_View.add("command", label = "computeAccurateVeng",command= self.computeAccurateVeng)
        #top_View.add("command", label = "computeAccurateVcut",command= self.computeAccurateVcut)

        self.menuBar.add("cascade", label="View", menu=top_View)

        top_Tools = Menu(self.menuBar, tearoff=0)
        self.menuBar.add("cascade", label="Tools", menu=top_Tools)
        USBmenu = Menu(self.master, relief = "raised", bd=2, tearoff=0)
          
        top_Tools.add("command", label = "Calculate Raster Time", command = self.menu_Calc_Raster_Time)
        top_Tools.add("command", label = "Trace Design Boundary <Ctrl-t>", command = self.TRACE_Settings_Window)
        top_Tools.add_separator()
        top_Tools.add("command", label = "Initialize Laser <Ctrl-i>", command = self.Initialize_Laser)
        top_Tools.add("command", label = "Unfreeze Laser <Ctrl-f>"  , command = self.Unfreeze_Laser)
        top_Tools.add_cascade(label="USB", menu=USBmenu)
        USBmenu.add("command", label = "Reset USB", command = self.Reset)
        USBmenu.add("command", label = "Release USB", command = self.Release_USB)

                    

        #top_USB = Menu(self.menuBar, tearoff=0)
        #top_USB.add("command", label = "Reset USB", command = self.Reset)
        #top_USB.add("command", label = "Release USB", command = self.Release_USB)
        #top_USB.add("command", label = "Initialize Laser", command = self.Initialize_Laser)
        #self.menuBar.add("cascade", label="USB", menu=top_USB)
        

        top_Settings = Menu(self.menuBar, tearoff=0)
        top_Settings.add("command", label = "General Settings <F2>", command = self.GEN_Settings_Window)
        top_Settings.add("command", label = "Raster Settings <F3>",  command = self.RASTER_Settings_Window)
        top_Settings.add("command", label = "Rotary Settings <F4>",  command = self.ROTARY_Settings_Window)
        top_Settings.add_separator()
        top_Settings.add_checkbutton(label = "Advanced Settings <F6>", variable=self.advanced ,command= self.menu_View_Refresh)
        
        self.menuBar.add("cascade", label="Settings", menu=top_Settings)
        
        top_Help = Menu(self.menuBar, tearoff=0)
        top_Help.add("command", label = "About (e-mail)", command = self.menu_Help_About)
        top_Help.add("command", label = "K40 Whisperer Web Page", command = self.menu_Help_Web)
        top_Help.add("command", label = "Manual (Web Page)", command = self.menu_Help_Manual)
        self.menuBar.add("cascade", label="Help", menu=top_Help)

        self.master.config(menu=self.menuBar)

        ##########################################################################
        #                  Config File and command line options                  #
        ##########################################################################
        config_file = "k40_whisperer.txt"
        home_config1 = self.HOME_DIR + "/" + config_file
        if ( os.path.isfile(config_file) ):
            self.Open_Settings_File(config_file)
        elif ( os.path.isfile(home_config1) ):
            self.Open_Settings_File(home_config1)


#        opts, args = None, None
#        try:
#            opts, args = getopt.getopt(sys.argv[1:], "ho:",["help", "other_option"])
#        except:
#            debug_message('Unable interpret command line options')
#            sys.exit()
#        for option, value in opts:
##            if option in ('-h','--help'):
##                fmessage(' ')
##                fmessage('Usage: python .py [-g file]')
##                fmessage('-o    : unknown other option (also --other_option)')
##                fmessage('-h    : print this help (also --help)\n')
##                sys.exit()
#            if option in ('-m','--micro'):
#                self.micro = True

        ##########################################################################

################################################################################

    def Master_Configure(self, event, update=0):
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
