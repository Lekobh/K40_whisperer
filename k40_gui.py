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

        # make a Status Bar
        self.statusbar = Label(self.master, textvariable=self.statusMessage, \
                                   bd=1, relief=SUNKEN , height=1)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
        

        # Canvas
        lbframe = Frame( self.master )
        self.PreviewCanvas_frame = lbframe
        self.PreviewCanvas = Canvas(lbframe, width=self.w-(220+20), height=self.h-200, background="grey75")
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
        self.Label_Reng_feed_u = Label(self.master,textvariable=self.funits, anchor=W)
        self.Entry_Reng_feed   = Entry(self.master,width="15")
        self.Entry_Reng_feed.configure(textvariable=self.Reng_feed,justify='center',fg="black")
        trace_variable(self.Reng_feed, self.Entry_Reng_feed_Callback)
        self.NormalColor =  self.Entry_Reng_feed.cget('bg')

        self.Label_Veng_feed_u = Label(self.master,textvariable=self.funits, anchor=W)
        self.Entry_Veng_feed   = Entry(self.master,width="15")
        self.Entry_Veng_feed.configure(textvariable=self.Veng_feed,justify='center',fg="blue")
        trace_variable(self.Veng_feed, self.Entry_Veng_feed_Callback)
        self.NormalColor =  self.Entry_Veng_feed.cget('bg')

        self.Label_Vcut_feed_u = Label(self.master,textvariable=self.funits, anchor=W)
        self.Entry_Vcut_feed   = Entry(self.master,width="15")
        self.Entry_Vcut_feed.configure(textvariable=self.Vcut_feed,justify='center',fg="red")
        trace_variable(self.Vcut_feed, self.Entry_Vcut_feed_Callback)
        self.NormalColor =  self.Entry_Vcut_feed.cget('bg')

        #Power
        self.Label_feed_u  = Label(self.master,textvariable=self.funits_label, anchor=CENTER)
        self.Label_power_u = Label(text="Power\nFraction", anchor=CENTER)

        self.Label_time_u  = Label(text="Time\nmSec", anchor=CENTER)
        self.Label_power2_u= Label(text="Power\nFraction", anchor=CENTER)
                        
        
        self.Entry_Reng_power   = Entry(self.master,width="15")
        self.Entry_Reng_power.configure(textvariable=self.Reng_power,justify='center',fg="black")
        trace_variable(self.Reng_power, self.Entry_Reng_power_Callback)
        self.NormalColor =  self.Entry_Reng_power.cget('bg')

        self.Entry_Veng_power   = Entry(self.master,width="15")
        self.Entry_Veng_power.configure(textvariable=self.Veng_power,justify='center',fg="blue")
        trace_variable(self.Veng_power, self.Entry_Veng_power_Callback)
        self.NormalColor =  self.Entry_Veng_power.cget('bg')

        self.Entry_Vcut_power   = Entry(self.master,width="15")
        self.Entry_Vcut_power.configure(textvariable=self.Vcut_power,justify='center',fg="red")
        trace_variable(self.Vcut_power, self.Entry_Vcut_power_Callback)
        self.NormalColor =  self.Entry_Vcut_power.cget('bg')

        self.Entry_Gcode_power   = Entry(self.master,width="15")
        self.Entry_Gcode_power.configure(textvariable=self.Gcode_power,justify='center',fg="red")
        trace_variable(self.Gcode_power, self.Entry_Gcode_power_Callback)
        self.NormalColor =  self.Entry_Gcode_power.cget('bg')


        ### Test Fire ###
        self.Test_Button  = Button(self.master,text="Test Fire Laser", command=self.Test_Fire)
        self.Label_Test_time_u = Label(self.master,text="ms", anchor=W)
        self.Entry_Test_time   = Entry(self.master,width="15")
        self.Entry_Test_time.configure(textvariable=self.test_time,justify='center',fg="black")

        trace_variable(self.test_time, self.Entry_Test_time_Callback)
        self.NormalColor =  self.Entry_Test_time.cget('bg')
        
        self.Entry_Test_power   = Entry(self.master,width="15")
        self.Label_Test_power_u = Label(self.master,text="%", anchor=W)
        self.Entry_Test_power.configure(textvariable=self.test_power,justify='center',fg="black")
        trace_variable(self.test_power, self.Entry_Test_power_Callback)
        self.NormalColor =  self.Entry_Test_power.cget('bg')

        ##################
                        
        # Buttons
        self.Reng_Button  = Button(self.master,text="Raster Engrave", command=self.Raster_Eng)
        self.Veng_Button  = Button(self.master,text="Vector Engrave", command=self.Vector_Eng)
        self.Vcut_Button  = Button(self.master,text="Vector Cut"    , command=self.Vector_Cut)
        self.Grun_Button  = Button(self.master,text="Run G-Code"    , command=self.Gcode_Cut)


        self.Reng_Veng_Button      = Button(self.master,text="Raster and\nVector Engrave", command=self.Raster_Vector_Eng)
        self.Veng_Vcut_Button      = Button(self.master,text="Vector Engrave\nand Cut", command=self.Vector_Eng_Cut)
        self.Reng_Veng_Vcut_Button = Button(self.master,text="Raster Engrave\nVector Engrave\nand\nVector Cut", command=self.Raster_Vector_Cut)
        
        self.Label_Position_Control = Label(self.master,text="Position Controls:", anchor=W)
        
        self.Initialize_Button = Button(self.master,text="Initialize Laser Cutter", command=self.Initialize_Laser)

        self.Open_Button       = Button(self.master,text="Open\nDesign File",   command=self.menu_File_Open_Design)
        self.Reload_Button     = Button(self.master,text="Reload\nDesign File", command=self.menu_Reload_Design)
        
        self.Home_Button       = Button(self.master,text="Home",            command=self.Home)
        self.UnLock_Button     = Button(self.master,text="Unlock Rail",     command=self.Unlock)
        self.Stop_Button       = Button(self.master,text="Pause/Stop",      command=self.Stop)

        try:            
            self.left_image  = PhotoImage(data=K40_Whisperer_Images.left_B64,  format='gif')
            self.right_image = PhotoImage(data=K40_Whisperer_Images.right_B64, format='gif')
            self.up_image    = PhotoImage(data=K40_Whisperer_Images.up_B64,    format='gif')
            self.down_image  = PhotoImage(data=K40_Whisperer_Images.down_B64,  format='gif')
            
            self.Right_Button   = Button(self.master,image=self.right_image, command=self.Move_Right)
            self.Left_Button    = Button(self.master,image=self.left_image,  command=self.Move_Left)
            self.Up_Button      = Button(self.master,image=self.up_image,    command=self.Move_Up)
            self.Down_Button    = Button(self.master,image=self.down_image,  command=self.Move_Down)

            self.UL_image  = PhotoImage(data=K40_Whisperer_Images.UL_B64, format='gif')
            self.UR_image  = PhotoImage(data=K40_Whisperer_Images.UR_B64, format='gif')
            self.LR_image  = PhotoImage(data=K40_Whisperer_Images.LR_B64, format='gif')
            self.LL_image  = PhotoImage(data=K40_Whisperer_Images.LL_B64, format='gif')
            self.CC_image  = PhotoImage(data=K40_Whisperer_Images.CC_B64, format='gif')

            self.UL_Button = Button(self.master,image=self.UL_image, command=self.Move_UL)
            self.UR_Button = Button(self.master,image=self.UR_image, command=self.Move_UR)
            self.LR_Button = Button(self.master,image=self.LR_image, command=self.Move_LR)
            self.LL_Button = Button(self.master,image=self.LL_image, command=self.Move_LL)
            self.CC_Button = Button(self.master,image=self.CC_image, command=self.Move_CC)
            
        except:
            self.Right_Button   = Button(self.master,text=">",          command=self.Move_Right)
            self.Left_Button    = Button(self.master,text="<",          command=self.Move_Left)
            self.Up_Button      = Button(self.master,text="^",          command=self.Move_Up)
            self.Down_Button    = Button(self.master,text="v",          command=self.Move_Down)

            self.UL_Button = Button(self.master,text=" ", command=self.Move_UL)
            self.UR_Button = Button(self.master,text=" ", command=self.Move_UR)
            self.LR_Button = Button(self.master,text=" ", command=self.Move_LR)
            self.LL_Button = Button(self.master,text=" ", command=self.Move_LL)
            self.CC_Button = Button(self.master,text=" ", command=self.Move_CC)

        self.Label_Step   = Label(self.master,text="Jog Step", anchor=CENTER )
        self.Label_Step_u = Label(self.master,textvariable=self.units, anchor=W)
        self.Entry_Step   = Entry(self.master,width="15")
        self.Entry_Step.configure(textvariable=self.jog_step, justify='center')
        trace_variable(self.jog_step, self.Entry_Step_Callback)

        ###########################################################################
        self.GoTo_Button    = Button(self.master,text="Move To", command=self.GoTo)
        
        self.Entry_GoToX   = Entry(self.master,width="15",justify='center')
        self.Entry_GoToX.configure(textvariable=self.gotoX)
        trace_variable(self.gotoX, self.Entry_GoToX_Callback)
        self.Entry_GoToY   = Entry(self.master,width="15",justify='center')
        self.Entry_GoToY.configure(textvariable=self.gotoY)
        trace_variable(self.gotoY, self.Entry_GoToY_Callback)
        
        self.Label_GoToX   = Label(self.master,text="X", anchor=CENTER )
        self.Label_GoToY   = Label(self.master,text="Y", anchor=CENTER )
        ###########################################################################
        # End Left Column #

        # Advanced Column     #
        self.separator_vert = Frame(self.master, height=2, bd=1, relief=SUNKEN)
        self.Label_Advanced_column = Label(self.master,text="Advanced Settings",anchor=CENTER)
        self.separator_adv = Frame(self.master, height=2, bd=1, relief=SUNKEN)       

        self.Label_Halftone_adv = Label(self.master,text="Halftone (Dither)")
        self.Checkbutton_Halftone_adv = Checkbutton(self.master,text=" ", anchor=W)
        self.Checkbutton_Halftone_adv.configure(variable=self.halftone)
        trace_variable(self.halftone, self.View_Refresh_and_Reset_RasterPath) #self.menu_View_Refresh_Callback

        self.Label_Negate_adv = Label(self.master,text="Invert Raster Color")
        self.Checkbutton_Negate_adv = Checkbutton(self.master,text=" ", anchor=W)
        self.Checkbutton_Negate_adv.configure(variable=self.negate)
        trace_variable(self.negate, self.View_Refresh_and_Reset_RasterPath)

        self.separator_adv2 = Frame(self.master, height=2, bd=1, relief=SUNKEN)  

        self.Label_Mirror_adv = Label(self.master,text="Mirror Design")
        self.Checkbutton_Mirror_adv = Checkbutton(self.master,text=" ", anchor=W)
        self.Checkbutton_Mirror_adv.configure(variable=self.mirror)
        trace_variable(self.mirror, self.View_Refresh_and_Reset_RasterPath)

        self.Label_Rotate_adv = Label(self.master,text="Rotate Design")
        self.Checkbutton_Rotate_adv = Checkbutton(self.master,text=" ", anchor=W)
        self.Checkbutton_Rotate_adv.configure(variable=self.rotate)
        trace_variable(self.rotate, self.View_Refresh_and_Reset_RasterPath)

        self.separator_adv3 = Frame(self.master, height=2, bd=1, relief=SUNKEN)
        
        self.Label_inputCSYS_adv = Label(self.master,text="Use Input CSYS")
        self.Checkbutton_inputCSYS_adv = Checkbutton(self.master,text=" ", anchor=W)
        self.Checkbutton_inputCSYS_adv.configure(variable=self.inputCSYS)
        trace_variable(self.inputCSYS, self.menu_View_inputCSYS_Refresh_Callback)

        self.Label_Inside_First_adv = Label(self.master,text="Cut Inside First")
        self.Checkbutton_Inside_First_adv = Checkbutton(self.master,text=" ", anchor=W)
        self.Checkbutton_Inside_First_adv.configure(variable=self.inside_first)
        trace_variable(self.inside_first, self.menu_Inside_First_Callback)

        self.Label_Inside_First_adv = Label(self.master,text="Cut Inside First")
        self.Checkbutton_Inside_First_adv = Checkbutton(self.master,text=" ", anchor=W)
        self.Checkbutton_Inside_First_adv.configure(variable=self.inside_first)

        self.Label_Rotary_Enable_adv = Label(self.master,text="Use Rotary Settings")
        self.Checkbutton_Rotary_Enable_adv = Checkbutton(self.master,text="")
        self.Checkbutton_Rotary_Enable_adv.configure(variable=self.rotary)
        trace_variable(self.rotary, self.Reset_RasterPath_and_Update_Time)


        #####
        self.separator_comb = Frame(self.master, height=2, bd=1, relief=SUNKEN)  

        self.Label_Comb_Engrave_adv = Label(self.master,text="Group Engrave Tasks")
        self.Checkbutton_Comb_Engrave_adv = Checkbutton(self.master,text=" ", anchor=W)
        self.Checkbutton_Comb_Engrave_adv.configure(variable=self.comb_engrave)
        trace_variable(self.comb_engrave, self.menu_View_Refresh_Callback)

        self.Label_Comb_Vector_adv = Label(self.master,text="Group Vector Tasks")
        self.Checkbutton_Comb_Vector_adv = Checkbutton(self.master,text=" ", anchor=W)
        self.Checkbutton_Comb_Vector_adv.configure(variable=self.comb_vector)
        trace_variable(self.comb_vector, self.menu_View_Refresh_Callback) 
        #####
        
        self.Label_Reng_passes = Label(self.master,text="Raster Eng. Passes")
        self.Entry_Reng_passes   = Entry(self.master,width="15")
        self.Entry_Reng_passes.configure(textvariable=self.Reng_passes,justify='center',fg="black")
        trace_variable(self.Reng_passes, self.Entry_Reng_passes_Callback)
        self.NormalColor =  self.Entry_Reng_passes.cget('bg')

        self.Label_Veng_passes = Label(self.master,text="Vector Eng. Passes")
        self.Entry_Veng_passes   = Entry(self.master,width="15")
        self.Entry_Veng_passes.configure(textvariable=self.Veng_passes,justify='center',fg="blue")
        trace_variable(self.Veng_passes, self.Entry_Veng_passes_Callback)
        self.NormalColor =  self.Entry_Veng_passes.cget('bg')

        self.Label_Vcut_passes = Label(self.master,text="Vector Cut Passes")
        self.Entry_Vcut_passes   = Entry(self.master,width="15")
        self.Entry_Vcut_passes.configure(textvariable=self.Vcut_passes,justify='center',fg="red")
        trace_variable(self.Vcut_passes, self.Entry_Vcut_passes_Callback)
        self.NormalColor =  self.Entry_Vcut_passes.cget('bg')

        self.Label_Gcde_passes = Label(self.master,text="G-Code Passes")
        self.Entry_Gcde_passes   = Entry(self.master,width="15")
        self.Entry_Gcde_passes.configure(textvariable=self.Gcde_passes,justify='center',fg="black")
        trace_variable(self.Gcde_passes, self.Entry_Gcde_passes_Callback)
        self.NormalColor =  self.Entry_Gcde_passes.cget('bg')

        
        self.Hide_Adv_Button = Button(self.master,text="Hide Advanced", command=self.Hide_Advanced)
                
        # End Right Column #
        self.calc_button = Button(self.master,text="Calculate Raster Time", command=self.menu_Calc_Raster_Time)

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
        
        self.display_power = False
        self.display_test  = False
        if (self.board_name.get()=='LASER-M3'):
            if self.show_power.get():
                self.display_power = True
                if self.show_test.get():
                    self.display_test = True    
            
        x = int(self.master.winfo_x())
        y = int(self.master.winfo_y())
        w = int(self.master.winfo_width())
        h = int(self.master.winfo_height())
        if (self.x, self.y) == (-1,-1):
            self.x, self.y = x,y
        if abs(self.w-w)>10 or abs(self.h-h)>10 or update==1:
            ###################################################
            #  Form changed Size (resized) adjust as required #
            ###################################################
            self.w=w
            self.h=h

            if True:                
                # Left Column #
                w_label=90
                w_entry=46
                w_units=52

                x_label_L=10
                x_entry_L=x_label_L+w_label+20-5
                x_units_L=x_entry_L+w_entry+4
                x_power_L=x_units_L+2 #x_entry_L+w_entry+2 +w_entry+2

                Yloc=10
                self.Initialize_Button.place (x=12, y=Yloc, width=100*2, height=23)
                Yloc=Yloc+33

                self.Open_Button.place (x=12, y=Yloc, width=100, height=40)
                self.Reload_Button.place(x=12+100, y=Yloc, width=100, height=40)                
                if h>=self.pi_mode_height:
                    Yloc=Yloc+50
                    self.separator1.place(x=x_label_L, y=Yloc,width=w_label+75+40, height=2)
                    Yloc=Yloc+6
                    self.Label_Position_Control.place(x=x_label_L, y=Yloc, width=w_label*2, height=21)

                    Yloc=Yloc+25
                    self.Home_Button.place (x=12, y=Yloc, width=100, height=23)
                    self.UnLock_Button.place(x=12+100, y=Yloc, width=100, height=23)

                    Yloc=Yloc+33
                    self.Label_Step.place(x=x_label_L, y=Yloc, width=w_label, height=21)
                    self.Label_Step_u.place(x=x_units_L, y=Yloc, width=w_units, height=21)
                    self.Entry_Step.place(x=x_entry_L, y=Yloc, width=w_entry, height=23)

                    ###########################################################################
                    Yloc=Yloc+30
                    bsz=40
                    xoffst=35
                    self.UL_Button.place    (x=xoffst+12      ,  y=Yloc, width=bsz, height=bsz)
                    self.Up_Button.place    (x=xoffst+12+bsz  ,  y=Yloc, width=bsz, height=bsz)
                    self.UR_Button.place    (x=xoffst+12+bsz*2,  y=Yloc, width=bsz, height=bsz)
                    Yloc=Yloc+bsz
                    self.Left_Button.place  (x=xoffst+12      ,y=Yloc, width=bsz, height=bsz)
                    self.CC_Button.place    (x=xoffst+12+bsz  ,y=Yloc, width=bsz, height=bsz)
                    self.Right_Button.place (x=xoffst+12+bsz*2,y=Yloc, width=bsz, height=bsz)
                    Yloc=Yloc+bsz
                    self.LL_Button.place    (x=xoffst+12      ,  y=Yloc, width=bsz, height=bsz)
                    self.Down_Button.place  (x=xoffst+12+bsz  ,  y=Yloc, width=bsz, height=bsz)
                    self.LR_Button.place    (x=xoffst+12+bsz*2,  y=Yloc, width=bsz, height=bsz)
            
                
                    Yloc=Yloc+bsz
                    ###########################################################################
                    self.Label_GoToX.place(x=x_entry_L, y=Yloc, width=w_entry, height=23)
                    self.Label_GoToY.place(x=x_units_L, y=Yloc, width=w_entry, height=23)
                    Yloc=Yloc+25
                    self.GoTo_Button.place (x=12, y=Yloc, width=100, height=23)
                    self.Entry_GoToX.place(x=x_entry_L, y=Yloc, width=w_entry, height=23)
                    self.Entry_GoToY.place(x=x_units_L, y=Yloc, width=w_entry, height=23)
                    ###########################################################################
                else:
                    ###########################################################################
                    self.separator1.place_forget()
                    self.Label_Position_Control.place_forget()
                    ##    
                    Yloc=Yloc+50
                    self.separator1.place(x=x_label_L, y=Yloc,width=w_label+75+40, height=2)
                    Yloc=Yloc+6
                    self.Home_Button.place (x=12, y=Yloc, width=100, height=23)
                    self.UnLock_Button.place(x=12+100, y=Yloc, width=100, height=23)
                    ##
                    self.Label_Step.place_forget()
                    self.Label_Step_u.place_forget()
                    self.Entry_Step.place_forget()
                    self.UL_Button.place_forget()
                    self.Up_Button.place_forget()
                    self.UR_Button.place_forget()
                    self.Left_Button.place_forget()
                    self.CC_Button.place_forget()
                    self.Right_Button.place_forget()
                    self.LL_Button.place_forget()
                    self.Down_Button.place_forget()
                    self.LR_Button.place_forget()
                    self.Label_GoToX.place_forget()
                    self.Label_GoToY.place_forget()
                    self.GoTo_Button.place_forget()
                    self.Entry_GoToX.place_forget()
                    self.Entry_GoToY.place_forget()
                    ###########################################################################

                #From Bottom up
                BUinit = self.h-70
                Yloc = BUinit
                self.Stop_Button.place (x=12, y=Yloc, width=100*2, height=30)
                
                self.Stop_Button.configure(bg='light coral')
                Yloc=Yloc-10+10

                wadv       = 220 #200
                wadv_use   = wadv-20
                Xvert_sep  = 220
                Xadvanced  = Xvert_sep+10
                w_label_adv= wadv-80 #  110 w_entry

                if self.GcodeData.ecoords == []:
                    self.Grun_Button.place_forget()
                    self.Reng_Veng_Vcut_Button.place_forget()
                    self.Reng_Veng_Button.place_forget()
                    self.Veng_Vcut_Button.place_forget()

                    Yloc=Yloc-30
                    self.Vcut_Button.place      (x=12, y=Yloc, width=100, height=23)
                    self.Entry_Vcut_feed.place  (x=x_entry_L, y=Yloc, width=w_entry, height=23)
                    if (self.display_power):
                        self.Label_Vcut_feed_u.place_forget()
                        self.Entry_Vcut_power.place (x=x_power_L, y=Yloc, width=w_entry, height=23)
                    else:
                        self.Entry_Vcut_power.place_forget()
                        self.Label_Vcut_feed_u.place(x=x_units_L, y=Yloc, width=w_units, height=23)
                    Y_Vcut=Yloc

                    Yloc=Yloc-30
                    self.Veng_Button.place  (x=12, y=Yloc, width=100, height=23)
                    self.Entry_Veng_feed.place(  x=x_entry_L, y=Yloc, width=w_entry, height=23)

                    if (self.display_power):
                        self.Label_Veng_feed_u.place_forget()
                        self.Entry_Veng_power.place(  x=x_power_L, y=Yloc, width=w_entry, height=23)
                    else:
                        self.Entry_Veng_power.place_forget()
                        self.Label_Veng_feed_u.place(x=x_units_L, y=Yloc, width=w_units, height=23)
                    Y_Veng=Yloc
                    
                    Yloc=Yloc-30
                    self.Reng_Button.place  (x=12, y=Yloc, width=100, height=23)
                    self.Entry_Reng_feed.place(  x=x_entry_L, y=Yloc, width=w_entry, height=23)
                    if (self.display_power):
                        self.Label_Reng_feed_u.place_forget()
                        self.Entry_Reng_power.place(  x=x_power_L, y=Yloc, width=w_entry, height=23)
                    else:
                        self.Entry_Reng_power.place_forget()
                        self.Label_Reng_feed_u.place(x=x_units_L, y=Yloc, width=w_units, height=23)

                    Y_Reng=Yloc
                    if self.comb_vector.get() or self.comb_engrave.get():
                        if self.comb_engrave.get():
                            self.Veng_Button.place_forget()                    
                            self.Reng_Button.place_forget()
                        if self.comb_vector.get():
                            self.Vcut_Button.place_forget()
                            self.Veng_Button.place_forget() 
                            
                        if self.comb_engrave.get():
                            if self.comb_vector.get():
                                self.Reng_Veng_Vcut_Button.place(x=12, y=Y_Reng, width=100, height=23*3+14)
                            else:
                                self.Reng_Veng_Button.place(x=12, y=Y_Reng, width=100, height=23*2+7)
                        elif self.comb_vector.get():
                            self.Veng_Vcut_Button.place(x=12, y=Y_Veng, width=100, height=23*2+7)

                    
                    if (self.display_power and h>=self.pi_mode_height):
                        Yloc=Yloc-35
                        self.Label_feed_u.place(x=x_entry_L, y=Yloc, width=w_entry, height=33)
                        self.Label_power_u.place(x=x_power_L, y=Yloc, width=w_entry, height=33)
                        #self.Label_feed_u.configure( bg = 'white', anchor=CENTER )
                        #self.Label_power_u.configure( bg = 'white', anchor=CENTER )
                    else:
                        self.Label_feed_u.place_forget()
                        self.Label_power_u.place_forget()
                        pass

                    if (self.display_test and h>=self.pi_mode_height):
                        Yloc=Yloc-30
                        self.Test_Button.place  (x=12, y=Yloc, width=100, height=23)
                        self.Entry_Test_power.place(  x=x_power_L, y=Yloc, width=w_entry, height=23)
                        self.Entry_Test_time.place(  x=x_entry_L, y=Yloc, width=w_entry, height=23)
                        
                        Yloc=Yloc-35
                        self.Label_time_u.place(x=x_entry_L, y=Yloc, width=w_entry, height=33)
                        self.Label_power2_u.place(x=x_power_L, y=Yloc, width=w_entry, height=33)
                        #self.Label_time_u.configure( bg = 'white', anchor=CENTER )
                        #self.Label_power2_u.configure( bg = 'white', anchor=CENTER )
                    else:
                        self.Test_Button.place_forget()
                        self.Entry_Test_time.place_forget()
                        self.Entry_Test_power.place_forget()
                        self.Label_time_u.place_forget()
                        self.Label_power2_u.place_forget()
                   
                    
                else:
                    self.Vcut_Button.place_forget()
                    self.Entry_Vcut_feed.place_forget()
                    self.Label_Vcut_feed_u.place_forget()
                    self.Entry_Vcut_power.place_forget()
                    
                    self.Veng_Button.place_forget()
                    self.Entry_Veng_feed.place_forget()
                    self.Label_Veng_feed_u.place_forget()
                    self.Entry_Veng_power.place_forget()
                    
                    self.Reng_Button.place_forget()
                    self.Entry_Reng_feed.place_forget()
                    self.Label_Reng_feed_u.place_forget()
                    self.Entry_Reng_power.place_forget()

                    self.Test_Button.place_forget()
                    self.Entry_Test_time.place_forget()
                    self.Entry_Test_power.place_forget()
                    self.Label_time_u.place_forget()
                    self.Label_power2_u.place_forget()

                    self.Reng_Veng_Vcut_Button.place_forget()
                    self.Reng_Veng_Button.place_forget()
                    self.Veng_Vcut_Button.place_forget()

                    self.Label_feed_u.place_forget()
                    self.Label_power_u.place_forget()
                    
                    Yloc=Yloc-30
                    self.Grun_Button.place  (x=12, y=Yloc, width=100*2, height=23)
                    if (self.display_power):
                        Yloc=Yloc-30
                        if (self.display_power):
                            self.Entry_Gcode_power.place(  x=x_power_L, y=Yloc, width=w_entry, height=23)
                        else:
                            self.Entry_Gcode_power.place_forget()
                        d=10
                        Yloc=Yloc-25-d
                        self.Label_power_u.place(x=x_power_L, y=Yloc, width=w_entry, height=23+d)
                        #self.Label_power_u.configure( bg = 'white', anchor=CENTER )
                    else:
                        self.Label_power_u.place_forget()
                        self.Entry_Gcode_power.place_forget()
                        pass
 
                if h>=self.pi_mode_height:
                    if (self.display_power):
                        Yloc=Yloc-5
                    else:
                        Yloc=Yloc-15
                    self.separator2.place(x=x_label_L, y=Yloc,width=w_label+75+40, height=2)
                else:
                    self.separator2.place_forget()
                    
                # End Left Column #

                if self.advanced.get():
                   
                    self.PreviewCanvas.configure( width = self.w-240-wadv, height = self.h-50 )
                    self.PreviewCanvas_frame.place(x=220+wadv, y=10)
                    self.separator_vert.place(x=220, y=10,width=2, height=self.h-50)

                    adv_Yloc=25-10 #15
                    self.Label_Advanced_column.place(x=Xadvanced, y=adv_Yloc, width=wadv_use, height=21)
                    adv_Yloc=adv_Yloc+25
                    self.separator_adv.place(x=Xadvanced, y=adv_Yloc,width=wadv_use, height=2)

                    if h>=self.pi_mode_height:
                        adv_Yloc=adv_Yloc+25-20 #15
                        self.Label_Halftone_adv.place(x=Xadvanced, y=adv_Yloc, width=w_label_adv, height=21)
                        self.Checkbutton_Halftone_adv.place(x=Xadvanced+w_label_adv+2, y=adv_Yloc, width=25, height=23)
                    
                        adv_Yloc=adv_Yloc+25
                        self.Label_Negate_adv.place(x=Xadvanced, y=adv_Yloc, width=w_label_adv, height=21)
                        self.Checkbutton_Negate_adv.place(x=Xadvanced+w_label_adv+2, y=adv_Yloc, width=25, height=23)

                        adv_Yloc=adv_Yloc+25
                        self.separator_adv2.place(x=Xadvanced, y=adv_Yloc,width=wadv_use, height=2)
                    
                        adv_Yloc=adv_Yloc+25-20
                        self.Label_Mirror_adv.place(x=Xadvanced, y=adv_Yloc, width=w_label_adv, height=21)
                        self.Checkbutton_Mirror_adv.place(x=Xadvanced+w_label_adv+2, y=adv_Yloc, width=25, height=23)

                        adv_Yloc=adv_Yloc+25
                        self.Label_Rotate_adv.place(x=Xadvanced, y=adv_Yloc, width=w_label_adv, height=21)
                        self.Checkbutton_Rotate_adv.place(x=Xadvanced+w_label_adv+2, y=adv_Yloc, width=25, height=23)

                        adv_Yloc=adv_Yloc+25
                        self.Label_inputCSYS_adv.place(x=Xadvanced, y=adv_Yloc, width=w_label_adv, height=21)
                        self.Checkbutton_inputCSYS_adv.place(x=Xadvanced+w_label_adv+2, y=adv_Yloc, width=25, height=23)
                    
                        adv_Yloc=adv_Yloc+25
                        self.separator_adv3.place(x=Xadvanced, y=adv_Yloc,width=wadv_use, height=2)

                        adv_Yloc=adv_Yloc+25-20
                        self.Label_Inside_First_adv.place(x=Xadvanced, y=adv_Yloc, width=w_label_adv, height=21)
                        self.Checkbutton_Inside_First_adv.place(x=Xadvanced+w_label_adv+2, y=adv_Yloc, width=25, height=23)
                    
                        adv_Yloc=adv_Yloc+25
                        self.Label_Rotary_Enable_adv.place(x=Xadvanced, y=adv_Yloc, width=w_label_adv, height=21)
                        self.Checkbutton_Rotary_Enable_adv.place(x=Xadvanced+w_label_adv+2, y=adv_Yloc, width=25, height=23)
                    else:
                        #self.Label_Advanced_column.place_forget()
                        #self.separator_adv.place_forget()
                        self.Label_Halftone_adv.place_forget()
                        self.Checkbutton_Halftone_adv.place_forget()
                        self.Label_Negate_adv.place_forget()
                        self.Checkbutton_Negate_adv.place_forget()
                        self.separator_adv2.place_forget()
                        self.Label_Mirror_adv.place_forget()
                        self.Checkbutton_Mirror_adv.place_forget()
                        self.Label_Rotate_adv.place_forget()
                        self.Checkbutton_Rotate_adv.place_forget()
                        self.Label_inputCSYS_adv.place_forget()
                        self.Checkbutton_inputCSYS_adv.place_forget()
                        self.separator_adv3.place_forget()
                        self.Label_Inside_First_adv.place_forget()
                        self.Checkbutton_Inside_First_adv.place_forget()
                        self.Label_Rotary_Enable_adv.place_forget()
                        self.Checkbutton_Rotary_Enable_adv.place_forget()

                    adv_Yloc = BUinit
                    self.Hide_Adv_Button.place (x=Xadvanced, y=adv_Yloc, width=wadv_use, height=30)

                    if self.RengData.image != None:
                        self.Label_inputCSYS_adv.configure(state="disabled")
                        self.Checkbutton_inputCSYS_adv.place_forget()              
                    else:
                        self.Label_inputCSYS_adv.configure(state="normal")
                        
                    if self.GcodeData.ecoords == []:
                        #adv_Yloc = adv_Yloc-40
                        self.Label_Vcut_passes.place(x=Xadvanced, y=Y_Vcut, width=w_label_adv, height=21)
                        self.Entry_Vcut_passes.place(x=Xadvanced+w_label_adv+2, y=Y_Vcut, width=w_entry, height=23)

                        #adv_Yloc=adv_Yloc-30
                        self.Label_Veng_passes.place(x=Xadvanced, y=Y_Veng, width=w_label_adv, height=21)
                        self.Entry_Veng_passes.place(x=Xadvanced+w_label_adv+2, y=Y_Veng, width=w_entry, height=23)

                        #adv_Yloc=adv_Yloc-30
                        self.Label_Reng_passes.place(x=Xadvanced, y=Y_Reng, width=w_label_adv, height=21)
                        self.Entry_Reng_passes.place(x=Xadvanced+w_label_adv+2, y=Y_Reng, width=w_entry, height=23)
                        self.Label_Gcde_passes.place_forget()
                        self.Entry_Gcde_passes.place_forget()
                        adv_Yloc = Y_Reng

                       ####
                        adv_Yloc=adv_Yloc-15
                        self.separator_comb.place(x=Xadvanced-1, y=adv_Yloc, width=wadv_use, height=2)

                        adv_Yloc=adv_Yloc-25
                        self.Label_Comb_Vector_adv.place(x=Xadvanced, y=adv_Yloc, width=w_label_adv, height=21)
                        self.Checkbutton_Comb_Vector_adv.place(x=Xadvanced+w_label_adv+2, y=adv_Yloc, width=25, height=23)
                        
                        adv_Yloc=adv_Yloc-25
                        self.Label_Comb_Engrave_adv.place(x=Xadvanced, y=adv_Yloc, width=w_label_adv, height=21)
                        self.Checkbutton_Comb_Engrave_adv.place(x=Xadvanced+w_label_adv+2, y=adv_Yloc, width=25, height=23)
                        ####
                        
                    else:
                        adv_Yloc=adv_Yloc-40
                        self.Label_Gcde_passes.place(x=Xadvanced, y=adv_Yloc, width=w_label_adv, height=21)
                        self.Entry_Gcde_passes.place(x=Xadvanced+w_label_adv+2, y=adv_Yloc, width=w_entry, height=23)
                        self.Label_Vcut_passes.place_forget()
                        self.Entry_Vcut_passes.place_forget()
                        self.Label_Veng_passes.place_forget()
                        self.Entry_Veng_passes.place_forget()
                        self.Label_Reng_passes.place_forget()
                        self.Entry_Reng_passes.place_forget()

                else:
                    self.PreviewCanvas_frame.place_forget()
                    self.separator_vert.place_forget()
                    self.Label_Advanced_column.place_forget()
                    self.separator_adv.place_forget() 
                    self.Label_Halftone_adv.place_forget()
                    self.Checkbutton_Halftone_adv.place_forget()
                    self.Label_Negate_adv.place_forget()
                    self.Checkbutton_Negate_adv.place_forget()
                    self.separator_adv2.place_forget()
                    self.Label_Mirror_adv.place_forget()
                    self.Checkbutton_Mirror_adv.place_forget()
                    self.Label_Rotate_adv.place_forget()
                    self.Checkbutton_Rotate_adv.place_forget()
                    self.Label_inputCSYS_adv.place_forget()
                    self.Checkbutton_inputCSYS_adv.place_forget()
                    self.separator_adv3.place_forget()
                    self.Label_Inside_First_adv.place_forget()
                    self.Checkbutton_Inside_First_adv.place_forget()

                    self.Label_Rotary_Enable_adv.place_forget()
                    self.Checkbutton_Rotary_Enable_adv.place_forget()

                    self.separator_comb.place_forget()
                    self.Label_Comb_Engrave_adv.place_forget()
                    self.Checkbutton_Comb_Engrave_adv.place_forget()
                    self.Label_Comb_Vector_adv.place_forget()
                    self.Checkbutton_Comb_Vector_adv.place_forget()


                    self.Entry_Vcut_passes.place_forget()
                    self.Label_Vcut_passes.place_forget()
                    self.Entry_Veng_passes.place_forget()
                    self.Label_Veng_passes.place_forget()
                    self.Entry_Reng_passes.place_forget()
                    self.Label_Reng_passes.place_forget()
                    self.Label_Gcde_passes.place_forget()
                    self.Entry_Gcde_passes.place_forget()
                    self.Hide_Adv_Button.place_forget()
                    
                    self.PreviewCanvas.configure( width = self.w-240, height = self.h-50 )
                    self.PreviewCanvas_frame.place(x=Xvert_sep, y=10)
                    self.separator_vert.place_forget()

                self.Set_Input_States()
                
            self.Plot_Data()
            
