from PyQt4.QtCore import Qt, QAbstractTableModel, QVariant


from qt_utils import Counter
counter = Counter()

COL_NWAY_SCORE = counter.pp()
COL_BINARY_SCORE = counter.pp()
COL_SR = counter.pp()
COL_PROBS = counter.pp()
import cPickle
classifier = cPickle.load(open("nlp/nway.pck"))
classifier.reloadClassifier()
from maphacking.trainer import Trainer, make_example_nway
trainer = Trainer()
import orange
class Entry:
    def __init__(self, i, sr, binary_score, geometry):
        self.i = i
        self.sr = sr
        self.binary_score = binary_score
        self.geometry = geometry
        ex = make_example_nway(geometry, trainer, classifier.table.domain)
        cls, probabilities = classifier(ex, orange.GetBoth)
        classes = list(classifier.table.domain.classVar.values)

        self.nway_score = probabilities[sr]
        print "cls", cls
        print "probs", probabilities
        print "probs", probabilities.__class__
        
        for c in classes:
            print c, probabilities[c]
        self.probs = ", ".join([(str(cls) + ":" + "%e" % probabilities[cls])
                               for cls in sorted(classes)])
        

class Model(QAbstractTableModel):
    def __init__(self, view):
        QAbstractTableModel.__init__(self)
        self._data = []
        self.view = view
        self.view.setModel(self)
        
    def columnCount(self, parent):
        return counter.cnt

    def rowCount(self, parent):
        return len(self._data)
    def setData(self, entries):
        self._data = entries
        self.reset()
        
    def get(self, i):
        return self._data[i]
    

    
    def data(self, idx, role=Qt.DisplayRole):

        e = self.get(idx.row())
        col = idx.column()
        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_NWAY_SCORE:
            return QVariant("%e" % e.nway_score)
        elif col == COL_BINARY_SCORE:
            return QVariant("%e" % e.binary_score)
        elif col == COL_SR:
            return QVariant(str(e.sr))
        elif col == COL_PROBS:
            return QVariant(str(e.probs))
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_NWAY_SCORE:
                return QVariant("NWay Score")
            elif section == COL_BINARY_SCORE:
                return QVariant("Binary Score")
            elif section == COL_SR:
                return QVariant("SR")
            elif section == COL_PROBS:
                return QVariant("Probs")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()
        

    def selectedEntry(self):
        entry = self.get(self.view.currentIndex().row())
        return entry

    def selectedEntries(self):
        return [self.get(idx.row()) for idx in self.view.selectedIndexes()]

    def sort(self, col, order):
        if col == COL_NWAY_SCORE:
            self._data.sort(key=lambda e: e.nway_score)
        elif col == COL_BINARY_SCORE:
            self._data.sort(key=lambda e: e.binary_score)
        elif col == COL_SR:
            self._data.sort(key=lambda e: e.sr)
        elif col == COL_PROBS:
            self._data.sort(key=lambda e: e.probs)

        if order == Qt.DescendingOrder:
            self._data.reverse()

        self.reset()


