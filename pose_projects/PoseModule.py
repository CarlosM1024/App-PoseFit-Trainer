import cv2
import mediapipe as mp
import time
import math

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
        Calcula el ángulo entre tres puntos (landmarks)
        p1, p2, p3 son los IDs de los landmarks
        p2 es el punto central (vértice del ángulo)
        Devuelve el ángulo interior (entre 0 y 180 grados)
        """
        if self.results.pose_landmarks:
            # Obtener las coordenadas de los landmarks
            h, w, _ = img.shape
            landmarks = self.results.pose_landmarks.landmark
            
            x1, y1 = int(landmarks[p1].x * w), int(landmarks[p1].y * h)
            x2, y2 = int(landmarks[p2].x * w), int(landmarks[p2].y * h)
            x3, y3 = int(landmarks[p3].x * w), int(landmarks[p3].y * h)

            # Calcular el ángulo usando la ley del coseno
            # Este método da el ángulo interior sin importar la orientación
            # Calcular las distancias
            a = math.sqrt((x2 - x3)**2 + (y2 - y3)**2)  # Distancia p2-p3
            b = math.sqrt((x1 - x3)**2 + (y1 - y3)**2)  # Distancia p1-p3
            c = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)  # Distancia p1-p2
            
            # Ley del coseno: cos(angle) = (a² + c² - b²) / (2ac)
            try:
                angle = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c)))
            except:
                angle = 0


            # Dibujar los puntos y líneas si draw=True
            if draw:
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
                cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
                cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
                cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
                cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
                cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                           cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            
            return angle
        
        return 0


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara")
        return

    pTime = 0
    detector = poseDetector()

    while True:
        success, img = cap.read()
        if not success:
            print("❌ No se pudo leer frame")
            break

        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)

        if lmList:
            # Landmark 14 = codo derecho
            cx, cy = lmList[14][1], lmList[14][2]
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime) if pTime != 0 else 0
        pTime = cTime

        cv2.putText(
            img,
            f"FPS: {int(fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

        cv2.imshow("Pose Detection", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()