from utils import *
import tkinter as tk

# Estado do jogo
origem = None
peca_selecionada = None


def clicar_casa(event):
    global origem, peca_selecionada

    # Converte pixel para casa (0-63) e coordenadas de grade (0-7)
    coluna = event.x // 50
    linha = event.y // 50
    casa_clicada = (linha * 8) + coluna + 1

    # Coordenadas do canto superior esquerdo da casa
    x_grid = coluna * 50
    y_grid = linha * 50

    if origem is None:
        # Primeiro clique: seleciona a casa de origem
        origem = casa_clicada
        # Desenha um retângulo verde para destacar a seleção
        peca_selecionada = canvas.create_rectangle(
            x_grid,
            y_grid,
            x_grid + 50,
            y_grid + 50,
            outline="green",
            width=3,
            tags="destaque",
        )
        print(f"Origem selecionada: {origem}")
    else:
        # Segundo clique: tenta mover para o destino
        destino = casa_clicada

        # Aqui você chamaria: if verify_move("rook", origem, destino):
        if verify_move("rook", origem, destino):
            print(f"Movimento válido de {origem} para {destino}")
            # Movemos o círculo para o centro da nova casa
            # (Apenas para exemplo visual, aqui entra a validação da peça)
            canvas.coords(peca, x_grid + 5, y_grid + 5, x_grid + 45, y_grid + 45)
        else:
            print(f"Movimento inválido de {origem} para {destino}")

        # Limpa o estado
        canvas.delete("destaque")
        origem = None
        peca_selecionada = None


# Configuração da Janela
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Desenhar o tabuleiro
for i in range(8):
    for j in range(8):
        cor = "white" if (i + j) % 2 == 0 else "gray"
        canvas.create_rectangle(i * 50, j * 50, i * 50 + 50, j * 50 + 50, fill=cor)

# Peça exemplo
peca = canvas.create_oval(10, 10, 40, 40, fill="red", tags="peca")

# Bind do clique no canvas inteiro
canvas.bind("<Button-1>", clicar_casa)

root.mainloop()
