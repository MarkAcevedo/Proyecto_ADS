import cv2
import mediapipe as mp

class GestureDetector:
    def __init__(self):
        self.captura = cv2.VideoCapture(0)
        self.mp_manos = mp.solutions.hands
        self.manos = self.mp_manos.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_dibujo = mp.solutions.drawing_utils
        self.contador_fotogramas = 0  # Contador de fotogramas

    def detectar_movimientos(self):
        ret, fotograma = self.captura.read()
        gestos_detectados = []

        if ret:
            # Procesar cada 30 fotogramas para optimizar el rendimiento
            if self.contador_fotogramas % 30 == 0:
                fotograma_rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)

                # Procesamiento de manos
                resultado = self.manos.process(fotograma_rgb)
                texto_gesto = "No se detecta ningún gesto"

                if resultado.multi_hand_landmarks:
                    for puntos_referencia_mano in resultado.multi_hand_landmarks:
                        puntos_referencia = puntos_referencia_mano.landmark

                        # Detectar los movimientos o inclinaciones específicos
                        if self.movimiento_arriba(puntos_referencia):
                            gestos_detectados.append("Movimiento Arriba")
                            texto_gesto = "Movimiento Arriba"
                        elif self.movimiento_abajo(puntos_referencia):
                            gestos_detectados.append("Movimiento Abajo")
                            texto_gesto = "Movimiento Abajo"
                        elif self.movimiento_izquierda(puntos_referencia):
                            gestos_detectados.append("Movimiento Izquierda")
                            texto_gesto = "Movimiento Izquierda"
                        elif self.movimiento_derecha(puntos_referencia):
                            gestos_detectados.append("Movimiento Derecha")
                            texto_gesto = "Movimiento Derecha"
                        elif self.inclinacion_enfrente_arriba(puntos_referencia):
                            gestos_detectados.append("Inclinacion Enfrente Arriba")
                            texto_gesto = "Inclinacion Enfrente Arriba"
                        elif self.inclinacion_enfrente_abajo(puntos_referencia):
                            gestos_detectados.append("Inclinacion Enfrente Abajo")
                            texto_gesto = "Inclinacion Enfrente Abajo"

                        # Dibujar las conexiones de la palma
                        self.mp_dibujo.draw_landmarks(
                            fotograma, puntos_referencia_mano, self.mp_manos.HAND_CONNECTIONS
                        )

                # Mostrar texto del gesto en la ventana
                cv2.putText(fotograma, texto_gesto, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Mostrar la imagen con los gestos detectados
            cv2.imshow('Deteccion de Gestos de Palma', fotograma)

            # Incrementar el contador de fotogramas
            self.contador_fotogramas += 1

            # Modificación para cerrar con 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return "cerrar"

        return gestos_detectados

    # Funciones de detección de gestos
    def movimiento_arriba(self, puntos_referencia):
        return puntos_referencia[0].y > puntos_referencia[9].y and puntos_referencia[5].y > puntos_referencia[9].y

    def movimiento_abajo(self, puntos_referencia):
        return puntos_referencia[0].y < puntos_referencia[9].y and puntos_referencia[5].y < puntos_referencia[9].y

    def movimiento_izquierda(self, puntos_referencia):
        return puntos_referencia[0].x > puntos_referencia[5].x > puntos_referencia[9].x

    def movimiento_derecha(self, puntos_referencia):
        return puntos_referencia[0].x < puntos_referencia[5].x < puntos_referencia[9].x

    def inclinacion_enfrente_arriba(self, puntos_referencia):
        return puntos_referencia[0].y > puntos_referencia[5].y and puntos_referencia[9].y < puntos_referencia[13].y

    def inclinacion_enfrente_abajo(self, puntos_referencia):
        return puntos_referencia[0].y < puntos_referencia[5].y and puntos_referencia[9].y > puntos_referencia[13].y

    def cerrar_camara(self):
        self.captura.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = GestureDetector()
    try:
        while True:
            gestos = detector.detectar_movimientos()
            if gestos == "cerrar":
                break
            elif gestos:
                print(f"Gestos detectados: {gestos}")
    finally:
        detector.cerrar_camara()