### BERNARD TOM ###

from pickle import FALSE
from signal import signal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import csv
import time
import serial
import csv
from custom_serial import *
from tabs import *
from widgets import *
import threading

class Controller():
    def __init__(self):
        self.showConnectFrame()

    def showConnectFrame(self):
        self.c = ConnectFrame()
        self.c.show()
        self.c.signal.connect(self.showMainFrame)
    
    def showMainFrame(self,com,baud):
        self.c.close()
        w = MainWindow(com,baud)
        w.showMaximized()

class ConnectFrame(QWidget):
    signal = pyqtSignal(str,int)
    def __init__(self):
        super().__init__()
        self.setFixedWidth(600)
        self.setFixedWidth(400)
        self.setWindowTitle('Serial Connection')
        self.serial = SerialCom()
        self.UIComponents()

    def UIComponents(self):
        mainLay = QGridLayout()
        self.setLayout(mainLay)

        comLabel = QLabel('COM')
        comCombo = QComboBox()
        comCombo.addItems(self.serial.serialPamInit()[0])
        baudLabel = QLabel('Baudrate')
        baudCombo = QComboBox()
        baudCombo.addItems(self.serial.serialPamInit()[1])

        connectBtn = QPushButton("Connection")
        connectBtn.clicked.connect(lambda : self.connection(comCombo.currentText(),baudCombo.currentText()))

        mainLay.addWidget(comLabel,0,0)
        mainLay.addWidget(comCombo,0,1)
        mainLay.addWidget(baudLabel,1,0)
        mainLay.addWidget(baudCombo,1,1)
        mainLay.addWidget(connectBtn,2,0,2,2)

    def connection(self,com,baud):
        self.signal.emit(com,int(baud))

class MainWindow(QWidget):
    def __init__(self,com,baud):
        super().__init__()
        self.setWindowTitle('IPS AMF IHM D-3')
        self.ACQ_REALTIME, self.ACQ_DELIMITED, self.CMD_INDICIEL, self.CMD_MANUAL = False, False, False, False
        self.port,self.baudrate = com,baud
        self.serial = SerialCom()
        self.tabs = Tabs()
        self.stop_thread = True
        self.UIComponents()

    def UIComponents(self):
        mainLay = QVBoxLayout()
        self.setLayout(mainLay)

        topLay = QHBoxLayout()
        mainLay.addLayout(topLay)

    #ACQUI GROUPBOX
        self.acqPrmGroupBox = AcquiGroupBox('ACQUISITION')
        self.acqPrmGroupBox.btnd.stateChanged.connect(lambda: self.btnEvent(self.acqPrmGroupBox.btnd))

    #COMMAND GROUPBOX
        self.cmdGroup = CmdGroupBox('COMMAND')
        self.cmdGroup.btnEch.stateChanged.connect(lambda: self.btnEvent(self.cmdGroup.btnEch))
        self.cmdGroup.btnManual.stateChanged.connect(lambda: self.btnEvent(self.cmdGroup.btnManual))
        self.cmdGroup.slider.valueChanged.connect(self.sliderEvent)

        topLay.addWidget(self.acqPrmGroupBox)
        topLay.addWidget(self.cmdGroup)

    #GRAPH TITLE
        grpTitleLay = QFormLayout()
        mainLay.addLayout(grpTitleLay)
        self.grpTitleEdit = QLineEdit()
        grpTitleLay.addRow(QLabel('GRAPH TITLE'),self.grpTitleEdit)

        topGrpLay = QHBoxLayout()
        mainLay.addLayout(topGrpLay)
        rmvGraphBtn = QPushButton('REMOVE GRAPH')
        rmvGraphBtn.clicked.connect(self.rmvGraph)
        addGraphBtn = QPushButton('ADD GRAPH')
        addGraphBtn.clicked.connect(self.addGraph)
        topGrpLay.addWidget(rmvGraphBtn)
        topGrpLay.addWidget(addGraphBtn)

    #GRAPH AREA
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scrollwidget = QWidget()

        self.scrollLay = QVBoxLayout()
        self.scrollLay.setGeometry

        scrollwidget.setLayout(self.scrollLay)
        scroll.setWidget(scrollwidget)
        mainLay.addWidget(scroll)

        startLay = QHBoxLayout()
        startBtn = QPushButton('START')
        startBtn.clicked.connect(self.start)
        stopBtn = QPushButton('STOP')
        stopBtn.clicked.connect(self.stopThread)
        clearBtn = QPushButton('CLEAR')
        clearBtn.clicked.connect(self.clearGraph)
        startLay.addWidget(startBtn)
        startLay.addWidget(stopBtn)
        startLay.addWidget(clearBtn)
        mainLay.addLayout(startLay)
        
    def addGraph(self):
        self.scrollLay.addWidget(GraphGroupBox(self.grpTitleEdit.text()))
        self.grpTitleEdit.setText('')
    
    def rmvGraph(self):
        if self.scrollLay.__len__()-1 >= 0:
            self.scrollLay.itemAt(self.scrollLay.__len__()-1).widget().setParent(None)

#set Parameters editable or not & set MODE
    def btnEvent(self,btn:QCheckBox):
        if btn.text() == "Acquisition delimited":
            if btn.isChecked():
                self.ACQ_DELIMITED = True
                self.ACQ_REALTIME = False
                self.acqPrmGroupBox.timeEdit.setEnabled(True)
                self.acqPrmGroupBox.stepEdit.setEnabled(True)
            else :
                self.ACQ_DELIMITED = False
                self.ACQ_REALTIME = True
                self.acqPrmGroupBox.timeEdit.setEnabled(False)
                self.acqPrmGroupBox.stepEdit.setEnabled(False)

        if btn.text() == "Indiciel":
            if btn.isChecked():
                self.CMD_INDICIEL = True
                self.CMD_MANUAL = False
                self.cmdGroup.echCmdEdit.setEnabled(True)
                self.cmdGroup.echDelayEdit.setEnabled(True)
            else :
                self.cmdGroup.echCmdEdit.setEnabled(False)
                self.cmdGroup.echDelayEdit.setEnabled(False)

        if btn.text() == "Manual":
            if btn.isChecked():
                self.CMD_INDICIEL = False
                self.CMD_MANUAL = True
                self.cmdGroup.slider.setEnabled(True)
            else:
                self.cmdGroup.slider.setEnabled(False)

    def sliderEvent(self):
        self.cmd = self.cmdGroup.slider.value()*10
        self.cmdGroup.cmdLabel.setText(f"Heigh Cmd : {self.cmd}")
        if self.stop_thread == False:
            self.serial.serialWrite(self.cmd)

    def clearRcvData(self):
        self.rcv_h, self.rcv_i, self.rcv_v, self.p = 0, 0, 0, 0

    def clearGraph(self):
        self.tabs.clearTab()
        self.clearRcvData()
        for i in range(self.scrollLay.__len__()):
            self.scrollLay.itemAt(i).widget().curve.setData(self.tabs.cmd_tab)

    def start(self):
        for i in range(self.scrollLay.__len__()):
            self.scrollLay.itemAt(i).widget().traceCombo.setEnabled(False)
            self.scrollLay.itemAt(i).widget().traceColorCombo.setEnabled(False)
        self.clearRcvData()

        self.readThread = threading.Thread(target = self.onRead)
        self.runThread = threading.Thread(target = self.run)
        self.stop_thread = False
        self.serial.openSerial(self.port,self.baudrate)

        self.readThread.start()
        time.sleep(0.2)
        self.runThread.start()

    def stopThread(self):
        for i in range(self.scrollLay.__len__()):
            self.scrollLay.itemAt(i).widget().traceCombo.setEnabled(True)
            self.scrollLay.itemAt(i).widget().traceColorCombo.setEnabled(True)
        self.stop_thread = True
        self.runThread.join()
        self.readThread.join()
        self.serial.closeSerial()
        self.saveCSV() 

    def run(self):
        while True:
            self.tabs.setTab(self.cmd,self.rcv_h,self.rcv_v,self.rcv_i)
            if self.scrollLay.__len__() != 0 :
                for i in range(self.scrollLay.__len__()):
                    if self.scrollLay.itemAt(i).widget().trace_title == 'Cmd':
                        self.scrollLay.itemAt(i).widget().curve.setData(self.tabs.cmd_tab)
                   
                    if self.scrollLay.itemAt(i).widget().trace_title == 'H':
                        self.scrollLay.itemAt(i).widget().curve.setData(self.tabs.h_tab)

                    if self.scrollLay.itemAt(i).widget().trace_title == 'I':
                        self.scrollLay.itemAt(i).widget().curve.setData(self.tabs.i_tab)

                    if self.scrollLay.itemAt(i).widget().trace_title == 'V':
                        self.scrollLay.itemAt(i).widget().curve.setData(self.tabs.v_tab)

                    if self.scrollLay.itemAt(i).widget().trace_title == 'P':
                        self.scrollLay.itemAt(i).widget().curve.setData(self.tabs.p_tab)
            time.sleep(0.05)
            if self.stop_thread == True : break
    
    def onRead(self):
        while True:
            self.rcv_h,self.rcv_i,self.rcv_v, = self.serial.serialRead()
            if self.stop_thread == True : 
                break

    def setSignals(self):
        if self.CMD_INDICIEL == True:
            self.cmd = self.cmdGroup.echCmdEdit.text()
            self.tabs.setStepTab(self.cmd)
        if self.CMD_MANUAL == True:
            self.cmd = str(self.cmdGroup.slider.value())
            self.tabs.setCmdTab(self.cmd)
        self.tabs.setTab(self.cmd,self.rcv_h,self.rcv_v,self.rcv_i)

    def saveCSV(self):
        csv_tab = []
        csv_tab.append(['TIME','CMD','H','I','V','P'])
        with open('./V2/data.csv','w',newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=' ')
            for i in range(len(self.tabs.time_tab)):
                row = [self.tabs.time_tab[i],self.tabs.cmd_tab[i],self.tabs.h_tab[i],self.tabs.i_tab[i],self.tabs.v_tab[i],self.tabs.p_tab[i]]
                csv_tab.append(row)
            writer.writerows(csv_tab)


def main():
    app = QApplication(sys.argv)
    c = Controller()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
