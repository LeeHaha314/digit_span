# -*- coding: utf-8 -*-

import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets

interval = 500	#	set the interval value for the number display 
path_name = './log.txt'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.isTimeStart=False
        self.current_timestr = '00:00:00'
        self.level = 3	#	begin with 3 numbers
        self.setupUI()


    def setupUI(self):
        
        self.timer = QtCore.QTimer()    #   create a timer
        self.timeClock = QtCore.QTime()
        self.timer.timeout.connect(self.addtime)

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setObjectName('main_widget')
        self.setCentralWidget(self.main_widget) # set main window

        self.center_widget = QtWidgets.QWidget()
        self.center_layout = QtWidgets.QVBoxLayout()
        self.center_widget.setLayout(self.center_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.center_widget)
        self.main_layout.addStretch(1)

        self.top_widget = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QHBoxLayout()
        self.top_widget.setLayout(self.top_layout)
        self.top_label_1 = QtWidgets.QPushButton("Time")
        self.top_label_1.setObjectName('top_label')
        self.label_time_val = QtWidgets.QPushButton("00:00:00")
        self.label_time_val.setObjectName('top_label')
        self.top_label_2 = QtWidgets.QPushButton("level "+str(self.level))
        self.top_label_2.setObjectName('level_label')
        self.top_layout.addWidget(self.top_label_1)
        self.top_layout.addWidget(self.label_time_val)
        self.top_layout.addStretch(1)
        self.top_layout.addWidget(self.top_label_2)
        self.top_widget.setFixedSize(500,100)

        self.display_widget = QtWidgets.QLabel()
        self.display_widget.setFixedSize(1000,600)
        self.display_widget.setText('准备开始测试')
        self.display_widget.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.input_widget = QtWidgets.QLineEdit()
        self.input_widget.setFixedSize(1000,60)
        self.input_widget.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.input_widget.returnPressed.connect(self.check)

        self.bottom_widget = QtWidgets.QWidget()
        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.bottom_widget.setLayout(self.bottom_layout)
        self.start_button = QtWidgets.QPushButton('start')
        self.start_button.setObjectName('bottom_button')
        self.start_button.setFixedSize(100,50)
        self.start_button.clicked.connect(self.start)
        self.stop_button = QtWidgets.QPushButton('stop')
        self.stop_button.setObjectName('bottom_button')
        self.stop_button.setFixedSize(100,50)
        self.stop_button.clicked.connect(self.stop)
        self.bottom_layout.addStretch(1)
        self.bottom_layout.addWidget(self.start_button)
        self.bottom_layout.addStretch(1)
        self.bottom_layout.addWidget(self.stop_button)
        self.bottom_layout.addStretch(1)

        self.center_layout.addWidget(self.top_widget)
        #self.center_layout.addStretch(1)
        self.center_layout.addWidget(self.display_widget)
        self.center_layout.addStretch(1)
        self.center_layout.addWidget(self.input_widget)
        self.center_layout.addStretch(1)
        self.center_layout.addWidget(self.bottom_widget)
        self.center_layout.addStretch(1)

        self.main_widget.setStyleSheet('''
            QWidget#main_widget{
                background:#554236;
                border:none
            }
            QLabel{
                background:white;
                border:none;
                border-radius:20px;
                color:#554236;
                font-family: "Microsoft YaHei";
                font-size:100px;
            }
            #QLabel:hover{background:#4d5e39;}
            QLineEdit{
            	background:white;border:none;border-radius:20px;color:#554236;font-family: "Segoe UI";font-size:20px;
            }
            QPushButton#top_label{
            	border:none;color:white;font-family: "Segoe UI";font-size:20px;
            }
            QPushButton#level_label{
            	border:none;color:#EBB471;font-family: "Segoe UI";font-size:25px;
           	}
            QPushButton#bottom_button{
                border:none;background:#724938;border-radius:10px;color:white;font-family: "Segoe UI";font-size:18px;
            }
            QPushButton#bottom_button:hover{background:#7d6c46;}
        ''')

        self.resize(1200, 1000)  #   设置窗口大小
        self.center()           #   设置窗口位于屏幕正中间
        self.setWindowTitle('Digit Span')      #   窗口标题
        self.setWindowOpacity(0.9)  #   设置窗口透明度

    def start(self):
        self.timestart()    # 总的时间显示
        self.num = 0
        self.index = 0
        self.display_timer = QtCore.QTimer(self)		 #	for number display time control
        self.display_timer.timeout.connect(self.operate) #	connect to operate() to control
        self.display_timer.start(interval)	#	set the interval

    def operate(self):
        with open(path_name,'a+') as f:
	        a = random.randint(0,9)
	        f.write(self.current_timestr+' 显示数字中 ')
	        self.index += 1
	        if self.index <= self.level:
	            self.num += a * (10**(self.index-1))
	            self.display_widget.setStyleSheet('QLabel{font-size:400px;}')
	            self.display_widget.setText(str(a))
	        elif (self.index == self.level + 1):
	            self.display_widget.setStyleSheet('QLabel{font-size:100px;}')
	            self.display_widget.setText('请反向输入\n刚刚的数字')
	            f.write('\n'+self.current_timestr+' 提示输入\n')
	            self.display_timer.stop()

    def check(self):
        inputnum = int(self.input_widget.text())
        with open(path_name,'a+') as f:
	        if inputnum == self.num:
	            f.write(self.current_timestr+' 判断：正确 level：'+str(self.level)+'\n')
	            self.level += 1 
	            self.start()
	        else:
	            f.write(self.current_timestr+' 判断：错误 level：'+str(self.level)+'\n')
	            self.start()
	        self.top_label_2.setText('level '+str(self.level))
	        self.input_widget.clear()


    def stop(self):
        self.timestop()

    #   set for timer
    def timestart(self):            
        if not self.isTimeStart:
            self.timeClock.setHMS(0,0,0)  	
            self.timer.start(1000)         
        self.isTimeStart=True

    def addtime(self):      
        self.timeClock = self.timeClock.addMSecs(1000)   
        self.current_timestr = self.timeClock.toString("hh:mm:ss")
        self.label_time_val.setText(self.current_timestr)   # only for time label display
    
    def timestop(self):    
        if self.isTimeStart:
            self.timer.stop()
            self.isTimeStart=False
        
    #   set main window to the center
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())