import os
import tkinter as tk
from PIL import Image, ImageTk
from utils import *

# Mapeamento inicial das posições (Casa 1 = a1, Casa 64 = h8)
posicoes_iniciais = {
    "white-rook": [1, 8],
    "white-knight": [2, 7],
    "white-bishop": [3, 6],
    "white-queen": [4],
    "white-king": [5],
    "white-pawn": [9, 10, 11, 12, 13, 14, 15, 16],
    "black-rook": [57, 64],
    "black-knight": [58, 63],
    "black-bishop": [59, 62],
    "black-queen": [60],
    "black-king": [61],
    "black-pawn": [49, 50, 51, 52, 53, 54, 55, 56],
}

pecas_pontos = {
    "pawn": 1,
    "knight": 3,
    "bishop": 3,
    "rook": 5,
    "queen": 9,
    "king": 0,  # O rei é inestimável, mas para fins de avaliação, pode ser considerado 0
}

# Variáveis globais de estado
origem = None
peca_selecionada_id = None
pecas_no_canvas = {}  # Armazena ID do canvas -> {nome, casa}

# Preenche o array 'board' (importado de utils) com o estado inicial
# Assumindo que board é uma lista de 64 elementos (índices 0 a 63)
for nome, casas in posicoes_iniciais.items():
    for pos in casas:
        board[pos - 1] = nome


def casa_para_coordenadas(posicao):
    """Converte 1-64 para (x, y) central da casa."""
    pos = posicao - 1
    coluna = pos % 8
    linha = 7 - (pos // 8)
    return coluna * 50 + 25, linha * 50 + 25


def get_notation(linha, coluna):
    return f"{chr(ord('a') + coluna)}{8 - linha}"


def atualizar_canvas_com_board():
    # 1. Remove todas as peças existentes no canvas (que estão marcadas com a tag "peca")
    canvas.delete("peca")

    # 2. Limpa nosso dicionário de controle
    pecas_no_canvas.clear()

    # 3. Itera sobre o board e redesenha tudo
    for posicao, nome_peca in enumerate(board):
        if nome_peca is not None:
            # Converte índice 0-63 para casa 1-64
            casa_numero = posicao + 1
            cx, cy = casa_para_coordenadas(casa_numero)

            # Redesenha a imagem
            obj_id = canvas.create_image(cx, cy, image=imagens[nome_peca], tags="peca")
            pecas_no_canvas[obj_id] = {"nome": nome_peca, "casa": casa_numero}


def clicar_casa(event):
    global origem, peca_selecionada_id

    coluna = event.x // 50
    linha = event.y // 50
    casa_clicada = ((7 - linha) * 8) + coluna + 1
    x_grid, y_grid = coluna * 50, linha * 50

    if origem is None:
        # Selecionar peça
        itens = canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in itens:
            if item in pecas_no_canvas:
                origem = casa_clicada
                peca_selecionada_id = item
                canvas.create_rectangle(
                    x_grid,
                    y_grid,
                    x_grid + 50,
                    y_grid + 50,
                    outline="green",
                    width=5,
                    tags="destaque",
                )
                return
    else:
        # Tentar mover
        destino = casa_clicada
        info_peca = pecas_no_canvas[peca_selecionada_id]

        # O tipo da peça é algo como 'white-queen', e queremos extrair 'white' para validar se o jogador pode mover essa peça
        tipo_peca = info_peca["nome"].split("-")[0]

        # O nome da peça é algo como 'white-queen', e queremos extrair 'queen' para a lógica de movimento
        nome_curto = info_peca["nome"].split("-")[1]

        # Validação gráfica e lógica
        if (
            verify_move(nome_curto, origem, destino, type_piece="white")
            and verify_if_square_is_free(info_peca["nome"], destino)
            and tipo_peca == "white"
        ):
            # 1. Move a imagem na tela
            canvas.coords(peca_selecionada_id, x_grid + 25, y_grid + 25)
            info_peca["casa"] = destino

            # 2. Atualiza o array board importado de utils
            board[origem - 1] = None
            board[destino - 1] = info_peca["nome"]

            atualizar_canvas_com_board()
            print(f"Movido de {origem} para {destino}")

            # 3. Vez do computador (movimento aleatório para teste)
            execute_simple_chess_engine(playing_as="black", board=board)
        else:
            print("Movimento inválido")

        canvas.delete("destaque")
        origem = None
        peca_selecionada_id = None


# Configuração
root = tk.Tk()
root.title("Tabuleiro de Xadrez")
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Carregar imagens
base_dir = os.path.dirname(os.path.abspath(__file__))
imagens = {}
for nome in posicoes_iniciais.keys():
    path = os.path.join(base_dir, "..", "assets", f"{nome}.png")
    if os.path.exists(path):
        img = (
            Image.open(path).convert("RGBA").resize((40, 40), Image.Resampling.LANCZOS)
        )
        imagens[nome] = ImageTk.PhotoImage(img)

# Desenhar tabuleiro e peças
for linha in range(8):
    for coluna in range(8):
        x, y = coluna * 50, linha * 50
        cor = "white" if (linha + coluna) % 2 == 0 else "gray"
        canvas.create_rectangle(x, y, x + 50, y + 50, fill=cor)
        canvas.create_text(
            x + 10, y + 10, text=get_notation(linha, coluna), font=("Arial", 7)
        )

for nome, casas in posicoes_iniciais.items():
    if nome in imagens:
        for pos in casas:
            cx, cy = casa_para_coordenadas(pos)
            obj_id = canvas.create_image(cx, cy, image=imagens[nome], tags="peca")
            pecas_no_canvas[obj_id] = {"nome": nome, "casa": pos}

canvas.bind("<Button-1>", clicar_casa)
root.mainloop()
