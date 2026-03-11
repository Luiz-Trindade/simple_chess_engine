board = [None for _ in range(64)]
border_top = [1, 2, 3, 4, 5, 6, 7, 8]
border_down = [57, 58, 59, 60, 61, 62, 63, 64]
border_left = [1, 9, 17, 25, 33, 41, 49, 57]
border_right = [8, 16, 24, 32, 40, 48, 56, 64]


def verify_if_is_border(position):
    if position in border_top:
        return "top"
    elif position in border_down:
        return "down"
    elif position in border_left:
        return "left"
    elif position in border_right:
        return "right"
    else:
        return None


def verify_if_is_same_square(start, end):
    if start == end:
        return True
    else:
        return False


def verify_if_is_same_line(start, end):
    if (start - 1) // 8 == (end - 1) // 8:
        return True
    else:
        return False


def verify_move(piece, start, end):
    if start == end:
        return False  # A peça não se moveu

    diff = abs(start - end)

    # Cavalo (Knight) - Lógica de distância (L)
    if piece == "knight":
        # Movimentos de cavalo são sempre diferença de 2 e 1 casa (eixos)
        # Em um tabuleiro linear, isso resulta em saltos de 6, 10, 15, 17
        return diff in [6, 10, 15, 17]

    # Bispo (Bishop) - Diagonal
    if piece == "bishop":
        # Se for diagonal, a diferença é múltipla de 7 ou 9
        return diff % 9 == 0 or diff % 7 == 0

    # Torre (Rook) - Vertical ou Horizontal
    if piece == "rook":
        # Vertical: diff é múltiplo de 8 | Horizontal: estão na mesma linha
        return diff % 8 == 0 or verify_if_is_same_line(start, end)

    # Rainha (Queen)
    if piece == "queen":
        return (
            diff % 9 == 0
            or diff % 7 == 0
            or diff % 8 == 0
            or verify_if_is_same_line(start, end)
        )

    # Rei (King)
    if piece == "king":
        # Distância de 1 (lado), 8 (cima/baixo), 7 ou 9 (diagonal)
        # O 'or verify_if_is_same_line' evita que o Rei pule de uma linha para outra
        # em movimentos laterais errados
        return diff in [1, 7, 8, 9] and (
            (diff in [7, 8, 9]) or verify_if_is_same_line(start, end)
        )

    return False
