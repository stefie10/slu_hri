from pyTklib import noise_model2D, motion_noise_model_slip
from pyTklib import simulator2D, occupancy_grid_mapper
from pyTklib import carmen_util_reading_to_xy, tklib_sse
from pyTklib import observation_noise_model
import carmen_maptools
from pylab import *
from scipy import mod

def test1():
    ion()

    #class noise_model2D{
    tv_nm = noise_model2D(1.0, 0, 0.1, 0.0)
    rv_nm = noise_model2D(0, 1.0, 0.0, 0.1)
    slip_nm = noise_model2D(0, 0, 0.01, 0.0)
    
    #make the papa of noise models here 
    nm =  motion_noise_model_slip(tv_nm, rv_nm, slip_nm)
    onm =  observation_noise_model(0.1, 0.01, 0.0001)
    x, y, theta = [6, 6, 0]
    
    #make a simulator, load and plot the map
    
    print "loading simulator"
    mysim = simulator2D(nm, onm, "/home/tkollar/local/repositories/tklib/data/maps/thickwean.map");

    print "starting gridmapper"
    mymap = occupancy_grid_mapper(0.9,0.9, 0.5, 20, 20, 0.1, mysim.get_pose(), 0.17)
    carmen_maptools.plot_map(mysim.map.get_map(), mysim.map.x_size, mysim.map.y_size);
    
    nn_plt, = plot([], [], 'ro');
    orig_plt, = plot([], [], 'bx');
    #do some simulation
    for i in range(100):
        #mysim.simulate_motion(1.0, 0.6, 0.1);
        sim_meas = mysim.simulate_measurements();

        print "starting"
        if(len(sim_meas) > 0):
            pts = carmen_util_reading_to_xy(mysim.get_pose(), sim_meas);

        #x, y, theta = mysim.get_true_pose()
        #xc, yc, thetac = mysim.get_pose()
        #print pts
        X, Y = pts
        orig_plt.set_data(X, Y);
        if(i==0):
            if(len(sim_meas) > 0):
                mymap.update_icp(1.0*0.1, 0.6*0.1, sim_meas);

        X, Y = mymap.nearest_neighbors_map_alloc(pts);
        nn_plt.set_data(X, Y);
        
        #print X, Y
        draw()

        #carmen_maptools.plot_map(mymap.map.get_map(), mymap.map.x_size, mymap.map.y_size, cmap="binary");
        #savefig("video/"+num_as_str(i, buff=6)+".png");
    show()

def test2():
    ion()

    #class noise_model2D{
    tv_nm = noise_model2D(1.0, 0, 0.1, 0.0)
    rv_nm = noise_model2D(0, 1.0, 0.0, 0.1)
    slip_nm = noise_model2D(0, 0, 0.01, 0.0)
    
    #make the papa of noise models here 
    nm =  motion_noise_model_slip(tv_nm, rv_nm, slip_nm)
    onm =  observation_noise_model(0.1, 0.01, 0.0001)
    x, y, theta = [6, 6, 0]
    
    #make a simulator, load and plot the map
    #mysim = simulator2D([x,y,theta], nm, onm, "/home/tkollar/local/tklib/data/maps/hurdles.map.gz");
    
    mysim = simulator2D(nm, onm, "/home/tkollar/local/repositories/tklib/data/maps/hurdles.map.gz");
    mymap = occupancy_grid_mapper(0.9,0.9, 0.5, 20, 20, 0.1, mysim.get_pose(), 0.17)
    #carmen_maptools.plot_map(mysim.map.get_map(), mysim.map.x_size, mysim.map.y_size);

    nn_plt, = plot([], [], 'ro');
    orig_plt, = plot([], [], 'bx');
    icp_plt, = plot([], [], 'gx');
    robot_pose_plt, = plot([], [], 'ko');
    robot_orient_plt, = plot([], [], 'k');
    
    #do some simulation
    for i in range(10):
        mysim.simulate_motion(1.0, 0.6, 0.1);
        sim_meas = mysim.simulate_measurements();
        if(len(sim_meas) > 0):
            pts = carmen_util_reading_to_xy(mysim.get_pose(), sim_meas);
        
        X, Y = pts
        orig_plt.set_data(X, Y);
        print "updating map"
        if(len(sim_meas) > 0):
            mymap.update_icp(mysim.get_pose(), sim_meas, 1);
        
        X, Y = mymap.icp_map(pts, 1);
        icp_plt.set_data(X, Y);
        
        X, Y = mymap.nearest_neighbors_map_alloc(pts);
        nn_plt.set_data(X, Y);

        x, y, theta = mymap.get_pose()
        robot_pose_plt.set_data([x], [y]);
        robot_orient_plt.set_data([x, x+0.3*cos(theta)], [y, y+0.3*sin(theta)]);
        
        
        
        carmen_maptools.plot_map(mymap.map.to_probability_map(), mymap.map.x_size, mymap.map.y_size, cmap="binary");
        
        draw()
    show()


def test3():
    A = array([[1,2,3,4],[5,6,7,8]])
    B = array([[2,3,4,5],[6,7,8,12]])
    sse = tklib_sse(A, B);
    print sse


def test4():
    ion()

    #class noise_model2D{
    tv_nm = noise_model2D(1.0, 0, 0.1, 0.0)
    rv_nm = noise_model2D(0, 1.0, 0.0, 0.1)
    slip_nm = noise_model2D(0, 0, 0.01, 0.0)
    
    #make the papa of noise models here 
    nm =  motion_noise_model_slip(tv_nm, rv_nm, slip_nm)
    onm =  observation_noise_model(0.1, 0.01, 0.0001)
    x, y, theta = [6, 6, 0]

    ax = gca()
    
    #make a simulator, load and plot the map
    #print "starting simulator"
    mysim = simulator2D(nm, onm, "/home/tkollar/repositories/tklib/data/maps/hurdles.cmf.gz");
    #print "occupancy grid mapper"
    mymap = occupancy_grid_mapper(0.9,0.9, 0.5, 20, 20, 0.1,
                                  mysim.get_pose(), 0.3, -pi/2.0, pi/2.0)

    myid = carmen_maptools.plot_map(mymap.map.to_probability_map_carmen(),
                                    mymap.map.x_size, mymap.map.y_size);
    nn_plt, = plot([], [], 'ro');
    orig_plt, = plot([], [], 'bx');
    icp_plt, = plot([], [], 'gx');
    robot_pose_plt, = plot([], [], 'ko');
    robot_orient_plt, = plot([], [], 'k');

    #do some simulation
    for i in range(1000):
        mysim.simulate_motion(1.0, 0.6, 0.1);
        sim_meas = mysim.simulate_measurements();
        if(len(sim_meas) > 0):
            mymap.update(mysim.get_pose(), sim_meas);


        if(mod(i, 5) == 0):
            print mymap.map.to_probability_map()
            carmen_maptools.plot_map(mymap.map.to_probability_map_carmen(),
                                     mymap.map.x_size, mymap.map.y_size);
            ax.images = [ax.images[len(ax.images)-1]]

        x, y, theta = mysim.get_pose();
        robot_pose_plt.set_data([x], [y]);
        robot_orient_plt.set_data([x, x+0.3*cos(theta)], [y, y+0.3*sin(theta)]);
        draw()
        
    show()
    
if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()
