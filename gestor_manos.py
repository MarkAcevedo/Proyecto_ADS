import cv2
import numpy as np

class GestureDetector:
    def __init__(self):
        mp = obtenciondeimagenes()
        self.captura = cv2.VideoCapture(0)
        self.mp_manos = mp.solutions.hands
        self.manos = self.mp_manos.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_dibujo = mp.solutions.drawing_utils
        self.contador_fotogramas = 0  # Contador de fotogramas

    def obtener_gestos(self):
        ret, fotograma = self.captura.read()
        gestos_detectados = []
        if ret:
            # Procesar cada 30 fotogramas para optimizar el rendimiento
            if self.contador_fotogramas % 30 == 0:
                fotograma_rgb = self.bgr_a_rgb_manual_fila(fotograma)

                # Procesar las manos usando MediaPipe
                resultado = self.manos.process(fotograma_rgb)
                texto_gesto = "No se detecta ningun gesto"

                if resultado.multi_hand_landmarks:
                    for puntos_referencia_mano, informacion_mano in zip(resultado.multi_hand_landmarks, resultado.multi_handedness):
                        etiqueta_mano = informacion_mano.classification[0].label  # 'Left' o 'Right'
                        puntos_referencia = puntos_referencia_mano.landmark
                        gesto_detectado = None

                        # Detectar gestos
                        if self.palma_abierta(puntos_referencia):
                            gesto_detectado = 'palma_abierta'
                            gestos_detectados.append((gesto_detectado, etiqueta_mano))
                            texto_gesto = f"Palma abierta ({etiqueta_mano})"
                        elif self.dedo_apuntando_arriba(puntos_referencia):
                            gesto_detectado = 'dedo_apuntando_arriba'
                            gestos_detectados.append((gesto_detectado, etiqueta_mano))
                            texto_gesto = "Dedo apuntando arriba"
                        elif self.dedo_apuntando_abajo(puntos_referencia):
                            gesto_detectado = 'dedo_apuntando_abajo'
                            gestos_detectados.append((gesto_detectado, etiqueta_mano))
                            texto_gesto = "Dedo apuntando abajo"
                        elif self.dedo_apuntando_izquierda(puntos_referencia):
                            gesto_detectado = 'dedo_apuntando_izquierda'
                            gestos_detectados.append((gesto_detectado, etiqueta_mano))
                            texto_gesto = "Dedo apuntando izquierda"
                        elif self.dedo_apuntando_derecha(puntos_referencia):
                            gesto_detectado = 'dedo_apuntando_derecha'
                            gestos_detectados.append((gesto_detectado, etiqueta_mano))
                            texto_gesto = "Dedo apuntando derecha"

                        # Dibujar puntos de referencia
                        self.mp_dibujo.draw_landmarks(fotograma, puntos_referencia_mano, self.mp_manos.HAND_CONNECTIONS)

                # Mostrar el gesto detectado
                cv2.putText(fotograma, texto_gesto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Mostrar la imagen con los gestos detectados
            cv2.imshow('Deteccion de Manos', fotograma)

            # Incrementar el contador de fotogramas
            self.contador_fotogramas += 1

            # Modificación para cerrar con 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return "cerrar"

        return gestos_detectados

    def bgr_a_rgb_manual_fila(self, fotograma):
        # Conversión manual de BGR a RGB
        altura, ancho, canales = fotograma.shape
        fotograma_rgb = [[[0, 0, 0] for _ in range(ancho)] for _ in range(altura)]
        
        for i in range(altura):
            for j in range(ancho):
                b, g, r = fotograma[i, j]
                fotograma_rgb[i][j] = [r, g, b]
        fotograma_rgb = np.array(fotograma_rgb, dtype="uint8")
        return fotograma_rgb

    # Funciones de detección de gestos
    def palma_abierta(self, puntos_referencia):
        dedos = [8, 12, 16, 20]
        for punta_dedo in dedos:
            base_dedo = punta_dedo - 2
            if puntos_referencia[punta_dedo].y > puntos_referencia[base_dedo].y:
                return False
        return True

    def dedo_apuntando_arriba(self, puntos_referencia):
        # Verifica si el dedo índice está apuntando hacia arriba
        return (puntos_referencia[8].y < puntos_referencia[6].y and
                puntos_referencia[6].y < puntos_referencia[5].y and
                puntos_referencia[0].y > puntos_referencia[9].y)

    def dedo_apuntando_abajo(self, puntos_referencia):
        # Verifica si el dedo índice está apuntando hacia abajo
        return (puntos_referencia[8].y > puntos_referencia[6].y and
                puntos_referencia[6].y > puntos_referencia[5].y and
                puntos_referencia[0].y < puntos_referencia[9].y)

    def dedo_apuntando_izquierda(self, puntos_referencia):
        # Verifica si el dedo índice está apuntando hacia la izquierda
        return (puntos_referencia[8].x < puntos_referencia[6].x and
                puntos_referencia[6].x < puntos_referencia[5].x and
                puntos_referencia[0].x > puntos_referencia[9].x)

    def dedo_apuntando_derecha(self, puntos_referencia):
        # Verifica si el dedo índice está apuntando hacia la derecha
        return (puntos_referencia[8].x > puntos_referencia[6].x and
                puntos_referencia[6].x > puntos_referencia[5].x and
                puntos_referencia[0].x < puntos_referencia[9].x)

    def release(self):
        self.captura.release()
        cv2.destroyAllWindows()

def obtenciondeimagenes():
    import mediapipe as mp
    return mp

# Código de prueba (opcional)
if __name__ == "__main__":
    detector = GestureDetector()
    try:
        while True:
            gestos = detector.obtener_gestos()
            if gestos == "cerrar":
                break
            elif gestos:
                print(f"Gestos detectados: {gestos}")
            else:
                print("No se detecta ningun gesto")
    finally:
        detector.release()
