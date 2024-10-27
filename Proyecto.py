import sys
import pygame


# Configuración de Pygame
pygame.init()
ANCHO, ALTO = 800, 800
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Damas Modernas")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (34, 34, 34)
ROJO = (220, 20, 60)
AZUL = (70, 130, 180)
VERDE = (34, 139, 34)
GRIS = (192, 192, 192)
AMARILLO = (255, 215, 0)
MORADO = (138, 43, 226)

# Dimensiones del tablero
TAM_CASILLA = ANCHO // 8

# Cargar la imagen de la corona
try:
    CROWN = pygame.transform.scale(pygame.image.load('corona.png'), (44, 25))
except FileNotFoundError:
    CROWN = None

# Inicializa el tablero de damas
def inicializar_tablero():
    tablero = [[0] * 8 for _ in range(8)]
    for fila in range(3):
        for col in range(fila % 2, 8, 2):
            tablero[fila][col] = 2
    for fila in range(5, 8):
        for col in range(fila % 2, 8, 2):
            tablero[fila][col] = 1
    imprimir_tablero(tablero)  # Imprimir el tablero inicial
    return tablero

# Función para imprimir el tablero
def imprimir_tablero(tablero):
    print("  0 1 2 3 4 5 6 7")
    for i, fila in enumerate(tablero):
        print(f"{i} {' '.join(map(str, fila))}")

# Dibuja el tablero y las piezas
def dibujar_tablero(ventana, tablero, movimientos_validos, mejor_movimiento=None):
    ventana.fill(NEGRO)
    for fila in range(8):
        for col in range(fila % 2, 8, 2):
            pygame.draw.rect(ventana, GRIS, (col * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))
    
    for fila in range(8):
        for col in range(8):
            if tablero[fila][col] == 1:
                color = AMARILLO if mejor_movimiento and (fila, col) in mejor_movimiento else ROJO
                pygame.draw.circle(ventana, color, (col * TAM_CASILLA + TAM_CASILLA // 2, fila * TAM_CASILLA + TAM_CASILLA // 2), TAM_CASILLA // 2 - 10)
            elif tablero[fila][col] == 2:
                color = AMARILLO if mejor_movimiento and (fila, col) in mejor_movimiento else AZUL
                pygame.draw.circle(ventana, color, (col * TAM_CASILLA + TAM_CASILLA // 2, fila * TAM_CASILLA + TAM_CASILLA // 2), TAM_CASILLA // 2 - 10)
            elif tablero[fila][col] == 3:
                color = AMARILLO if mejor_movimiento and (fila, col) in mejor_movimiento else ROJO
                pygame.draw.circle(ventana, color, (col * TAM_CASILLA + TAM_CASILLA // 2, fila * TAM_CASILLA + TAM_CASILLA // 2), TAM_CASILLA // 2 - 10)
                if CROWN:
                    ventana.blit(CROWN, (col * TAM_CASILLA + TAM_CASILLA // 2 - CROWN.get_width() // 2, fila * TAM_CASILLA + TAM_CASILLA // 2 - CROWN.get_height() // 2))
            elif tablero[fila][col] == 4:
                color = AMARILLO if mejor_movimiento and (fila, col) in mejor_movimiento else AZUL
                pygame.draw.circle(ventana, color, (col * TAM_CASILLA + TAM_CASILLA // 2, fila * TAM_CASILLA + TAM_CASILLA // 2), TAM_CASILLA // 2 - 10)
                if CROWN:
                    ventana.blit(CROWN, (col * TAM_CASILLA + TAM_CASILLA // 2 - CROWN.get_width() // 2, fila * TAM_CASILLA + TAM_CASILLA // 2 - CROWN.get_height() // 2))
    
    for mov in movimientos_validos:
        fila, col = mov
        pygame.draw.circle(ventana, VERDE, (col * TAM_CASILLA + TAM_CASILLA // 2, fila * TAM_CASILLA + TAM_CASILLA // 2), TAM_CASILLA // 2 - 10)
    
    pygame.display.update()

def dibujar_botones(ventana):
    fuente = pygame.font.SysFont(None, 36)
    botones = {
        'Avanzar': (ANCHO - 150, ALTO - 50, 100, 30),
        'Retroceder': (70, ALTO - 50, 150, 30),
        'Menu': (ANCHO // 2 - 50, ALTO - 50, 100, 30),
        'Salir': (ANCHO // 2 - 50, ALTO - 100, 100, 30)
    }
    for texto, (x, y, w, h) in botones.items():
        pygame.draw.rect(ventana, BLANCO, (x, y, w, h), border_radius=5)
        texto_render = fuente.render(texto, True, NEGRO)
        ventana.blit(texto_render, (x + (w - texto_render.get_width()) // 2, y + (h - texto_render.get_height()) // 2))
    return botones

def mostrar_retroalimentacion(ventana, jugadas_erroneas):
    idx = 0
    ventana = pygame.display.set_mode((1000, 900))
    while True:
        if idx < 0:
            idx = 0
        elif idx >= len(jugadas_erroneas):
            idx = len(jugadas_erroneas) - 1

        tablero_antes, tablero_despues = jugadas_erroneas[idx]
        ventana.fill(GRIS)
        fuente = pygame.font.SysFont(None, 50)
        mensaje = f"Jugada {idx + 1}:"
        texto = fuente.render(mensaje, True, NEGRO)
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 20))
        
        for idx_tab, (tablero, titulo) in enumerate([(tablero_antes, "Antes"), (tablero_despues, "Mejor Movimiento")]):
            offset_x = idx_tab * (ANCHO // 2)
            for fila in range(8):
                for col in range(fila % 2, 8, 2):
                    pygame.draw.rect(ventana, BLANCO, (offset_x + col * TAM_CASILLA, fila * TAM_CASILLA + 100, TAM_CASILLA, TAM_CASILLA))
            
            for fila in range(8):
                for col in range(8):
                    if tablero[fila][col] == 1:
                        color = AMARILLO if idx_tab == 1 and (fila, col) in tablero_despues else ROJO
                        pygame.draw.circle(ventana, color, (offset_x + col * TAM_CASILLA + TAM_CASILLA // 2, fila * TAM_CASILLA + TAM_CASILLA // 2 + 100), TAM_CASILLA // 2 - 10)
                    elif tablero[fila][col] == 2:
                        color = AMARILLO if idx_tab == 1 and (fila, col) in tablero_despues else AZUL
                        pygame.draw.circle(ventana, color, (offset_x + col * TAM_CASILLA + TAM_CASILLA // 2, fila * TAM_CASILLA + TAM_CASILLA // 2 + 100), TAM_CASILLA // 2 - 10)
                    elif tablero[fila][col] == 3:
                        color = AMARILLO if idx_tab == 1 and (fila, col) in tablero_despues else ROJO
                        pygame.draw.circle(ventana, color, (offset_x + col * TAM_CASILLA + TAM_CASILLA // 2, fila * TAM_CASILLA + TAM_CASILLA // 2 + 100), TAM_CASILLA // 2 - 10)
                        if CROWN:
                            ventana.blit(CROWN, (offset_x + col * TAM_CASILLA + TAM_CASILLA // 2 - CROWN.get_width() // 2, fila * TAM_CASILLA + TAM_CASILLA // 2 + 100 - CROWN.get_height() // 2))
                    elif tablero[fila][col] == 4:
                        color = AMARILLO if idx_tab == 1 and (fila, col) in tablero_despues else AZUL
                        pygame.draw.circle(ventana, color, (offset_x + col * TAM_CASILLA + TAM_CASILLA // 2, fila * TAM_CASILLA + TAM_CASILLA // 2 + 100), TAM_CASILLA // 2 - 10)
                        if CROWN:
                            ventana.blit(CROWN, (offset_x + col * TAM_CASILLA + TAM_CASILLA // 2 - CROWN.get_width() // 2, fila * TAM_CASILLA + TAM_CASILLA // 2 + 100 - CROWN.get_height() // 2))
            
            if idx_tab == 1:  # Mostrar movimiento óptimo
                for f in range(8):
                    for c in range(8):
                        if tablero_antes[f][c] != tablero_despues[f][c]:
                            pygame.draw.circle(ventana, MORADO, (offset_x + c * TAM_CASILLA + TAM_CASILLA // 2, f * TAM_CASILLA + TAM_CASILLA // 2 + 100), TAM_CASILLA // 2 - 10)

            titulo_texto = fuente.render(titulo, True, NEGRO)
            ventana.blit(titulo_texto, (offset_x + ANCHO // 4 - titulo_texto.get_width() // 2, ALTO - 150))
        
        botones = dibujar_botones(ventana)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if botones['Avanzar'][0] <= x <= botones['Avanzar'][0] + botones['Avanzar'][2] and botones['Avanzar'][1] <= y <= botones['Avanzar'][1] + botones['Avanzar'][3]:
                    idx += 1
                elif botones['Retroceder'][0] <= x <= botones['Retroceder'][0] + botones['Retroceder'][2] and botones['Retroceder'][1] <= y <= botones['Retroceder'][1] + botones['Retroceder'][3]:
                    idx -= 1
                elif botones['Menu'][0] <= x <= botones['Menu'][0] + botones['Menu'][2] and botones['Menu'][1] <= y <= botones['Menu'][1] + botones['Menu'][3]:
                    jugar_damas()  # Iniciar un nuevo juego
                    return
                elif botones['Salir'][0] <= x <= botones['Salir'][0] + botones['Salir'][2] and botones['Salir'][1] <= y <= botones['Salir'][1] + botones['Salir'][3]:
                    pygame.quit()
                    sys.exit()

# Genera movimientos posibles para una pieza
def generar_movimientos(tablero, fila, col):
    movimientos = []
    pieza = tablero[fila][col]
    if pieza == 1:  # Movimiento para rojas
        direcciones = [(-1, -1), (-1, 1)]
    elif pieza == 2:  # Movimiento para azules
        direcciones = [(1, -1), (1, 1)]
    elif pieza in [3, 4]:  # Dama
        direcciones = [(1, -1), (1, 1), (-1, -1), (-1, 1)]
    
    for d in direcciones:
        nueva_fila, nueva_col = fila + d[0], col + d[1]
        if 0 <= nueva_fila < 8 and 0 <= nueva_col < 8 and tablero[nueva_fila][nueva_col] == 0:
            movimientos.append((nueva_fila, nueva_col))
    
    movimientos += generar_capturas(tablero, fila, col, pieza)
    print(f"Movimientos generados para la pieza en ({fila}, {col}): {movimientos}")  # Depuración
    return movimientos

def generar_capturas(tablero, fila, col, pieza):
    capturas = []
    if pieza == 1:  # Captura para rojas
        direcciones = [(-2, -2), (-2, 2)]
    elif pieza == 2:  # Captura para azules
        direcciones = [(2, -2), (2, 2)]
    elif pieza in [3, 4]:  # Dama
        direcciones = [(2, -2), (2, 2), (-2, -2), (-2, 2)]
    
    for d in direcciones:
        salto_fila, salto_col = fila + d[0], col + d[1]
        if 0 <= salto_fila < 8 and 0 <= salto_col < 8:
            intermedia_fila, intermedia_col = fila + d[0] // 2, col + d[1] // 2
            if tablero[salto_fila][salto_col] == 0 and tablero[intermedia_fila][intermedia_col] != 0 and tablero[intermedia_fila][intermedia_col] % 2 != pieza % 2:
                capturas.append((salto_fila, salto_col))
    
    return capturas

def mover(tablero, origen, destino):
    pieza = tablero[origen[0]][origen[1]]
    tablero[destino[0]][destino[1]] = pieza
    tablero[origen[0]][origen[1]] = 0
    
    # Verifica y realiza captura
    if abs(destino[0] - origen[0]) == 2:
        intermedia_fila = (origen[0] + destino[0]) // 2
        intermedia_col = (origen[1] + destino[1]) // 2
        tablero[intermedia_fila][intermedia_col] = 0
        return True  # Se realizó una captura
    
    return False  # No se realizó una captura

def validar_promociones(tablero):
    for col in range(8):
        if tablero[0][col] == 1:
            tablero[0][col] = 3  # Promocionar pieza roja a dama
            print(f"Pieza en (0, {col}) promovida a Dama Roja")
        if tablero[7][col] == 2:
            tablero[7][col] = 4  # Promocionar pieza azul a dama
            print(f"Pieza en (7, {col}) promovida a Dama Azul")

def es_estado_terminal(tablero):
    rojos, azules = 0, 0
    for fila in tablero:
        for pieza in fila:
            if pieza in [1, 3]:
                rojos += 1
            elif pieza in [2, 4]:
                azules += 1
    return rojos == 0 or azules == 0 or not hay_movimientos(tablero, 1) or not hay_movimientos(tablero, 2)

def ver_comer(tablero, fila, col, pieza):
    if pieza == 1:  # Ver captura para rojas
        direcciones = [(-2, -2), (-2, 2)]
    elif pieza == 2:  # Ver captura para azules
        direcciones = [(2, -2), (2, 2)]
    elif pieza in [3, 4]:  # Dama
        direcciones = [(2, -2), (2, 2), (-2, -2), (-2, 2)]
    else:
        return False  # Si la pieza no es válida, no puede capturar
    
    for d in direcciones:
        salto_fila, salto_col = fila + d[0], col + d[1]
        if 0 <= salto_fila < 8 and 0 <= salto_col < 8:
            intermedia_fila, intermedia_col = fila + d[0] // 2, col + d[1] // 2
            if tablero[salto_fila][salto_col] == 0 and tablero[intermedia_fila][intermedia_col] != 0 and tablero[intermedia_fila][intermedia_col] % 2 != pieza % 2:
                return True
    return False

def comer_aut(tablero, fila, col, pieza):
    while ver_comer(tablero, fila, col, pieza):
        capturas = generar_capturas(tablero, fila, col, pieza)
        if capturas:
            destino = capturas[0]
            mover(tablero, (fila, col), destino)
            fila, col = destino
        else:
            break

# Función para evaluar el estado del tablero para el minimax
def evaluar(tablero):
    evaluacion = 0
    for fila in tablero:
        for pieza in fila:
            if pieza == 1:
                evaluacion -= 1
            elif pieza == 2:
                evaluacion += 1
            elif pieza == 3:
                evaluacion -= 2
            elif pieza == 4:
                evaluacion += 2
    return evaluacion

# Implementación del algoritmo Minimax con poda Alpha-Beta
def minimax(tablero, profundidad, alpha, beta, maximizando):
    if profundidad == 0 or es_estado_terminal(tablero):
        return evaluar(tablero), tablero

    if maximizando:
        maxEval = float('-inf')
        mejor_tablero = None
        for movimiento in obtener_todos_movimientos(tablero, 2):  # Movimientos de la computadora (azules)
            evaluacion, _ = minimax(movimiento, profundidad - 1, alpha, beta, False)
            if evaluacion > maxEval:
                maxEval = evaluacion
                mejor_tablero = movimiento
            alpha = max(alpha, evaluacion)
            if beta <= alpha:
                break
        return maxEval, mejor_tablero
    else:
        minEval = float('inf')
        mejor_tablero = None
        for movimiento in obtener_todos_movimientos(tablero, 1):  # Movimientos del jugador (rojas)
            evaluacion, _ = minimax(movimiento, profundidad - 1, alpha, beta, True)
            if evaluacion < minEval:
                minEval = evaluacion
                mejor_tablero = movimiento
            beta = min(beta, evaluacion)
            if beta <= alpha:
                break
        return minEval, mejor_tablero

# Obtener todos los movimientos posibles para un jugador
def obtener_todos_movimientos(tablero, jugador):
    tableros = []
    for fila in range(8):
        for col in range(8):
            if tablero[fila][col] != 0 and tablero[fila][col] % 2 == jugador % 2:
                movimientos = generar_movimientos(tablero, fila, col)
                for mov in movimientos:
                    copia_tablero = [fila[:] for fila in tablero]
                    mover(copia_tablero, (fila, col), mov)
                    tableros.append(copia_tablero)
    return tableros

def mostrar_menu():
    VENTANA.fill(GRIS)
    fuente = pygame.font.SysFont(None, 75)
    texto = fuente.render("Damas", True, NEGRO)
    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 4))

    fuente = pygame.font.SysFont(None, 50)
    facil = fuente.render("Fácil", True, NEGRO)
    VENTANA.blit(facil, (ANCHO // 2 - facil.get_width() // 2, ALTO // 2))

    medio = fuente.render("Medio", True, NEGRO)
    VENTANA.blit(medio, (ANCHO // 2 - medio.get_width() // 2, ALTO // 2 + 50))

    dificil = fuente.render("Difícil", True, NEGRO)
    VENTANA.blit(dificil, (ANCHO // 2 - dificil.get_width() // 2, ALTO // 2 + 100))

    pygame.display.update()

def obtener_dificultad():
    mostrar_menu()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if ANCHO // 2 - 50 <= x <= ANCHO // 2 + 50:
                    if ALTO // 2 <= y <= ALTO // 2 + 50:
                        return 1  # Fácil
                    elif ALTO // 2 + 50 <= y <= ALTO // 2 + 100:
                        return 3  # Medio
                    elif ALTO // 2 + 100 <= y <= ALTO // 2 + 150:
                        return 6  # Difícil

def jugar_damas():
    while True:
        dificultad = obtener_dificultad()
        tablero = inicializar_tablero()
        seleccionado = None
        movimientos_validos = []
        turno = 1  # Turno de las piezas rojas primero
        jugadas_erroneas = []  # Guardar las jugadas no óptimas
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.MOUSEBUTTONDOWN and turno == 1:
                    x, y = pygame.mouse.get_pos()
                    fila, col = y // TAM_CASILLA, x // TAM_CASILLA
                    if seleccionado:
                        if (fila, col) in movimientos_validos:
                            _, mejor_movimiento = minimax(tablero, dificultad, float('-inf'), float('inf'), False)
                            if mejor_movimiento and mejor_movimiento != tablero:
                                jugadas_erroneas.append((tablero, mejor_movimiento))  # Guardar jugada no óptima
                            captura = mover(tablero, seleccionado, (fila, col))
                            validar_promociones(tablero)  # Validar promociones después de cada movimiento
                            if captura:
                                comer_aut(tablero, fila, col, tablero[fila][col])
                                if not ver_comer(tablero, fila, col, tablero[fila][col]):
                                    turno = 3 - turno
                            else:
                                turno = 3 - turno
                            seleccionado = None
                            movimientos_validos = []
                        else:
                            seleccionado = None
                            movimientos_validos = []
                    elif tablero[fila][col] != 0 and tablero[fila][col] % 2 == turno % 2:
                        seleccionado = (fila, col)
                        movimientos_validos = generar_movimientos(tablero, fila, col)
            
            dibujar_tablero(VENTANA, tablero, movimientos_validos)
            
            if turno == 2:  # Turno de la computadora
                _, mejor_movimiento = minimax(tablero, dificultad, float('-inf'), float('inf'), True)
                if mejor_movimiento is not None:
                    tablero = mejor_movimiento
                    validar_promociones(tablero)
                    turno = 1  # Cambia al turno del jugador
                imprimir_tablero(tablero)  # Imprimir el tablero después del movimiento de la computadora
            
            if es_estado_terminal(tablero):
                corriendo = False
                ganador = 'Rojo' if turno == 2 else 'Azul' if turno == 1 else 'Empate'
                print(f"Juego terminado. Ganador: {ganador}")
                
                # Mostrar retroalimentación al jugador
                if jugadas_erroneas:
                    mostrar_retroalimentacion(VENTANA, jugadas_erroneas)

        pygame.quit()
        sys.exit()

def hay_movimientos(tablero, jugador):
    for fila in range(8):
        for col in range(8):
            if tablero[fila][col] != 0 and tablero[fila][col] % 2 == jugador % 2:
                if generar_movimientos(tablero, fila, col):
                    return True
    return False

jugar_damas()
