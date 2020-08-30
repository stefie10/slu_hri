import math
import pyCarmen
from Tkinter import *
import tkMessageBox
from multiprocessing import Process, Array, Value
from du.controller.carmen import RobotCallback
import sys
import cPickle
from du.dir_util import direction_parser_sdc
from scipy import transpose

def create_gui():
    global mytext

    root = Tk()
    
    root.title("Tkinter Entry Widget")
    root["padx"] = 40
    root["pady"] = 20       

    # Create a text frame to hold the text Label and the Entry widget
    textFrame = Frame(root)
    
    #Create a Label in textFrame
    entryLabel = Label(textFrame)
    entryLabel["text"] = "Enter the text:"
    entryLabel.pack(side=LEFT)

    # Create an Entry Widget in textFrame
    mytext = StringVar()
    entryWidget = Entry(textFrame, textvariable=mytext)
    entryWidget["width"] = 50
    entryWidget.pack(side=LEFT)

    textFrame.pack()

    button = Button(root, text="Submit", command=set_command)
    button.pack() 
    root.mainloop()

def set_command():
    global mytext

    curr_command=""

    if mytext.get().strip() == "":
        print "Got Nothing"
    else:
        print "Got =" + mytext.get().strip()
        curr_command = mytext.get().strip()

    mytext.set("")
    run_direction_inference(curr_command)
    
def run_direction_inference(curr_command):
    global curr_goal, curr_location, dg_model, sdc_parser, is_goal
    
    keywords = sdc_parser.extract_SDCs(curr_command)
    vals, lprob, sdc_eval = dg_model.infer_path(keywords, curr_location[0:2], [curr_location[2]])
    
    path_pred = []
    for myreg in vals:
        topo, orient = myreg.split("_")
        path_pred.append(dg_model.tmap_locs[float(topo)])

    path_pred = transpose(path_pred)
    
    print "mypath", path_pred
    print curr_command
    curr_goal[0] = path_pred[0,-1]
    curr_goal[1] = path_pred[1,-1]
    is_goal.value = 1
    #print "current pose:", curr_pose
    print "set goal to:", curr_goal
    print "current location:", curr_location[0], curr_location[1], curr_location[2]
    
    
def navigator_run(is_goal, curr_goal, curr_pose):
    #curr_goal, curr_pose = myargs

    print "carmen"
    robot = RobotCallback().__disown__()

    print "loc"
    loc = pyCarmen.global_pose(robot)

    #robot.initialize_pose(5.3, 11.5, 0)
    #robot.set_goal(15, 12)
    #robot.command_go()

    while True:
        pyCarmen.carmen_ipc_sleep(0.1)
        
        #print is_goal
        if(is_goal.value == 1):
            print "setting goal", curr_goal[0], curr_goal[1]
            robot.set_goal(curr_goal[0], curr_goal[1])
            robot.command_go()
            is_goal.value=0
            print "G",

        if robot.has_data:
            #print "pos", robot.position
            #print "orient", math.degrees(robot.orientation)
            #print "my command:", curr_command
            print ".",
            #print robot.position
            curr_pose[0] = robot.position[0]
            curr_pose[1] = robot.position[1]
            curr_pose[2] = robot.orientation
            
            sys.stdout.flush()

    

def run_everything(model_filename):
    global curr_goal, curr_location, dg_model, sdc_parser, is_goal
    
    dg_model = cPickle.load(open(model_filename, 'r'))
    sdc_parser = direction_parser_sdc()

    is_goal = Value('i', 0)
    curr_goal = Array('d', [sys.maxint, sys.maxint])
    curr_location = Array('d', [sys.maxint, sys.maxint, sys.maxint])
    p2 = Process(target=navigator_run, args=(is_goal, curr_goal, curr_location))
    
    print "started the gui"
    p2.start()
    #p2.join()
    create_gui()


if __name__ == "__main__":
    if(len(sys.argv) == 2):
        run_everything(sys.argv[1])
    else:
        print "usage:\n\tpython run_carmen.py model_filename.pck"
