"""

Surround suppression experiment, based on Zenger-Landolt and Heeger (2003)

And on the Psychtoolbox version used to get the data in Yoon et al. (2009 and
2010).

""" 
import wx
import numpy as np
from ss_classes import Params
from psychopy import gui

#This brings in all of the classes defined in ss_classes:
from ss_classes import *

if __name__ == "__main__":
    """ The main function. This actually runs the experiment """

    #Initialize params from file:
    params = Params()
    app = wx.App()
    params.set_by_gui(app)
    app.MainLoop()

    if params.stimulus_condition == 0: #Parallel
        params.annulus_ori = params.surround_ori
    elif params.stimulus_condition == 1: #Orthogonal
        params.annulus_ori = params.surround_ori + 90 
        
    #After this is done, info now has in it what the user put in there.

##     #This initializes the window (for now, this is just a part of monitor 0):
##     win = visual.Window([800,600],allowGUI=True)

##     #Compile a list of events
##     #XXX TODO
        
##     #Loop over this list, while consuming each event, by calling it:
    
## ##     for this_event in event_list:
        
## ##         this_event.finalize(inputs) #What needs to be provided as input 
## ##         result = this_event(other_inputs) #The __call__ method makes the event
## ##                                         #actually happen

## ##         #Record the result of this event somehow and pass it on to the next
## ##         #event in the line. Maybe update the staircase at this point? 

##     win.close()
