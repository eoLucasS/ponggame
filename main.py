import pygame
import sys
import time
import random
import os

# Inicialização do módulo pygame
pygame.init()

# Verificação do modo de execução: script ou executável compilado
if getattr(sys, 'frozen', False):
    # Caminho base quando executado como executável PyInstaller
    bundle_dir = sys._MEIPASS
else:
    # Caminho base quando executado como script Python
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Construção do caminho para carregar a imagem de fundo
image_path = os.path.join(bundle_dir, 'assets', 'praia.jpg')

# Definição das dimensões da janela do jogo
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PongGame - github.com/eoLucasS')

# Definição das cores usadas no jogo
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Carregamento e ajuste da imagem de fundo
background = pygame.image.load(image_path)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Inicialização das variáveis do jogo
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 5
player_score = 0
opponent_score = 0
game_active = False
paused = False
start_time = None

# Criação dos objetos do jogo (bola, jogador, oponente)
ball = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 - 15, 30, 30)
player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - 70, 10, 140)
opponent = pygame.Rect(10, SCREEN_HEIGHT // 2 - 70, 10, 140)

# Configuração da fonte de texto
font = pygame.font.Font(None, 36)

# Configuração do relógio para controle da taxa de atualização do jogo
clock = pygame.time.Clock()

def draw():
    """
    Função para desenhar os elementos na tela do jogo.
    Atualiza a tela a cada frame, desenhando a bola, os jogadores e os textos.
    """
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)
    if not game_active and start_time is None:
        # Exibe a mensagem inicial para começar o jogo
        welcome_text = font.render("Press ENTER to start", True, WHITE)
        text_rect = welcome_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        background_rect = pygame.Rect(text_rect.left - 20, text_rect.top - 10, text_rect.width + 40, text_rect.height + 20)
        pygame.draw.rect(screen, GRAY, background_rect)
        screen.blit(welcome_text, text_rect)
    elif paused:
        # Exibe a mensagem de jogo pausado
        pause_text = font.render("Paused - ESC to continue or Q to quit", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        background_rect = pygame.Rect(pause_rect.left - 20, pause_rect.top - 10, pause_rect.width + 40, pause_rect.height + 20)
        pygame.draw.rect(screen, GRAY, background_rect)
        screen.blit(pause_text, pause_rect)
    elif not paused:
        # Exibe o placar e o tempo de jogo
        score_text = font.render(f"{opponent_score} - {player_score}", False, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 30, 20))
        if start_time:
            elapsed_time = int(time.time() - start_time)
            time_text = font.render(f"Time: {elapsed_time}s", False, BLACK)
            screen.blit(time_text, (10, 20))
    pygame.display.flip()

def ball_animation():
    """
    Função para controlar a movimentação da bola e verificar colisões.
    Altera a direção da bola ao colidir com as bordas da tela ou com os jogadores.
    """
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    if not paused:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1
    
        if ball.right >= SCREEN_WIDTH:
            opponent_score += 1
            ball_reset()
        elif ball.left <= 0:
            player_score += 1
            ball_reset()

def ball_reset():
    """
    Reinicia a posição da bola ao centro após um ponto ser marcado.
    A direção inicial da bola é aleatória após o reinício.
    """
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed_y = 7 * random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

def player_animation():
    """
    Atualiza a posição do jogador com base na entrada do usuário.
    Mantém o jogador dentro dos limites da tela.
    """
    if not paused:
        player.y += player_speed
        player.clamp_ip(screen.get_rect())

def opponent_ai():
    """
    Controla a IA do oponente.
    O oponente se move em direção à bola com uma margem de erro para simular desafio.
    """
    margin = 15
    if not paused and abs(opponent.centery - ball.centery) > margin:
        if opponent.centery < ball.centery:
            opponent.y += opponent_speed
        elif opponent.centery > ball.centery:
            opponent.y -= opponent_speed
    opponent.clamp_ip(screen.get_rect())

while True:
    """
    Loop principal do jogo.
    Processa eventos de entrada, atualiza o estado do jogo e redesenha a tela.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed = 7
            elif event.key == pygame.K_UP:
                player_speed = -7
            elif event.key == pygame.K_ESCAPE:
                paused = not paused
            elif event.key == pygame.K_q and paused:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN and not game_active:
                game_active = True
                start_time = time.time()
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                player_speed = 0

    if not paused and game_active:
        ball_animation()
        player_animation()
        opponent_ai()
    draw()
    clock.tick(60)