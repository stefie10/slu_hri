from PyQt4.QtCore import *
from PyQt4.QtGui import *

import breadbox_ui
import trainer
import annotation_reader
from environ_vars import TKLIB_HOME

class MainWindow(QMainWindow, breadbox_ui.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)    
        self.connect(self.nounPhraseBox,
                     SIGNAL("returnPressed()"),
                     self.classify)
#        annotator2 = annotation_reader.from_file("%s/data/directions/breadbox/nouns_dlaude.partial.txt" % TKLIB_HOME)
        annotator2 = annotation_reader.from_file("%s/data/directions/breadbox/nouns_stefie10.txt" % TKLIB_HOME)
        self.engine = trainer.WordnetParentsEngine(annotator2)
        

    def classify(self):
        noun = str(self.nounPhraseBox.text())
        result = self.engine.classify(noun)
        print "result", result, result.__class__
        self.resultLabel.setText(result)


def main():
    from sys import argv
    import cPickle
    import basewindow
    app = basewindow.makeApp()
    wnd = MainWindow()
    wnd.setWindowTitle("Breadbox")
    wnd.show()
    retval = app.exec_()


if __name__ == "__main__":
    main()
