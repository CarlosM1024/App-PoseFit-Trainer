import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(static_image_mode=True) as pose:

    image = cv2.imread('im_0005.jpg')
    height, width, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = pose.process(image_rgb)
    print("Pose landmarks: ", results.pose_landmarks)

    '''
        if results.pose_landmarks is not None:
            mp_drawing.draw_landmarks(image, results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(128, 0, 250), thickness=2, circle_radius=3),
            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2))
    '''

    if results.pose_landmarks is not None:
        #Por nombre:
        #Punto del hombro de brazo derecho
        print(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width))
        x1 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width)
        y1 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height)

        # Punto del codo de brazo derecho
        x2 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x * width)
        y2 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y * height)

        # Punto de la muñeca de brazo derecho
        x3 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * width)
        y3 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * height)

        #Por indices:
        # Punto del hombro de brazo izquierdo
        x4 = int(results.pose_landmarks.landmark[11].x * width)
        y4 = int(results.pose_landmarks.landmark[11].y * height)

        # Punto del codo de brazo izquierdo
        x5 = int(results.pose_landmarks.landmark[13].x * width)
        y5 = int(results.pose_landmarks.landmark[13].y * height)

        # Punto de la muñeca de brazo izquierdo
        x6 = int(results.pose_landmarks.landmark[15].x * width)
        y6 = int(results.pose_landmarks.landmark[15].y * height)

        #Dibujar lineas y circulos del lado derecho
        cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255))
        cv2.line(image, (x2, y2), (x3, y3), (255, 255, 255))
        cv2.circle(image, (x1, y1), 6, (128, 0, 255), -1)
        cv2.circle(image, (x2, y2), 6, (128, 0, 255), -1)
        cv2.circle(image, (x3, y3), 6, (128, 0, 255), -1)

        #Dibujar lineas y circulos del lado izquierdo
        cv2.line(image, (x4, y4), (x5, y5), (255, 255, 255))
        cv2.line(image, (x5, y5), (x6, y6), (255, 255, 255))
        cv2.circle(image, (x4, y4), 6, (128, 0, 255), -1)
        cv2.circle(image, (x5, y5), 6, (128, 0, 255), -1)
        cv2.circle(image, (x6, y6), 6, (128, 0, 255), -1)

    cv2.imshow('Image', image)
    cv2.waitKey()
cv2.destroyAllWindows()