import matplotlib_qt
import pyCarmen
from du.controller.carmen import RobotCallback
from du import dir_util
import basewindow
import modelBrowser
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from pyTklib import kNN_index, tklib_normalize_theta
import math
from math import radians
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import scipy as na
import traceback
import socket
import math2d
import xmlRpc_ui


class MainWindow(QMainWindow, xmlRpc_ui.Ui_MainWindow):
    def __init__(self, m4du, corpus_fname=None, addFigureToMainWindow=True):
        QMainWindow.__init__(self)
        self.setupUi(self)

        

class Server:
    def __init__(self, entryWnd, modelBrowser):
        self.entryWnd = entryWnd
        self.mbWnd = modelBrowser
        class RequestHandler(SimpleXMLRPCRequestHandler):
            rpc_paths = ('/du',)

        host = socket.gethostname()
        print "host", host
        #self.server = SimpleXMLRPCServer((host, 4242),
        #                                 requestHandler=RequestHandler)
        self.server = SimpleXMLRPCServer(("127.0.0.1", 4242),
                                         requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.server.register_function(self.directionsToPath, 'directionsToPath')

        self.server.register_function(self.loadDirections, 'du.sendCommand')


    
        self.entryWnd.connect(self.entryWnd.submitButton,
                              SIGNAL("clicked()"),
                              self.sendCommand)



        self.robot = RobotCallback().__disown__()
        self.loc = pyCarmen.global_pose(self.robot)
        self.goal = None
        self.curr_pose = [0, 0]
        self.yaw = 0

        self.timer = QTimer()
        self.entryWnd.connect(self.timer, SIGNAL("timeout()"),
                              self.processCarmen)
        self.timer.start(50)

        
    def setGoal(self, curr_goal):
        print "setting goal", curr_goal
        self.robot.set_goal(curr_goal[0], curr_goal[1])
        #self.robot.command_go()

    def processCarmen(self):

        pyCarmen.carmen_ipc_sleep(0.1)

        if self.robot.has_data:
            self.curr_pose[0] = self.robot.position[0]
            self.curr_pose[1] = self.robot.position[1]
            self.yaw = self.robot.orientation
            

    


    @property
    def m4du(self):
        return self.mbWnd.m4du
           
    def loadDirections(self, directions):
        self.entryWnd.inputTextEdit.setPlainText(directions)
        return True
        
    def sendCommand(self, directions=None):
        print 'got', directions
        if  directions != None:
            self.loadDirections(directions)
        else:
            directions = str(self.entryWnd.inputTextEdit.toPlainText())

        print "pose", self.curr_pose
        waypoints = self.directionsToWaypoints(directions, self.curr_pose[0], self.curr_pose[1], 
                                               1, self.yaw, 0, 0)
        print "going to", waypoints[-1]
        xyz, yaw = waypoints[-1]
        self.setGoal(xyz[0:2])
        return True

    def directionsToWaypoints(self, directions, x, y, z, yaw, pitch, roll):
        start_xyz = na.array((x, y, z))
        loc_index, = kNN_index((x, y, z),
                               na.transpose([self.m4du.tmap_locs_3d[x] for x in self.m4du.tmap_keys]),
                               1)
        
        topo_key = self.m4du.tmap_keys[int(loc_index)]
            


        yaw = tklib_normalize_theta(yaw)
        if yaw < 0:
            yaw += 2*math.pi
        orient = yaw
        print "yaw", math.degrees(yaw)
        curr_theta = yaw
        #orient = get_orientations_annotated(self.m4du, region, self.dataset_name)[0][0]
        
        orients = [na.append(self.m4du.orients, 360.0)]
        print "orients", orients
        i_tmp, = kNN_index([math.degrees(orient)], orients, 1);
        print "i",i_tmp
        i_tmp = int(i_tmp % len(self.m4du.orients))
        vp = str(topo_key) + "_" + str(self.m4du.orients[i_tmp])
        print "topo_key", topo_key, topo_key.__class__
        print "vp", vp
        vp_i = self.m4du.vpt_to_num[vp]
        print "vp", self.m4du.vpt_to_num
        #vp_i = self.m4du.
        print "vp", vp_i
        path = self.mbWnd.runSentence(directions, vp_i)
        
        
        path_as_locs = [(start_xyz, orient)]
        for p in path:
            topo, orient = p.split("_")
            xyz = self.m4du.tmap_locs_3d[float(topo)].tolist()
            theta = radians(float(orient))
            path_as_locs.append((xyz, theta))

        return path_as_locs

    def directionsToPath(self, directions, x, y, z, yaw, pitch, roll):
        path_as_locs = self.directionsToWaypoints(directions, x, y, z, 
                                                  yaw, pitch, roll)
            
        waypoints = []
        for (s_xyz, s_p_theta), (e_xyz, e_p_theta) in zip(path_as_locs, path_as_locs[1:]):

            X, Y = self.m4du.clusters.skel.compute_path(s_xyz[0:2], e_xyz[0:2])


            last = None
            curr_theta = s_p_theta
            curr_z = s_xyz[2]
            end_z = e_xyz[2]
            start_z = s_xyz[2]
            for i, (x, y) in enumerate(zip(X, Y)):
                print i, (x, y)
                z = start_z + i * (end_z - start_z)/len(X) 
                if last != None:
                    print "last", last
                    print "x", (x, y)
                    curr_theta = math2d.direction(last, (x, y))
                if len(s_xyz) == 3:
                    waypoints.append([float(n) for n in
                                      (x, y, z, curr_theta, 0.0, 0.0)])
                else:
                    waypoints.append([float(n) for n in
                                      (x, y, z, curr_theta, 0.0, 0.0)])
                last = (x, y)
                                                       


        step = 1
        if math2d.normalizeAngleMinusPiToPi(curr_theta - e_p_theta) < math2d.normalizeAngleMinusPiToPi(e_p_theta - curr_theta):
            sign = 1
        else:
            sign = -1

        theta = curr_theta
        while math.fabs(math2d.normalizeAngleMinusPiToPi(e_p_theta - theta)) > 2:
            waypoints.append([float(n) for n in
                              (x, y, e_xyz[2], theta, 0.0, 0.0)])

            theta += step*sign                
            
        z = e_xyz[2]
        for i in range(10):
            
            waypoints.append([float(n) for n in
                              (x, y, z, e_p_theta, 0.0, 0.0)])
            #z += 0.1

        print "start", curr_theta
        print "endtheta", e_p_theta
        print "sign", sign
        print "waypoints", waypoints


        return waypoints
        

    # Register a function under a different name
    def directionsToPath(self, *args):
        try:
            return self.directionsToPathImpl(*args)
        except:
            traceback.print_exc()
            raise

    @property
    def socketFileno(self):
        return self.server.socket.fileno()

    def handleRequest(self):
        self.server.handle_request()

def main(argv):

    print "loading model"
    model_fname = argv[1]

    #server = Server(None)
    m4du = dir_util.load(model_fname)
    

    app = basewindow.makeApp()

    wnd = MainWindow(m4du)
    wnd.show()

    mb_wnd = modelBrowser.MainWindow(m4du)
    mb_wnd.setWindowTitle(model_fname)

    print "--------------loading server---------------"
    server = Server(wnd, mb_wnd)
    socket = QSocketNotifier(server.socketFileno, QSocketNotifier.Read)
    mb_wnd.connect(socket,
                   SIGNAL("activated(int)"),
                   server.handleRequest)

    mb_wnd.startingSlocTable.selectRow(42)
    print "done"
    mb_wnd.show()
    retval = app.exec_()


if __name__=="__main__":
    import sys
    main(sys.argv)
