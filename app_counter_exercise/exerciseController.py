import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import poseModule as pm


class ExerciseController:
    """
    Controlador que maneja toda la lógica de ejercicios.
    """
    
    def __init__(self):
        # Variables de video
        self.cap = None
        self.detector = None
        self.counter = None
        self.running = False
        
        # Configuración del ejercicio actual
        self.current_exercise = None
        self.landmarks = None
        
        # Datos para mostrar en la UI
        self.current_count = 0
        self.current_angle = 0
        self.current_frame = None
        
        # Configuraciones de ejercicios disponibles
        self.exercises_config = {
            # Ejercicios de bíceps
            "curl_left": {
                "name": "Curl de Bíceps - Brazo Izquierdo",
                "angle_up": 140,
                "angle_down": 60,
                "landmarks": (11, 13, 15),  # Hombro-Codo-Muñeca izquierda
                "side": "left"
            },
            "curl_right": {
                "name": "Curl de Bíceps - Brazo Derecho",
                "angle_up": 140,
                "angle_down": 60,
                "landmarks": (12, 14, 16),  # Hombro-Codo-Muñeca derecha
                "side": "right"
            },
            
            # Ejercicios de piernas
            "squat_left": {
                "name": "Sentadillas - Pierna Izquierda",
                "angle_up": 150,
                "angle_down": 80,
                "landmarks": (23, 25, 27),  # Cadera-Rodilla-Tobillo izquierda
                "side": "left"
            },
            "squat_right": {
                "name": "Sentadillas - Pierna Derecha",
                "angle_up": 150,
                "angle_down": 80,
                "landmarks": (24, 26, 28),  # Cadera-Rodilla-Tobillo derecha
                "side": "right"
            },
            
            # Ejercicios compuestos
            "pushup": {
                "name": "Flexiones",
                "angle_up": 150,
                "angle_down": 90,
                "landmarks": (11, 13, 15),  # Hombro-Codo-Muñeca
                "side": "both"
            },
            
            # Futuros ejercicios - DESPLANTES (lunges)
            "lunge_left": {
                "name": "Desplantes - Pierna Izquierda",
                "angle_up": 170,
                "angle_down": 90,
                "landmarks": (23, 25, 27),  # Cadera-Rodilla-Tobillo izquierda
                "side": "left"
            },
            "lunge_right": {
                "name": "Desplantes - Pierna Derecha",
                "angle_up": 170,
                "angle_down": 90,
                "landmarks": (24, 26, 28),  # Cadera-Rodilla-Tobillo derecha
                "side": "right"
            },
            
            # Más ejercicios para agregar fácilmente
            "shoulder_press_left": {
                "name": "Press de Hombro - Brazo Izquierdo",
                "angle_up": 170,
                "angle_down": 90,
                "landmarks": (11, 13, 15),
                "side": "left"
            },
            "shoulder_press_right": {
                "name": "Press de Hombro - Brazo Derecho",
                "angle_up": 170,
                "angle_down": 90,
                "landmarks": (12, 14, 16),
                "side": "right"
            }
        }
    
    def initialize_camera(self):
        """Inicializar la cámara"""
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            return True
        return False
    
    def initialize_detector(self):
        """Inicializar el detector de pose"""
        if self.detector is None:
            self.detector = pm.poseDetector()
            return True
        return False
    
    def start_exercise(self, exercise_key):
        """
        Iniciar un ejercicio por su clave.
        exercise_key: clave del diccionario exercises_config
        """
        if exercise_key not in self.exercises_config:
            return f"Error: Ejercicio '{exercise_key}' no configurado"
        
        config = self.exercises_config[exercise_key]
        
        self.current_exercise = exercise_key
        self.counter = pm.ExerciseCounter(
            angle_up=config["angle_up"],
            angle_down=config["angle_down"]
        )
        self.landmarks = config["landmarks"]
        self.running = True
        
        return config["name"]
    
    # Métodos específicos para compatibilidad
    def start_curl(self, side="left"):
        """Configurar ejercicio de curl de bíceps"""
        exercise_key = f"curl_{side}"
        return self.start_exercise(exercise_key)
    
    def start_squat(self, side="right"):
        """Configurar ejercicio de sentadillas"""
        exercise_key = f"squat_{side}"
        return self.start_exercise(exercise_key)
    
    def start_pushup(self):
        """Configurar ejercicio de flexiones"""
        return self.start_exercise("pushup")
    
    def start_lunge(self, side="left"):
        """Configurar ejercicio de desplantes"""
        exercise_key = f"lunge_{side}"
        return self.start_exercise(exercise_key)
    
    def start_shoulder_press(self, side="left"):
        """Configurar ejercicio de press de hombro"""
        exercise_key = f"shoulder_press_{side}"
        return self.start_exercise(exercise_key)
    
    def add_custom_exercise(self, exercise_key, name, angle_up, angle_down, landmarks, side="both"):
        """
        Agregar un nuevo ejercicio dinámicamente
        """
        self.exercises_config[exercise_key] = {
            "name": name,
            "angle_up": angle_up,
            "angle_down": angle_down,
            "landmarks": landmarks,
            "side": side
        }
        return f"Ejercicio '{name}' agregado exitosamente"
    
    def get_available_exercises(self):
        """Obtener lista de ejercicios disponibles"""
        return list(self.exercises_config.keys())
    
    def get_exercise_info(self, exercise_key):
        """Obtener información de un ejercicio específico"""
        if exercise_key in self.exercises_config:
            return self.exercises_config[exercise_key]
        return None
    
    def process_frame(self):
        """
        Procesar un frame de video.
        Retorna: (frame_base64, count, angle, status_ok)
        """
        if not self.running or self.cap is None:
            return None, 0, 0, False
        
        ret, frame = self.cap.read()
        if not ret:
            return None, 0, 0, False
        
        # Procesar pose
        frame = self.detector.findPose(frame, draw=False)
        lmList = self.detector.findPosition(frame, draw=False)
        
        if self.landmarks and len(lmList) > max(self.landmarks):
            # Calcular ángulo
            angle = self.detector.findAngle(
                frame,
                self.landmarks[0],
                self.landmarks[1],
                self.landmarks[2],
                draw=False
            )
            
            # Dibujar visualización
            frame = self.detector.drawAngleTriangle(
                frame,
                self.landmarks[0],
                self.landmarks[1],
                self.landmarks[2]
            )
            
            # Actualizar contador
            self.counter.update(angle)
            
            # Guardar datos actuales
            self.current_count = self.counter.getCount()
            self.current_angle = int(angle)
        
        # Convertir frame a base64
        frame_base64 = self._frame_to_base64(frame)
        
        return frame_base64, self.current_count, self.current_angle, True
    
    def _frame_to_base64(self, frame):
        """Convertir frame de OpenCV a base64 para Flet"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)
        pil_img = pil_img.resize((800, 600))
        
        buffered = BytesIO()
        pil_img.save(buffered, format="JPEG", quality=85)
        return base64.b64encode(buffered.getvalue()).decode()

    def reset_counter(self):
        """Reiniciar contador"""
        if self.counter:
            self.counter.reset()
            self.current_count = 0
            return "Contador reiniciado"
        return "No hay ejercicio activo"
    
    def cleanup(self):
        """Liberar recursos"""
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        return "Recursos liberados"
    
    def get_placeholder_image(self):
        """Crear imagen placeholder"""
        img = np.ones((600, 800, 3), dtype=np.uint8) * 50
        
        text = "Selecciona un ejercicio para comenzar"
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, 1, 2)[0]
        text_x = (img.shape[1] - text_size[0]) // 2
        text_y = (img.shape[0] + text_size[1]) // 2
        
        cv2.putText(img, text, (text_x, text_y), font, 1, (255, 255, 255), 2)
        
        pil_img = Image.fromarray(img)
        buffered = BytesIO()
        pil_img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()


# ============================================
# Funciones para la interfaz
# ============================================

# Variable global para mantener el controlador
_controller = None

def get_controller():
    """Obtener o crear el controlador global"""
    global _controller
    if _controller is None:
        _controller = ExerciseController()
    return _controller


def boton_curl_presionado(side="left"):
    """Función que se llama cuando presionas el botón de curl"""
    controller = get_controller()
    controller.initialize_camera()
    controller.initialize_detector()
    return controller.start_curl(side)


def boton_curl_derecho_presionado():
    """Función específica para curl derecho"""
    controller = get_controller()
    controller.initialize_camera()
    controller.initialize_detector()
    return controller.start_curl("right")


def boton_squat_presionado(side="left"):
    """Función que se llama cuando presionas el botón de sentadillas"""
    controller = get_controller()
    controller.initialize_camera()
    controller.initialize_detector()
    return controller.start_squat(side)


def boton_squat_derecho_presionado():
    """Función específica para sentadilla pierna derecha"""
    controller = get_controller()
    controller.initialize_camera()
    controller.initialize_detector()
    return controller.start_squat("right")


def boton_pushup_presionado():
    """Función que se llama cuando presionas el botón de flexiones"""
    controller = get_controller()
    controller.initialize_camera()
    controller.initialize_detector()
    return controller.start_pushup()


def boton_lunge_presionado(side="left"):
    """Función que se llama cuando presionas el botón de desplantes"""
    controller = get_controller()
    controller.initialize_camera()
    controller.initialize_detector()
    return controller.start_lunge(side)


def boton_lunge_derecho_presionado():
    """Función específica para desplante pierna derecha"""
    controller = get_controller()
    controller.initialize_camera()
    controller.initialize_detector()
    return controller.start_lunge("right")


def boton_shoulder_press_presionado(side="left"):
    """Función que se llama cuando presionas el botón de press de hombro"""
    controller = get_controller()
    controller.initialize_camera()
    controller.initialize_detector()
    return controller.start_shoulder_press(side)


def boton_reset_presionado():
    """Función que se llama cuando presionas reset"""
    controller = get_controller()
    return controller.reset_counter()


def obtener_frame():
    """Obtener el frame actual procesado"""
    controller = get_controller()
    return controller.process_frame()


def obtener_placeholder():
    """Obtener imagen placeholder"""
    controller = get_controller()
    return controller.get_placeholder_image()


def agregar_ejercicio_personalizado(exercise_key, name, angle_up, angle_down, landmarks, side="both"):
    """Agregar un nuevo ejercicio personalizado"""
    controller = get_controller()
    return controller.add_custom_exercise(exercise_key, name, angle_up, angle_down, landmarks, side)


def obtener_ejercicios_disponibles():
    """Obtener lista de ejercicios disponibles"""
    controller = get_controller()
    return controller.get_available_exercises()