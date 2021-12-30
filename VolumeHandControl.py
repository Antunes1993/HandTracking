import cv2 
import math
import time 
import numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

###############################################################
wCam, hCam = 640, 480
###############################################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector()

###############################################################
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
volBar = 400
vol = 0
###############################################################

while True:
    ret, frame = cap.read()
    detector.FindHands(frame, draw=False)
    lmList = detector.FindHandsCoord(frame, draw=False)    
    
    if len(lmList) != 0:
        print(lmList[4], lmList[8])
        x1,y1 = lmList[4][1], lmList[4][2]
        x2,y2 = lmList[8][1], lmList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2


        cv2.circle(frame, (x1,y1), 10, (255, 0, 150), cv2.FILLED)
        cv2.circle(frame, (x2,y2), 10, (255, 0, 150), cv2.FILLED)
        cv2.circle(frame, (cx,cy), 5, (255, 0, 150), cv2.FILLED)

        cv2.line(frame, (x1,y1), (x2,y2), (255, 0, 150), 2)

        length = round(math.hypot(x2-x1, y2-y1))
        cv2.putText(frame, str(length), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 150), 2)

        #Hand range - 11 to 140
        #Volume Range -65 - 0
        vol = np.interp(length, [11,110], [minVol, maxVol])
        volBar = np.interp(length, [11,110], [400, 150])
        volume.SetMasterVolumeLevel(vol, None)


    cv2.rectangle(frame, (50, 150), (85, 400), (255, 100, 50), 3)
    cv2.rectangle(frame, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

