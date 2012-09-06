#from matplotlib.backends.backend_wx import Toolbar, FigureCanvasWx,\
     #FigureManager
import wx
import matplotlib
matplotlib.use('WxAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas,\
     FigureManager
import numpy as np
from psychopy import *
import numpy
import time
import numpy.random
from wx import *
from matplotlib.figure import Figure

# for our monitors: contr=100%, bright=50%
rslope = 2.201
gslope = 2.473
bslope = 2.055
vda = 9156 # empirical: mean of values after 50

# Based on line fitting of the overall for one of the monitors, with the range of indices from 0 to 1:
oslope = 2.4
oint = 4.95
#indices = linspace(0,1,256*6)
#backsteal = 768

myred = "#800000"

class PlotFigure(wx.Frame):
    def __init__(self, title='Pyception results'): #, style=wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP):
    #def __init__(self,title='Pyception Lab', pos=None, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE|wx.DIALOG_NO_PARENT):
        Frame.__init__(self, None, -1, title, style=wx.STAY_ON_TOP|wx.RESIZE_BORDER) # style=wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP)
        #try:
            #wx.Dialog.__init__(self, None,-1,title)
        #except:
            #global app
            #app = wx.PySimpleApp()
            #wx.Dialog.__init__(self, None,-1,title) 
        #wx.Dialog.__init__(self, None,-1,title="Pyception results")
#style=style|wx.RESIZE_BORDER

        #self.fig = Figure((9,8), 75)
        self.fig = Figure()
        self.canvas = FigCanvas(self, -1, self.fig)
        #self.toolbar = Toolbar(self.canvas)
        #self.toolbar.Realize()

        # On Windows, default frame size behaviour is incorrect
        # you don't need this under Linux
        #tw, th = self.toolbar.GetSizeTuple()
        #fw, fh = self.canvas.GetSizeTuple()
        #self.toolbar.SetSize(Size(fw, th))

        # Create a figure manager to manage things
        self.figmgr = FigureManager(self.canvas, 1, self)
        # Now put all into a sizer
        sizer = BoxSizer(VERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(self.canvas, 1, LEFT|TOP|GROW)
        # Best to allow the toolbar to resize!
        #sizer.Add(self.toolbar, 0, GROW)

        btn = wx.Button(self, label='Close')
        btn.Bind( wx.EVT_BUTTON, self.onClose)
        sizer.Add(btn, 0, GROW)

        self.SetSizer(sizer)
        self.Fit()

    def onClose(self, event):
        self.eventLoop.Exit()
        self.Close()

    def ShowModal(self):
        self.MakeModal()
        self.fig.show()
        self.Show()
        self.eventLoop = wx.EventLoop()
        self.eventLoop.Run()

    #def plot_data(self):
        ## Use ths line if using a toolbar
        #a = self.fig.add_subplot(111)

        # Or this one if there is no toolbar
        #a = Subplot(self.fig, 111)

        #t = numpy.arange(0.0,3.0,0.01)
        #s = numpy.sin(2*numpy.pi*t)
        #c = numpy.cos(2*numpy.pi*t)
        #a.plot(t,s)
        #a.plot(t,c)
        #self.toolbar.update()

    #def GetToolBar(self):
        # You will need to override GetToolBar if you are using an
        # unmanaged toolbar in your frame
        #return self.toolbar

class MyDlg(wx.Dialog):
    def __init__(self,title='Pyception Lab', pos=None, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE|wx.DIALOG_NO_PARENT):
        style=style|wx.RESIZE_BORDER
        self.aborted = False
        try:
            wx.Dialog.__init__(self, None,-1,title,pos,size,style)
        except:
            global app
            app = wx.PySimpleApp()
            wx.Dialog.__init__(self, None,-1,title,pos,size,style) 

        sizer = wx.FlexGridSizer( 12, 2, 5, 5)

        label0 = wx.StaticText( self, -1, "Number of observers:") 
        label1 = wx.StaticText( self, -1, "Threshold determination method:") 
        label2 = wx.StaticText( self, -1, "Task type:") 
        label3 = wx.StaticText( self, -1, "Stimulus:")
        label4 = wx.StaticText( self, -1, "Background level (cd/m2):")
        labelStimSize = wx.StaticText( self, -1, "Stimulus size:")
        label5 = wx.StaticText( self, -1, "Incr. values (Weber fracs.):")
        label6 = wx.StaticText( self, -1, "Trials per value:")
        label65 =wx.StaticText( self, -1, "Catch trial sets:")
        label7 = wx.StaticText( self, -1, "Stimulus duration (secs):")
        label8 = wx.StaticText( self, -1, "Show stimulus frame:")
        label9 = wx.StaticText( self, -1, "Show 2AFC line:")
        #labelFix = wx.StaticText( self, -1, "No fixation") 
        #labelFix = wx.StaticText( self, -1, " 5 deg fixation") 
        #labelFix = wx.StaticText( self, -1, "10 deg fixation") 
        #labelFix = wx.StaticText( self, -1, "15 deg fixation") 
        #label3 = wx.StaticText( self, -1, "Stimulus:") 
        #label4 = wx.StaticText( self, -1, "Background level:") 
        #label5 = wx.StaticText( self, -1, "Stimulus level:") 
        #label6 = wx.StaticText( self, -1, "Show frame:") 
        threshold_methods_list = ['Constant Stimuli', 'Hybrid: Adj/CS', 'Ascending Limits', 'Descending Limits']
        task_type = ['Yes/No', '2AFC']
        stimulus_type = ['"E" optotype', 'Tiny square', 'Large square']

        #self.button =wx.Button(self, label="Push me")
        #self.OK = wx.Button( self, wx.ID_OK, " OK ")
        self.methods_list = wx.ListBox( self, -1, choices= threshold_methods_list ) 
        self.type_list = wx.ListBox( self, -1, choices=task_type) 
        self.stimulus_list = wx.ListBox( self, -1, choices=stimulus_type) 
        self.background = wx.TextCtrl( self, -1 )
        self.stimulus_values = wx.TextCtrl( self, -1 )

        self.txtStimSize = wx.TextCtrl( self, -1 )

        self.fixN = wx.RadioButton( self, -1, 'No fixation', style=wx.RB_GROUP)
        self.fix5 = wx.RadioButton( self, -1, '5 deg fixation')
        self.fix10 = wx.RadioButton( self, -1, '10 deg fixation')
        self.fix15 = wx.RadioButton( self, -1, '15 deg fixation')

        self.whichLum = wx.RadioButton( self, -1, 'Luminance', style=wx.RB_GROUP)
        self.whichTemp1 = wx.RadioButton( self, -1, 'Temporal Summation 1' )
        #self.whichTemp2 = wx.RadioButton( self, -1, 'Temporal Summation 2' )
        #self.whichSpatial = wx.RadioButton( self, -1, 'Spatial Summation')

        #self.stimulus_values.SetValue( '[0, 0, 2, 4, 8, 12, 32]' )
        self.reps = wx.TextCtrl( self, -1 )
        self.catches = wx.TextCtrl( self, -1 )
        self.duration = wx.TextCtrl( self, -1 )
        self.show_frame = wx.CheckBox( self, -1 )
        self.show_line = wx.CheckBox( self, -1 )
        #self.show_fixation = wx.CheckBox( self, -1 )
        self.observers = wx.TextCtrl( self, -1 )
        self.btn_run =wx.Button(self, label="Run experiment")
        #self.btn_abort =wx.Button(self, label="Run experiment")
        #self.OK = wx.Button( self, wx.ID_OK, " OK ")
        #self.btn_abort.Bind( wx.EVT_BUTTON, self.abort)
        self.btn_run.Bind( wx.EVT_BUTTON, self.run )

        # Defaults:
        self.methods_list.SetSelection(1) # constant stim, adjust, lims, etc.
        self.stimulus_list.SetSelection(1) # E vs. square
        self.type_list.SetSelection(1) # YN, 2afc
        #self.whichTemp1.SetValue(0) # Luminance 
        self.background.SetValue( '5.0' ) # 30
        #self.stimulus_values.SetValue( '[ 2, 4, 8, 12, 32]' ) # catchtrials are added later
        self.stimulus_values.SetValue( '0.01, 0.03, 0.05, 0.1' ) # catchtrials are added later
        self.reps.SetValue( '8' )
        self.catches.SetValue( '2' )
        self.duration.SetValue( '0.010' )
        self.observers.SetValue( "3" )
        self.show_frame.SetValue( False )
        self.show_line.SetValue( True )
        self.txtStimSize.SetValue( '5' )

        sizer.Add( label0)
        sizer.Add( self.observers)
        sizer.Add( label1)
        sizer.Add( self.methods_list)
        sizer.Add( label2)
        sizer.Add( self.type_list)
        sizer.Add( label3)
        sizer.Add( self.stimulus_list)

        sizer.Add( self.whichLum)
        sizer.Add( self.whichTemp1 )
        #sizer.Add( self.whichTemp2 )
        #sizer.Add( self.whichSpatial)

        sizer.Add( labelStimSize)
        sizer.Add( self.txtStimSize)

        sizer.Add( label4)
        sizer.Add( self.background)
        sizer.Add( label5)
        sizer.Add( self.stimulus_values)
        sizer.Add( label6)
        sizer.Add( self.reps)
        sizer.Add( label65)
        sizer.Add( self.catches)
        sizer.Add( label7)
        sizer.Add( self.duration)
        sizer.Add( label8)
        sizer.Add( self.show_frame)
        sizer.Add( label9)
        sizer.Add( self.show_line)
        #sizer.Add( labelFix )

        sizer.Add( self.fixN)
        sizer.Add( self.fix5)
        sizer.Add( self.fix10)
        sizer.Add( self.fix15)

        sizer.Add( self.btn_run)
        border = wx.BoxSizer()
        border.Add( sizer, 0, wx.ALL, -1 )
        self.SetSizerAndFit(border)
        self.Fit()

    def abort(self, event):
        self.aborted = True
        self.Close()

    def run(self, event):
        self.aborted = False
        self.Close()

def abslum( (r,g,b) ):
    return ((r**rslope+g**gslope+b**rslope))/vda

stealpat = [ [-1,-1,0], [0,-1,0], [0,-1,1], [-1,0,-1], [-1,0,0], [0,0,0] ]
stealpatlen = len(stealpat)
def gentable2( r ):
    vals = np.zeros( len(r) * stealpatlen )
    coords = np.zeros( (len(r) * stealpatlen,3) )
    count = 0
    for baseval in r:
        for (r,g,b) in stealpat:
        #for (r,g,b) in ([-1,-1,-1], [-1,-1,0], [-1,0,-1], [-1,0,0], [0,-1,-1], [0,-1,0], [0,0,-1] ):
        #for (r,g,b) in ([-1,-1,-1], [-1,-1,0], [0,-1,-1], [0,-1,0], [-1,0,-1], [0,0,-1], [-1,0,0] ):
                coords[count] = [baseval+r, baseval+g, baseval+b ]
                #vals[count] = abslum( (baseval+r, baseval+g, baseval+b )    )
                vals[count] = abslum( coords[count] )
                count += 1
    withkeys = numpy.array([ (val,n) for n,val in enumerate(vals) ], [('val',float), ('idx', int) ] )
    #return sort( withkeys, order='val' )
    return withkeys,coords

def possible(r):
    poss = gentable2( r )
    figure();
    plot( np.arange(len(r)* stealpatlen), poss['val'], 'k.-' )
    for n,val in enumerate(r):
        plot( [0,len(r)*stealpatlen], np.tile(abslum( (val,val,val ) ),2), 'b--' )  
    
steallum = gentable2( np.arange(256) )[0]['val']
stealcoords = gentable2( np.arange(256) )[1]

def ltoidx( l ):
    return int( round( l**(1.0/oslope)/numpy.exp(oint/oslope)*(256*stealpatlen) ) )

def buildtrialseq():
    #global trialseq, method, stimval, stimreps, trial_inA, maxtrials
    global trialseq, trial_inA, maxtrials, results
    # Repeat each stim value the given number of times. With tile() it repeats the array,
    # This repeats each element in order. 
    trialseq = numpy.array( [numpy.tile(stimval,stimreps) for stimval in stimvals] ).flatten()
    if method == methDL: 
        trialseq = trialseq[::-1]
    elif method == methCS:
        # TODO: Should put catch trials in some other place
        if task_type==taskYN:
            trialseq = numpy.concatenate( ( numpy.tile([catchval],catch_trials*stimreps), trialseq) )

        trialseq = numpy.random.permutation( trialseq )
    
    if which_expt==exptL:
        trialseq = numpy.concatenate( ([allwhitesteal], trialseq) )
    else:
        trialseq = numpy.concatenate( ( [10/100.0], trialseq) ) # 10 ticks
    maxtrials = len(trialseq)

    if task_type==task2afc:
        trial_inA = numpy.random.permutation( numpy.tile( numpy.array([True,False]), numpy.ceil(maxtrials/2.0) ) )
        trial_inA = numpy.concatenate( ([True],trial_inA) )

    results = numpy.zeros( (num_observers, maxtrials) )

def drawstim():
    if (task_type==taskYN) or (which_expt == exptT1) :
        if stimulus_type==stimE:
            if show_frame:
                theframe.draw()
            target.setColor( "#%02X%02X%02X" % (rgb[0],rgb[1], rgb[2]) )
        else:
            target.setFillColor( "#%02X%02X%02X" % (rgb[0],rgb[1], rgb[2]) )
        target.draw()
    else: # task2afc:
        if trial_inA[trial]:
            rgbA = stealcoords[stolen]
            rgbB = stealcoords[backsteal]
        else:
            rgbA = stealcoords[backsteal]
            rgbB = stealcoords[stolen]

        if stimulus_type==stimE:
            targetA.setColor( "#%02X%02X%02X" % (rgbA[0],rgbA[1], rgbA[2]) )
            targetB.setColor( "#%02X%02X%02X" % (rgbB[0],rgbB[1], rgbB[2]) )
        else:
            targetA.setFillColor( "#%02X%02X%02X" % (rgbA[0],rgbA[1], rgbA[2]) )
            targetB.setFillColor( "#%02X%02X%02X" % (rgbB[0],rgbB[1], rgbB[2]) )
        if show_line:
            theLine.draw()

        targetA.draw()
        targetB.draw()
        if show_frame:
            theframeA.draw()
            theframeB.draw()

    if show_fix:
        theFix1.draw()
        theFix2.draw()
        
fullscr = False  # make sure this matches next
#screendim = (1024,768)
screendim = ( 800, 600 )
screensize = 100.0 / 36.0 # pix/cm for Sony Trinitron
distance = 400.0 # mm
fixation_text='+'

SubjectName = 'dc2' 

refresh_rate = 1/100.0 # we can push the monitors to 100 Hz

# Set up the screen, etc.
#myWin = visual.Window(screendim, allowGUI=True, color=backcol, units='pix', fullscr=fullscr )
myWin = visual.Window(screendim, allowGUI=True, units='pix', fullscr=fullscr )

message  = visual.TextStim(myWin,pos=(-200,140), alignHoriz='left',height=16, ori=00, color=(-1.00,-1.00,-1.00))
message0 = visual.TextStim(myWin,pos=(-200,220), alignHoriz='left',height=16, ori=00, color=(-1.00,-1.00,-1.00))
message1 = visual.TextStim(myWin,pos=(-200,200), alignHoriz='left',height=16, ori=00, color=(-1.00,-1.00,-1.00))
message2 = visual.TextStim(myWin,pos=(-200,180), alignHoriz='left',height=16, ori=00, color=(-1.00,-1.00,-1.00))
message0.setText("Subject 1: 'a' = Yes/Left , 's'=No/Right.")
message1.setText("Subject 2: 'v' = Yes/Left, 'b'=No/Right.")
message2.setText("Subject 3: 'k' = Yes/Left, 'l'=No/Right.")

taskYN = 0
task2afc = 1
stimE = 0
stimSmSq = 1
stimLgSq = 2
methCS=0
methA=1
methAL=2
methDL=3

exptL=0
exptT1=1
exptT2=2
exptS=3

displaytext = visual.TextStim(myWin,pos=(0,280),alignHoriz='center', height=14, font='Arial', color=myred ) 
count = visual.TextStim(myWin,pos=(0,200), color=(-1,-1,-1), height=20, text="ready")

disptext = "'bak=%s stealidx=%d steallum=%f rgb=%s' % ( str(backcol),stolen, steallum[stolen], str(rgb) )"
disptext = "'L=%03.3f deltaL=%03.3f dl/L=%03.3f, (Lfore=%03.3f)' % ( steallum[backsteal], steallum[stolen]-steallum[backsteal], (steallum[stolen]-steallum[backsteal])/steallum[backsteal], steallum[stolen] )"

alldone=False
while not alldone:
    theDlg = MyDlg()
    theDlg.ShowModal()

    if theDlg.aborted==True:
        alldone=True
        continue

    #myWin.setMouseVisible(False)

    backcd = float( theDlg.background.GetValue() )

    backsteal = ltoidx( backcd )
    abslumtemp = backsteal

    #backsteal = int( theDlg.background.GetValue() )
    num_observers = int( theDlg.observers.GetValue() )
    stimreps = int( theDlg.reps.GetValue() )
    catch_trials = int( theDlg.catches.GetValue() )
    ontime = float( theDlg.duration.GetValue() )
    stimsize_pixels = int( theDlg.txtStimSize.GetValue() )

    #elif theDlg.whichTemp2.GetValue():
        #which_expt = exptT2
    #elif theDlg.whichSpatial.GetValue():
        #which_expt = exptS

    task_type = theDlg.type_list.GetSelection()
    stimulus_type = theDlg.stimulus_list.GetSelection()
    method = theDlg.methods_list.GetSelection()
    show_frame = theDlg.show_frame.GetValue()
    show_line = theDlg.show_line.GetValue()
    show_fix = not (theDlg.fixN.GetValue() )
    # TODO: make sure show_frame == True works!! 09/15

    if theDlg.whichLum.GetValue():
        which_expt = exptL
    elif theDlg.whichTemp1.GetValue():
        which_expt = exptT1
        show_line = False

    #stimvals = numpy.array( eval(theDlg.stimulus_values.GetValue()) ) + backsteal
    stimvalsfrac = numpy.array( eval( '[' + theDlg.stimulus_values.GetValue() + ']') ) 

    if which_expt==exptL:
        stimvals = numpy.array( [ltoidx( backcd+backcd*x) for x in stimvalsfrac]  ) 
    else:
        stimvals = stimvalsfrac

    if which_expt==exptL:
        disptext = "'bak=%s stealidx=%d steallum=%f rgb=%s' % ( str(backcol),stolen, steallum[stolen], str(rgb) )"
    else:
        disptext = "'time=%f lum=%f' % ( stolen, abslumtemp)"

    continc = 1
    backcol = (stealcoords[backsteal]-127.0)/128.0#[0,0,0]
    #backcol=( "#404040" )
    myWin.setColor( backcol )
    
    if show_fix:
        if theDlg.fix5.GetValue():
            fixlocY = 100
        elif theDlg.fix10.GetValue():
            fixlocY = 100*2
        elif theDlg.fix15.GetValue():
            fixlocY = 100*3
        fixheight=5; fixwidth=5
        theFix1 = visual.ShapeStim( myWin, vertices=((0,fixlocY-fixheight), (0,fixlocY+fixheight)), lineWidth=1, closeShape=False, lineColor="black")
        theFix2 = visual.ShapeStim( myWin, vertices=((0-fixwidth,fixlocY), (0+fixwidth,fixlocY)), lineWidth=1, closeShape=False, lineColor="black")

    framec=75

    # To avoid errors, create something off-screen
    theLine = visual.ShapeStim( myWin, vertices=((1200,1200),(1200,1210)), lineWidth=1, closeShape=False, lineColor=myred)

    if (task_type==task2afc) and (which_expt==exptL):
        if stimulus_type==stimE:
            let_height = 100
            abloc=100
            theframeA = visual.ShapeStim(myWin,pos=(-abloc,0),vertices=((-framec,-framec), (-framec,framec), (framec,framec), (framec,-framec) ), lineColor="white", fillColor=None )
            theframeB = visual.ShapeStim(myWin,pos=(abloc,0),vertices=((-framec,-framec), (-framec,framec), (framec,framec), (framec,-framec) ), lineColor="white", fillColor=None )
            targetA   = visual.TextStim(myWin,pos=(-abloc,0), color=backcol, height=let_height, text="E")
            targetB = visual.TextStim(myWin,pos=( abloc,0), color=backcol, height=let_height, text="E")

            theLine = visual.ShapeStim( myWin, vertices=((0,let_height/3.0), (0,-let_height/3.0)), lineWidth=3, closeShape=False, lineColor=myred)

        elif stimulus_type==stimSmSq:
            sqrad=stimsize_pixels
            abloc=sqrad * 4
            #theframeA = visual.ShapeStim(myWin,pos=(abloc*3.0,0),vertices=((-framec,-framec), (-framec,framec), (framec,framec), (framec,-framec) ), lineColor=backcol, fillColor=None )
            #theframeB = visual.ShapeStim(myWin,pos=(abloc*3.0,0),vertices=((-framec,-framec), (-framec,framec), (framec,framec), (framec,-framec) ), lineColor=backcol, fillColor=None )
            theLine = visual.ShapeStim( myWin, vertices=((0,sqrad*3), (0,-sqrad*3)), lineWidth=2, closeShape=False, lineColor=myred)

            targetA = visual.ShapeStim(myWin,pos=(-abloc,0), vertices=((-sqrad,-sqrad), (-sqrad,sqrad), (sqrad,sqrad), (sqrad,-sqrad) ), lineColor=backcol ) 
            targetB = visual.ShapeStim(myWin,pos=( abloc,0), vertices=((-sqrad,-sqrad), (-sqrad,sqrad), (sqrad,sqrad), (sqrad,-sqrad) ), lineColor=backcol ) 
        elif stimulus_type==stimLgSq:
            abloc= 300
            sqrad = 100
            target = visual.ShapeStim(myWin,pos=(0,0), vertices=((-sqrad,-sqrad), (-sqrad,sqrad), (sqrad,sqrad), (sqrad,-sqrad) ), lineColor=backcol ) 
            theLine = visual.ShapeStim( myWin, vertices=((0,sqrad*1.5), (0,-sqrad*1.5)), lineWidth=1, closeShape=False, lineColor=myred)

            targetA = visual.ShapeStim(myWin,pos=(-abloc,0), vertices=((-sqrad,-sqrad), (-sqrad,sqrad), (sqrad,sqrad), (sqrad,-sqrad) ), lineColor=backcol ) 
            targetB = visual.ShapeStim(myWin,pos=( abloc,0), vertices=((-sqrad,-sqrad), (-sqrad,sqrad), (sqrad,sqrad), (sqrad,-sqrad) ), lineColor=backcol ) 

    else: # taskYN | temp1 
        if stimulus_type==stimE:
            theframe = visual.ShapeStim(myWin,vertices=((-framec,-framec), (-framec,framec), (framec,framec), (framec,-framec) ), lineColor="white", fillColor=None )
            target = visual.TextStim(myWin,pos=(0,0), color=backcol, height=100, text="E")
        elif stimulus_type==stimSmSq:
            sqrad = 10
            target = visual.ShapeStim(myWin,pos=(0,0), vertices=((-sqrad,-sqrad), (-sqrad,sqrad), (sqrad,sqrad), (sqrad,-sqrad) ), lineColor=backcol ) 
        elif stimulus_type==stimLgSq:
            sqrad = 250
            target = visual.ShapeStim(myWin,pos=(0,0), vertices=((-sqrad,-sqrad), (-sqrad,sqrad), (sqrad,sqrad), (sqrad,-sqrad) ), lineColor=backcol ) 

    # Other controls:
    done = False
    display=False
    allwhitesteal = 200*stealpatlen
    catchval = 0 + backsteal

    offtime = 0 # 0.270
    counttime = 0.225

    if (task_type==task2afc) and (which_expt==exptL):
        if stimulus_type==stimE:
            targetA.setColor( "#%02X%02X%02X" % (stealcoords[allwhitesteal][0], stealcoords[allwhitesteal][1], stealcoords[allwhitesteal][2]) )
            targetB.setColor( "#%02X%02X%02X" % (stealcoords[backsteal][0], stealcoords[backsteal][1], stealcoords[backsteal][2]) )
        else:
            targetA.setFillColor( "#%02X%02X%02X" % (stealcoords[allwhitesteal][0], stealcoords[allwhitesteal][1], stealcoords[allwhitesteal][2]) )
            targetB.setFillColor( "#%02X%02X%02X" % (stealcoords[backsteal][0], stealcoords[backsteal][1], stealcoords[backsteal][2]) )

        if show_line:
            theLine.draw()
        if show_frame:
            theframeA.draw()
            theframeB.draw()

        targetA.draw()
        targetB.draw()
    else:
        if stimulus_type == stimE:
            target.setColor( "#%02X%02X%02X" % (stealcoords[allwhitesteal][0], stealcoords[allwhitesteal][1], stealcoords[allwhitesteal][2]) )
        else:
            target.setFillColor( "#%02X%02X%02X" % (stealcoords[allwhitesteal][0], stealcoords[allwhitesteal][1], stealcoords[allwhitesteal][2]) )
        if show_frame:
            theframe.draw()
        target.draw()

    if method==methA:
        message.setText("Use up and down arrows until just below threshold.\nThen use 't' to enter constant stimuli (and respond with YN/2AFC keys above).")
    elif task_type==task2afc:
        message.setText("The first trial will be a test trial. Which side has the the white flashed target? Press any key to start.")
    else:
        message.setText("The first trial will be a test trial. Do you see the white flashed target? Press any key to start.")

    if show_fix:
        theFix1.draw()
        theFix2.draw()
        
    message.draw()
    message0.draw()
    if num_observers>1:
        message1.draw()
    if num_observers>2:
        message2.draw()
    myWin.flip()
    event.waitKeys()
    message.setText("")

    if which_expt == exptT1:
        stolen = 0.001
        continc = 0.001 # inc/dev by ms
    else:
        stolen = backsteal # start at 127,127,127 (= background) # start at this

    resp_keys = numpy.array( ['a','s', 'v','b', 'k', 'l'] )

    trial = 0

    buildtrialseq()

    # Main loop
    while not done:
        if not (method == methA):
            stolen = trialseq[trial]

        if which_expt == exptT1:
            rgb = stealcoords[abslumtemp]# hardcode
        else:
            rgb = stealcoords[stolen]

        # Countdown:
        if not (method == methA):
            if show_line:
                theLine.draw()

            if show_fix:
                theFix1.draw()
                theFix2.draw()

            count.draw()
            myWin.flip()
            core.wait(counttime)

        # Drawing text during brief stimuli is too risky
        #if display:
            #displaytext.setText( eval(disptext) )
            #displaytext.draw()
    
        # Loop for a certain number of 'flips'
        if which_expt==exptT1:
            fliploop = stolen*100
            fliploop = 1 # on for just 1 flip
            while fliploop > 0:
                drawstim()
                myWin.flip()
                fliploop -= 1
            fliploop = stolen #*100
            if (method==methA) or ((task==task2afc) and not (trial_inA[trial])):
                if show_fix:
                    theFix1.draw()
                    theFix2.draw()
                myWin.flip()
                core.wait(fliploop)
                #while fliploop > 0:
                    #yWin.flip()
                    #liploop -= 1
            #if not (trial_inA[trial]):
            fliploop = 1 # on for just 1 flip
            while fliploop > 0:
                drawstim()
                myWin.flip()
                fliploop -= 1
        else:
            drawstim()
            if ontime>0:    
                myWin.flip()
                core.wait(ontime)
    
        if display:
            displaytext.setText( eval(disptext) )
            displaytext.draw()

        if show_line:
            theLine.draw()

        if show_fix:
            theFix1.draw()
            theFix2.draw()

        if not (method==methA):
            message0.draw()
            if num_observers>1:
                message1.draw()
            if num_observers>2:
                message2.draw()

        myWin.flip()
        #core.wait(offtime) # Unnecessary ?
    
        gotall=False
        resps = numpy.tile( False, num_observers)
        while not gotall:
            for key in event.getKeys():
                if key in [ 'q' ]:
                    alldone = True
                    done = True
                if key in [ 'escape' ]:
                    done = True
                elif key in [ 'left' ]:
                    abslumtemp -= 1
                elif key in [ 'right' ]:
                    abslumtemp += 1
                elif key in [ 'down' ]:
                    stolen -= continc
                elif key in [ 'home' ]:
                    stolen = 0
                elif key in [ 'equal' ]:
                    stolen = backsteal 
                elif key in [ 'end' ]:
                    stolen = len(stealcoords)-1
                elif key in [ 'up' ]:
                    stolen += continc
                elif key in [ 'r' ]:
                    repeat = (repeat == False)
                elif key in [ '0' ] :
                    key = '10'
                elif key in [ 'quoteleft']:
                    key = '0'
                elif key in [ 'd']:
                    display = (display==False)
                elif key in [ 't']:
                    # hybrid: switch to 2afc constant stim. based on initial manual thresh est.
                    # make 5 points between: halfway btwn. 0 and their threshold and this + their threshold
                    stimvals = numpy.array( [numpy.floor(x) for x in numpy.linspace( (stolen-backsteal)/4.0+backsteal, (stolen-backsteal)/2.0+stolen, 5 )], dtype='int' )
                    if which_expt==exptT1:
                        stimvals = numpy.array( [numpy.floor(x) for x in numpy.linspace( stolen/4.0, stolen/2.0+stolen, 5 )], dtype='int' )
                    #stimvals = numpy.array( [ltoidx( backcd+backcd*x) for x in stimvalsfrac]  ) 
                    #stimvals = numpy.array( [ltoidx( backcd+backcd*x) for x in stimvalsfrac]  ) 
                    method=methCS
                    buildtrialseq()
                    continue

                elif key in resp_keys:
                    try:
                        (obs,idx) = divmod( numpy.where( resp_keys == key )[0][0], 2)
                        resps[obs] = True
                        results[obs, trial] = idx
                        gotall = all(resps)
                    except:
                        gotall = all(resps)
                    
                if method==methA:
                    gotall = True
                else:
                    if not resps[0]:
                        message0.draw()
                    if num_observers>1:
                        if not resps[1]:
                            message1.draw()
                        if num_observers>2:
                            if not resps[2]:
                                message2.draw()
                    if show_line:
                        theLine.draw()
                    if show_fix:
                        theFix1.draw()
                        theFix2.draw()
                    myWin.flip()

        if not (method==methA):
            trial += 1

        if trial==maxtrials:
            done=True
        
    if task_type==taskYN: # TODO: put earlier?
        #trial_inA=(trialseq==catchval) # for Y/n, first/left/0 key is 'Yes'  # the 0 is unfortunate...
        trial_inA=numpy.tile(0,maxtrials)  # For YN, it's just freq of seeing, not correct...
    else:
        # TODO: there are more 'trial_inA's than there should be
        trial_inA = (trial_inA[0:maxtrials]==False)

    # Post process: collate and display
    trial_correct = numpy.array([ trial_inA == results[subj, :] for subj in numpy.arange(num_observers) ])
    
    if method==methA:
        doplot = False
    else:
        doplot = True

    if doplot:
        tots = [ [len( numpy.where( numpy.all( (trialseq==stim,trial_correct[subj]),0))[0]) for stim in stimvals] for subj in numpy.arange(num_observers) ]
        FAs = [ [len( numpy.where( numpy.all( (trialseq==stim,trial_correct[subj]),0))[0]) for stim in [catchval] ] for subj in numpy.arange(num_observers) ]

        myWin.setMouseVisible(True)
        theResults = PlotFigure()

        for i in numpy.arange(num_observers):
            subp = theResults.fig.add_subplot( '32%d'%(i*2+1), title='Subject %i' % (i+1) )
            #xtext = subp.set_xlabel('Weber fraction ($\Delta I/I$)') 
            xtext = subp.set_xlabel('$\Delta I$') 

            if task_type == taskYN:
                ytext = subp.set_ylabel('Prop. seen') 
            else:
                ytext = subp.set_ylabel('Prop. corr.')
            #pyplot.plot( stimvals, numpy.array(tots[i]) / float(stimreps), 'o-' )
            #subp.plot( [(abslum(coord)-abslum(stealcoords[backsteal]))/abslum(stealcoords[backsteal]) for coord in stealcoords[stimvals]], numpy.array(tots[i]) / float(stimreps), 'o-' )

            if which_expt==exptL:
                xvals = [(abslum(coord)-abslum(stealcoords[backsteal])) for coord in stealcoords[stimvals]]
            #pyplot.xticks( numpy.arange(len(stimvals)), [str('%.2f') % (abslum(coord)-abslum(stealcoords[backsteal])) for coord in stealcoords[stimvals]] ) 
            #subp.suptitle( 'Subject %i' % (i+1))
                subp.semilogx()
            elif which_expt==exptT1:
                xvals = stimvals

            subp.plot( xvals, numpy.array(tots[i]) / float(stimreps), 'o-' )

            xl = subp.get_xlim()
            subp.plot( xl, [0.75,0.75],  'k--' )

            ypad = 0.1
            subp.grid()
            #subp.set_ylim( (0.5-ypad, 1+ypad) )    
            subp.set_ylim( (0.5, 1.0) ) 

            #subp.set_xlim( (0.001, 0.23 ) )     # Let it float now
            #subp.ylim( 0-0.1,1.0+0.1 )
            #subp.xlabel( 'Weber fraction ($\Delta I/I$)')
            #subp.ylabel( 'Prop. seen')
            #pyplot.legend( ['%i' % i for i in numpy.arange(num_observers)] )
            #pyplot.show(f)

            if task_type==taskYN:
                #subp2 = theResults.fig.add_subplot( '32%d'%(i*2+2))
                subp.text( 1.25, 0.8, 'Hits: %02d/%02d ' % ( sum(tots[i]),stimreps*(len(stimvals)) )) # TODO: not generic for hits/misses
                subp.text( 1.25, 0.5, 'False Alarms: %02d/%02d ' % ( ( (FAs[i][0]),stimreps*catch_trials))) # TODO: not generic for hits/misses 

        theResults.fig.subplots_adjust(hspace=1.2)
        theResults.ShowModal()

    # main loop: while !alldone

myWin.close()
