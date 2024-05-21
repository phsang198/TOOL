import cv2
import numpy as np
import win32api
import mss
import socket
from time import  sleep
from PyQt5.QtCore import QThread


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDP_IP = "192.168.1.50"
UDP_PORT = 8080
sct = mss.mss()


class Process(QThread):

    def __init__(self,parent=None):
        QThread.__init__(self,parent)
    
    

    def capture_frame(self):
        return np.array(sct.grab(self.baitap))


    def convert_to_hsv(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    def create_mask(self, hsv_frame):
        return cv2.inRange(hsv_frame, self.lower, self.upper)   


    def get_contour(self, mask):
        contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            return min(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
        
        

    def calculate_coordinates(self, contour):
        
        a,b = cv2.boundingRect(contour)[:2]
        A = int( a - self.mid ), int (b  - self.mid + self.offset)
        C = int(A[0] / self.speed_X), int(A[1] / self.speed_Y)
        return C[0], C[1]


    def run(self):
        while True:
            
            frame = self.capture_frame()
            hsv_frame = self.convert_to_hsv(frame)
            mask = self.create_mask(hsv_frame)
            contours = self.get_contour(mask)
            

            if contours is not None:
                

                result = self.calculate_coordinates(contours)
                x, y = int(result[0]), int(result[1])


                if  win32api.GetAsyncKeyState(self.virutal_key):
                    
                    if self.mouse_click:
                        self.mouse_X(x,y)
                        
                    elif self.rec_click:
                        self.rec_X(x)


                elif win32api.GetAsyncKeyState(self.virutal_key1):
                        self.alt_X(x,y)

                elif win32api.GetAsyncKeyState(self.virutal_key2):
                        self.only(x)



     
    def set_option(self,fov,offset,speed,speed_recoil,color,monitors,width,height,mouse_click,rec_click,mouse,mouse_1,mouse_2):
        self.mid = int(fov/2)
        self.shoot = float(1 + speed_recoil)
        self.offset = int(offset)
        self.speed  = float(speed)
        self.speed_recoil = float(speed_recoil)
        self.mouse_click = mouse_click
        self.rec_click = rec_click
        
        self.speed_X = float( self.speed + 0.9)
        self.speed_Y = float( self.speed + 1.1)

        self.baitap = sct.monitors[monitors]

        self.baitap = {"left": 0,"top": 0,"width": 0,"height": 0}


        self.baitap["left"]= int(width/2-self.mid)
        self.baitap["top"]= int(height/2-self.mid)
        self.baitap["width"]= int(fov)
        self.baitap["height"]= int(fov)

        if  color == "P":
            self.lower = np.array([140,70,204])
            self.upper = np.array([150,255,255])
        elif color == "Y":
            self.lower = np.array([30,157,252])
            self.upper = np.array([30,255,255])
        elif color == "R":
            self.lower = np.array([0,50,180])
            self.upper = np.array([0,255,255])

        if mouse == "ML":
            self.virutal_key = 0x01
        elif mouse == "NO":
            self.virutal_key = 0x00
        elif mouse == "AT":
            self.virutal_key = 0x12
        elif mouse == "CT":
            self.virutal_key = 0x11
        elif mouse == "M1":
            self.virutal_key = 0x06
        elif mouse == "M2":
            self.virutal_key = 0x05
        elif mouse == "MR":
            self.virutal_key = 0x02


        if mouse_1 == "AT":
            self.virutal_key1 = 0x12
        elif mouse_1 == "NO":
            self.virutal_key1 = 0x00
        elif mouse_1 == "ML":
            self.virutal_key1 = 0x01
        elif mouse_1 == "CT":
            self.virutal_key1 = 0x11
        elif mouse_1 == "M1":
            self.virutal_key1 = 0x06
        elif mouse_1 == "M2":
            self.virutal_key1 = 0x05
        elif mouse_1 == "MR":
            self.virutal_key1 = 0x02


        if mouse_2 == "NO":
            self.virutal_key2 = 0x00
        elif mouse_2 == "ML":
            self.virutal_key2 = 0x01
        elif mouse_2 == "AT":
            self.virutal_key2 = 0x12
        elif mouse_2 == "CT":
            self.virutal_key2 = 0x11
        elif mouse_2 == "M1":
            self.virutal_key2 = 0x06
        elif mouse_2 == "M2":
            self.virutal_key2 = 0x05
        elif mouse_2 == "MR":
            self.virutal_key2 = 0x02
          
        
    def mouse_X(self,x,y):
        if not self.mouse_click:
            return
        data = f'{x},{y}'.encode()
        sock.sendto(data,(UDP_IP, UDP_PORT))



    def alt_X(self,x,y):
        data = f'{x},{y}'.encode()
        sock.sendto(data,(UDP_IP, UDP_PORT))

    
    def rec_X(self,x):
        shoot = self.shoot
        data = f'{x},{shoot}'.encode()
        sock.sendto(data,(UDP_IP, UDP_PORT))

    def only(self,x):
        data = f'{x}'.encode()
        sock.sendto(data,(UDP_IP, UDP_PORT))


        
class Trigger(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        
    
    def run(self):
     
     while True:

        if   self.cboxTrigger_2 == "P":
                self.lower = np.array([140,70,204])
                self.upper = np.array([150,255,255])
        elif self.cboxTrigger_2 == "Y":
                self.lower = np.array([30,157,252])
                self.upper = np.array([30,255,255])
        elif self.cboxTrigger_2 == "R":
                self.lower = np.array([0,50,180])
                self.upper = np.array([0,255,255])

     
        if self.cboxTrigger == "F":
                self.key = 0x46
        elif self.cboxTrigger == "SHT":
                self.key = 0x10
        elif self.cboxTrigger == "AT":
                self.key = 0x12
        elif self.cboxTrigger == "M1":
                self.key = 0x05
        elif self.cboxTrigger == "M2":
                self.key = 0x06

        if win32api.GetAsyncKeyState(self.key):
             haha = self.grab()
             mask = cv2.inRange(haha,self.lower,self.upper) 
             contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
             for contour in contours:
                  result = cv2.boundingRect(contour)[:2]
                  x, y = int(result[0]), int(result[1])
                  self.str(x,y)



        sleep(self.spTimer)
             
        
        
             
    def set_option(self,zoneTrigger,cboxTrigger,cboxTrigger_2,width,height,spTimer):
        self.zoneTrigger = zoneTrigger
        self.cboxTrigger = cboxTrigger
        self.cboxTrigger_2 = cboxTrigger_2
        self.width = width
        self.height = height
        self.spTimer = spTimer
        

    def str(self,x,y):
        shoot = 1
        data = f'{int(x)},{int(y)},{shoot}'.encode()
        sock.sendto(data,(UDP_IP, UDP_PORT))


    def grab(self):
        S_HEIGHT = self.width
        S_WIDTH  = self.height
        GRABZONE = self.zoneTrigger
        bbox     = (int(S_HEIGHT / 2 - GRABZONE), int(S_WIDTH / 2 - GRABZONE), int(S_HEIGHT / 2 + GRABZONE), int(S_WIDTH / 2 + GRABZONE))
        sct_img  = np.array(sct.grab(bbox))
        return cv2.cvtColor(sct_img, cv2.COLOR_BGR2HSV)


    def stop(self):
        self.terminate()
