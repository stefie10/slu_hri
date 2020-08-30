from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Widget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
    
        
        self.events = {}
        
        self.startTime = 0
        self.endTime = 1000
        
        self.playhead = 0
        
        
        
    def setSituation(self, situation):
        self.startTime = situation.startTime
        self.endTime = situation.endTime
        
        if self.startTime == None or self.endTime == None:
            self.startTime = 0
            self.endTime = 1000
            
        if self.endTime == self.startTime:
            self.endTime += 1000

    def setEvents(self, key, times):
        print "setting", key
        self.events[key] = times

        if len(times) != 0:
            start = min(times)
            if start < self.startTime:
                self.startTime = start
            end = max(times)
            if end > self.endTime:
                self.endTime = end
        self.repaint()

    def setPlayhead(self, offset):
        self.playhead = offset
        self.update()
        
    def params(self):
        start_pixel = 15
        end_pixel = self.width() - 15
        pix_width = end_pixel - start_pixel
        return start_pixel, end_pixel, pix_width
    
    def time_to_pix(self, time):
        start_pixel, end_pixel, pix_width = self.params()
        return (float(time) / self.endTime) * pix_width + start_pixel

    def pix_to_time(self, pix):
        start_pixel, end_pixel, pix_width = self.params()
        return (float(pix) / pix_width) * self.endTime
        

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.red)
        pen.setWidth(5)
        painter.setPen(pen)
        
        colors = [Qt.red, Qt.green, Qt.lightGray, Qt.yellow, Qt.darkBlue, Qt.darkCyan, Qt.darkGray, Qt.darkMagenta, Qt.darkRed]
        print "painting timeline", len(self.events)
        
        if len(self.events) > 0:
            height = (self.height() - 15) / len(self.events)
        
            start = 0
            for i, key in enumerate(sorted(self.events.keys())):
                times = self.events[key]
                
                pen = QPen(colors[i % len(colors)])
                pen.setWidth(5)
                painter.setPen(pen)
                
                
                for time in times:
                    x_pix = self.time_to_pix(time)
                    painter.drawLine(x_pix, start,x_pix, start + height - 2)
                    
                painter.setPen(Qt.black)
                painter.drawText(0, start + height/2, key)
                                    
                start += height

        pen = QPen(Qt.blue)
        pen.setWidth(5)
        painter.setPen(pen)
        playhead_pix = self.time_to_pix(self.playhead)
        painter.drawLine(playhead_pix, 15, playhead_pix, self.height() - 15)

        painter.setPen(Qt.black)
        for time in range(self.startTime, self.endTime + 1, 5*1000):
            painter.drawText(self.time_to_pix(time) - 10, 
                             self.height(), "%.1f" % (time/1000))

        painter.end()
        
            
        
    def mouseReleaseEvent(self, event):
        pix_x, pix_y = event.x(), event.y()
        print pix_x, pix_y
        time = self.pix_to_time(pix_x)
        self.emit(SIGNAL("eventClicked"), (time))
        
        
        

        
        
        
