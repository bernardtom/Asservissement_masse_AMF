from random import *
import time
import threading
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Tabs():
    def __init__(self):
        self.clearTab()

    def setCmdTab(self,cmd):
        self.time_tab.append(self.cnt)
        self.cmd_tab.append(cmd)
        self.cnt += 1

    def setStepTab(self,cmd : int,low_time : int):
        if self.cnt < low_time:
            self.setCmdTab(0)
        else: self.setCmdTab(cmd)
    
    def setTab(self,cmd,h,v,i):
        self.time_tab.append(self.cnt)
        self.cmd_tab.append(cmd)
        self.h_tab.append(h)
        self.v_tab.append(v)
        self.i_tab.append(i)
        self.p_tab.append(v*i)
        self.cnt += 1
    
    def clearTab(self):
        self.cnt = 0
        self.time_tab = []
        self.cmd_tab = []
        self.h_tab = []
        self.i_tab = []
        self.v_tab = []
        self.p_tab = []

    