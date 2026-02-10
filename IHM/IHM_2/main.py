#Yassine

import sys
from turtle import distance 
from PyQt5.QtWidgets import QMainWindow,QApplication
from GUI import *
from customSerial import customSerial
import serial
import time
import random

class MiApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		#Serial
		self.serial = customSerial()

		self.ui.BaudList.addItems(self.serial.baudratesDIC.keys())
		self.ui.BaudList.setCurrentText('115200')
		self.update_ports()
		
		#Events
		self.ui.connectBtn.clicked.connect(self.connect_serial)
		self.ui.sendBtn.clicked.connect(self.send_data)
		self.ui.distance_button.clicked.connect(self.sendDisCommand)
		self.ui.updateBtn.clicked.connect(self.update_ports)
		self.ui.clearBtn.clicked.connect(self.clear_terminal)
		self.serial.data_available.connect(self.update_terminal)

	def update_terminal(self,data):
		self.ui.Terminal.append(data)
	#Établissement de la connection
	def connect_serial(self):
		if(self.ui.connectBtn.isChecked()):
			port = self.ui.portList.currentText()
			baud = self.ui.BaudList.currentText()
			self.serial.serialPort.port = port 
			self.serial.serialPort.baudrate = baud
			self.serial.connect_serial()
			
			if(self.serial.serialPort.is_open):
				self.ui.connectBtn.setText('DECONNECTER')
				#print("Connecté")

			else:
				#print("pas connecté")
				self.ui.connectBtn.setChecked(False)
			
		else:
			
			self.serial.disconnect_serial()
			self.ui.connectBtn.setText('CONNECTER')
	
	#Réception
	def onRead():
		#if not serial.canReadLine(): return
		rx = serial.readline()
		rxs = str(rx, 'utf-8').strip()
		print(rxs)
		data = rxs.split(',')
		dt = data[0].strip().replace("\x00","")
		print(dt)
		if dt == '0':
			ui.tension_ressort.display(data[1])
		if dt == '2':
			ui.puissance_chaufe.display(data[1])
		if dt == '3':
			global listX
			global listY
			listY = listY[1:]
			listY.append(int(data[1]))
			ui.widget_graph.clear()
			ui.widget_graph.plot(listY)
			ui.position_masse.display(data[1])
	
	#Envoi des données ----------------------------------------------------------------------------
	def send_data(self):
		data = self.ui.input.text()
		print(data,type(data))
		self.serial.send_data(data)

	#Envoi de la distance
	def sendDisCommand(self): 
		distance =[0]*2
		valueTosend = ui.distance_input.text()
		valueTosend = int(valueTosend)
		distance[0]=1
		distance[1]=valueTosend
		serial.write(bytearray(distance))
	
	#Actualisation des ports
	def update_ports(self):
		self.serial.update_ports()
		self.ui.portList.clear()
		self.ui.portList.addItems(self.serial.portList)
	#Reset
	def clear_terminal(self):
		self.ui.Terminal.clear()
	#Deconnexion
	def closeEvent(self,e):
		self.serial.disconnect_serial()

class Serial(serial.Serial):
	def __init__(self,COM,baud):
		super().__init__()
		self.port = COM
		self.baudrate = baud

	def update(self):
		value = random.randrange(0,100,1)
		self.serialWrite(value)

	def serialWrite(self,value):
		valuebyte = value.to_bytes(2,'big')
		print(value,valuebyte,int.from_bytes(valuebyte,'big'))
		ser = serial.Serial(self.port, self.baudrate, timeout=None)
		ser.write(valuebyte)
		ser.close()

#Affichage graphique
listX = []
for x in range(2000): listX.append(0)
listY = []
for x in range(100): listY.append(80)
#ui.widget_graph.setYRange(0,200); #(80,200)
#ui.widget_graph.setXRange(0,200);



if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = MiApp()
	w.show()
	sys.exit(app.exec_())


	#****************************************************************************
