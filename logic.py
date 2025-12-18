"""Plantilla con las funciones que el alumnado debe completar para M3.

La capa gráfica llama a estas funciones para mover el estado del juego. No es
necesario crear clases; basta con manipular listas, diccionarios y tuplas.
"""
from __future__ import annotations

import random
from typing import Dict, List, Tuple

# Constantes de estado
STATE_HIDDEN = "hidden"
STATE_VISIBLE = "visible"
STATE_FOUND = "found"

# Tipado para mayor claridad
Card = Dict[str, str]
Board = List[List[Card]]
Position = Tuple[int, int]
GameState = Dict[str, object]


def build_symbol_pool(rows: int, cols: int) -> List[str]:
    """Crea la lista de símbolos necesaria para rellenar todo el tablero.

    Cada símbolo aparece dos veces y la lista final se baraja.
    """
    total_cells = rows * cols
    num_pairs = total_cells // 2

    # Usamos caracteres simples (A, B, C...) como símbolos. 
    # Podríamos usar números o iconos si quisiéramos.
    symbols = []
    for i in range(num_pairs):
        # Generamos un símbolo basado en el índice (A, B, C...)
        symbol = chr(65 + i)
        symbols.append(symbol)
        symbols.append(symbol)

    # Barajamos la lista para que las parejas no estén juntas
    random.shuffle(symbols)
    return symbols


def create_game(rows: int, cols: int) -> GameState:
    """Genera el diccionario con el estado inicial del juego."""
    pool = build_symbol_pool(rows, cols)
    
    board: Board = []
    idx = 0
    for _ in range(rows):
        row_list = []
        for _ in range(cols):
            # Creamos el diccionario de cada carta
            card: Card = {
                "symbol": pool[idx],
                "state": STATE_HIDDEN
            }
            row_list.append(card)
            idx += 1
        board.append(row_list)

    return {
        "board": board,
        "pending": [],  # Almacenará tuplas (row, col)
        "moves": 0,
        "matches": 0,
        "total_pairs": (rows * cols) // 2,
        "rows": rows,
        "cols": cols
    }


def reveal_card(game: GameState, row: int, col: int) -> bool:
    """Intenta descubrir la carta ubicada en row, col."""
    # 1. Validar coordenadas
    if not (0 <= row < int(game["rows"]) and 0 <= col < int(game["cols"])):
        return False

    board = game["board"]
    card = board[row][col]
    pending = game["pending"]

    # 2. Solo revelar si está oculta y no hay ya 2 cartas reveladas esperando resolución
    if card["state"] == STATE_HIDDEN and len(pending) < 2:
        card["state"] = STATE_VISIBLE
        pending.append((row, col))
        return True

    return False


def resolve_pending(game: GameState) -> Tuple[bool, bool]:
    """Resuelve el turno si hay dos cartas pendientes."""
    pending = game["pending"]
    
    if len(pending) != 2:
        return False, False

    # Extraemos las posiciones
    pos1, pos2 = pending[0], pending[1]
    board = game["board"]
    card1 = board[pos1[0]][pos1[1]]
    card2 = board[pos2[0]][pos2[1]]

    # Incrementamos siempre el contador de movimientos
    game["moves"] += 1
    
    pair_found = False
    if card1["symbol"] == card2["symbol"]:
        # ¡Pareja encontrada!
        card1["state"] = STATE_FOUND
        card2["state"] = STATE_FOUND
        game["matches"] += 1
        pair_found = True
    else:
        # No coinciden, se vuelven a ocultar
        card1["state"] = STATE_HIDDEN
        card2["state"] = STATE_HIDDEN

    # Vaciamos la lista de pendientes para el siguiente turno
    game["pending"] = []
    
    return True, pair_found


def has_won(game: GameState) -> bool:
    """Indica si se han encontrado todas las parejas."""
    return game["matches"] == game["total_pairs"]