# Importación de módulos necesarios
import sys
from copy import deepcopy  # Para crear copias profundas de objetos
import os
import tkinter as tk
from tkinter import messagebox

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
                        messagebox.showinfo("Game Over", f"{winner} wins by checkmate!")
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

def playerNameMenu():
    """Crea y gestiona la ventana de entrada de nombres de jugadores"""
    def getPlayerNames():
        """Callback para procesar los nombres ingresados"""
        global p1Name, p2Name
        p1Name = entryPlayer1.get()
        p2Name = entryPlayer2.get()
        if not p1Name:
            p1Name = "player1"
        if not p2Name:
            p2Name = "player2"
        playerInputWin.destroy()
    
    # Creación de frames para organizar la interfaz
    frameP1 = tk.Frame(playerInputWin, width=150, height=200)
    frameP1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    frameP2 = tk.Frame(playerInputWin, width=150, height=200)
    frameP2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    
    # Campos de entrada para nombres
    entryPlayer1 = tk.Entry(frameP1, width=20)
    entryPlayer1.grid(row=1, column=0, sticky=tk.W)
    entryPlayer2 = tk.Entry(frameP2, width=20)
    entryPlayer2.grid(row=1, column=0, sticky=tk.W)

    # Etiquetas para los campos
    labelPlayer1 = tk.Label(frameP1, text="Enter name for white:")
    labelPlayer1.grid(row=0, column=0, sticky=tk.W)
    labelPlayer2 = tk.Label(frameP2, text="Enter name for black:")
    labelPlayer2.grid(row=0, column=0, sticky=tk.W)

    # Botón de envío
    submitButton = tk.Button(playerInputWin, text="Submit", command=getPlayerNames)
    submitButton.place(relx=0.5, rely=0.8)

    # Vincula la tecla Enter para enviar el formulario
    playerInputWin.bind("<Return>", lambda e: getPlayerNames())

# Función para limpiar la consola de manera compatible con diferentes sistemas operativos
def clear_console():
    """Limpia la consola de manera compatible con diferentes sistemas operativos"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')

# Bloque principal del programa
if __name__ == '__main__':
    # Limpia la consola e imprime el banner
    #clear_console()
    #print("======================== [PYCHESS - By @Constructogamer and @iikerm] ========================")
    
    # Inicialización de variables para nombres de jugadores
    p1Name = ""
    p2Name = ""

    # Creación y configuración de la ventana de nombres
    #playerInputWin = tk.Tk()
    #playerInputWin.title("Choose player")
    #playerInputWin.geometry("320x420")
    #playerNameMenu()
    #playerInputWin.mainloop()
    
    # Creación y configuración de la ventana del tablero
    boardWin = tk.Tk()
    boardWin.title("PyChess")
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

    # Inicializa el juego con los jugadores
    chessGame = game.ChessGame(brd.Board(), plr.Player(p1Name, True), plr.Player(p2Name, False))
    updateBoardUI(0, 0)  # Actualiza la interfaz inicial
    boardWin.mainloop()  # Inicia el bucle principal de la interfaz
