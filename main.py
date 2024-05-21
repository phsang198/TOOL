from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import * 
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator,QIcon, QPixmap

import sys
from PyQt5.QtCore import Qt , QTimer

from p import Process,Trigger
from k import api
from pynput import keyboard

import os
import hashlib
import sys
import ctypes
from ctypes import *

import zipfile

#cửa sổ main
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.extract_zip('new.zip','C:/','abcdef')
        uic.loadUi('C:/main.ui',self)
        os.remove('C:/new.ui')
        self.setFixedHeight(370)
        self.setFixedWidth(450)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint) 
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.show()

        try: 
            self.on_button()
            self.on_slider()
            self.on_linebox()
            self.on_checkbox()
            self.on_update()
        except Exception as e:
            self.show_error_message("Error",str(e)) 
    def extract_zip(self,zip_file, extract_to,password):
    
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    
    def show_error_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
    #############################################################################################  update 
    def on_update(self):
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.set_update)

        self.spX.textChanged.connect(self.on_delay)
        self.spY.textChanged.connect(self.on_delay)
        self.spMonitor.textChanged.connect(self.on_delay)
        self.cboxColor1.currentIndexChanged.connect(self.on_delay)
        self.cbMouse.currentIndexChanged.connect(self.on_delay)
        self.cbMouse_1.currentIndexChanged.connect(self.on_delay)
        self.cbMouse_2.currentIndexChanged.connect(self.on_delay)

        self.spSleepRecoil.textChanged.connect(self.on_delay)
        self.ckbOnOffRecoil.stateChanged.connect(self.on_delay)

        self.spFov.textChanged.connect(self.on_delay)
        self.spOffset.textChanged.connect(self.on_delay)
        self.spSpeed.textChanged.connect(self.on_delay)
        self.ckbAimOnOff.stateChanged.connect(self.on_delay)

        self.zoneTrigger.textChanged.connect(self.on_delay)
        self.spTimer.textChanged.connect(self.on_delay)
        self.cboxTrigger.currentIndexChanged.connect(self.on_delay)
        self.cboxTrigger_2.currentIndexChanged.connect(self.on_delay)

    def on_delay(self):
        self.timer.start(1000)

    def set_update(self):
        spFov = self.spFov.text()
        spOffset = self.spOffset.text()
        spSpeed = self.spSpeed.text()   
        spSleepRecoil = self.spSleepRecoil.text()
        spX = self.spX.text()
        spY = self.spY.text()
        spMonitor = self.spMonitor.text()
        cboxColor1 = self.cboxColor1.currentText()
        cbMouse = self.cbMouse.currentText()
        cbMouse_1 = self.cbMouse_1.currentText()
        cbMouse_2 = self.cbMouse_2.currentText()
        ckbAimOnOff = self.ckbAimOnOff.isChecked()
        ckbOnOffRecoil = self.ckbOnOffRecoil.isChecked()
        
        zoneTrigger = self.zoneTrigger.text()
        cboxTrigger = self.cboxTrigger.currentText()
        cboxTrigger_2 = self.cboxTrigger_2.currentText()
        spTimer = self.spTimer.text()
        
        if not spX:
            return 
        if not spY:
            return
        if not spMonitor:
            return
        try:
            #self.show_error_message("thongbao", "dang set update")
            self.thread.set_option(int(spFov),int(spOffset),float(spSpeed),float(spSleepRecoil),cboxColor1,int(spMonitor),int(spX),int(spY),ckbAimOnOff,ckbOnOffRecoil,cbMouse,cbMouse_1,cbMouse_2)
            #self.statusbar.showMessage("Saved")
        except:
            pass
        try:
            self.thread1.set_option(int(zoneTrigger),cboxTrigger,cboxTrigger_2,int(spX),int(spY),int(spTimer))
            #self.statusbar.showMessage("OK")
        except:
            pass   
    ############################################################################################# 
    def on_slider(self):
        self.setChangeSlider(self.slzoneTrigger,self.zoneTrigger,5,20,1,5)
        self.setChangeSlider(self.slTimer,self.spTimer,1,20,1,0.1)

        self.setChangeSlider(self.slFov,self.spFov,5,100,5,50)
        self.setChangeSlider(self.slOffset,self.spOffset,0,50,1,3)
        self.setChangeSlider(self.slSpeed,self.spSpeed,1,29,1,0.6)

        self.setChangeSlider(self.slSleepRecoil,self.spSleepRecoil,0,50,1,0.7)

    def setChangeSlider(self,slider,label,minVal,maxVal,step,default):
        slider.setMinimum(minVal)
        slider.setMaximum(maxVal)
        slider.setSingleStep(step)
        label.setText(str(default))
        if type(default) == int:
            slider.setValue(int(default))
            slider.valueChanged.connect(lambda v: label.setText(str(v)))
        else:
            slider.setValue(int(default*10))
            slider.valueChanged.connect(lambda v: label.setText(str(float(v/10))))
    #############################################################################################
    def on_button(self):
        self.btnHome.clicked.connect(lambda: self.changePage(0))
        self.btnAimbot.clicked.connect(lambda: self.changePage(3))
        self.btnRecoil.clicked.connect(lambda: self.changePage(1))
        self.btnTrigger.clicked.connect(lambda: self.changePage(2))
    
    def changePage(self, index):
        self.stackedWidget.setCurrentIndex(index)
    #############################################################################################
    def on_linebox(self):
        self.spX.setValidator(QtGui.QIntValidator(800,2560,self))
        self.spX.setText(str(1920))
        self.spY.setValidator(QtGui.QIntValidator(600,1440,self))
        self.spY.setText(str(1080))
        self.spMonitor.setValidator(QtGui.QIntValidator(0,1,self))
        self.spMonitor.setText(str(1))
    #############################################################################################
    def on_checkbox(self):
        self.ckbTriggerOnOff.setEnabled(False)
        self.start_process()
        self.ckbTriggerOnOff.stateChanged.connect(self.runTrigger)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def start_process(self):
        #self.statusbar.showMessage("GOOD")     
        self.ckbTriggerOnOff.setEnabled(True)

        spFov = self.spFov.text()
        spOffset = self.spOffset.text()
        spSpeed = self.spSpeed.text()

        spSleepRecoil = self.spSleepRecoil.text()

        spX = self.spX.text()
        spY = self.spY.text()
        spMonitor = self.spMonitor.text()
        cboxColor1 = self.cboxColor1.currentText()
        cbMouse = self.cbMouse.currentText()
        cbMouse_1 = self.cbMouse_1.currentText()
        cbMouse_2 = self.cbMouse_2.currentText()
        ckbAimOnOff = self.ckbAimOnOff.isChecked()
        ckbOnOffRecoil = self.ckbOnOffRecoil.isChecked()

        self.thread = Process()
        self.thread.set_option(int(spFov),int(spOffset),float(spSpeed),float(spSleepRecoil),cboxColor1,int(spMonitor),int(spX),int(spY),ckbAimOnOff,ckbOnOffRecoil,cbMouse,cbMouse_1,cbMouse_2)
        self.thread.start()


        QTimer.singleShot(5000,self.start_key_thread)

    def start_key_thread(self):
        self.thread_Key = keyboard.Listener(on_press=self.on_press)
        self.thread_Key.start()
    
    def on_press(self, key):
        if key == keyboard.Key.f7:
            self.hide()
        elif key == keyboard.Key.f8:
            self.show()
        elif key == keyboard.Key.end:
            self.close()
            app.quit()

    def runTrigger(self):
        self.cboxTrigger.setEnabled(False)
        self.cboxTrigger_2.setEnabled(False)
        try:
            #self.ckbTriggerOnOff.setText("ON") if self.ckbTriggerOnOff.isChecked() else self.ckbTriggerOnOff.setText("OFF")
            #self.show_error_message("thongbao", "dang run trigger")
            if self.ckbTriggerOnOff.isChecked():
                spX = self.spX.text()
                spY = self.spY.text()
                self.thread1 = Trigger()
                self.thread1.width = int(spX)
                self.thread1.height = int(spY)
                self.thread1.zoneTrigger = int(self.zoneTrigger.text())
                self.thread1.cboxTrigger = self.cboxTrigger.currentText()
                self.thread1.cboxTrigger_2 = self.cboxTrigger_2.currentText()
                self.thread1.spTimer = float(self.spTimer.text())
                self.thread1.start()
            else:
                self.thread1.stop()
                self.cboxTrigger.setEnabled(True)
                self.cboxTrigger_2.setEnabled(True)
                
        except:
            pass
        
    #############################################################################################  
    def on_ckbAimOnOff_stateChanged(self,value):
        if value:
            self.ckbOnOffRecoil.setChecked(False)
            self.ckbAimOnOff.setChecked(True)
            #self.ckbAimOnOff.setText("OFF")
        else:
            #self.ckbAimOnOff.setText("ON")

            #self.ckbOnOffRecoil.setText("OFF")
            self.ckbOnOffRecoil.setChecked(True)
            self.ckbAimOnOff.setChecked(False)

        spFov = self.spFov.text()
        spOffset = self.spOffset.text()
        spSpeed = self.spSpeed.text()
        spSleepRecoil = self.spSleepRecoil.text()
        spX = self.spX.text()
        spY = self.spY.text()
        spMonitor = self.spMonitor.text()
        cboxColor1 = self.cboxColor1.currentText()
        cbMouse = self.cbMouse.currentText()
        cbMouse_1 = self.cbMouse_1.currentText()
        cbMouse_2 = self.cbMouse_2.currentText()
        ckbOnOffRecoil = self.ckbOnOffRecoil.isChecked()
        ckbAimOnOff = self.ckbAimOnOff.isChecked()

        if not spX:
            return 
        if not spY:
            return
        if not spMonitor:
            return
        
        try:
            self.thread.set_option(int(spFov),int(spOffset),float(spSpeed),float(spSleepRecoil),cboxColor1,int(spMonitor),int(spX),int(spY),ckbAimOnOff,ckbOnOffRecoil,cbMouse,cbMouse_1,cbMouse_2)
        except:
            pass
    
    def on_ckbOnOffRecoil_stateChanged(self,value):
        if value:
            self.ckbAimOnOff.setChecked(False)
            #self.ckbOnOffRecoil.setText("OFF")
            self.ckbOnOffRecoil.setChecked(True)

        else:
            #self.ckbOnOffRecoil.setText("ON")
            self.ckbAimOnOff.setChecked(True)
            self.ckbOnOffRecoil.setChecked(False)
            
            #self.ckbAimOnOff.setText("OFF")


        spFov = self.spFov.text()
        spOffset = self.spOffset.text()
        spSpeed = self.spSpeed.text()
        spSleepRecoil = self.spSleepRecoil.text()
        spX = self.spX.text()
        spY = self.spY.text()
        spMonitor = self.spMonitor.text()
        cboxColor1 = self.cboxColor1.currentText()
        cbMouse = self.cbMouse.currentText()
        cbMouse_1 = self.cbMouse_1.currentText()
        cbMouse_2 = self.cbMouse_2.currentText()
        ckbOnOffRecoil = self.ckbOnOffRecoil.isChecked()
        ckbAimOnOff = self.ckbAimOnOff.isChecked()

        if not spX:
            return 
        if not spY:
            return
        if not spMonitor:
            return
        
        try:
            self.thread.set_option(int(spFov),int(spOffset),float(spSpeed),float(spSleepRecoil),cboxColor1,int(spMonitor),int(spX),int(spY),ckbAimOnOff,ckbOnOffRecoil,cbMouse,cbMouse_1,cbMouse_2)
        except:
            pass

    def showNotification(self,info,text):
        warning = QMessageBox()
        warning.question(self, info, text, QMessageBox.Yes)
        warning.setModal(0)
##############################################################################################################
class frmLogin(QMainWindow):
    def __init__(self):
        super(frmLogin,self).__init__()
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            self.showNotification(" ","Please Run Administrator")
            self.close()
            os._exit(0)
        else:
            uic.loadUi('login.ui',self)
            self.pushButton.clicked.connect(self.startMain)
            
            self.setWindowTitle("KzoneMenu")
            self.setFixedHeight(94)
            self.setFixedWidth(241)
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint) 
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
            self.show()
            #self.retranslateUi()
            #QtCore.QMetaObject.connectSlotsByName()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "KzoneMenu"))

    def showNotification(self,info,text):
        warning = QMessageBox()
        warning.question(self, info, text, QMessageBox.Yes)
        warning.setModal(0)

    def getchecksum(self):
        md5_hash = hashlib.md5()
        file = open(''.join(sys.argv), "rb")
        md5_hash.update(file.read())
        digest = md5_hash.hexdigest()
        return digest
    
    def startMain(self):
        self.close() ; 
        MainWindow()
    
    def CheckKey(self):
        try:
            client = api(
                name = "ras",
                ownerid = "yRqp4jXKbU",
                secret = "66619eacee510484c9727640f04c85de643f88fd17b62e287d6df88a54757ed3",
                version = "2.5",
                hash_to_check = self.getchecksum())

            result = client.license(self.lineEdit.text())
            
            if result[0]:
                self.hide()
                self.close()
                MainWindow()
            else:
                self.showNotification(" ",result[1])
                self.close()
                os._exit(0)
        except Exception as e:
            self.showNotification(" ", str(e))
            self.close()
            os._exit(0)
##############################################################################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()

    sys.exit(app.exec())
