from utils import *

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

    opponet = "white" if playing_as == "black" else "black"

    opponet_threats = gerar_mapa_ameacas(board, verify=opponet)
    my_threats = gerar_mapa_ameacas(board, verify=playing_as)

    print(f"Casas ameaçadas por {opponet}: {len(opponet_threats)}")
    print(f"Casas ameaçadas por {playing_as}: {len(my_threats)}")
