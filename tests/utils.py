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


def path_is_clear(start, end):
    diff = end - start
    abs_diff = abs(diff)

    # 1. Define o passo (step)
    if verify_if_is_same_line(start, end):  # Horizontal tem prioridade
        step = 1 if diff > 0 else -1
    elif abs_diff % 8 == 0:
        step = 8 if diff > 0 else -8
    elif abs_diff % 9 == 0:
        step = 9 if diff > 0 else -9
    elif abs_diff % 7 == 0:
        step = 7 if diff > 0 else -7
    else:
        return False

    # 2. Verifica obstruções
    curr = start + step
    while curr != end:
        if 1 <= curr <= 64:
            if board[curr - 1] is not None:
                return False
        curr += step
    return True


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


def gerar_mapa_ameacas(board, verify="white"):
    """
    Lista todas as casas 'ameaçadas' ou 'controladas' por peças brancas ou pretas.
    """
    casas_controladas = set()

    for i in range(64):
        peca = board[i]
        if peca and peca.startswith(verify):
            tipo_peca = peca.split("-")[1]
            posicao_atual = i + 1

            # 1. Lógica para PEÕES (Ameaçam apenas as diagonais frontais)
            if tipo_peca == "pawn":
                # Peão branco na casa X ameaça X+7 e X+9 (se não estiver na borda)
                borda = verify_if_is_border(posicao_atual)
                if borda != "left":
                    casas_controladas.add(posicao_atual + 7)
                if borda != "right":
                    casas_controladas.add(posicao_atual + 9)
                continue

            # 2. Lógica para as demais peças
            for destino in range(1, 65):
                if verify_move(tipo_peca, posicao_atual, destino):

                    # Peças de "salto" ou curto alcance não precisam checar caminho livre
                    if tipo_peca in ["knight", "king"]:
                        casas_controladas.add(destino)

                    # Peças "deslizantes" precisam de caminho limpo
                    elif tipo_peca in ["rook", "bishop", "queen"]:
                        if path_is_clear(posicao_atual, destino):
                            casas_controladas.add(destino)

    # Remove casas fora do tabuleiro (ex: peão na linha 8 ameaçando linha 9)
    return {c for c in casas_controladas if 1 <= c <= 64}


def execute_simple_chess_engine(playing_as="black", board=[]):
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

    print(gerar_mapa_ameacas(board, verify="white"))
