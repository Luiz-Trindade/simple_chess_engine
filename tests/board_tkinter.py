import os
import tkinter as tk
from PIL import Image, ImageTk
from utils import *

# Estado do jogo
history = []
origem = None


def clicar_casa(event):
    global origem

    coluna = event.x // 50
    linha = event.y // 50
    casa_clicada = (linha * 8) + coluna + 1

    x_grid = coluna * 50
    y_grid = linha * 50

    if origem is None:
        origem = casa_clicada
        # Desenha destaque
        canvas.create_rectangle(
            x_grid,
            y_grid,
            x_grid + 50,
            y_grid + 50,
            outline="green",
            width=5,
            tags="destaque",
        )
        print(f"Origem selecionada: {origem}")
    else:
        destino = casa_clicada

        if verify_move("knight", origem, destino):
            print(f"Movimento válido de {origem} para {destino}")
            # Corrigido: Centralizando em 25, 25 (centro da casa 50x50)
            canvas.coords(peca, x_grid + 25, y_grid + 25)
            history.append(f"k{origem}-{destino}")
        else:
            print(f"Movimento inválido de {origem} para {destino}")

        canvas.delete("destaque")
        origem = None


# Configuração da Janela
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Corrigido: Subindo um nível (..) para sair da pasta 'tests' e entrar em 'assets'
base_dir = os.path.dirname(os.path.abspath(__file__))
caminho_imagem = os.path.join(base_dir, "..", "assets", "white-knight.png")

# Carrega a imagem
img_origem = Image.open(caminho_imagem).convert("RGBA")
img_resized = img_origem.resize((40, 40), Image.Resampling.LANCZOS)
img_peca = ImageTk.PhotoImage(img_resized)

# Desenhar o tabuleiro
for i in range(8):
    for j in range(8):
        cor = "white" if (i + j) % 2 == 0 else "black"
        canvas.create_rectangle(i * 50, j * 50, i * 50 + 50, j * 50 + 50, fill=cor)

# Inicializa a peça no centro da casa 1 (coordenadas iniciais)
peca = canvas.create_image(25, 25, image=img_peca, tags="peca")

canvas.bind("<Button-1>", clicar_casa)
root.mainloop()
