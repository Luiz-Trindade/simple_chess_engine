history = []

board = [None for _ in range(64)]

border_top = [1, 2, 3, 4, 5, 6, 7, 8]
border_down = [57, 58, 59, 60, 61, 62, 63, 64]
border_left = [1, 9, 17, 25, 33, 41, 49, 57]
border_right = [8, 16, 24, 32, 40, 48, 56, 64]

white_pawns = [9, 10, 11, 12, 13, 14, 15, 16]
black_pawns = [49, 50, 51, 52, 53, 54, 55, 56]


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


def path_is_clear(start, end):
    diff = end - start
    abs_diff = abs(diff)

    # Define o passo (step)
    if verify_if_is_same_line(start, end):
        step = 1 if diff > 0 else -1
    elif abs_diff % 8 == 0:
        step = 8 if diff > 0 else -8
    # AQUI ESTÁ O SEGREDO PARA BISPOS/RAINHAS:
    elif abs_diff % 9 == 0:
        step = 9 if diff > 0 else -9
    elif abs_diff % 7 == 0:
        step = 7 if diff > 0 else -7
    else:
        return False

    if step in [7, -7, 9, -9]:
        col_start = (start - 1) % 8
        col_end = (end - 1) % 8
        row_start = (start - 1) // 8
        row_end = (end - 1) // 8
        # Em uma diagonal real, a distância entre colunas é igual à distância entre linhas
        if abs(col_start - col_end) != abs(row_start - row_end):
            return False

    # VERIFICAÇÃO DE BORDA (O QUE FALTA NO SEU CÓDIGO):
    # Se estivermos movendo na diagonal (passo 7 ou 9), não podemos permitir
    # que a peça salte da coluna A para a H (ou vice-versa) durante o trajeto.
    curr = start
    while curr != end:
        curr += step

        # Se a peça chegou no destino, está ok
        if curr == end:
            break

        # Se o próximo passo sair do tabuleiro ou cruzar uma borda indevida
        if not (1 <= curr <= 64):
            return False

        # Se a peça for 'atropelar' alguém, o caminho está bloqueado
        if board[curr - 1] is not None:
            return False

        # TRUQUE DA BORDA: Se o passo for 7 ou 9 (diagonal),
        # a casa atual e a anterior não podem estar na mesma coluna
        # (a menos que seja o destino).
        if step in [7, -7, 9, -9]:
            if abs((curr % 8) - ((curr - step) % 8)) > 1:
                return False  # Tentou pular colunas, movimento ilegal

    return True


def verify_target_square(cor_origem, position):
    """
    Verifica se a casa de destino está vazia OU ocupada por uma peça inimiga.
    """
    peca_destino = board[position - 1]

    if peca_destino is None:
        return True  # Casa vazia, pode mover

    cor_destino = peca_destino.split("-")[0]
    if cor_origem != cor_destino:
        return True  # É uma peça inimiga, pode capturar!
    else:
        return False  # É uma peça amiga, movimento bloqueado


def verify_move(piece, start, end, color="white"):
    # Agora passamos a 'color' para saber se o alvo é amigo ou inimigo
    if start == end or not verify_target_square(color, end):
        return False  # A peça não se moveu ou bateu num aliado

    diff = abs(start - end)
    # pawn_diff = 8 if color == "white" else -8

    # Cavalo (Knight) - Lógica de distância (L)
    if piece == "knight":
        # Movimentos de cavalo são sempre diferença de 2 e 1 casa (eixos)
        # Em um tabuleiro linear, isso resulta em saltos de 6, 10, 15, 17
        return diff in [6, 10, 15, 17]

    # Bispo (Bishop) - Diagonal
    if piece == "bishop" and path_is_clear(start, end):
        # Se for diagonal, a diferença é múltipla de 7 ou 9
        return diff % 9 == 0 or diff % 7 == 0

    # Torre (Rook) - Vertical ou Horizontal
    if piece == "rook" and path_is_clear(start, end):
        # Vertical: diff é múltiplo de 8 | Horizontal: estão na mesma linha
        return diff % 8 == 0 or verify_if_is_same_line(start, end)

    # Rainha (Queen)
    if piece == "queen" and path_is_clear(start, end):
        return (
            diff % 9 == 0
            or diff % 7 == 0
            or diff % 8 == 0
            or verify_if_is_same_line(start, end)
        )

    # Rei (King)
    if piece == "king" and path_is_clear(start, end):
        # Distância de 1 (lado), 8 (cima/baixo), 7 ou 9 (diagonal)
        # O 'or verify_if_is_same_line' evita que o Rei pule de uma linha para outra
        # em movimentos laterais errados
        return diff in [1, 7, 8, 9] and (
            (diff in [7, 8, 9]) or verify_if_is_same_line(start, end)
        )

    # Peão (Pawn)
    if piece == "pawn":
        if color == "white":
            # Movimento normal: 1 casa para frente (diff = 8)
            # Movimento inicial: 2 casas para frente (diff = 16) se estiver na linha inicial
            if start in white_pawns:
                return diff == 8 or (diff == 16 and start in white_pawns)
            else:
                return diff == 8 and end - start == 8
        else:
            # Movimento normal: 1 casa para frente (diff = 8)
            # Movimento inicial: 2 casas para frente (diff = 16) se estiver na linha inicial
            if start in black_pawns:
                return diff == 8 or (diff == 16 and start in black_pawns)
            else:
                return diff == 8 and end - start == -8
    return False
