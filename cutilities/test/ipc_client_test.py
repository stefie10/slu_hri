import pyTklib
from tklib_ipc import *
from scipy import zeros

if __name__ == "__main__":
    myhandler = tklib_ipc_handler().__disown__()
    pyTklib.subscribe_spline_free_request_message(myhandler);
    pyTklib.subscribe_spline_free_response_message(myhandler);
    pyTklib.subscribe_ekf_message(myhandler);
    pyTklib.subscribe_gridmapping_pose_message(myhandler);

    pyTklib.subscribe_trajopt_config_message(myhandler);
    pyTklib.subscribe_trajopt_config_message(myhandler);
    pyTklib.subscribe_trajopt_destinations_message(myhandler);
    pyTklib.subscribe_trajopt_stop_message(myhandler);
    pyTklib.subscribe_trajopt_go_message(myhandler);
    pyTklib.subscribe_trajopt_curr_spline_message(myhandler);

    i=0
    while(1):
        #ekf message
        #pyTklib.carmen_publish_ekf_message([10, 11, 12], [[1,2,3], [4,5,6], [7,8,9]]);
        
        #spline request
        pyTklib.carmen_publish_spline_free_request_message(pyTklib.SplineC([0, 0, 0], [1, 1, 1], 10.0, 10.0));
        
        #spline response isfree
        #pyTklib.carmen_publish_spline_free_response_message(2, 10);
        #pyTklib.carmen_publish_gridmapping_pose_message(1, 2, 3);

        
        #pyTklib.carmen_publish_trajopt_config_message(i);
        #pyTklib.carmen_publish_trajopt_set_destinations_message([[1,2,3,4],[5,6,7,8]]);

        pyTklib.carmen_publish_current_spline_message(pyTklib.SplineC([0, 9, 10], [1, 2, 3], 10.0, 15.0));

        #pyTklib.carmen_publish_trajopt_go_message();
        #pyTklib.carmen_publish_trajopt_stop_message();
        pyTklib.carmen_ipc_sleep(0.05);
    
        i+=1
