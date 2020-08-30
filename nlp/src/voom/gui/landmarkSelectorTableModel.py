from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter
import numpy as na

counter = Counter()


COL_NAME = counter.pp()
COL_LOCATION = counter.pp()

def plotLandmarks(figure, tag_file, idx=None, useText=True, washoutFactor=0):
    from matplotlib.transforms import offset_copy
    import landmark_icon_cache

    transOffset = offset_copy(figure.gca().transData, fig=figure,
                              x=0.02, y=-0.17, units='inches')
    gridmap = tag_file.get_map()
    plots = []
    iconIdx = 0
    for obj in tag_file.objects:

        x, y = gridmap.to_xy(obj.centroid())

        icon = landmark_icon_cache.getIcon(obj.tag)
        if icon is not None and (idx is None or iconIdx == idx):
            
            icon = na.minimum(icon + washoutFactor, 1)
        
            #print "using", obj.tag
            width, height, channels = icon.shape
            draw_width = 1.5
            draw_height = draw_width*width/height
            lower_left_x = x - draw_width / 2.0
            lower_left_y = y - draw_height / 2.0

            img = figure.gca().imshow(icon, origin="lower",
                                      extent=(lower_left_x, lower_left_x + draw_width, 
                                              lower_left_y, lower_left_y + draw_height))
            plots.append((img,))
        elif useText:
                #p1, = figure.gca().plot((x,), (y,), 'ko')
                #p2 = figure.gca().text(x, y, obj.tag, transform=transOffset, size=16)
            text = obj.tag
            print "text", text, text.__class__
            if text == "landing":
                text = "LZ"
            elif text == "charlie":
                text = "CC"
            elif text == "triangle":
                text = "TR"
            elif text == "flagpole":
                text = "FP"
            else:
                text = None
                
            if text != None:
                text = " " + text

                p1, = figure.gca().plot((x,), (y,), 'ko')
                p2 = figure.gca().text(x, y, text, size=20)
                plots.append(p1)
                plots.append(p2)
        iconIdx += 1
    return plots

class Entry:
    def __init__(self, m4du, i):
        self.i = i
        self.name = m4du.obj_names[i]
        self.location = m4du.obj_locations[0][i], m4du.obj_locations[1][i]


class Model(QAbstractTableModel):
    def __init__(self, view, tag_file):
        QAbstractTableModel.__init__(self)

        self.tag_file = tag_file

        self.view = view
        self.view.setModel(self)
        self.view.selectAll()


    def selectedIndexes(self):
        return set([self.get(idx.row()).i for idx in self.view.selectedIndexes()])

    def columnCount(self, parent=None):
        return counter.cnt
    def rowCount(self, parent=None):
        return len(self.tag_file)

    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()

        e = self.tag_file[idx.row()]

        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_NAME:
            return QVariant(e.tag)
        elif col == COL_LOCATION:
            return QVariant("%.2f, %.2f" % tuple(e.centroid()))
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_NAME:
                return QVariant("Name")
            elif section == COL_LOCATION:
                return QVariant("Location")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()

