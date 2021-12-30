import os
import cv2 
import math
import time 
import numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


folderPath = "FingersImg"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(os.path.join(folderPath, imPath))
    print(f'{folderPath}/{imPath}')
    overlayList.append(image)

detector = htm.handDetector()
tipIds = [4, 8, 12, 16, 20]

capture = cv2.VideoCapture(0)

while(True):
    ret, frame = capture.read()
    frame = detector.FindHands(frame)
    lmList = detector.FindHandsCoord(frame)
    if len(lmList) != 0:
        fingers = []
        #Polegar
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #Dedo indicador até o mindinho
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        
        totalFingers = fingers.count(1)
       
        h, w, c = overlayList[totalFingers-1].shape     
        frame[0:h, 0:w] = overlayList[totalFingers-1]         

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

