import cv2 
import mediapipe as mp 
import time 

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands 


'''
hands = mpHands.Hands()
Default Values: 
static_image_mode = False
max_num_hands = 2 
min_detection_confidence = 0.5
min_tracking_confidence = 0.5

[Portuguese] Se colocarmos o valor static_image_mode = False, as vezes a mão será detectada e as vezes será seguida, de acordo 
com o intervalo de confiança. Se colocarmos como True, sempre será ativado o script de detecção, o que fará com que o programa 
seja mais lento.
'''
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0 
cTime = 0 

while True:
    ret, frame = cap.read()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)

    #Verifica se foram detectadas mãos
    #print(results.multi_hand_landmarks)
    #Extrair as multiplas mãos detectadas: 
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            #Desenha os landmarks na imagem
            mpDraw.draw_landmarks(frame, handLandmarks, mpHands.HAND_CONNECTIONS)
            
            #Exibe a posição em xyz de cada landmark da mão. (As coordenadas estão em pixels)
            for id, lm in enumerate(handLandmarks.landmark):
                print(id) #id do landmark
                print(lm) #coordenadas em pixels
                h, w ,c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)  #id do landmark, coordenadas considerando a largura e altura da imagem
                
                #Desenha um circulo amarelo em um landmark específico, de acordo com o ID. ID = 0 é o ponto mais próximo ao pulso.
                if id==0:
                    cv2.circle(frame, (cx, cy), 10, (0,255,255), -1)            

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
