import pygame
import random
import requests
from io import BytesIO

# Inicialização do Pygame
pygame.init()

# Configurações da janela
largura = 800
altura = 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pong - By https://github.com/eoLucasS")

# Definir o ícone da janela
icon_url = "https://cdn.discordapp.com/attachments/1104525551898734632/1119015427536855070/favicon-32x32.png"
response = requests.get(icon_url)
icon = pygame.image.load(BytesIO(response.content))
pygame.display.set_icon(icon)

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Variáveis do jogo
tamanho_raquete = 60
velocidade_jogador = 5
velocidade_computador = 5
tamanho_bola = 10
pontuacao_jogador = 0
pontuacao_computador = 0

# Fonte para o placar
fonte_placar = pygame.font.Font("freesansbold.ttf", 32)

# Função para desenhar a raquete
def desenhar_raquete(x, y):
    pygame.draw.rect(tela, BRANCO, (x, y, 10, tamanho_raquete))

# Função para desenhar a bola
def desenhar_bola(x, y):
    pygame.draw.ellipse(tela, BRANCO, (x, y, tamanho_bola, tamanho_bola))

# Função para atualizar a tela do jogo
def atualizar_tela(background):
    tela.fill(PRETO)
    tela.blit(background, (0, 0))  # Exibe a imagem de background
    desenhar_raquete(10, jogador_posicao_y)
    desenhar_raquete(largura - 20, computador_posicao_y)
    desenhar_bola(bola_posicao_x, bola_posicao_y)

    # Exibe o placar do jogador
    placar_jogador = fonte_placar.render(str(pontuacao_jogador), True, BRANCO)
    tela.blit(placar_jogador, (largura // 2 - 50, 10))

    # Exibe o placar do computador
    placar_computador = fonte_placar.render(str(pontuacao_computador), True, BRANCO)
    tela.blit(placar_computador, (largura // 2 + 30, 10))

    pygame.display.update()

# Função principal do jogo
def jogo_pong():
    global jogador_posicao_y, computador_posicao_y, bola_posicao_x, bola_posicao_y, velocidade_bola_x, velocidade_bola_y, pontuacao_jogador, pontuacao_computador

    jogador_posicao_y = altura // 2 - tamanho_raquete // 2
    computador_posicao_y = altura // 2 - tamanho_raquete // 2
    bola_posicao_x = largura // 2
    bola_posicao_y = altura // 2
    velocidade_bola_x = random.choice([-1, 1]) * random.randint(5, 7)
    velocidade_bola_y = random.choice([-1, 1]) * random.randint(5, 7)

    relogio = pygame.time.Clock()
    jogo_rodando = True

    # Download e carregamento da imagem de background
    response = requests.get("https://cdn.discordapp.com/attachments/1104525551898734632/1118978557343973557/background.jpg")
    background = pygame.image.load(BytesIO(response.content))
    background = pygame.transform.scale(background, (largura, altura))  # Redimensiona a imagem para o tamanho da tela

    while jogo_rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_rodando = False

        # Movimento da raquete do jogador
        teclas_pressionadas = pygame.key.get_pressed()
        if teclas_pressionadas[pygame.K_UP] and jogador_posicao_y > 0:
            jogador_posicao_y -= velocidade_jogador
        if teclas_pressionadas[pygame.K_DOWN] and jogador_posicao_y < altura - tamanho_raquete:
            jogador_posicao_y += velocidade_jogador

        # Movimento da raquete do computador
        if bola_posicao_y < computador_posicao_y + tamanho_raquete // 2:
            computador_posicao_y -= velocidade_computador
        elif bola_posicao_y > computador_posicao_y + tamanho_raquete // 2:
            computador_posicao_y += velocidade_computador

        # Movimento da bola
        bola_posicao_x += velocidade_bola_x
        bola_posicao_y += velocidade_bola_y

        # Colisão da bola com as raquetes
        if (bola_posicao_x <= 20 and jogador_posicao_y - tamanho_bola <= bola_posicao_y <= jogador_posicao_y + tamanho_raquete) or (bola_posicao_x >= largura - 30 and computador_posicao_y - tamanho_bola <= bola_posicao_y <= computador_posicao_y + tamanho_raquete):
            velocidade_bola_x *= -1
            if jogador_posicao_y - tamanho_bola <= bola_posicao_y <= jogador_posicao_y + tamanho_raquete:
                velocidade_bola_y *= -1
            else:
                if bola_posicao_x <= 20:
                    bola_posicao_x = 30
                else:
                    bola_posicao_x = largura - 30

        # Colisão da bola com as bordas
        if bola_posicao_y <= 0 or bola_posicao_y >= altura - tamanho_bola:
            velocidade_bola_y *= -1

        # Pontuação
        if bola_posicao_x <= 0:
            pontuacao_computador += 1
            bola_posicao_x = largura // 2
            bola_posicao_y = altura // 2
            velocidade_bola_x = random.choice([-1, 1]) * random.randint(5, 7)
            velocidade_bola_y = random.choice([-1, 1]) * random.randint(5, 7)
        elif bola_posicao_x >= largura - tamanho_bola:
            pontuacao_jogador += 1
            bola_posicao_x = largura // 2
            bola_posicao_y = altura // 2
            velocidade_bola_x = random.choice([-1, 1]) * random.randint(5, 7)
            velocidade_bola_y = random.choice([-1, 1]) * random.randint(5, 7)

        atualizar_tela(background)
        relogio.tick(60)

    pygame.quit()

# Executar o jogo
jogo_pong()