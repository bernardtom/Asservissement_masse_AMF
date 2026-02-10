import serial
import serial.tools.list_ports

class SerialCom():
    def __init__(self):
        self.rcv_h = 0
        self.rcv_i = 0
        self.rcv_v = 0

    def openSerial(self,port,baudrate):
        self.ser = serial.Serial(port,baudrate,timeout = None)

    def serialWrite(self,data : int):
        data_to_send = str(data)+"\n"
        data_to_send = data_to_send.encode('ascii')
        self.ser.write(data_to_send)
        print(f'cmd : {data_to_send}')

    def serialRead(self):
        tram = self.ser.readline().decode('utf-8')
        try:
            iH = tram.find('H')
            iV = tram.find('V')
            iI = tram.find('I')
            self.rcv_h = int(tram[iH+1:iV])
            self.rcv_v = int(tram[iV+1:iI])/1000
            self.rcv_i = int(tram[iI+1:])/1000
        except:
            pass
        #print(f'h : {self.rcv_h} ; v : {self.rcv_v} ; i : {self.rcv_i}')
        return(self.rcv_h,self.rcv_v,self.rcv_i)

    def serialPamInit(self):
        comList = [comport.device for comport in serial.tools.list_ports.comports()]
        baudList = ["9600","115200"]
        return(comList,baudList)

    def closeSerial(self):
        self.ser.close()
            
