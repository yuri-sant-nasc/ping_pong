import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura_tela = 1080
altura_tela = 720
tela = pygame.display.set_mode((largura_tela, altura_tela))

# Configurações da raquete
largura_raquete = 15
altura_raquete = 80
velocidade_raquete = 1

# Configurações da bola
tamanho_bola = 20
velocidade_bola_x = 0.8  # Velocidade horizontal reduzida pela metade
velocidade_bola_y = 0.8  # Velocidade vertical reduzida pela metade

# Cores
cor_branca = (255, 255, 255)

# Raquetes e bola
raquete1 = pygame.Rect(0, altura_tela / 2, largura_raquete, altura_raquete)
raquete2 = pygame.Rect(largura_tela - largura_raquete, altura_tela / 2, largura_raquete, altura_raquete)
bola_pos_x = largura_tela / 2  # Posição x da bola como um número de ponto flutuante
bola_pos_y = altura_tela / 2  # Posição y da bola como um número de ponto flutuante
bola = pygame.Rect(bola_pos_x, bola_pos_y, tamanho_bola, tamanho_bola)

# Estado do jogo e placar
em_jogo = False
novo_round = False
placar = [0, 0]

# Fonte para o placar e o menu de início
fonte_placar = pygame.font.Font(None, 36)
fonte_menu = pygame.font.Font(None, 72)

# Loop do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Verifica se o usuário pressionou a tecla ESPAÇO para iniciar o jogo ou mudar a cor das raquetes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                em_jogo = True
                novo_round = False

    # Se o jogo não estiver em andamento ou se estamos esperando por um novo round, exibe o menu de início e pula o resto do loop
    if not em_jogo or novo_round:
        tela.fill((0, 0, 0))
        menu_texto = fonte_menu.render("Pressione ESPAÇO para começar", True, cor_branca)
        tela.blit(menu_texto, (largura_tela / 2 - menu_texto.get_width() / 2, altura_tela / 2 - menu_texto.get_height() / 2))
        pygame.display.flip()
        continue

    # Movimentação das raquetes
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        raquete1.move_ip(0, -velocidade_raquete)
    if keys[pygame.K_DOWN]:
        raquete1.move_ip(0, velocidade_raquete)
    if keys[pygame.K_w]:
        raquete2.move_ip(0, -velocidade_raquete)
    if keys[pygame.K_s]:
        raquete2.move_ip(0, velocidade_raquete)

    # Movimentação da bola e atualização do placar se a bola atinge a borda esquerda ou direita da tela
    bola_pos_x += velocidade_bola_x
    bola_pos_y += velocidade_bola_y

    # Atualiza a posição da bola para ser a posição arredondada da bola
    bola.x = round(bola_pos_x)
    bola.y = round(bola_pos_y)

    if bola.left < 0:
        velocidade_bola_x *= -1
        placar[1] += 1
        # Faz a bola retornar ao centro e espera pelo próximo round
        bola_pos_x = largura_tela / 2
        bola_pos_y = altura_tela / 2
        novo_round = True

    if bola.right > largura_tela:
        velocidade_bola_x *= -1
        placar[0] += 1
        # Faz a bola retornar ao centro e espera pelo próximo round
        bola_pos_x = largura_tela / 2
        bola_pos_y = altura_tela / 2
        novo_round = True

    # Colisão com as bordas da tela
    if raquete1.top < 0:
        raquete1.top = 0
    if raquete1.bottom > altura_tela:
        raquete1.bottom = altura_tela
    if raquete2.top < 0:
        raquete2.top = 0
    if raquete2.bottom > altura_tela:
        raquete2.bottom = altura_tela

    # Adiciona colisão da bola com as bordas superior e inferior da tela
    if bola.top < 0 or bola.bottom > altura_tela:
        velocidade_bola_y *= -1

    # Colisão da bola com as raquetes
    if bola.colliderect(raquete1) or bola.colliderect(raquete2):
        velocidade_bola_x *= -1

    # Limpa a tela e desenha as raquetes e a bola
    tela.fill((0, 0, 0))
    pygame.draw.rect(tela, cor_branca, raquete1)
    pygame.draw.rect(tela, cor_branca, raquete2)
    pygame.draw.ellipse(tela, cor_branca, bola)
    pygame.draw.aaline(tela, cor_branca, (largura_tela / 2, 0), (largura_tela / 2, altura_tela))

    # Desenha o placar na tela
    placar_texto = fonte_placar.render(f"{placar[0]} - {placar[1]}", True, cor_branca)
    tela.blit(placar_texto, (largura_tela / 2 - placar_texto.get_width() / 2, 10))

    # Atualiza a tela
    pygame.display.flip()
