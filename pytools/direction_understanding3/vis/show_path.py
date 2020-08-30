import cPickle
from sys import argv
from tag_util import tag_file
from du.eval_util import model_evaluator
from du.explore import explore
from logfile_util import logfile_du
from pylab import *
from pyTklib import *
import carmen_maptools
from copy import copy
from math import atan2
from carmen_util import num_as_str
import os

'''Goal is to show the locations 
in the map and the set of images through which 
the robot transtions'''

def plot_map(filename):
    #show the gridmap
    gridmap  = tklib_log_gridmap()
    gridmap.load_carmen_map(argv[5]);
    themap = gridmap.to_probability_map_carmen();
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);

def initialize_plots():
    figure(0)
    #ion()
    subplot(121)
    plot_map(argv[5])
    p1, = plot([], [], 'go')
    p2, = plot([], [], 'bo')
    axis('off')
    
    subplot(122)
    p3 = imshow(zeros([964,1296,3]), origin='lower')
    axis('off')

    #subplot(223)
    figure(1)
    p4, = plot([], [], 'k.', markersize=0.5)
    p5, = plot([], [], 'go')
    
    p7, = plot([], [], 'g^')
    p6, = plot([], [], 'r^')

    p8, = plot([], [], 'g-')
    

    #axis('off')

    return p1, p2, p3, p4, p5, p6, p7, p8

def show_path(me, lf, sentence, start_region, 
              use_laser=True, use_images=True, use_exploration=False, save_files=False):
    p1, p2, p3, p4, p5, p6, p7, p8 = initialize_plots()
    
    path, probs, sdcs_eval = None, None, None
    sdcs, frontiers, frontiers_all = None, None, None
    
    print "evaluating sentence"
    if(not use_exploration):
        path, probs, sdcs_eval, sdcs= me.evaluate_sentence(mysentence, start_region=start_region)
    else:
        print "doing exploration"
        #res = me.evaluate_sentence_explore(mysentence, start_pose=(23.82, 48.89, 0))
        res = me.evaluate_sentence_explore(mysentence, start_region=start_region)
        path, probs, sdcs_eval, sdcs, frontiers, frontiers_all, front_allowed = res
        
        full_path = [path[:,0]]
        full_path.extend(copy(frontiers))
        full_path.append(path[:,-1])
        path = transpose(full_path)

    #print "frontiers, sdcs", len(frontiers), len(sdcs)
    #raw_input()
    
    skel_map = me.get_skeleton_map()
    grid_map = me.get_skeleton_map().get_map()

    X_full, Y_full = [], []
    X_topo, Y_topo = [], []
    #Laser_X, Laser_Y = [], []
    Laser_XY = []

    myim = None
    fig_i = 0
    for i in range(len(path[0])-1):
        X, Y = skel_map.compute_path(path[0:2,i], path[0:2,i+1])
        
        #curr_orient = path[2,i]
        #fin_orient = path[2,i+1]
        #title(str(sdcs[i]))
        if(sdcs_eval[i]['verb'] == None):
            sdcs_eval[i]['verb']=""
        if(sdcs_eval[i]['sr'] == None):
            sdcs_eval[i]['sr']="" 
        if(sdcs_eval[i]['landmark'] == None):
            sdcs_eval[i]['landmark']="" 
        
        figure(0)
        if(not use_exploration):
            title(sdcs_eval[i]['verb']+" "+sdcs_eval[i]['sr']+" "+sdcs_eval[i]['landmark'])
        elif(i < len(sdcs)):
            title(str(sdcs[i]))
        figure(1)

        if(use_exploration and i < len(frontiers)):
            #front_allowed = front_allowed)
            #print front_allowed[i]
            #raw_input()
            
            print "fall:", transpose(frontiers_all[i])
            #p7.set_data(front_allowed[i][0], front_allowed[i][1])
            myfrontiers_all = transpose(frontiers_all[i])
            print "plotting", myfrontiers_all[0,:], myfrontiers_all[1,:]
            p7.set_data(myfrontiers_all[0,:], myfrontiers_all[1,:])
            
            best_frontier = frontiers[i]
            p6.set_data([best_frontier[0]], [best_frontier[1]])

            figure(1)
            draw()
            if(save_files):
                savefig("../output_vid/"+num_as_str(fig_i)+"_keyframe.png")

            #axis([-30, 30, -30, 30])
            #draw()
            
            #raw_input()

        th = None
        for j in range(len(X)):
            #X_full.append(X[j]);
            #Y_full.append(Y[j]);
            X_full = [X[j]]; Y_full = [Y[j]]
            p1.set_data(X_full, Y_full)

            if(j < len(X)-1):
                th = atan2(Y[j+1]-Y[j], X[j+1]-X[j])
            #sf = j*1.0/len(X)*1.0
            #rotation = tklib_normalize_theta(fin_orient-curr_orient)

            ther, theim_str, odom = lf.get_readings([X[j], Y[j], th])
            
            ############################################
            #get the laser readings
            if(use_laser):
                D=grid_map.ray_trace(X[j], Y[j], linspace(0,2*pi,360));
                
                Laser_newX = X[j] + D*cos(linspace(0,2*pi,360))
                Laser_newY = Y[j] + D*sin(linspace(0,2*pi,360))
                
                #if(len(Laser_XY) > 2000):
                #    Laser_XY = Laser_XY[len(Laser_XY)-2000:]

                #add the points only if they are new points
                for m in range(len(Laser_newX)):
                    if(not [Laser_newX[m], Laser_newY[m]] in Laser_XY):
                        Laser_XY.append([Laser_newX[m], Laser_newY[m]])

                print "length", len(Laser_XY)
                Laser_X, Laser_Y = transpose(Laser_XY)
                p4.set_data(Laser_X, Laser_Y)
                p5.set_data([X[j]], [Y[j]])
                
                p8.set_data([X[j], X[j]+cos(th)], [Y[j], Y[j]+sin(th)])

                curra = [min(Laser_X), max(Laser_X), min(Laser_Y), max(Laser_Y)]
                offset = max([curra[1]-curra[0], curra[3]-curra[2]])
                axis([curra[0]-5.0, curra[0]+offset+5.0, 
                      curra[2]-5.0, curra[2]+offset+5.0])
                axis('off')

            if(use_images):
                #get the images
                myim = lf.get_image(theim_str)
                p3.set_data(myim)

            figure(0)
            draw()
            figure(1)
            draw()
            if(save_files):
                print "saving:", "../output_vid/"+num_as_str(fig_i)+"_im.jpg"
                savefig("../output_vid/"+num_as_str(fig_i)+"_map.png")
                lf.save_image(theim_str, "../output_vid/"+num_as_str(fig_i)+"_im.jpg")


                if(i < len(sdcs)):
                    myoutfile=open("../output_vid/"+num_as_str(fig_i)+".txt", 'w')
                    myoutfile.write("curr_sdc:"+ str(sdcs[i]))
                    myoutfile.close()
                    
                fig_i+=1

        X_topo.append(X_full[-1])
        Y_topo.append(Y_full[-1])
        p2.set_data(X_topo, Y_topo)

        draw()
        #raw_input()

    show()




if __name__=="__main__":
    if(len(argv) == 6):
        print "loading logfile"
        lf = logfile_du(argv[1], argv[2])
        
        print "loading model evaluator"
        #try out standard inference
        gtruth_tf = tag_file(argv[4], argv[5])
        me = model_evaluator(cPickle.load(open(argv[3], 'r')), gtruth_tf, "d8")
        
        #mysentence = "Go through the doors and past the elevators to the fountains"

        #mysentence = ''' Go through the door near the
        #elevators. Continue straight past the whiteboard.  Turn left
        #at the end of the hall.  Then turn right and go straight to
        #the end of the hall towards the kitchen area.  Take a left and
        #go through the doors, you should see a nice view.'''

        #mysentence = '''Exit through the door at the left.  Go through
        #the hallway following it around as it turns right.  Take a
        #right and then a quick left.  Go through the double doors,
        #another set of double doors and enter ther room with couches
        #and a nice view.'''


        #mysentence = '''Start facing the whiteboard.  Go down the exit
        #at right, take a right and go past the cubby holes.  Enter the
        #lounge that has a beautiful view of Boston and go toward the
        #couches.  Exit through the double doors, and take a quick
        #left.  Enter the glass-walled elevator lobby.'''
        


        # works with Naive Bayes, but it's ugly because of "screen."
        #mysentence = '''Start at the computers.  Turn right down the
        #hall.  Continue straight.  You will go past some mailboxes.
        #Walk past the stairs, through the room with a nice view
        #towards the screen and couches. Continue left through the
        #double doors, and then turn left to the lobby.'''

        mysentence = '''Go through the double doors and past the
        lobby.  Go into a lounge with some couches. Enjoy the nice
        view.  Go past the spiral staircase.  Continue towards the
        hallway with the cubby holes.  But don't go down that
        hallway. Instead take a right into the kitchen.'''
        
        
        show_path(me, lf, mysentence, "R9", 
                  use_laser=True, use_images=True, use_exploration=True, save_files=True)

    else:
        print "usage:\n\tpython evaluate_model.py log_fn image_dir dg_model.pck gtruth.tag map_filename"

