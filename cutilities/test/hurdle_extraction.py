import carmen_maptools
from pylab import *
import time
from carmen_util import num_as_str
from pyTklib import *

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

    #plot the measurements
    reading_plt, = plot([], [], 'ro');

    #true plots
    position_plt, = plot([], [], 'go');
    orient_plt, = plot([], []);

    #corrupted plots
    positionc_plt, = plot([], [], 'ko');
    orientc_plt, = plot([], []);

    hurdles_plt, = plot([], [], 'k^', markersize=10);
     
    #make a simulator, load and ploxt the map
    #mysim = simulator2D(array([x,y,theta]), nm, onm, "/home/tkollar/local/tklib/data/maps/hurdles.map.gz");
    mysim = simulator2D(nm, onm, "../../data/maps/longwood.map");
    mysim.add_hurdles(0.2413, 0.03, 20)
    
    #"/home/tkollar/local/tklib/data/maps/hurdles.map.gz");
    
    
    themap = mysim.map.get_map()
    carmen_maptools.plot_map(themap, mysim.map.x_size, mysim.map.y_size);

    #do some simulation
    for i in range(300):
        mysim.simulate_motion(1.0, 0.6, 0.1);
        sim_meas = mysim.simulate_measurements();
        x, y, theta = mysim.get_true_pose()
        xc, yc, thetac = mysim.get_pose()

        if(len(sim_meas) > 0):
            XY = carmen_util_reading_to_xy(mysim.get_true_pose(), sim_meas);
            XYc = carmen_util_reading_to_xy(mysim.get_pose(), sim_meas);
            #do some plotting
            reading_plt.set_data(XY[0], XY[1]);
            
        position_plt.set_data([x], [y]);
        orient_plt.set_data([x, x+cos(theta)], [y, y+sin(theta)]);
        positionc_plt.set_data([xc], [yc]);
        orientc_plt.set_data([xc, xc+cos(thetac)], [yc, yc+sin(thetac)]);

        hurdles = mysim.simulate_extracted_hurdles(mysim.get_true_pose())
        if(len(hurdles) > 0):
            hurdles_plt.set_data(hurdles[0], hurdles[1])

        draw()


if __name__=="__main__":
    test1()
