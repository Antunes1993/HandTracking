#Modules
import cv2 
import mediapipe as mp 
import time 


class handDetector(): 
    def __init__(self, mode=False, maxHands=2, detectionConf=0.95, trackConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        self.mpHands = mp.solutions.hands 
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

        self.tipsIds = [4, 8, 12, 16, 20] #Finger Tips

    #Find hands in a frame
    def FindHands(self, frame, draw = True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        self.results = self.hands.process(frameRGB)         
        

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw: 
                    #Draw landmarks in input image
                    self.mpDraw.draw_landmarks(frame, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return frame
    
    #Find hand's coordinates in a frame
    def FindHandsCoord(self, frame, handLandMarkId=0, draw=True):
        self.lmList = []

        if self.results.multi_hand_landmarks: 
            #Select wich hand will be used (always the first one)
            myHand = self.results.multi_hand_landmarks[0]

            #Shows the coordinates of the hand's landmarks
            for id, lm in enumerate(myHand.landmark):
                #print(id) #landmark id
                #print(lm) #pixels coordinates
                h, w ,c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])  #landmark id considering the width and height of the image
                
                
                #Draws yellow circles in the landmarks of the hand. id = 0 --> point closest to pulse
                if draw:
                    if id==0:                     
                        cv2.circle(frame, (cx, cy), 10, (255,0,155), -1)  
        return self.lmList

    def FindFingers(self):
        fingers = []
       
        if (len(self.lmList) > 0):
            #Thumb 
            if self.lmList[self.tipsIds[0]][1] > self.lmList[self.tipsIds[0]-1][1]:
                fingers.append(0)
            else:
                fingers.append(1)

            #Other fingers
            for id in range(1,5):
                if self.lmList[self.tipsIds[id]][2] > self.lmList[self.tipsIds[id]-2][2]:
                    fingers.append(0)
                else:
                    fingers.append(1)
        
        return fingers


def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    pTime = 0 
    cTime = 0 

    while True:
        ret, frame = cap.read()
        detector.FindHands(frame)
        lmList = detector.FindHandsCoord(frame)
        
        #Calculando e exibindo a taxa de FPS
        cTime = time.time()
        fps = 1/(cTime - pTime) 
        pTime = cTime       
        cv2.putText(frame, "FPS: " + str(int(fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()