import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from system_hotkey import SystemHotkey
import collections
collections.Iterable = collections.abc.Iterable


config=[]
with open('config.ini','r',encoding='utf-8') as file:
    config=file.read().split('\n')
for i in config:
    name,valuse=i.split(':')y
    match name:
        case 'time':
            time=int(valuse)
        case 'start':
            start=tuple(valuse.split(' '))
        case 'reset':
            reset=tuple(valuse.split(' '))
        case 'move':
            move=tuple(valuse.split(' '))
        case 'x':
            x=int(valuse)
        case 'y':
            y=int(valuse)

class TimmerDemo(QWidget):
    sigkeyhot = pyqtSignal(str)
    def __init__(self, parent=None):
        super(TimmerDemo, self).__init__(parent)
        self.setWindowTitle("爆能器已部署")
        self.time_s = time
        self.time_ms=0
        self.updateTime()
        self.TextSeted=False

        self.setText()
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 设置无边框窗口|置顶|穿越窗口
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 初始化一个定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.showtime)

        self.move(x,y)
        #快捷键
        self.sigkeyhot.connect(self.KeypressEvent)
        self.hk_start,self.hk_reset,self.hk_move = SystemHotkey(),SystemHotkey(),SystemHotkey()
        self.hk_start.register(start,callback=lambda x:self.sendkeyevent("hk_start"))
        self.hk_reset.register(reset, callback=lambda x: self.sendkeyevent("hk_reset"))
        self.hk_move.register(move, callback=lambda x: self.sendkeyevent("hk_move"))


        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 0, 1, 2)
 
        self.setLayout(layout)

    #热键处理函数
    def KeypressEvent(self,i_str):
        match i_str:
            case "hk_start":
                self.starttimer()
            case "hk_reset":
                self.endtimer()
            case 'hk_move':
                x = QCursor.pos().x()
                y = QCursor.pos().y()
                label_width=self.label.geometry().width()
                label_height=self.label.geometry().width()
                label_x=self.label.geometry().x()
                label_y=self.label.geometry().y()
                self.move(int(x-label_width/2)-label_x,int(y-label_height/2)+label_y)
                print(int(x-label_width/2)-label_x,int(y-label_height/2)+label_y)
                
        
    #热键信号发送函数(将外部信号，转化成qt信号)
    def sendkeyevent(self,i_str):
        self.sigkeyhot.emit(i_str)

    def showtime(self):
        if self.time_ms==0:
            self.time_ms=100
            self.time_s-=1
        self.time_ms -= 1
        self.updateTime()

        self.setText()
        if self.time_s == 0 and self.time_ms==0:
            self.endtimer()
        
    def starttimer(self):
        self.timer.start(10)

    def endtimer(self):
        self.timer.stop()
        self.time_s=time
        self.time_ms=0
        self.updateTime()
        self.setText()
    
    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件

        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
 
    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True
 
    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None
    
    def updateTime(self):
        if self.time_s<10:
            self.str_time_s='0'+str(self.time_s)
        else:
            self.str_time_s=str(self.time_s)
        if self.time_ms<10:
            self.str_time_ms='0'+str(self.time_ms)
        else:
            self.str_time_ms=str(self.time_ms)

    def setText(self):
        text="<font color=red size=64 > <b>%s:%s</b>"
        if(self.TextSeted==False):
            self.TextSeted=True
            self.label = QLabel(text % (self.str_time_s,self.str_time_ms))
        else:
            self.label.setText(text % (self.str_time_s,self.str_time_ms))
        
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    listwidget = TimmerDemo()
    listwidget.show()
    sys.exit(app.exec_())
