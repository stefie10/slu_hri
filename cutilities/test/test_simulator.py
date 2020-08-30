from pyTklib import *
import carmen_maptools
from pylab import *
import time
from carmen_util import num_as_str


def test2():
    ion()

    #class noise_model2D{
    tv_nm = noise_model2D(1.0, 0, 0.1, 0.0)
    rv_nm = noise_model2D(0, 1.0, 0.0, 0.1)
    slip_nm = noise_model2D(0, 0, 0.01, 0.0)
    
    #make the papa of noise models here 
    nm =  motion_noise_model_slip(tv_nm, rv_nm, slip_nm)
    x, y, theta = [6, 6, 0]

    #plot the measurements
    reading_plt, = plot([], [], 'ro');

    #true plots
    position_plt, = plot([], [], 'go');
    orient_plt, = plot([], []);

    #corrupted plots
    positionc_plt, = plot([], [], 'ko');
    orientc_plt, = plot([], []);


    #make a simulator, load and plot the map
    mysim = simulator2D(nm, 0.1, "../../data/maps/hurdles.map.gz");
    themap = mysim.get_map()
    carmen_maptools.plot_map(themap, mysim.map.x_size, mysim.map.y_size);


    #do some simulation
    for i in range(300):
        mysim.simulate_motion(1.0, 0.6, 0.1);
        sim_meas = mysim.simulate_measurements();

        if(len(sim_meas) > 0):
            XY = carmen_util_reading_to_xy(mysim.get_true_pose(), sim_meas, -pi/2.0, pi/2.0);
            XYc = carmen_util_reading_to_xy(mysim.get_pose(), sim_meas, -pi/2.0, pi/2.0);
        x, y, theta = mysim.get_true_pose()
        xc, yc, thetac = mysim.get_pose()
        #do some plotting
        reading_plt.set_data(XY[0], XY[1]);
        position_plt.set_data([x], [y]);
        orient_plt.set_data([x, x+cos(theta)], [y, y+sin(theta)]);
        positionc_plt.set_data([xc], [yc]);
        orientc_plt.set_data([xc, xc+cos(thetac)], [yc, yc+sin(thetac)]);
        draw()


        #savefig("video/"+num_as_str(i, buff=6)+".png");
    
    #show()

def test3():
    #class noise_model2D{
    tv_nm = noise_model2D(1.0, 0, 0.1, 0.0)
    rv_nm = noise_model2D(0, 1.0, 0.0, 0.1)
    slip_nm = noise_model2D(0, 0, 0.01, 0.0)
    
    #make the papa of noise models here 
    nm =  motion_noise_model_slip(tv_nm, rv_nm, slip_nm)
    x, y, theta = [6, 6, 0]

    #make a simulator, load and plot the map
    mysim = simulator2D(nm, 0.1, "../../data/maps/hurdles.map.gz");

    #do some simulation
    for i in range(6000):
        mysim.simulate_motion(1.0, 0.6, 0.1);
        sim_meas = mysim.simulate_measurements();
        
        if(len(sim_meas) > 0):
            XY = carmen_util_reading_to_xy(mysim.get_true_pose(), sim_meas, -pi/2.0, pi/2.0);
            XYc = carmen_util_reading_to_xy(mysim.get_pose(), sim_meas, -pi/2.0, pi/2.0);

        x, y, theta = mysim.get_true_pose()
        xc, yc, thetac = mysim.get_pose()
        
if __name__ == "__main__":
    test2()
