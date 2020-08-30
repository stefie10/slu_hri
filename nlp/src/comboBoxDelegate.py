from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qt_utils

class Delegate(QItemDelegate):
    def __init__(self, data):
        QAbstractItemDelegate.__init__(self)
        self._data = data

    def valueForIdx(self, idx):
        for id, name in self._data:
            if id == idx:
                return name
        raise ValueError("Idx wasn't found. " + `idx` + " name: " + `self._data`)


    def createEditor(self, parent, option, idx):
        typeBox = QComboBox(parent)

        def commitSlot(idx):
            self.emit(SIGNAL("commitData(QWidget *)"), 
                      (typeBox))


        self.connect(typeBox, SIGNAL("currentIndexChanged(int)"),
                     commitSlot)

        for id, name in self._data:
            typeBox.addItem(name, QVariant(id))
        return typeBox
    def setEditorData(self, editor, idx):
        value = qt_utils.toInt(idx.model().data(idx))
        if value == None:
            editor.setCurrentIndex(-1)
            return
        else:
            for i in range(0, editor.count()):
                if editor.itemData(i) == QVariant(value):
                    editor.setCurrentIndex(i)
                    return
            raise ValueError("Unexpected index: %s" % (value))
        

        
    def setModelData(self, editor, model, idx):
        value = editor.itemData(editor.currentIndex())
        model.setData(idx, value, Qt.EditRole)
        
    def updateEditorGeometry(self, editor, option, idx):
        editor.setGeometry(option.rect);
