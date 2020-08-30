from tklib_ipc import *
from thread import start_new_thread
from pylab import *
from time import sleep
from sys import argv

tkipc = tklib_ipc_handler()
class destination_picker:
    def __init__(self, horizon=1):
        self.horizon = horizon;
        self.num_selected = 0;
        self.X, self.Y = [], [];
        self.dest_plt, = plot([], [], 'yo', markersize=10);
        self.run();

    def myclick(self, msg):
        x, y =  msg.xdata, msg.ydata
        self.X.append(x);self.Y.append(y);
        self.dest_plt.set_data(self.X, self.Y)
        draw()
        self.num_selected += 1
        
        if(self.num_selected == self.horizon):
            self.num_selected = 0
            tkipc.set_destinations([[x],[y]])
            pyTklib.carmen_ipc_sleep(0.1)
            self.X, self.Y = [], []
        

    def run(self):
        p2, = plot([0, 0], [-150, 150], 'k--')
        p2, = plot([-150, 150], [0, 0], 'k--')
        p1, = plot([0], [0], 'ro', markersize=10);
        p2, = plot([0, 1], [0, 0], 'r', linewidth=3);
        
        R = arange(0, 100);
        Th = arange(-pi, pi, 0.01)
        for r in R:
            plot(r*cos(Th), r*sin(Th), 'k--')
    
        axis([-8, 8, -8, 8])
        connect('button_press_event',self.myclick)
        show()        

if __name__ == "__main__":

    if(len(argv) == 1):
        v = destination_picker();
    elif(len(argv) == 2):
        v = destination_picker(int(argv[1]))
    else:
        print "usage:\n\t python destination_picker.py [horizon=1]"


