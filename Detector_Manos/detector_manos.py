import cv2
import mediapipe as mp

# Inicializar Mediapipe para la detección de manos
mp_manos = mp.solutions.hands
mp_dibujo = mp.solutions.drawing_utils
manos = mp_manos.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Inicializar la captura de video
captura = cv2.VideoCapture(0)

# Función para procesar las manos y devolver los resultados
def procesar_manos(imagen_rgb):
    resultado = manos.process(imagen_rgb)
    if resultado.multi_hand_landmarks:
        return zip(resultado.multi_hand_landmarks, resultado.multi_handedness)
    return None

# Función para dibujar los resultados de las manos
def dibujar_resultados(imagen, resultado):
    if resultado:
        for puntos_referencia_mano, informacion_mano in resultado:
            mp_dibujo.draw_landmarks(imagen, puntos_referencia_mano, mp_manos.HAND_CONNECTIONS)
            procesar_gestos(imagen, puntos_referencia_mano, informacion_mano)

# Función personalizada para procesar los gestos
def procesar_gestos(imagen, puntos_referencia_mano, informacion_mano):
    etiqueta_mano = informacion_mano.classification[0].label
    if palma_abierta(puntos_referencia_mano.landmark):
        if etiqueta_mano == 'Right':
            cv2.putText(imagen, "Regresar a la derecha", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        elif etiqueta_mano == 'Left':
            cv2.putText(imagen, "Regresar a la izquierda", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        if dedo_indice_levantado(puntos_referencia_mano.landmark):
            if etiqueta_mano == 'Right':
                cv2.putText(imagen, "Moverse a la derecha", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            elif etiqueta_mano == 'Left':
                cv2.putText(imagen, "Moverse a la izquierda", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Verificar si el dedo índice está levantado
def dedo_indice_levantado(puntos_referencia):
    return puntos_referencia[8].y < puntos_referencia[5].y

# Verificar si la palma está abierta
def palma_abierta(puntos_referencia):
    dedos = [8, 12, 16, 20]
    for punta_dedo in dedos:
        if puntos_referencia[punta_dedo].y > puntos_referencia[punta_dedo - 3].y:
            return False
    return True

# Loop principal para capturar el video y procesar las manos
while True:
    ret, fotograma = captura.read()
    if not ret:
        break

    # Convertir el frame a RGB utilizando OpenCV
    fotograma_rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)

    # Procesar las manos y dibujar resultados
    resultado = procesar_manos(fotograma_rgb)
    dibujar_resultados(fotograma, resultado)

    # Mostrar el video con las manos detectadas y el texto
    cv2.imshow('Deteccion de Manos', fotograma)

    # Presionar 'q' para salir del loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
captura.release()
cv2.destroyAllWindows()
