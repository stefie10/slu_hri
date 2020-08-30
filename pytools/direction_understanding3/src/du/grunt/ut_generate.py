import matplotlib 
import random
matplotlib.use('Qt4Agg')
import pylab as mpl
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
from datetime import datetime
from datetime import timedelta
import utbot
from pyTklib import kNN_index
import spatialRelationClassifier
import describe

from PyQt4.QtCore import *
from PyQt4.QtGui import *


from du.grunt import ut_generate_ui
from du.gui.modelBrowser import plot_map_for_model

import extract_ut_tags
import math2d

# magic numbers were from extract_ut_tags, figuring out where
# specific objects in the map were in carmen space.
translate_function = extract_ut_tags.derive_transform((-2235, -413), (5255, 1343),
                                                      (20.9, 10.7), (28.1, 40.2))

verb_forms = {
   "turnLeft" : ["go left", "turn left"],
   "turnRight" : ["go right", "turn right"],
   "straight" : ["go straight", "walk","continue"],
}

object_forms = {
    "tree": ["tree"],
    "blue_blazer" : ["SUV", "car", "blue SUV", "blue car"],
    "red_blazer" : ["SUV", "car", "red car",],
    "blazer" : ["SUV", "car"],
    "car" : ["car"],
    "streetlight" : ["street light", "light"],
    "van" : ["van", "truck"],
    "archway" : ["arch", "archway", "doorway"],
    "newsboxes" : ["newsboxes", "newspaper stands", "newspapers"],
    "newsboxes" : ["newsboxes", "newspaper stands", "newspapers"],
    "door" : ["door", "doorway",],
    "passageway" : ["passageway", "alley"],
    "speedlimit_sign" : ["speed limit sign", "sign", "25 mph sign"],
}


class MainWindow(QMainWindow, ut_generate_ui.Ui_MainWindow):
    def __init__(self, m4du):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.m4du = m4du

        srEngineMap = dict([(key, spatialRelationClassifier.engineMap[key]) 
                            for key in ["across", "through", "past", "around", 
                                        "to", "out", "towards", "away from"]])

        verbEngineMap = dict([(key, spatialRelationClassifier.engineMap[key]) 
                              for key in ["turnLeft", "turnRight", "straight"]])

        self.describe_window = describe.MainWindow(verbEngineMap, srEngineMap)
        self.describe_window.show()
        

        self.figure = mpl.figure()
        self.oldParent = self.figure.canvas.parent()
        self.figure.canvas.setParent(self)
        self.matplotlibFrame.layout().addWidget(self.figure.canvas)
        self.toolbar = NavigationToolbar2QT(self.figure.canvas, self)
        self.addToolBar(self.toolbar)
        
        plot_map_for_model(self.m4du)

        self.bot = utbot.utbot()
        self.bot.spawn_bot("USARBot.MDS",(-7.68,-21.44,18.24), (0, 0, 1.58))

        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.setInterval(300)
        self.timer.start()
        
        self.connect(self.timer,
                     SIGNAL("timeout()"),
                     self.updateBot)
        self.connect(self.actionReset, SIGNAL("triggered()"), 
                     self.reset)

        self.player_location_plot, = mpl.plot([], [], '-', 
                                              linewidth=4, color="red")
        self.selected_landmark_plot, = mpl.plot([], [], '*',  markersize=10,
                                                color="blue")

        self.last_describe_time = datetime.now()
        self.last_describe_loc = None
        self.reset()

    def reset(self):
        self.figure_start = 0
        self.player_locs = []
        self.segments = []
        self.landmarks = []
        self.descriptionLabel.setText("")
        self.selected_landmark_plot.set_data([], [])

    def updateBot(self):
        self.bot.update()
        utx, uty, utz = self.bot.player_loc
        x, y = translate_function(utx, uty)

        self.player_locs.append((x, y))
        self.player_location_plot.set_data([x for x, y in self.player_locs],
                                           [y for x, y in self.player_locs])
        #self.player_locs = self.player_locs[-20:]

        if (datetime.now() - self.last_describe_time > timedelta(seconds=2)):
            self.describe()

        mpl.draw()

    def pick_landmark(self, figure):
        current_loc = figure[-1]
        figure_idx = random.choice([0, len(figure)/2, -1])

        landmark_probs = self.m4du.make_tag_probability_map()
        
        #tag_prob

        indices = kNN_index(figure[figure_idx], self.m4du.obj_locations, 4)
        #print "geomes", self.m4du.obj_geometries[0]
        candidates = [int(i) for i in indices
                      if self.m4du.clusters.tf.is_visible(self.m4du.obj_locations[:, int(i)], 
                                                          figure[-1],
                                                          max_dist=10)]
        blacklist = ["streetlight", "speedlimit_sign", "tree"] + self.landmarks[-1:]
        if len(candidates) == 0:
            return None
        else:
            for i in range(5):
                i = random.choice(candidates)
                landmark_name = self.m4du.obj_names[i]
                if not landmark_name in blacklist:
                    break

            if len(self.landmarks) > 0 and landmark_name == self.landmarks[-1]:
                print "landmark", landmark_name
                print "landmarks", self.landmarks
                return None
            
            if landmark_name in blacklist:
                if random.choice([True, False]):
                    return None
                else:
                    return i 
            return i

    def plot_landmark(self, i):
        x, y = self.m4du.obj_locations[:, i]
        X, Y = self.selected_landmark_plot.get_data()
        X = list(X)
        Y = list(Y)
        X.append(x)
        Y.append(y)
        self.selected_landmark_plot.set_data(X, Y)
        self.landmarks.append(self.m4du.obj_names[i])

    def describe(self):
        figure = self.player_locs[self.figure_start:]
        if math2d.sorta_eq(math2d.length(figure), 0):
            return
        
        if (self.last_describe_loc != None and
            math2d.dist(self.last_describe_loc, figure[-1]) < 1):
            return 

        landmark_i = self.pick_landmark(figure)
        if landmark_i == None:
            return

        object_name = self.m4du.obj_names[landmark_i]


        ground = self.m4du.createGroundFromPolygon(landmark_i)
        self.describe_window.generate(geometry={"figure":figure,
                                                "ground":ground})

        #verb_choices = [e.engine.name() 
        #                for e in self.describe_window.verbResultModel._data
        #                if e.p_true > 0.7]
        verb_choices = ["straight"]
        print "choices", verb_choices
        if "straight" in verb_choices or True:
            verb_name = "straight"
        else:
            if len(verb_choices) == 0:
                return
            else: 
                verb = self.describe_window.verbResultModel.get(0)
                verb_name = verb.engine.name()
        verb_str = random.choice(verb_forms[verb_name])

        print "object name", object_name, landmark_i
        object_str = random.choice(object_forms[object_name])

        sr_choices = []
        for e in self.describe_window.srResultModel._data:
            if e.p_true > 0.7:
                sr_choices.append(e)


        if len(sr_choices) == 0:
            return 
        engine_names = [e.engine.name() for e in sr_choices]

        if "through" in engine_names:
            sr = sr_choices[engine_names.index("through")]
        else:
            sr = random.choice(sr_choices)

        next_segment = "%s %s the %s." % (verb_str,
                                          sr.engine.name(),
                                          object_str,
                                          )
        connectors = ["Next", "Then", "", "After that"]
        connector = random.choice(connectors)
        if len(self.segments) >= 1 and connector != "":
            next_segment = "%s %s" % (connector, next_segment)
        else:
            next_segment = next_segment.capitalize()

        self.segments.append(next_segment)

        self.descriptionLabel.setText(" ".join(self.segments))
        bar = self.labelScrollArea.verticalScrollBar()
        #bar.setSliderPosition(bar.maximum() + 100)


        self.last_describe_time = datetime.now()

        self.last_describe_loc = figure[-1]
        self.figure_start = len(figure) - 1
        self.plot_landmark(landmark_i)
        

def main():
    from sys import argv
    import cPickle
    import basewindow
    model_file = argv[1]
    m4du = cPickle.load(open(model_file, 'r'))
    m4du.initialize()
    app = basewindow.makeApp()
    wnd = MainWindow(m4du)
    wnd.setWindowTitle(model_file)
    wnd.show()
    retval = app.exec_()


if __name__ == "__main__":
    main()
