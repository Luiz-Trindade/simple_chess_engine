import os
import tkinter as tk
from PIL import Image, ImageTk
from utils import *

# Estado do jogo
history = []
origem = None


def get_notation(linha, coluna):
    """Converte índice (0-7, 0-7) para notação a1-h8."""
    col_letter = chr(ord("a") + coluna)
    row_number = 8 - linha
    return f"{col_letter}{row_number}"


def clicar_casa(event):
    global origem

    # Cálculo da casa clicada (considerando o tabuleiro visual 8x8)
    coluna = event.x // 50
    linha = event.y // 50

    # Lógica: o Tkinter desenha linha 0 (topo) até 7 (base)
    # No xadrez, a base é a linha 1.
    casa_clicada = ((7 - linha) * 8) + coluna + 1

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
        print(f"Origem selecionada: {casa_clicada}")
    else:
        destino = casa_clicada
        if verify_move("queen", origem, destino):
            print(f"Movimento válido de {origem} para {destino}")
            canvas.coords(peca, x_grid + 25, y_grid + 25)
            history.append(f"q{origem}-{destino}")
        else:
            print(f"Movimento inválido de {origem} para {destino}")

        canvas.delete("destaque")
        origem = None


# Configuração da Janela
root = tk.Tk()
root.title("Tabuleiro de Xadrez")
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Caminho da imagem
base_dir = os.path.dirname(os.path.abspath(__file__))
caminho_imagem = os.path.join(base_dir, "..", "assets", "white-queen.png")

# Carrega a imagem
img_origem = Image.open(caminho_imagem).convert("RGBA")
img_resized = img_origem.resize((40, 40), Image.Resampling.LANCZOS)
img_peca = ImageTk.PhotoImage(img_resized)

# Desenhar o tabuleiro e a numeração
for linha in range(8):
    for coluna in range(8):
        x = coluna * 50
        y = linha * 50

        # Cor das casas
        cor = "white" if (linha + coluna) % 2 == 0 else "black"
        canvas.create_rectangle(x, y, x + 50, y + 50, fill=cor)

        # Desenha a notação a1-h8
        texto = get_notation(linha, coluna)
        canvas.create_text(
            x + 15, y + 15, text=texto, fill="gray", font=("Arial", 8, "bold")
        )

# Inicializa a peça na casa 1 (a1) -> coluna 0, linha 7
peca = canvas.create_image(25, 375, image=img_peca, tags="peca")

canvas.bind("<Button-1>", clicar_casa)
root.mainloop()
