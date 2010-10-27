"""
Surround suppression experiment, based on Zenger-Landolt and Heeger (2003)

And on the Psychtoolbox version used to get the data in Yoon et al. (2009 and
2010).

""" 
import gc

import wx
import numpy as np
from ss_classes import Params
from psychopy import core
import psychopy.monitors.calibTools as calib


#This brings in all of the classes defined in ss_classes:
from ss_classes import *
from ss_tools import start_data_file
    
if __name__ == "__main__":
    """ The main function. This actually runs the experiment """

    #Initialize params from file:
    params = Params()
    #For some reason, if this call is inside ss_classes, just importing
    #ss_classes starts an instance of the GUI, so we put it out here:
    app = wx.App()
    app.MainLoop()
    params.set_by_gui()
    
    f = start_data_file(params.subject)

    #Start by saving in the parameter setting:
    params.save(f)
    
    #For now, assume that the target and the annulus are going to have the same
    #orientation: 
    params.target_ori = params.annulus_ori
    
    #This initializes the window:

    #This is the folder where we keep the calibration data:
    calib.monitorFolder = './calibration/'# over-ride the usual setting of
                                          # where monitors are stored
    mon = calib.Monitor(params.monitor) #Get the monitor object and pass that
                                        #as an argument to win:

    
    win = visual.Window(monitor=mon,
                        screen=params.screen,
                        fullscr=params.fullscreen,
                        units=params.display_units)

    #Initialize all the instances of stimulus bits and pieces for reuse: 
    bank = StimulusBank(win,params)

    #Make a trial list:
    trial_list = make_trial_list(win,params)

    #Initialize the staircase, depending on which task is performed
    if params.task == 'Annulus':
        message = """ On which side are the targets in the GRATING?\n Press 1 for left and 2 for right\n Press any key to start""" 
        staircaseA = Staircase(params.start_target_contrastA,
                            params.annulus_contrast/params.contrast_increments,
                            harder = -1, #For this task, higher values are
                                      #actually harder => closer to the annulus
                                      #value
                            ub=params.targetA_contrast_max,
                            lb=params.targetA_contrast_min)
        staircaseB = Staircase(params.start_target_contrastB,
                            params.annulus_contrast/params.contrast_increments,
                            harder = -1, #For this task, higher values are
                                      #actually harder => closer to the annulus
                                      #value
                            ub=params.targetB_contrast_max,
                            lb=params.targetB_contrast_min)
#        staircase = Staircase(params.start_target_contrastB,
#                            params.annulus_contrast/params.contrast_increments,
#                            harder = -1, #For this task, higher values are
#                                      #actually harder => closer to the annulus
#                                      #value
#                            ub=params.target_contrast_max,
#                            lb=params.target_contrast_min
#2                            )
        if params._replay is None:
            #The fixation target appears but has a constant contrast set to the
            #starting point 
            other_contrast = np.ones(len(trial_list)) * params.fix_target_start
        else:
            #Replay a previous run
            other_contrast = params._replay
            
    elif params.task == 'Fixation':
        message = """ On which side are the targets in the FIXATION?\n Press 1 for left and 2 for right\n Press any key to start"""

        #Just one staircase:
        staircaseA = staircaseB = Staircase(params.fix_target_start,
                            params.fix_target_start/params.contrast_increments,
                            harder = -1, 
                            ub=params.fix_target_max,
                            lb=params.fix_target_min
                            )

        if params._replay is None:
            #The annulus target appears and has a constant contrast set to the
            #starting point: 
            other_contrast = np.ones(len(trial_list)) * params.fix_target_start
        else:
            #Replay a previous run:
            other_contrast = params._replay


    #Send a message to the screen and wait for a subject keypress:
    Text(win,text=message,height=0.7)() 

    win.flip()
    
    #If this is in the scanner, we would want to wait for the ttl pulse right
    #here:
    if params.scanner:
       Text(win,text='',keys=['t'])() #Assuming a TTL is a 't' key
       
    #Loop over the event list, while consuming each event, by calling it:
    for trial_idx,this_trial in enumerate(trial_list):
        trial_clock = core.Clock()
        if this_trial.block_type == 'A':
            this_trial.finalize_stim(params,bank,staircaseA,other_contrast[trial_idx])
        elif this_trial.block_type == 'B':
            this_trial.finalize_stim(params,bank,staircaseB,other_contrast[trial_idx])
        this_trial.stimulus()
        if this_trial.block_type == 'A':
            this_trial.finalize_fix(params,bank,staircaseA,other_contrast[trial_idx])
        if this_trial.block_type == 'B':
            this_trial.finalize_fix(params,bank,staircaseB,other_contrast[trial_idx])
        this_trial.fixation()
        this_trial.response.finalize(correct_key = this_trial.correct_key,
                                     file_name=f)
        this_trial.response()
        if this_trial.correct_key is not None:
            this_trial.feedback.finalize(this_trial.response.correct)
        this_trial.feedback()


#Update and save only on trials in which there was a target:
        if trial_idx % params.trials_per_block == 0:
               #On the first trial, insert the header: 
            this_trial.save(f,insert_header=True)
        else:
               #On other trials, just insert the data:
            this_trial.save(f)
            #update after saving:
        if this_trial.block_type == 'A':
            staircaseA.update(this_trial.response.correct)
        elif this_trial.block_type == 'B':
            staircaseB.update(this_trial.response.correct)
        this_trial.wait_iti(trial_clock)

        #dbg
        # trial_clock.getTime()
    
    f.close()
    core.quit()
    
