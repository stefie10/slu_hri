from pyTklib import SplineC
from pyTklib import noise_model2D, motion_noise_model_slip, observation_noise_model
from pyTklib import simulator2D, occupancy_grid_mapper
from pyTklib import carmen_util_reading_to_xy, tklib_sse
import carmen_maptools
from pylab import *
from scipy import mod
from Spline import Spline
from datatypes import point
from time import sleep


def test1():
    ion()

    tv_nm = noise_model2D(1.0, 0, 0.1, 0.0)
    rv_nm = noise_model2D(0, 1.0, 0.0, 0.1)
    slip_nm = noise_model2D(0, 0, 0.01, 0.0)
    
    #make the papa of noise models here 
    nm =  motion_noise_model_slip(tv_nm, rv_nm, slip_nm)
    onm =  observation_noise_model(0.1, 0.01, 0.0001)
    x, y, theta = [6, 6, 0]

    ax = gca()
    
    #make a simulator, load and plot the map
    mysim = simulator2D([x,y,theta], nm, onm, "/home/tkollar/local/tklib/data/maps/hurdles.map.gz");
    mymap = occupancy_grid_mapper(0.9,0.9, 0.5, 20, 20, 0.1, mysim.get_pose(), 0.17)
    
    myid = carmen_maptools.plot_map(mymap.map.get_map(),
                                    mymap.map.x_size, mymap.map.y_size);
    nn_plt, = plot([], [], 'ro');
    orig_plt, = plot([], [], 'bx');
    icp_plt, = plot([], [], 'gx');
    robot_pose_plt, = plot([], [], 'ko');
    robot_orient_plt, = plot([], [], 'k');
    spline_plt, = plot([], [], 'b');
    spline_pltc, = plot([], [], 'g');

    #do some simulation
    for i in range(1000):
        mysim.simulate_motion(1.0, 0.6, 0.1);
        sim_meas = mysim.simulate_measurements();
        mymap.update(mysim.get_pose(), sim_meas, 2);
        
        x, y, theta = mymap.get_pose()
        if(mod(i, 0) == 0):
            carmen_maptools.plot_map(mymap.map.get_map(), mymap.map.x_size, mymap.map.y_size, cmap="binary");
            ax.images = [ax.images[len(ax.images)-1]]

        #do some spline processing
        x, y, theta = mysim.get_pose()
        spline = Spline(point(x, y, theta), point(9.0, 6.1, 0), 20.0, 20.0)

        X, Y = spline.getVals(arange(0, 1, 0.01))
        spline_plt.set_data(X, Y);
        
        #to C type
        cspline = spline.toCtype()
        X, Y = cspline.value(arange(0, 1, 0.01))
        spline_pltc.set_data(X, Y)

        
        isfree = mymap.map.path_free(cspline)



        if(isfree == 1):
            print "its free"
        elif(isfree == 0):
            print "hit obstacle"
        elif(isfree == -1):
            print "outside map"
        elif(isfree == -2):
            print "hit unknown"

        
        robot_pose_plt.set_data([x], [y]);
        robot_orient_plt.set_data([x, x+0.3*cos(theta)], [y, y+0.3*sin(theta)]);

        draw()
        sleep(0.1)        
        
        
    show()

def test2():
    ion()

    tv_nm = noise_model2D(1.0, 0, 0.1, 0.0)
    rv_nm = noise_model2D(0, 1.0, 0.0, 0.1)
    slip_nm = noise_model2D(0, 0, 0.01, 0.0)
    
    #make the papa of noise models here 
    nm =  motion_noise_model_slip(tv_nm, rv_nm, slip_nm)
    onm =  observation_noise_model(0.1, 0.01, 0.0001)
    x, y, theta = [10, 20, 0]
    
    ax = gca()
    
    #make a simulator, load and plot the map
    print "simulator"
    mysim = simulator2D([x,y,theta], nm, onm, "../../data/maps/thickwean.map");

    print "ogm"
    mymap = occupancy_grid_mapper(0.8,0.8, 0.5, 100, 100, 0.1, mysim.get_pose(), 0.2)
    
    myid = carmen_maptools.plot_map(mymap.map.get_map(), mymap.map.x_size, mymap.map.y_size);
    nn_plt, = plot([], [], 'ro');
    orig_plt, = plot([], [], 'bx');
    icp_plt, = plot([], [], 'gx');
    robot_pose_plt, = plot([], [], 'ko');
    robot_orient_plt, = plot([], [], 'k');
    spline_plt, = plot([], [], 'b');
    spline_pltc, = plot([], [], 'g');
    
    #do some simulation
    for i in range(1000):
        mysim.simulate_motion(1.0, 0.6, 0.1);
        sim_meas = mysim.simulate_measurements();
        
        mymap.update(mysim.get_pose(), sim_meas);
        
        x, y, theta = mymap.get_pose()
        if(mod(i, 5) == 0):
            carmen_maptools.plot_map(mymap.map.get_map(), mymap.map.x_size, mymap.map.y_size, cmap="binary");
            ax.images = [ax.images[len(ax.images)-1]]

        
        #do some spline processing
        x, y, theta = mysim.get_pose()
        #spline = Spline(point(x, y, theta), point(22.0, 27.1, 0), 20.0, 20.0)

        spline = Spline(point(x, y, theta), point(19.0, 20.6, pi/8.0), 30.0, 40.0)
        
        X, Y = spline.getVals(arange(0, 1, 0.01))
        spline_plt.set_data(X, Y);
        
        #to C type
        cspline = spline.toCtype()
        X, Y = cspline.value(arange(0, 1, 0.01))
        spline_pltc.set_data(X, Y)
        
        isfree = mymap.map.path_free(cspline)



        if(isfree == 1):
            print "its free"
        elif(isfree == 0):
            print "hit obstacle"
        elif(isfree == -1):
            print "outside map"
        elif(isfree == -2):
            print "hit unknown"

        robot_pose_plt.set_data([x], [y]);
        robot_orient_plt.set_data([x, x+0.3*cos(theta)], [y, y+0.3*sin(theta)]);

        draw()
        
        
    show()
    
if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test2()

