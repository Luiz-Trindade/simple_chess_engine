from random import *
from utils import *

board_center_squares = [27, 28, 29, 30, 31, 35, 36, 37, 38, 39]


def detect_game_stage(board):
    """
    Detecta a fase do jogo (abertura, meio-jogo, final) com base na quantidade de peças restantes no tabuleiro.
    """
    total_pecas = sum(1 for p in board if p is not None)

    if total_pecas > 20:
        return "oppening"
    elif 10 < total_pecas <= 20:
        return "middlegame"
    else:
        return "final"


def gerar_ameacas_peca(board, posicao_origem):
    """
    Lista todas as casas ameaçadas por uma peça específica em uma posição.
    posicao_origem: Inteiro (1-64)
    """
    ameacas = set()
    peca = board[posicao_origem - 1]

    if not peca:
        return ameacas

    tipo_peca = peca.split("-")[1]
    color = peca.split("-")[0]  # "white" ou "black"

    # 1. Lógica para PEÕES (Diferença de direção baseado na cor)
    if tipo_peca == "pawn":
        # Brancas sobem (somam), Pretas descem (subtraem)
        direcao = 8 if color == "white" else -8
        borda = verify_if_is_border(posicao_origem)

        # Ameaças diagonais
        if borda != "left":
            ameacas.add(posicao_origem + direcao - 1)
        if borda != "right":
            ameacas.add(posicao_origem + direcao + 1)

    # 2. Lógica para as demais peças
    else:
        for destino in range(1, 65):
            if destino == posicao_origem:
                continue

            if verify_move(tipo_peca, posicao_origem, destino, color):
                # Peças de salto
                if tipo_peca in ["knight"]:
                    ameacas.add(destino)
                    print(f"{peca} ameaça a casa {destino} (movimento de salto).")

                # Peças deslizantes
                elif tipo_peca in ["rook", "bishop", "queen", "king"]:
                    if path_is_clear(posicao_origem, destino):
                        ameacas.add(destino)
                        print(f"{peca} ameaça a casa {destino} (caminho limpo).")

    # Filtra apenas casas válidas no tabuleiro
    return {c for c in ameacas if 1 <= c <= 64}


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
                    if tipo_peca in ["knight"]:
                        casas_controladas.add(destino)

                    # Peças "deslizantes" precisam de caminho limpo
                    elif tipo_peca in ["rook", "bishop", "queen", "king"]:
                        if path_is_clear(posicao_atual, destino):
                            casas_controladas.add(destino)

    # Remove casas fora do tabuleiro (ex: peão na linha 8 ameaçando linha 9)
    return {c for c in casas_controladas if 1 <= c <= 64}


def get_positions_of_pieces(board, color="white"):

    pass


def calculate_valid_moves(calculate_for="black", board=[]):
    """
    Função para calcular todos os movimentos válidos para as peças de um jogador específico (preto ou branco).
    """

    pieces_and_valid_moves = {}
    piece_count = {}

    for i in range(64):
        peca = board[i]
        if peca and peca.startswith(calculate_for):
            peca_name = peca.split("-")[1]
            posicao_atual = i + 1

            # Contar peças do mesmo tipo
            if peca_name not in piece_count:
                piece_count[peca_name] = 0
            piece_count[peca_name] += 1

            valid_moves_for_piece = []

            for destino in range(1, 65):
                if verify_move(
                    piece=peca_name,
                    start=posicao_atual,
                    end=destino,
                    color=calculate_for,
                ):

                    # Peças de "salto" ou curto alcance não precisam checar caminho livre
                    if peca_name in ["knight"]:
                        valid_moves_for_piece.append(destino)

                    # Peças "deslizantes" precisam de caminho limpo
                    elif peca_name in ["rook", "bishop", "queen", "king", "pawn"]:
                        if path_is_clear(posicao_atual, destino):
                            valid_moves_for_piece.append(destino)

            # Criar chave com número incrementado
            peca_key = f"{calculate_for}-{peca_name}-{piece_count[peca_name]}"
            pieces_and_valid_moves[peca_key] = valid_moves_for_piece

    return pieces_and_valid_moves


def get_captureble_pieces(board, attacking_color="white"):
    """
    Função para identificar quais peças do oponente estão ameaçadas por um jogador específico.
    """
    threatened_pieces = []

    for i in range(64):
        peca = board[i]
        if peca and peca.startswith(attacking_color):
            posicao_atual = i + 1
            ameacas = gerar_ameacas_peca(board, posicao_atual)

            for ameaca in ameacas:
                peca_ameacada = board[ameaca - 1]
                if peca_ameacada and not peca_ameacada.startswith(attacking_color):
                    threatened_pieces.append((peca_ameacada, ameaca))

    return threatened_pieces


def modify_board_with_move(board, start, end):
    """
    Função para modificar o estado do tabuleiro após um movimento.
    """
    piece = board[start - 1]
    board[start - 1] = None
    board[end - 1] = piece
    return board


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

    # Variáveis para avaliação
    game_stage = detect_game_stage(board)
    opponet = "white" if playing_as == "black" else "black"
    opponet_threats = gerar_mapa_ameacas(board, verify=opponet)
    my_threats = gerar_mapa_ameacas(board, verify=playing_as)
    my_valid_moves = calculate_valid_moves(calculate_for=playing_as, board=board)
    missions = {
        "dominate_center": 0,
        "develop_pieces": 0,
    }

    print(f"Fase do jogo: {game_stage}")
    print(f"Casas ameaçadas por '{opponet}': {len(opponet_threats)}")
    print(f"Casas ameaçadas por '{playing_as}': {len(my_threats)}")
    print(f"Minhas peças ameaçam as seguintes casas: {my_threats}")
    print(f"Peças do oponente ameaçam as seguintes casas: {opponet_threats}")
    print(
        f"Peças que o oponente ameaça: {get_captureble_pieces(board, attacking_color=opponet)}"
    )

    if game_stage == "oppening":
        print("Estratégia: Controle do centro e desenvolvimento de peças.")
        print(f"Movimentos válidos para minhas peças: {my_valid_moves}")

        # Peças que têm movimentos válidos para o centro recebem prioridade
        valid_pieces_for_center = {}

        # Selecionar as peças e seus movimentos válidos que mais chegam perto do centro
        for piece, moves in my_valid_moves.items():
            for move in moves:
                # Se o movimento leva a uma casa central ou próxima, marca essa peça como prioritária
                if move in board_center_squares:
                    valid_pieces_for_center[piece] = moves
                    print(
                        f"Peça {piece} tem os seguintes movimentos válidos para o centro: {moves}"
                    )

        # Selecionar das peças válidas, aquelas que ameaçam o centro
        if valid_pieces_for_center:
            # 1. Escolha a peça e o movimento
            selected_piece_key = choice(list(valid_pieces_for_center.keys()))
            selected_move = choice(valid_pieces_for_center[selected_piece_key])

            # 2. Extrair informações para localizar a peça no board
            # Formato da chave: "black-pawn-1"
            parts = selected_piece_key.split("-")
            color_peca = parts[0]
            tipo_peca = parts[1]
            instancia_peca = int(parts[2])

            posicao_atual = -1
            count = 0

            # 3. Localizar a posição correta (índice 1-64)
            for i in range(64):
                peca_no_board = board[i]
                if peca_no_board and peca_no_board == f"{color_peca}-{tipo_peca}":
                    count += 1
                    if count == instancia_peca:
                        posicao_atual = i + 1
                        break

            # 4. Executar o movimento APÓS localizar a posição
            if posicao_atual != -1:
                modify_board_with_move(board, posicao_atual, selected_move)
                print(f"Peça selecionada: {selected_piece_key}")
                print(f"Movendo de {posicao_atual} para {selected_move}.")
            else:
                print(
                    f"Erro: Não foi possível localizar {selected_piece_key} no tabuleiro."
                )

    elif game_stage == "middlegame":
        print("Estratégia: Táticas, ataques e defesas.")

    else:
        print("Estratégia: Simplificação e promoção de peões.")
