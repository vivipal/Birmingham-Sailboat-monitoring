import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic

from UI import Ui_MainWindow

import serial
import time
import mysql.connector
import struct



class Update_DB_THREAD(QtCore.QThread):

    def __init__(self,db):
        QtCore.QThread.__init__(self)
        self.ser =  None
        self.send = False
        self.db = db

    def __del__(self):
        self.wait()

    def run(self):
        data = {'mode':0,'yaw':0,'ws':0,'wd':0,'SOG':0,'COG':0,'TWBD':0,'lat':0,'lon':0,'wp':0}
        sql = "INSERT INTO boat (lat, lon, heading, speed, true_wind_direction) VALUES (%s,%s,%s,%s,%s)"

        while 1 :
            if self.send and self.ser:
                try :
                    self.ser.write(b'i')
                    line = str(self.ser.readline())[4:-3]
                    L = line.split(";")
                    data['mode'] = float(L[0])
                    data['date'] = L[1]
                    data['wd'] = float(L[2])
                    data['ws'] = float(L[3])
                    data['yaw'] = float(L[4])
                    data['SOG'] = float(L[5])
                    data['lat'] = float(L[6])
                    data['lon'] = float(L[7])
                    data['TWBD'] = float(L[10])
                    data['COG'] = data['yaw']
                    data['wp'] = int(L[11])
                    print(L)
                except:
                    pass
                val = (data['lat'],data['lon'],data['yaw'],data['SOG'],data['TWBD'])
                # lat,lon = 52.484691,-1.888775
                # val = (lat,lon,data['yaw'],0,data['TWBD'])
                self.db.cursor().execute("DELETE FROM boat;")
                self.db.cursor().execute(sql, val,multi=False)
                self.db.commit()
            time.sleep(0.2)



class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.widget2disable = [self.ui.left,
                            self.ui.right,
                            self.ui.up,
                            self.ui.down,
                            self.ui.take_control_radio_button,
                            self.ui.update_radio_button,
                            self.ui.log_start,
                            self.ui.log_stop,
                            self.ui.lineEdit,
                            self.ui.send_mission_button]

        self.mydb = mysql.connector.connect(
          host="localhost",
          user="",
          password="",
          database=""
        )

        self.thread_update = Update_DB_THREAD(self.mydb)
        self.thread_update.start()


        for wid in self.widget2disable :
            wid.setEnabled(False)

        self.ui.left.clicked.connect(self.left_clicked)
        self.ui.right.clicked.connect(self.right_clicked)
        self.ui.up.clicked.connect(self.up_clicked)
        self.ui.down.clicked.connect(self.down_clicked)

        self.ui.connect_serial.clicked.connect(self.connect_serial)
        self.ui.disconnect_serial.clicked.connect(self.disconnect_serial)

        self.ui.take_control_radio_button.toggled.connect(self.controlMode)
        self.ui.update_radio_button.toggled.connect(self.update)

        self.ui.log_start.clicked.connect(self.start_log)
        self.ui.log_stop.clicked.connect(self.stop_log)

        self.ui.send_mission_button.clicked.connect(self.send_mission)


    def controlMode(self,checked):

        self.ui.left.setEnabled(checked)
        self.ui.right.setEnabled(checked)
        self.ui.up.setEnabled(checked)
        self.ui.down.setEnabled(checked)
        self.ui.log_start.setEnabled(not checked)
        self.ui.log_stop.setEnabled(not checked)
        self.ui.lineEdit.setEnabled(not checked)
        self.ui.update_radio_button.setEnabled(not checked)
        self.ui.send_mission_button.setEnabled(not checked)

        if checked :
            self.ser.write(b"c")
        else :
            self.ser.write(b"q")
            self.ui.control_text.setText("")
            self.ser.readline()



    def disconnect_serial(self):
        if self.ser :
            self.ui.update_radio_button.setChecked(False)
            self.ser.close()
            self.ser = None
            for wid in self.widget2disable :
                wid.setEnabled(False)
            self.ui.serial_connection_status.setText("*not connected*")
            self.ui.connect_serial.setEnabled(True)
            self.ui.disconnect_serial.setEnabled(False)
            self.thread_update.ser = self.ser

    def connect_serial(self):
        try:
            self.ser = serial.Serial(
              port=self.ui.serial_device.text(),
              baudrate = 9600,
              parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              bytesize=serial.EIGHTBITS,
              timeout=1
            )
        except:
            self.ui.serial_connection_status.setText("*could not open "+self.ui.serial_device.text()+"*")
        else:
            self.thread_update.ser = self.ser
            self.ui.serial_connection_status.setText("*"+self.ui.serial_device.text()+" openned*")
            for wid in self.widget2disable :
                wid.setEnabled(True)
            self.ui.connect_serial.setEnabled(False)
            self.ui.disconnect_serial.setEnabled(True)




    def update(self,checked):
        self.thread_update.send = checked

        if not checked :
            while self.ser.in_waiting > 0:
                self.ser.read()

        for wid in self.widget2disable:
            if wid != self.ui.update_radio_button:
                wid.setEnabled(not checked)



    def start_log(self):
        self.ser.write(b's')
        time.sleep(0.3)
        self.ser.write(b'o')
        time.sleep(0.3)
        self.ui.lineEdit.setText(str(self.ser.readline())[2:-5])

    def stop_log(self):
        self.ser.write(b's')
        time.sleep(0.3)
        self.ser.write(b'c')
        time.sleep(0.3)
        self.ui.lineEdit.setText(str(self.ser.readline())[2:-5])



    def left_clicked(self):
        if self.ui.take_control_radio_button.isChecked():
            self.ser.write(b"h")
            time.sleep(0.1)
            self.ui.control_text.setText(str(self.ser.readline())[2:-5])

    def right_clicked(self):
        if self.ui.take_control_radio_button.isChecked():
            self.ser.write(b"l")
            time.sleep(0.1)
            self.ui.control_text.setText(str(self.ser.readline())[2:-5])

    def up_clicked(self):
        if self.ui.take_control_radio_button.isChecked():
            self.ser.write(b"k")
            time.sleep(0.1)
            self.ui.control_text.setText(str(self.ser.readline())[2:-5])

    def down_clicked(self):
        if self.ui.take_control_radio_button.isChecked():
            self.ser.write(b"j")
            time.sleep(0.1)
            self.ui.control_text.setText(str(self.ser.readline())[2:-5])


    def send_mission(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open your save', '',"Fichier texte (*.txt);;All Files (*)")
        print(filename)

        with open(filename[0],'r') as f :
            LatLon_data =[]
            for l in f.readlines():
                lat,lon = l.split(' ')
                lat, lon = float(lat), float(lon)
                LatLon_data.append([lat,lon])

        sql = "INSERT INTO waypoints (lat, lon) VALUES (%s, %s)"
        self.mydb.cursor().execute("DELETE FROM waypoints;")

        self.ser.write(struct.pack("c",bytes('m','utf-8')))
        self.ser.write(struct.pack("B",len(LatLon_data)))

        for c in LatLon_data:
            data = struct.pack('<f',float(c[0]))
            self.ser.write(data)
            data = struct.pack('<f',float(c[1]))
            self.ser.write(data)

            val = (c[0],c[1])
            self.mydb.cursor().execute(sql, val,multi=False)
        self.mydb.commit()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()
