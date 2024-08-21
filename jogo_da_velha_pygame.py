import pygame
import sys
import numpy as np

# Inicialização do Pygame
pygame.init()

# Dimensões da janela
WIDTH = 600
HEIGHT = 650  # Aumentado para adicionar espaço para o botão de reiniciar
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Cores
BG_COLOR = (100, 170, 156)
LINE_COLOR = (89, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
BUTTON_COLOR = BG_COLOR  # Botão com a mesma cor do fundo
BUTTON_TEXT_COLOR = (255, 255, 255)

# Criando a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo da Velha')
screen.fill(BG_COLOR)

# Criando o tabuleiro
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Função para desenhar as linhas do tabuleiro
def draw_lines():
    # Linhas horizontais
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Linhas verticais
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)

# Função para desenhar as figuras (círculos e cruzes)
def draw_figures():
    # Percorre cada célula do tabuleiro para desenhar as figuras de acordo com o valor
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)

# Função para marcar uma célula
def mark_square(row, col, player):
    board[row][col] = player

# Função para verificar se a célula está disponível
def available_square(row, col):
    return board[row][col] == 0

# Função para verificar se o tabuleiro está cheio
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

# Função para verificar se há um vencedor
def check_win(player):
    # Verificação das linhas
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # Verificação das colunas
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    # Verificação das diagonais
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_ascending_diagonal(player)
        return True

    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_descending_diagonal(player)
        return True

    return False

# Funções para desenhar as linhas de vitória
def draw_horizontal_winning_line(row, player):
    posX = SQUARE_SIZE // 2
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), LINE_WIDTH)

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    posY = SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 65), LINE_WIDTH)

def draw_ascending_diagonal(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 65), (WIDTH - 15, 15), LINE_WIDTH)

def draw_descending_diagonal(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 65), LINE_WIDTH)

# Função para desenhar o botão de reiniciar
def draw_restart_button():
    # Desenha o botão na mesma cor do fundo
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 2 - 100, HEIGHT - 50, 200, 40))
    font = pygame.font.Font(None, 40)
    text = font.render('Reiniciar', True, BUTTON_TEXT_COLOR)  # Renderiza o texto "Reiniciar"
    screen.blit(text, (WIDTH // 2 - 70, HEIGHT - 45))  # Desenha o texto no botão

# Função para verificar se o botão de reiniciar foi clicado
def is_restart_button_clicked(pos):
    # Verifica se o clique está dentro das coordenadas do botão
    if WIDTH // 2 - 100 <= pos[0] <= WIDTH // 2 + 100 and HEIGHT - 50 <= pos[1] <= HEIGHT - 10:
        return True
    return False

# Função para reiniciar o jogo
def restart():
    screen.fill(BG_COLOR)  # Limpa a tela
    draw_lines()  # Redesenha as linhas do tabuleiro
    draw_restart_button()  # Redesenha o botão de reiniciar
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0  # Zera todas as células do tabuleiro

# Desenhar as linhas iniciais e o botão de reiniciar
draw_lines()  # Desenha as linhas do tabuleiro
draw_restart_button()  # Desenha o botão de reiniciar

# Inicializando variáveis de controle do jogo
player = 1  # Começa com o jogador 1
game_over = False  # Indica se o jogo terminou

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Se o jogador fechar a janela
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Verifica clique do mouse
            mouseX = event.pos[0]  # Coordenada X do clique
            mouseY = event.pos[1]  # Coordenada Y do clique

            # Verifica se o botão de reiniciar foi clicado
            if is_restart_button_clicked(event.pos):
                restart()  # Reinicia o jogo
                game_over = False  # Reinicia o estado de game_over
                player = 1  # Reinicia com o jogador 1

            if not game_over:
                clicked_row = mouseY // SQUARE_SIZE  # Determina a linha clicada
                clicked_col = mouseX // SQUARE_SIZE  # Determina a coluna clicada

                # Se a célula clicada estiver disponível
                if clicked_row < BOARD_ROWS and available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)  # Marca a célula com o jogador atual
                    if check_win(player):  # Verifica se o jogador venceu
                        game_over = True  # Marca o jogo como terminado
                    player = 3 - player  # Alterna entre o jogador 1 e 2

                    draw_figures()  # Redesenha as figuras no tabuleiro

    pygame.display.update()  # Atualiza a tela
