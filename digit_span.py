# -*- coding: utf-8 -*-

import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets

def randomcolor():	#	随机生成颜色
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.isTimeStart=False
        self.level = 3	#	由三个数字开始
        self.setupUI()


    def setupUI(self):
        
        self.timer = QtCore.QTimer()
        self.timeClock = QtCore.QTime()
        self.timer.timeout.connect(self.addtime)

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setObjectName('main_widget')
        self.setCentralWidget(self.main_widget) # 设置窗口主部件

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
        self.display_widget.setFixedSize(500,400)
        self.display_widget.setText('准备开始测试')
        self.display_widget.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.input_widget = QtWidgets.QLineEdit()
        self.input_widget.setFixedSize(500,60)
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
        self.center_layout.addStretch(1)
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
                font-size:60px;
            }
            #QLabel:hover{background:#4d5e39;}
            QLineEdit{background:white;border:none;border-radius:20px;color:#554236;font-family: "Segoe UI";font-size:20px;}
            QPushButton#top_label{border:none;color:white;font-family: "Segoe UI";font-size:20px;}
            QPushButton#level_label{border:none;color:#EBB471;font-family: "Segoe UI";font-size:25px;}
            QPushButton#bottom_button{
                border:none;background:#724938;border-radius:10px;color:white;font-family: "Segoe UI";font-size:18px;
            }
            QPushButton#bottom_button:hover{background:#7d6c46;}
        ''')

        self.resize(600, 800)  #   设置窗口大小
        self.center()           #   设置窗口位于屏幕正中间
        self.setWindowTitle('Digit Span')      #   窗口标题
        self.setWindowOpacity(0.9)  #   设置窗口透明度


    def start(self):
        self.timestart()    # 总的时间显示
        self.num = 0
        self.index = 0
        self.display_timer = QtCore.QTimer(self) #   控制每个数字显示一秒
        self.display_timer.timeout.connect(self.operate) #计时结束调用operate()方法
        self.display_timer.start(1000) #设置计时间隔并启动

    def operate(self):
        a = random.randint(0,9)
        self.index += 1
        print(self.num)
        if self.index <= self.level:
            self.num += a * (10**(self.index-1))
            self.display_widget.setStyleSheet('QLabel{color:%s;font-size: 200px}'%randomcolor())	#	随机改变颜色以区分两次相同数字
            self.display_widget.setText(str(a))
        elif (self.index == self.level + 1):
            self.display_widget.setStyleSheet('QLabel{color:#554236;font-size:60px}')
            self.display_widget.setText('请反向输入\n刚刚的数字')
            self.display_timer.stop()

    def check(self):
        inputnum = int(self.input_widget.text())
        if inputnum == self.num:
            self.level += 1
            self.start()
        else:
            self.start()
        self.top_label_2.setText('level '+str(self.level))
        self.input_widget.clear()


    def stop(self):
        self.timestop()

    #   显示计时器几个功能
    def timestart(self):            #启动计时
        if not self.isTimeStart:
            self.timeClock.setHMS(0,0,0)  #初始时设置时间为  00：00：00
            self.timer.start(1000)         #启动定时器，定时器对象每隔一秒发射一个timeout信号
        self.isTimeStart=True

    def addtime(self):      #计时时间增一秒，并显示在QLable上
        self.timeClock = self.timeClock.addMSecs(1000)   #时间增加一秒
        self.label_time_val.setText(self.timeClock.toString("hh:mm:ss"))   #标签显示时间
    
    def timestop(self):    #停止计时
        if self.isTimeStart:
            self.timer.stop()
            self.isTimeStart=False
        

    #   使窗口显示在屏幕正中
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