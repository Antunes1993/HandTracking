
import os 
import cv2 
import time 
import numpy as np 
from modules import HandTrackingModule as htm
import socket 


#Instancia variáveis
width, height = 1280, 720
drawColor = (255,0,0)
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = htm.handDetector()

#Comunicação 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddressPort = ("127.0.0.1", 5052)

#Loop principal
while True: 
    data = []
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    #Detecta landmarks das mãos
    detector.FindHands(frame, draw=True)
    lmList = detector.FindHandsCoord(frame, draw=True)

    if len(lmList) != 0:
        for lm in lmList:
            #Arrumar dados para enviar para o unit.
            data.extend([lm[0], height - lm[1], lm[2]])
        #print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)


    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()    