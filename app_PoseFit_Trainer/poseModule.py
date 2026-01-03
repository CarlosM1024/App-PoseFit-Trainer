import cv2
import mediapipe as mp
import math
import numpy as np

class poseDetector():

    def __init__(self, mode=False, model_complexity=1, 
                 smooth=True, detectionCon=0.5, trackCon=0.5):
    
        self.mode = mode
        self.model_complexity = model_complexity
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            model_complexity=self.model_complexity,
            smooth_landmarks=self.smooth,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.results = None

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(
                img,
                self.results.pose_landmarks,
                self.mpPose.POSE_CONNECTIONS
            )
        return img

    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            h, w, _ = img.shape
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        """
        Calcula el ángulo entre tres puntos usando ley del coseno
        p2 es el vértice del ángulo
        Retorna ángulo entre 0-180 grados
        """
        if self.results.pose_landmarks:
            h, w, _ = img.shape
            landmarks = self.results.pose_landmarks.landmark
            
            x1, y1 = int(landmarks[p1].x * w), int(landmarks[p1].y * h)
            x2, y2 = int(landmarks[p2].x * w), int(landmarks[p2].y * h)
            x3, y3 = int(landmarks[p3].x * w), int(landmarks[p3].y * h)

            # Calcular distancias
            p1_arr = np.array([x1, y1])
            p2_arr = np.array([x2, y2])
            p3_arr = np.array([x3, y3])
            
            l1 = np.linalg.norm(p2_arr - p3_arr)
            l2 = np.linalg.norm(p1_arr - p3_arr)
            l3 = np.linalg.norm(p1_arr - p2_arr)
            
            # Ley del coseno
            try:
                angle = math.degrees(math.acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))
            except:
                angle = 0

            if draw:
                # Dibujar líneas
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
                cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
                
                # Dibujar círculos
                cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
                cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
                cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
                
                # Mostrar ángulo
                cv2.putText(img, str(int(angle)), (x2 + 30, y2 + 30),
                           cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            
            return angle
        return 0

    def drawAngleTriangle(self, img, p1, p2, p3, color=(128, 0, 250), alpha=0.8):
        """
        Dibuja un triángulo relleno entre tres puntos (mejor visualización)
        """
        if self.results.pose_landmarks:
            h, w, _ = img.shape
            landmarks = self.results.pose_landmarks.landmark
            
            x1, y1 = int(landmarks[p1].x * w), int(landmarks[p1].y * h)
            x2, y2 = int(landmarks[p2].x * w), int(landmarks[p2].y * h)
            x3, y3 = int(landmarks[p3].x * w), int(landmarks[p3].y * h)

            # Crear imagen auxiliar para transparencia
            aux_img = np.zeros(img.shape, np.uint8)
            
            # Dibujar líneas gruesas
            cv2.line(aux_img, (x1, y1), (x2, y2), (255, 255, 0), 20)
            cv2.line(aux_img, (x2, y2), (x3, y3), (255, 255, 0), 20)
            cv2.line(aux_img, (x3, y3), (x1, y1), (255, 255, 0), 5)
            
            # Rellenar triángulo
            contours = np.array([[x1, y1], [x2, y2], [x3, y3]])
            cv2.fillPoly(aux_img, pts=[contours], color=color)
            
            # Mezclar con imagen original
            output = cv2.addWeighted(img, 1, aux_img, alpha, 0)
            
            # Dibujar círculos en los puntos
            cv2.circle(output, (x1, y1), 6, (0, 255, 255), 4)
            cv2.circle(output, (x2, y2), 6, color, 4)
            cv2.circle(output, (x3, y3), 6, (255, 191, 0), 4)
            
            return output
        return img


class ExerciseCounter():
    """
    Clase para contar repeticiones de ejercicios
    Usa lógica de estados para mayor robustez
    """
    def __init__(self, angle_up, angle_down):
        self.angle_up = angle_up      # Ángulo para posición arriba/extendido
        self.angle_down = angle_down  # Ángulo para posición abajo/flexionado
        self.count = 0
        self.up = False
        self.down = False
    
    def update(self, angle):
        """
        Actualiza el contador basándose en el ángulo actual
        Retorna True si se completó una repetición
        """
        completed = False
        
        # Detectar posición extendida
        if angle >= self.angle_up:
            self.up = True
        
        # Detectar posición flexionada
        if self.up and not self.down and angle <= self.angle_down:
            self.down = True
        
        # Detectar repetición completa
        if self.up and self.down and angle >= self.angle_up:
            self.count += 1
            self.up = False
            self.down = False
            completed = True
        
        return completed
    
    def getCount(self):
        return self.count
    
    def reset(self):
        self.count = 0
        self.up = False
        self.down = False


def main():
    cap = cv2.VideoCapture(0)
    detector = poseDetector()
    
    # Contador de sentadillas: 150° arriba, 80° abajo
    counter = ExerciseCounter(angle_up=150, angle_down=80)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = detector.findPose(frame, draw=False)
        lmList = detector.findPosition(frame, draw=False)
        
        if len(lmList) > 28:
            # Calcular ángulo de la rodilla derecha (cadera-rodilla-tobillo)
            angle = detector.findAngle(frame, 24, 26, 28, draw=False)
            
            # Dibujar triángulo visual
            frame = detector.drawAngleTriangle(frame, 24, 26, 28)
            
            # Actualizar contador
            counter.update(angle)
            
            # Mostrar ángulo
            #cv2.putText(frame, f'Angle: {int(angle)}', (50, 100),
            #          cv2.FONT_HERSHEY_PLAIN, 3, (128, 0, 250), 3)
            
            # Mostrar contador
            #cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 0), -1)
            #cv2.putText(frame, str(counter.getCount()), (20, 70),
            #           cv2.FONT_HERSHEY_PLAIN, 5, (128, 0, 250), 5)
        
        cv2.imshow("Exercise Counter", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()