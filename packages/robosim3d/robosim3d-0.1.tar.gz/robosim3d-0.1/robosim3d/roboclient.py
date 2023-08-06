import socket
import time
import threading
import os
import sys
SERVER = "127.0.0.1"
PORT = 8052

class Robot:


    def __init__(self):
        self.maxForwardVel = 5
        self.maxSideVel = 5
        self.maxTurnVel = 90
        self.forwardVel = 0
        self.turnVel = 0
        self.sideVel = 0
        self.trueVel = (0,0,0)
        self.trueAngVel = 0
        self.gyroAngle = 0
        self.forwardDist = 19
        self.backDist = 0
        self.leftDist = 0
        self.rightDist = 0
        self.connected = True 
        self.turnedOn = True
        self.started = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        self.t1 = threading.Thread(target=self.inundate)
        self.t1.start()

    def inundate(self):
        try:
            while(self.connected):
                in_data =  self.client.recv(1024).decode()
                dataParts = in_data.split(' ')
                if(dataParts[0] != "data"):
                    return
                self.maxForwardVel = float(dataParts[1])
                self.maxSideVel = float(dataParts[2])
                self.maxTurnVel = float(dataParts[3])
                self.forwardVel = float(dataParts[4])
                self.turnVel = float(dataParts[5])
                self.sideVel = float(dataParts[6])
                self.trueVel = (float(dataParts[7]),float(dataParts[8]),float(dataParts[9]))
                self.trueAngVel = float(dataParts[10])
                self.gyroAngle = float(dataParts[11])
                self.forwardDist = float(dataParts[12])
                self.backDist = float(dataParts[13])
                self.leftDist = float(dataParts[14])
                self.rightDist = float(dataParts[15])
                self.turnedOn = True if int(dataParts[16]) == 1 else False
                self.started = True if int(dataParts[17]) == 1 else False
                if(not self.turnedOn):
                    self.sendKill()
                    self.connected = False
                    self.t1.join()
                    sys.exit(0)
                time.sleep(0.01)
        except:
            print("Disconnected")


    
    def setMaxForwardVel(self, val):
        string = "robocommand setMaxForwardVel " + str(val)+"|"
        self.client.sendall(bytes(string,'UTF-8'))
        time.sleep(0.001)

    def setMaxSideVel(self, val):
        string = "robocommand setMaxSideVel " + str(val)+"|"
        self.client.sendall(bytes(string,'UTF-8'))
        time.sleep(0.001)

    def setMaxTurnVel(self, val):
        string = "robocommand setMaxTurnVel " + str(val)+"|"
        self.client.sendall(bytes(string,'UTF-8'))
        time.sleep(0.001)

    def setForwardVel(self, val):
        string = "robocommand setForwardVel " + str(val)+"|"
        self.client.sendall(bytes(string,'UTF-8'))
        time.sleep(0.001)

    def setSideVel(self, val):
        string = "robocommand setSideVel " + str(val)+"|"
        self.client.sendall(bytes(string,'UTF-8'))
        time.sleep(0.001)

    def setTurnVel(self, val):
        string = "robocommand setTurnVel " + str(val)+"|"
        self.client.sendall(bytes(string,'UTF-8'))
        time.sleep(0.001)

    def sendKill(self):
        string = "robocommand kill 0|"
        self.client.sendall(bytes(string,'UTF-8'))
        time.sleep(0.001)

    def getMaxForwardVel(self):
       return self.maxForwardVel
        

    def getMaxSideVel(self):
        return self.maxSideVel

    def getMaxTurnVel(self):
        return self.maxTurnVel

    def getForwardVel(self):
        return self.forwardVel

    def getSideVel(self):
        return self.sideVel

    def getTurnVel(self):
        return self.turnVel

    def getTrueVelocity(self):
        return self.trueVel

    def getTrueAngularVelocity(self):
        return self.trueAngVel

    def getGyroAngle(self):
        return self.gyroAngle

    def getForwardDist(self):
        return self.forwardDist

    def getBackDist(self):
        return self.backDist

    def getLeftDist(self):
        return self.leftDist

    def getRightDist(self):
        return self.rightDist

    def stop(self):
        self.sendKill()
        self.client.close()
        self.connected = False

    def wait(self):
        if(not self.turnedOn):
            sys.exit(0)

    
    