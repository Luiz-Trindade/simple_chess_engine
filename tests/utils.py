history = []

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


# Falta implementar a lógica de movimento do peão
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

    if piece == "pawn":
        pass

    return False


def verify_if_square_is_free(peca_origem, position):
    """
    Verifica se a casa de destino está livre e printa a interação.
    peca_origem: O nome da peça que está tentando se mover (ex: 'white-queen')
    position: O número da casa de destino (1 a 64)
    """
    peca_destino = board[position - 1]

    if peca_destino is None:
        print(f"[{peca_origem}] quer mover para a casa {position}, que está LIVRE.")
        return True
    else:
        print(
            f"[{peca_origem}] quer mover para a casa {position}, mas está OCUPADA por [{peca_destino}]."
        )
        return False


def execute_simple_chess_engine(playing_as="black"):
    """
    Função simples para simular o movimento do computador.

    Passos Teóricos de um Motor de Xadrez Simples:
    1. Avaliação do Tabuleiro: O motor analisa o estado atual do tabuleiro, identificando as peças, suas posições e possíveis ameaças.
    2. Geração de Movimentos: O motor gera uma lista de movimentos legais para as peças do jogador (neste caso, para as peças pretas).
    3. Avaliação de Movimentos: Para cada movimento gerado, o motor avalia o resultado potencial do movimento, considerando fatores como ganho de material, controle do centro, segurança do rei, etc.
    4. Seleção do Melhor Movimento: O motor seleciona o movimento que tem a melhor avaliação, ou seja, aquele que maximiza as chances de vitória ou minimiza as chances de derrota.
    5. Execução do Movimento: O motor executa o movimento selecionado, atualizando o estado do tabuleiro e preparando-se para a próxima jogada do jogador.
    """
    print("Bem-vindo ao Simple Chess Engine!")
    print(f"Eu, o computador, estou jogando de '{playing_as}'")
