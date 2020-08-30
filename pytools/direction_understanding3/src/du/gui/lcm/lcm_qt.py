import matplotlib_qt

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from du.dir_util import load
from du.eval_util import get_topo_to_region_hash, get_orientations_annotated
from du.gui import modelBrowser
from du.gui.lcm import lcm_ui
from du.gui.lcm.lcm_networking_enlivn import App
from pyTklib import kNN_index, tklib_normalize_theta
from qt_utils import isChecked
from scipy import transpose
from tag_util import tag_file
import basewindow
import math
import sys
import numpy as na



class MainWindow(QMainWindow, lcm_ui.Ui_MainWindow):
    def __init__(self, m4du, region_tagfile, map_fname):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.m4du = m4du
        

        self.lcmApp = App(self.m4du, region_tagfile, map_fname)
        self.socket = QSocketNotifier(self.lcmApp.lc.fileno(), QSocketNotifier.Read)
        self.connect(self.socket,
                     SIGNAL("activated(int)"),
                     self.socketActivated)    
        
        self.connect(self.sendPathButton,
                     SIGNAL("clicked()"),
                     self.followDirections)

        self.connect(self.sendAndExecutePathButton,
                     SIGNAL("clicked()"),
                     self.sendAndExecutePath)
        
        self.connect(self.confirmPathButton,
                     SIGNAL("clicked()"),
                     self.confirmPath)
        
        self.connect(self.clearPathButton,
                     SIGNAL("clicked()"),
                     self.lcmApp.clear_path)

        self.modelBrowser = modelBrowser.MainWindow(self.m4du)
        self.modelBrowser.show()
        self.tf_region = tag_file(region_tagfile, map_fname)
        self.dataset_name = region_tagfile.split("/")[-1].split("_")[0]
        
        self.topo_to_region = get_topo_to_region_hash(self.tf_region, self.m4du)
        
    
        
    def socketActivated(self, arg):
        self.lcmApp.lc.handle()
        if self.lcmApp.cmd != None:
            cmd = self.lcmApp.cmd
            self.lcmApp.cmd = None
            self.commandText.setPlainText(cmd)
            self.sendAndExecutePath()
        
    def sendAndExecutePath(self):
        self.followDirections()
        self.confirmPath()
        
    def followDirections(self):
        txt = str(self.commandText.toPlainText())
        print "txt", txt
        if self.lcmApp.cur_pose != None:
            print "loc", self.lcmApp.cur_pose[0:3]
            loc_index, = kNN_index(self.lcmApp.cur_pose[0:3],
                                   transpose([self.m4du.tmap_locs_3d[x] for x in self.m4du.tmap_keys]),
                                   1)

            topo_key = self.m4du.tmap_keys[int(loc_index)]

            if isChecked(self.useRobotYawBox):
                yaw = self.lcmApp.cur_pose[3]
                print "yaw", yaw
                yaw = tklib_normalize_theta(yaw)
                if yaw < 0:
                    yaw += 2*math.pi
                orient = yaw
                print "yaw", math.degrees(yaw)

                orients = [na.append(self.m4du.orients, 360.0)]
                i_tmp, = kNN_index([math.degrees(orient)], orients, 1);
                i_tmp = int(i_tmp % len(self.m4du.orients))
                vp = str(topo_key) + "_" + str(self.m4du.orients[i_tmp])
                vp_i = self.m4du.vpt_to_num[vp]
                vps = [vp_i]
            else:

                vps = []
                for orient in self.m4du.orients:
                    vp = str(topo_key) + "_" + str(orient)
                    vp_i = self.m4du.vpt_to_num[vp]
                    vps.append(vp_i)
        else:
            vps = None
        self.path = self.modelBrowser.runSentence(txt, vps)

    def confirmPath(self):
        self.lcmApp.publish_waypoints(self.path)
        
        
    
def main():
    app = basewindow.makeApp()
    model_fname = sys.argv[1]
    region_tagfile = sys.argv[2]
    map_fname = sys.argv[3]
    
    m4du = load(model_fname)
    wnd = MainWindow(m4du, region_tagfile, map_fname)
    wnd.show()
    app.exec_()

if __name__ == "__main__":
    main()
            
