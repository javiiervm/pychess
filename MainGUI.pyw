# Importación de módulos necesarios
import sys
from copy import deepcopy  # Para crear copias profundas de objetos
import os
import tkinter as tk
from tkinter import messagebox
import random  # Añadido para la generación aleatoria de posiciones

modules_path = f"./Modules"
sys.path.append(modules_path)
from Modules import ChessGame as game, Position as pos, Player as plr, Square as sq, Board as brd

# Definición de colores para la interfaz
WHITE_BG = "#ffffff"  # Color blanco para casillas blancas
BLACK_BG = "#000000"  # Color negro para casillas negras
MOVE_BG = "#ffdd44"   # Color amarillo para movimientos posibles
CHECK_BG = "#990000"  # Color rojo para situaciones de jaque

# Variables globales
global squareMatrix, chessGame, selected_square, current_turn
selected_square = None      # Almacena la casilla seleccionada actualmente
current_turn = True         # True para turno blanco, False para turno negro

# Variable para el modo de juego
game_mode = "Normal"  # Por defecto, modo normal

class indexedButton:
    """Clase para manejar los botones del tablero con sus posiciones indexadas"""
    instances = []  # Lista para almacenar todas las instancias de botones
    
    def __init__(self, bt_obj: tk.Button, isWhite: bool):
        """Constructor que inicializa un botón indexado
        Args:
            bt_obj: Objeto botón de tkinter
            isWhite: Booleano que indica si es una casilla blanca
        """
        indexedButton.instances.append(self)
        self.bt_obj = bt_obj
        # Calcula la posición del botón en el tablero (fila y columna)
        self.idx = pos.Position(indexedButton.instances.index(self)//8, indexedButton.instances.index(self)%8)
        self.isWhite = isWhite
    
    def cmd(self):
        """Función que maneja los eventos de clic en las casillas del tablero"""
        global selected_square, current_turn
        # Restaura los colores originales del tablero
        for btn in indexedButton.instances:
            btn.bt_obj.configure(bg=WHITE_BG if btn.isWhite else BLACK_BG)
        
        currentSquare = chessGame.getBoard().findSquare(self.idx)
        
        # Primer clic: seleccionar una pieza para mover
        if selected_square is None:
            if not currentSquare.hasPiece():
                return
            # Verifica que la pieza corresponda al turno actual
            if currentSquare.getPiece().isWhite() != current_turn:
                return
            
            selected_square = self
            ischeck, danger, _ = chessGame.checkForCheck(current_turn)
            
            # Si hay jaque, solo permitir movimientos que lo eviten
            if ischeck:
                available = getDestinyList(currentSquare, danger)
                
                # Filtrar movimientos que no evitan el jaque
                for square in available[:]:
                    testGame = game.ChessGame(deepcopy(chessGame.getBoard()), "1", "2")
                    testGame.board.movePiece(
                        testGame.getBoard().findSquare(currentSquare.getPosition()), 
                        testGame.getBoard().findSquare(square.getPosition())
                    )
                    newCheck, _, _ = testGame.checkForCheck(current_turn)
                    if newCheck:
                        available.remove(square)
                
                if not available:
                    selected_square = None
                    return
            else:
                available = getDestinyList(currentSquare, [])
                
                # Filtrar movimientos que resultarían en jaque
                for square in available[:]:
                    testGame = game.ChessGame(deepcopy(chessGame.getBoard()), "1", "2")
                    testGame.board.movePiece(
                        testGame.getBoard().findSquare(currentSquare.getPosition()), 
                        testGame.getBoard().findSquare(square.getPosition())
                    )
                    newCheck, _, _ = testGame.checkForCheck(current_turn)
                    if newCheck:
                        available.remove(square)
            
            # Muestra los movimientos posibles
            moves = [self.idx] + [sq.getPosition() for sq in available]
            movePainterUI(moves)
        else:
            # Segundo clic: intentar mover la pieza
            originSquare = chessGame.getBoard().findSquare(selected_square.idx)
            ischeck, danger, _ = chessGame.checkForCheck(current_turn)
            available = getDestinyList(originSquare, danger if ischeck else [])
            
            # Filtrar movimientos que no evitan el jaque si hay jaque
            if ischeck:
                for square in available[:]:
                    testGame = game.ChessGame(deepcopy(chessGame.getBoard()), "1", "2")
                    testGame.board.movePiece(
                        testGame.getBoard().findSquare(originSquare.getPosition()), 
                        testGame.getBoard().findSquare(square.getPosition())
                    )
                    newCheck, _, _ = testGame.checkForCheck(current_turn)
                    if newCheck:
                        available.remove(square)
            
            valid = any(self.idx.getX() == a.getPosition().getX() and self.idx.getY() == a.getPosition().getY() for a in available)
            
            if valid:
                # Manejo del enroque
                if (originSquare.getPiece().getName() == "King" and 
                    currentSquare.hasPiece() and 
                    currentSquare.getPiece().getName() == "Rook" and 
                    originSquare.getPiece().isWhite() == currentSquare.getPiece().isWhite()):
                    
                    rookMoving = deepcopy(currentSquare)
                    # Enroque largo
                    if rookMoving.getPosition().getY() == 0:
                        chessGame.board.movePiece(originSquare, sq.Square(pos.Position(currentSquare.getPosition().getX(), currentSquare.getPosition().getY() + 1), None))
                        chessGame.board.movePiece(rookMoving, sq.Square(pos.Position(currentSquare.getPosition().getX(), currentSquare.getPosition().getY() + 2), None))
                    # Enroque corto
                    elif rookMoving.getPosition().getY() == 7:
                        chessGame.board.movePiece(originSquare, sq.Square(pos.Position(currentSquare.getPosition().getX(), currentSquare.getPosition().getY() - 1), None))
                        chessGame.board.movePiece(rookMoving, sq.Square(pos.Position(currentSquare.getPosition().getX(), currentSquare.getPosition().getY() - 2), None))
                else:
                    # Movimiento normal de pieza
                    chessGame.board.movePiece(originSquare, currentSquare)
                
                # Cambio de turno
                current_turn = not current_turn
                chessGame.addRound()
                
                # Verificación de jaque y jaque mate
                ischeck, danger, _ = chessGame.checkForCheck(current_turn)
                if ischeck:
                    checkPainterUI(danger)
                    # Verifica si hay jaque mate
                    playerSquares = chessGame.getBoard().getPlayerSquares(current_turn)
                    hasValidMoves = False
                    
                    # Comprobar si alguna pieza puede evitar el jaque
                    for square in playerSquares:
                        moveList = getDestinyList(square, danger)
                        
                        # Filtrar movimientos que no evitan el jaque
                        for move in moveList[:]:
                            testGame = game.ChessGame(deepcopy(chessGame.getBoard()), "1", "2")
                            testGame.board.movePiece(
                                testGame.getBoard().findSquare(square.getPosition()), 
                                testGame.getBoard().findSquare(move.getPosition())
                            )
                            newCheck, _, _ = testGame.checkForCheck(current_turn)
                            if newCheck:
                                moveList.remove(move)
                        
                        if moveList:
                            hasValidMoves = True
                            break
                    
                    if not hasValidMoves:
                        chessGame.setCheckMate(current_turn)
                        winner = "Black" if current_turn else "White"
                        messagebox.showinfo("Game Over", f"{winner} king wins!")
                        boardWin.quit()
            
            selected_square = None
            updateBoardUI(0, 0)
    
    def configureCmd(self):
        """Configura el comando del botón"""
        self.bt_obj.configure(command=lambda: self.cmd())

def castlingChecker(kingPiece, playerSquares):
    """Verifica las posibilidades de enroque
    Args:
        kingPiece: Pieza rey que podría hacer enroque
        playerSquares: Lista de casillas del jugador actual
    Returns:
        Lista de torres disponibles para enroque
    """
    if not kingPiece.getPiece().getCastling():
        return []
    
    rooks = []
    king_pos = kingPiece.getPosition()
    board = chessGame.getBoard()
    
    for square in playerSquares[:]:
        if square.getPiece().getName() == "Rook" and square.getPiece().getCastling():
            rook_pos = square.getPosition()
            
            # Verificar que el camino esté despejado
            path_clear = True
            
            # Si la torre está a la izquierda del rey
            if rook_pos.getY() < king_pos.getY():
                for y in range(rook_pos.getY() + 1, king_pos.getY()):
                    if board.findSquare(pos.Position(king_pos.getX(), y)).hasPiece():
                        path_clear = False
                        break
            # Si la torre está a la derecha del rey
            elif rook_pos.getY() > king_pos.getY():
                for y in range(king_pos.getY() + 1, rook_pos.getY()):
                    if board.findSquare(pos.Position(king_pos.getX(), y)).hasPiece():
                        path_clear = False
                        break
            
            if path_clear:
                rooks.append(square)
    
    return rooks

def getDestinyList(chosenSquare: sq.Square, danger=[]):
    """Obtiene la lista de movimientos posibles para una pieza
    Args:
        chosenSquare: Casilla que contiene la pieza a mover
        danger: Lista de posiciones peligrosas (para el rey)
    Returns:
        Lista de casillas a las que se puede mover la pieza
    """
    if not chosenSquare.hasPiece():
        return []
    availableSquares = chosenSquare.getPiece().possibleMoves(chessGame.getBoard(), chosenSquare.getPosition())
    
    # Si es un rey, añadir las torres disponibles para enroque
    if chosenSquare.getPiece().getName() == "King":
        # Obtener las casillas del jugador actual
        playerSquares = chessGame.getBoard().getPlayerSquares(chosenSquare.getPiece().isWhite())
        # Obtener torres disponibles para enroque
        castlingRooks = castlingChecker(chosenSquare, playerSquares)
        # Añadir torres a los movimientos disponibles
        availableSquares.extend(castlingRooks)
        # Filtrar movimientos peligrosos
        return checkKingMoves(availableSquares, danger)
    
    return availableSquares

def checkKingMoves(kingmoves, bannedMoves):
    """Filtra los movimientos del rey para evitar posiciones peligrosas
    Args:
        kingmoves: Lista de movimientos posibles del rey
        bannedMoves: Lista de posiciones prohibidas por estar amenazadas
    Returns:
        Lista filtrada de movimientos seguros para el rey
    """
    newList = []
    for kingMove in kingmoves:
        is_banned = False
        king_pos = kingMove.getPosition()
        for bannedMove in bannedMoves:
            if king_pos.getX() == bannedMove.getX() and king_pos.getY() == bannedMove.getY():
                is_banned = True
                break
        if not is_banned:
            newList.append(kingMove)
    return newList

def squareSelectionChecker(squareList, selected):
    """Verifica si una casilla seleccionada está en la lista de casillas válidas
    Args:
        squareList: Lista de casillas válidas
        selected: Posición seleccionada a verificar
    Returns:
        Tupla (bool, Square): True y la casilla si es válida, False y None si no
    """
    for square in squareList:
        if square.getPosition().getX() == selected.getX() and square.getPosition().getY() == selected.getY():
            return True, square
    return False, None

def movePainterUI(moveList: list):
    """Resalta en el tablero los movimientos posibles
    Args:
        moveList: Lista de posiciones a resaltar
    """
    for position in moveList:
        squareMatrix[position.getX()][position.getY()].bt_obj.configure(bg=MOVE_BG)

def checkPainterUI(checkList):
    """Resalta en el tablero las posiciones de jaque
    Args:
        checkList: Lista de posiciones que causan jaque
    """
    for position in checkList:
        squareMatrix[position.getX()][position.getY()].bt_obj.configure(bg=CHECK_BG)

def updateBoardUI(i, j):
    """Actualiza la interfaz gráfica del tablero
    Args:
        i, j: Coordenadas (no utilizadas en la implementación actual)
    """
    squares = chessGame.getBoard().getSquares()
    for row in range(len(squareMatrix)):
        for column in range(len(squareMatrix[row])):
            square = deepcopy(squares[row][column])
            if square.hasPiece():
                pieceIcon = square.getPiece().getIcon()
                squareMatrix[row][column].bt_obj.configure(text=pieceIcon)
            else:
                squareMatrix[row][column].bt_obj.configure(text="")

# Función para limpiar la consola de manera compatible con diferentes sistemas operativos
def clear_console():
    """Limpia la consola de manera compatible con diferentes sistemas operativos"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')

# Función para crear un tablero con piezas en posiciones aleatorias (MixMode)
def create_mix_mode_board():
    """Crea un tablero con piezas en posiciones aleatorias para el modo MixMode"""
    board = brd.Board(initialize=False)  # Crear tablero vacío
    
    # Crear listas de posiciones disponibles
    white_positions = []
    black_positions = []
    
    # Llenar las posiciones disponibles (4 filas para cada color)
    for i in range(4, 8):  # Filas 4-7 para blancas (abajo)
        for j in range(8):
            white_positions.append(pos.Position(i, j))
    
    for i in range(4):  # Filas 0-3 para negras (arriba)
        for j in range(8):
            black_positions.append(pos.Position(i, j))
    
    # Función para verificar si una posición corresponde a una casilla blanca
    def is_white_square(position):
        # En un tablero de ajedrez, una casilla es blanca si la suma de sus coordenadas es par
        return (position.getX() + position.getY()) % 2 == 0
    
    # Función para colocar piezas y verificar que el rey no esté en jaque
    def place_pieces_safely():
        # Reiniciar el tablero
        board.resetBoard()
        
        # Crear copias de las posiciones para no modificar las originales
        white_pos_copy = white_positions.copy()
        black_pos_copy = black_positions.copy()
        
        # Mezclar las posiciones
        random.shuffle(white_pos_copy)
        random.shuffle(black_pos_copy)
        
        # Separar posiciones por color de casilla para las piezas blancas
        white_player_white_squares = [pos for pos in white_pos_copy if is_white_square(pos)]
        white_player_black_squares = [pos for pos in white_pos_copy if not is_white_square(pos)]
        
        # Separar posiciones por color de casilla para las piezas negras
        black_player_white_squares = [pos for pos in black_pos_copy if is_white_square(pos)]
        black_player_black_squares = [pos for pos in black_pos_copy if not is_white_square(pos)]
        
        # Verificar que hay suficientes casillas de cada color
        if (len(white_player_white_squares) < 2 or len(white_player_black_squares) < 2 or
            len(black_player_white_squares) < 2 or len(black_player_black_squares) < 2):
            return False
        
        # Seleccionar posiciones para los alfiles (uno en casilla blanca, otro en casilla negra)
        white_bishop1_pos = white_player_white_squares.pop(0)
        white_bishop2_pos = white_player_black_squares.pop(0)
        black_bishop1_pos = black_player_white_squares.pop(0)
        black_bishop2_pos = black_player_black_squares.pop(0)
        
        # Seleccionar posiciones para los caballos (uno en casilla blanca, otro en casilla negra)
        white_knight1_pos = white_player_white_squares.pop(0)
        white_knight2_pos = white_player_black_squares.pop(0)
        black_knight1_pos = black_player_white_squares.pop(0)
        black_knight2_pos = black_player_black_squares.pop(0)
        
        # Combinar las posiciones restantes para las demás piezas
        remaining_white_positions = white_player_white_squares + white_player_black_squares
        remaining_black_positions = black_player_white_squares + black_player_black_squares
        
        # Mezclar las posiciones restantes
        random.shuffle(remaining_white_positions)
        random.shuffle(remaining_black_positions)
        
        # Verificar que hay suficientes posiciones restantes
        if len(remaining_white_positions) < 12 or len(remaining_black_positions) < 12:
            return False
        
        # Colocar alfiles blancos en casillas de distinto color
        board.placePiece("Bishop", white_bishop1_pos, True)
        board.placePiece("Bishop", white_bishop2_pos, True)
        
        # Colocar caballos blancos en casillas de distinto color
        board.placePiece("Knight", white_knight1_pos, True)
        board.placePiece("Knight", white_knight2_pos, True)
        
        # Colocar alfiles negros en casillas de distinto color
        board.placePiece("Bishop", black_bishop1_pos, False)
        board.placePiece("Bishop", black_bishop2_pos, False)
        
        # Colocar caballos negros en casillas de distinto color
        board.placePiece("Knight", black_knight1_pos, False)
        board.placePiece("Knight", black_knight2_pos, False)
        
        # Definir las piezas restantes a colocar
        white_remaining_pieces = ["Rook", "Queen", "King", "Rook"] + ["Pawn"] * 8
        black_remaining_pieces = ["Rook", "Queen", "King", "Rook"] + ["Pawn"] * 8
        
        # Asegurarse de que hay suficientes posiciones para todas las piezas
        if len(remaining_white_positions) < len(white_remaining_pieces) or len(remaining_black_positions) < len(black_remaining_pieces):
            return False
        
        # Colocar las demás piezas blancas (excepto alfiles y caballos)
        for i, piece_type in enumerate(white_remaining_pieces):
            board.placePiece(piece_type, remaining_white_positions[i], True)
        
        # Colocar las demás piezas negras (excepto alfiles y caballos)
        for i, piece_type in enumerate(black_remaining_pieces):
            board.placePiece(piece_type, remaining_black_positions[i], False)
        
        # Verificar que todas las piezas están colocadas
        white_pieces = board.getPlayerSquares(True)
        black_pieces = board.getPlayerSquares(False)
        
        # Contar cada tipo de pieza
        white_piece_counts = {}
        black_piece_counts = {}
        
        for square in white_pieces:
            piece_name = square.getPiece().getName()
            white_piece_counts[piece_name] = white_piece_counts.get(piece_name, 0) + 1
        
        for square in black_pieces:
            piece_name = square.getPiece().getName()
            black_piece_counts[piece_name] = black_piece_counts.get(piece_name, 0) + 1
        
        # Verificar que están todas las piezas necesarias
        expected_counts = {
            "Pawn": 8,
            "Rook": 2,
            "Knight": 2,
            "Bishop": 2,
            "Queen": 1,
            "King": 1
        }
        
        # Verificar que cada tipo de pieza tiene la cantidad correcta
        for piece_name, count in expected_counts.items():
            if white_piece_counts.get(piece_name, 0) != count or black_piece_counts.get(piece_name, 0) != count:
                return False
        
        # Verificar que ningún rey esté en jaque
        temp_game = game.ChessGame(board, "White", "Black")
        white_check, _, _ = temp_game.checkForCheck(True)
        black_check, _, _ = temp_game.checkForCheck(False)
        
        # Si algún rey está en jaque, retornar False para intentar de nuevo
        return not (white_check or black_check)
    
    # Intentar colocar las piezas hasta que ningún rey esté en jaque y todas las piezas estén presentes
    max_attempts = 100  # Límite de intentos para evitar bucles infinitos
    attempts = 0
    
    while attempts < max_attempts:
        if place_pieces_safely():
            # Verificación final de que todas las piezas están presentes
            white_pieces = board.getPlayerSquares(True)
            black_pieces = board.getPlayerSquares(False)
            
            if len(white_pieces) == 16 and len(black_pieces) == 16:
                # Verificar que hay exactamente 8 peones de cada color
                white_pawns = sum(1 for square in white_pieces if square.getPiece().getName() == "Pawn")
                black_pawns = sum(1 for square in black_pieces if square.getPiece().getName() == "Pawn")
                
                if white_pawns == 8 and black_pawns == 8:
                    return board
        
        attempts += 1
    
    # Si después de muchos intentos no se logra, crear un tablero estándar
    print("No se pudo crear un tablero aleatorio válido después de varios intentos. Usando tablero estándar.")
    return brd.Board()

# Función para mostrar la ventana de selección de modo de juego
def game_mode_selection():
    """Muestra una ventana para seleccionar el modo de juego"""
    global game_mode
    
    def select_normal_mode():
        global game_mode
        game_mode = "Normal"
        mode_selection_win.destroy()
    
    def select_mix_mode():
        global game_mode
        game_mode = "MixMode"
        mode_selection_win.destroy()
    
    # Crear ventana de selección de modo
    mode_selection_win = tk.Tk()
    mode_selection_win.title("Selección de Modo de Juego")
    mode_selection_win.geometry("400x200")
    
    # Etiqueta de instrucción
    label = tk.Label(mode_selection_win, text="Selecciona el modo de juego:", font=("Arial", 14))
    label.pack(pady=20)
    
    # Frame para los botones
    button_frame = tk.Frame(mode_selection_win)
    button_frame.pack(pady=10)
    
    # Botones de selección
    normal_button = tk.Button(button_frame, text="Normal", command=select_normal_mode, 
                             width=10, height=2, font=("Arial", 12))
    normal_button.grid(row=0, column=0, padx=20)
    
    mix_button = tk.Button(button_frame, text="MixMode", command=select_mix_mode, 
                          width=10, height=2, font=("Arial", 12))
    mix_button.grid(row=0, column=1, padx=20)
    
    # Centrar la ventana
    mode_selection_win.update_idletasks()
    width = mode_selection_win.winfo_width()
    height = mode_selection_win.winfo_height()
    x = (mode_selection_win.winfo_screenwidth() // 2) - (width // 2)
    y = (mode_selection_win.winfo_screenheight() // 2) - (height // 2)
    mode_selection_win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    mode_selection_win.mainloop()

# Bloque principal del programa
if __name__ == '__main__':
    # Mostrar ventana de selección de modo de juego
    game_mode_selection()
    
    # Inicialización de variables para nombres de jugadores - Ahora simplificados
    p1Name = "White"
    p2Name = "Black"
    
    # Creación y configuración de la ventana del tablero
    boardWin = tk.Tk()
    boardWin.title("PyChess - " + game_mode)
    squareMatrix = []
    
    # Creación del tablero de ajedrez
    whiteSquare = False
    for i in range(8):
        whiteSquare = not whiteSquare  # Alterna colores para patrón de tablero
        squareMatrix.append([])
        for j in range(8):
            # Crea y configura cada botón del tablero con dimensiones cuadradas
            btn = tk.Button(boardWin, bd=0, bg=BLACK_BG, fg=WHITE_BG, width=2, height=1, font=("Arial", 36))
            ib = indexedButton(btn, whiteSquare)
            ib.configureCmd()
            if whiteSquare:
                ib.bt_obj.configure(bg=WHITE_BG, fg=BLACK_BG)
            # Usar sticky para que los botones se expandan uniformemente
            ib.bt_obj.grid(row=i, column=j, sticky="nsew", padx=0, pady=0)
            squareMatrix[-1].append(ib)
            whiteSquare = not whiteSquare
    
    # Configurar el grid para que todas las filas y columnas tengan el mismo peso
    for i in range(8):
        boardWin.grid_rowconfigure(i, weight=1)
        boardWin.grid_columnconfigure(i, weight=1)

    # Configura la ventana como no redimensionable
    boardWin.resizable(False, False)

    # Inicializa el juego con los jugadores según el modo seleccionado
    if game_mode == "MixMode":
        # Crear tablero con piezas en posiciones aleatorias
        mix_board = create_mix_mode_board()
        chessGame = game.ChessGame(mix_board, plr.Player(p1Name, True), plr.Player(p2Name, False))
    else:
        # Modo normal con tablero estándar
        chessGame = game.ChessGame(brd.Board(), plr.Player(p1Name, True), plr.Player(p2Name, False))
    
    updateBoardUI(0, 0)  # Actualiza la interfaz inicial
    boardWin.mainloop()  # Inicia el bucle principal de la interfaz
