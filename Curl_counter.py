import cv2
import mediapipe as mp
import numpy as np
from math import acos, degrees

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

#Variables booleanas
up = False
down = False
count = 0
dir = 0
post = 0
col = "Incorrecto"

with mp_pose.Pose(static_image_mode=False) as pose:

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1280, 720))
        if ret == False:
            break
        #frame = cv2.flip(frame,1)
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks is not None:
            x1 = int(results.pose_landmarks.landmark[11].x * width)
            y1 = int(results.pose_landmarks.landmark[11].y * height)

            x2 = int(results.pose_landmarks.landmark[13].x * width)
            y2 = int(results.pose_landmarks.landmark[13].y * height)

            x3 = int(results.pose_landmarks.landmark[15].x * width)
            y3 = int(results.pose_landmarks.landmark[15].y * height)

            x4 = int(results.pose_landmarks.landmark[11].x * width)
            y4 = int(results.pose_landmarks.landmark[11].y * height)

            x5 = int(results.pose_landmarks.landmark[23].x * width)
            y5 = int(results.pose_landmarks.landmark[23].y * height)

            x6 = int(results.pose_landmarks.landmark[25].x * width)
            y6 = int(results.pose_landmarks.landmark[25].y * height)

            #Trigonometria
            p1 = np.array([x1, y1])
            p2 = np.array([x2, y2])
            p3 = np.array([x3, y3])
            p4 = np.array([x4, y4])
            p5 = np.array([x5, y5])
            p6 = np.array([x6, y6])

            l1 = np.linalg.norm(p2 - p3)
            l2 = np.linalg.norm(p1 - p3)
            l3 = np.linalg.norm(p1 - p2)

            l4 = np.linalg.norm(p5 - p6)
            l5 = np.linalg.norm(p4 - p6)
            l6 = np.linalg.norm(p4 - p5)

            #Calcular el angulo
            angle = degrees(acos((l1**2 + l3**2 - l2**2)/(2*l1*l3)))
            angle2 = degrees(acos((l4**2 + l6**2 - l5**2)/(2*l4*l6)))

            if (180 >= angle2 >= 175) :
                col = "Buena postura"
                post = True
            if (180 < angle2 < 175):
                col = "Mala postura"
                post = False

            if angle >= 170:
                up = True
            if up == True and down == False and angle <= 50 and post == True:
                down = True
            if up == True and down == True and angle >= 170 and post == True:
                count += 1
                up = False
                down = False

            per = np.interp(angle, (45, 170), (0, 100))
            bar = np.interp(angle, (45, 170), (650, 100))
            # print(angle, per)

            # check for the dumbbell curls
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
            if per == 0:
                color = (0, 255, 0)

            #Visualizacion
            #Dibujar lineas entre puntos
            aux_imge = np.zeros(frame.shape, np.uint8)
            cv2.line(aux_imge, (x1, y1), (x2, y2), (255,255,0), 20)
            cv2.line(aux_imge, (x2, y2), (x3, y3), (255, 255, 0), 20)
            cv2.line(aux_imge, (x3, y3), (x1, y1), (255, 255, 0), 5)
            cv2.line(aux_imge, (x4, y4), (x5, y5), (255, 255, 0), 5)
            cv2.line(aux_imge, (x5, y5), (x6, y6), (255, 255, 0), 5)

            countours = np.array([[x1, y1], [x2, y2], [x3, y3]])
            cv2.fillPoly(aux_imge, pts=[countours], color=(128, 0, 250))

            output = cv2.addWeighted(frame, 1, aux_imge, 0.8, 0)
            #Dibujar circulos en puntos
            cv2.circle(output, (x1, y1), 6, (0, 255, 255), 4)
            cv2.circle(output, (x2, y2), 6, (128, 0, 250), 4)
            cv2.circle(output, (x3, y3), 6, (255, 191, 0), 4)
            cv2.circle(output, (x4, y4), 6, (0, 255, 255), 4)
            cv2.circle(output, (x5, y5), 6, (128, 0, 250), 4)
            cv2.circle(output, (x6, y6), 6, (255, 191, 0), 4)

            cv2.rectangle(output, (0,0), (60,60), (255, 255, 0), -1)
            #Dibujar el angulo entre lineas de brazo
            cv2.putText(output, str(int(angle)), (x2 + 30, y2), 1, 1.5, (128, 0, 250), 2)
            #Dibujar la cuenta en la pantalla
            cv2.putText(output, str(count), (10, 50), 1, 1.5, (128, 0, 250), 2)

            #Dibujar barra
            cv2.rectangle(output, (1100, 100), (1175, 650), color, 3)
            cv2.rectangle(output, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
            cv2.putText(output, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

            #Dibujar el angulo del torso en la pantalla
            cv2.putText(output, str(int(angle2)), (x5 + 30, y5), 1, 1.5, (128, 0, 250), 2)
            #Dibujar la postura en la pantalla
            cv2.rectangle(output, (10,650), (500, 700), (255, 255, 0), -1)
            cv2.putText(output, str(col), (10, 700), 1, 4, (128, 0, 250), 2)

            #cv2.imshow("aux_image", aux_imge)
            cv2.imshow("Output", output)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()