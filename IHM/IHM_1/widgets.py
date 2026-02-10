from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg

class Slider(QSlider):
    def __init__(self,min,max):
        super().__init__()
        self.setOrientation(Qt.Horizontal)
        self.setMinimum(min)
        self.setMaximum(max)
        self.setValue(0)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.setSingleStep(1)
        self.setPageStep(1)

class GroupBox(QGroupBox):
    def __init__(self,title):
        super().__init__()
        self.setTitle(title)
        self.setStyleSheet("font-size: 15px")
        self.setContentsMargins(0,0,0,0)

class AcquiGroupBox(GroupBox):
    def __init__(self, title):
        super().__init__(title)
        lay = QGridLayout()
        #self.setMaximumHeight(40)
        #lay.setHorizontalSpacing(10)
        self.setLayout(lay)
        btnGroup = QButtonGroup(self)
        self.btnr = QCheckBox("Real Time")
        self.btnd = QCheckBox("Acquisition delimited")
        timeLabel = QLabel('Acquisition time (s) :')
        stepLabel = QLabel("Step (s) :")
        self.timeEdit = QLineEdit()
        self.timeEdit.textChanged.connect(self.updateTime)
        self.timeEdit.setEnabled(False)
        self.stepEdit = QLineEdit()
        self.stepEdit.textChanged.connect(self.updateStep)
        self.stepEdit.setEnabled(False)

        btnGroup.addButton(self.btnr)
        btnGroup.addButton(self.btnd)

        lay.addWidget(self.btnd,0,0)
        lay.addWidget(timeLabel,0,1)
        lay.addWidget(self.timeEdit,0,2)
        lay.addWidget(stepLabel,1,1)
        lay.addWidget(self.stepEdit,1,2)
        lay.addWidget(self.btnr,2,0)

    def updateTime(self):
        self.acq_time = self.timeEdit.text()

    def updateStep(self):
        self.step_time = self.stepEdit.text()

class CmdGroupBox(GroupBox):
    def __init__(self, title):
        super().__init__(title)
        lay = QGridLayout()
        self.setLayout(lay)
        #lay.setHorizontalSpacing(10)
        btngroup = QButtonGroup(self)
        self.btnEch = QCheckBox("Indiciel")
        self.btnManual = QCheckBox("Manual")
        btngroup.addButton(self.btnEch)
        btngroup.addButton(self.btnManual)

        self.echCmdEdit = QLineEdit()
        self.echCmdEdit.setEnabled(False)
        self.echDelayEdit = QLineEdit()
        self.echDelayEdit.setEnabled(False)
        self.cmdLabel = QLabel('Heigh Cmd : ')
        self.cmdLabel.setAlignment(Qt.AlignCenter)
        self.slider = Slider(9,20)
        self.slider.setEnabled(False)

        lay.addWidget(self.btnEch,0,0)
        lay.addWidget(QLabel("Cmd (m) :"),0,1)
        lay.addWidget(self.echCmdEdit,0,2)
        lay.addWidget(QLabel('Low Delay (s) :'),1,1)
        lay.addWidget(self.echDelayEdit,1,2)
        lay.addWidget(self.btnManual,2,0)
        lay.addWidget(self.cmdLabel,3,0,1,3)
        lay.addWidget(self.slider,4,0,1,3)

class LunchGroupBox(GroupBox):
    def __init__(self,title):
        super().__init__(title)
        lay = QVBoxLayout()
        lchBtn = QPushButton("LUNCH")
        lay.addWidget(lchBtn)
        self.setLayout(lay)

class GraphGroupBox(GroupBox):
    def __init__(self,title):
        super().__init__(title)
        self.setMinimumHeight(300)
        self.graph_title = title

        self.traceCombo = QComboBox()
        self.traceCombo.addItems(['Cmd','H','I','V','P'])
        self.traceCombo.currentIndexChanged.connect(self.comboUpdate)
        self.trace_title = self.traceCombo.currentText()

        self.traceColorCombo = QComboBox()
        self.traceColorCombo.addItems(['Black','Red','Green','Blue','Yellow'])
        self.traceColorCombo.currentIndexChanged.connect(self.comboUpdate)
        self.trace_color = self.traceColorCombo.currentText()

        mainLay = QHBoxLayout()
        lay = QFormLayout()
        mainLay.addLayout(lay)

        lay.addRow(QLabel("TRACE"),self.traceCombo)
        lay.addRow(QLabel("COLOR"),self.traceColorCombo)

        self.graph = pg.PlotWidget()
        self.graph.setBackground('w')
        self.curve = self.graph.plot()
        self.comboUpdate()
        #self.graph.setXRange(0,10)
        #self.graph.setYRange(-10,10)

        mainLay.addWidget(self.graph)
        self.setLayout(mainLay)

    def comboUpdate(self):
        print(self.graph_title)
        self.trace_title = self.traceCombo.currentText()
        self.trace_color = self.traceColorCombo.currentText()
        self.curve = self.graph.plot(pen = pg.mkPen(QColor(self.trace_color), width= 5))