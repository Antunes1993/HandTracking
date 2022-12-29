
import os 
import cv2 
import time 
import numpy as np 
from modules import HandTrackingModule as htm




#Instancia variáveis
drawColor = (255,0,0)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector()
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280,3), np.uint8)

#Loop principal
while True: 
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    #Detecta landmarks das mãos
    detector.FindHands(frame, draw=False)
    lmList = detector.FindHandsCoord(frame, draw=False)

    if len(lmList)!= 0:
        x1,y1 = lmList[8][1:]  #first finger
        x2,y2 = lmList[12][1:] #second finger

    fingers = detector.FindFingers()
    #print(fingers)
    if len(fingers) == 5:
        #Modo de seleção (2 dedos levantados) 
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0

            cv2.rectangle(frame, (x1,y1-25), (x2,y2+25),drawColor, cv2.FILLED)
            #print(fingers, " Selection Mode")
            
            #Verifica se estamos no topo da janela para verificar se estamos em posição de clique.
            if x1 < 300:                
                if 50 < y1 < 100:
                    #print("Azul")
                    drawColor = (255,0,0) 
                if 120 < y1 < 170:
                    #print("Verde")
                    drawColor = (0,255,0) 
                if 190 < y1 < 240:
                    #print("Vermelho")
                    drawColor = (0,0,255) 
                if 260 < y1 < 310:
                    #print("Preto")
                    drawColor = (0,0,0) 
                
        #Modo desenho (1 dedo levantado)
        if fingers[1] and fingers[2] == False:
            cv2.circle(frame, (x1,y1), 10, drawColor, cv2.FILLED)
            #print(fingers, "Drawing Mode")

            if xp==0 and yp==0:
                xp, yp = x1, y1
            
            if drawColor == (0,0,0):
                cv2.line(imgCanvas, (xp,yp), (x1,y1), (0,0,0), 110)
            else:
                cv2.line(frame, (xp,yp),(x1,y1),drawColor,3)
                cv2.line(imgCanvas, (xp,yp),(x1,y1),drawColor,3)

            xp,yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 127, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, imgInv)
    frame = cv2.bitwise_or(frame, imgCanvas)



    #Painel de cores
    cv2.rectangle(frame, (100,50), (300,100), (255,0,0), 2)
    cv2.putText(frame, "Destacar", (110,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
    cv2.rectangle(frame, (100,120), (300,170), (0,255,0), 2)
    cv2.putText(frame, "Ligar", (110,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
    cv2.rectangle(frame, (100,190), (300,240), (0,0,255), 2)
    cv2.putText(frame, "Desligar", (110,220), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
    cv2.rectangle(frame, (100,260), (300,310), (0,0,0), 2)
    cv2.putText(frame, "Apagar", (110,290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
    
    #frame = cv2.addWeighted(frame, 0.5, imgCanvas, 0.5, 0)

    cv2.imshow("Frame", frame)
    #cv2.imshow("Canvas", imgCanvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()    