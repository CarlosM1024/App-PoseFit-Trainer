import cv2
import numpy as np
import time
import PoseModule as pm
import os

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

count = 0
dir = 0
pTime = 0
detector = None

while True:
    ret, img = cap.read()
    if not ret or img is None:
        print("Frame vacío")
        continue

    img = cv2.resize(img, (1280, 720))

    # Crear MediaPipe SOLO cuando ya hay frames
    if detector is None:
        detector = pm.poseDetector()
        print("✅ MediaPipe inicializado")

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) > 15:
        # Calcular ángulo del codo izquierdo (hombro-codo-muñeca)
        angle = detector.findAngle(img, 11, 13, 15)
        
        # RANGOS CORREGIDOS:
        # Brazo extendido (casi recto): ~160-180 grados
        # Brazo flexionado (curl completo): ~30-50 grados
        
        # Interpolar porcentaje: 
        # 50 grados (flexionado) = 100%
        # 160 grados (extendido) = 0%
        per = np.interp(angle, (50, 160), (100, 0))
        
        # Barra visual (invertida para que suba al flexionar)
        bar = np.interp(angle, (50, 160), (100, 650))

        # Color según el estado
        color = (255, 0, 255)  # Magenta por defecto
        
        # Cuando está flexionado (100%)
        if per == 100:
            color = (0, 255, 0)  # Verde
            if dir == 0:
                count += 0.5
                dir = 1
        
        # Cuando está extendido (0%)
        if per == 0:
            color = (0, 255, 0)  # Verde
            if dir == 1:
                count += 0.5
                dir = 0

        # Dibujar barra de progreso
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75),
                    cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Mostrar el ángulo actual (para debug)
        cv2.putText(img, f'Angle: {int(angle)}', (50, 150),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)

        # Cuadro del contador
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670),
                    cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

    # Calcular FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime != 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (50, 100),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    cv2.imshow("IA Trainer", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
