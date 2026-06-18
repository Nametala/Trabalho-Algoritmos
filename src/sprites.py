import pygame
from src.config import CAMINHO_CHEFE, LARGURA_TELA, CAMINHO_TIRO, CAMINHO_NAVE, CAMINHO_INIMIGO, ALTURA_TELA, vidas, CAMINHO_13_VIDA, CAMINHO_23_VIDA, CAMINHO_VIDA_CHEIA, CAMINHO_VIDA_VAZIA

def pegar_sprite(CAMINHO_TIRO, x, y, width, height, scale=1.0):
    """Carrega uma imagem e recorta um pedaço específico dela (spritesheet)."""
    imagem_completa = pygame.image.load(CAMINHO_TIRO).convert_alpha()
    
    # Cria uma superfície vazia com o tamanho do corte
    superficie_corte = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Copia o pedaço da folha para a superfície vazia
    superficie_corte.blit(imagem_completa, (0, 0), (x, y, width, height))
    
    # Aplica a escala de tamanho se necessário
    if scale != 1.0:
        novo_tamanho = (int(width * scale), int(height * scale))
        superficie_corte = pygame.transform.scale(superficie_corte, novo_tamanho)
    
    return superficie_corte


class Projetil(pygame.sprite.Sprite):
    def __init__(self, x_jogador, y_jogador, CAMINHO_TIRO):
        super().__init__()
        
        imagem_original = pygame.image.load(CAMINHO_TIRO).convert_alpha()
        
        # Define a escala do projétil
        escala_laser = 1.5 
        largura_nova = int(imagem_original.get_width() * escala_laser)
        altura_nova = int(imagem_original.get_height() * escala_laser)
        
        # Redimensiona o tiro mantendo as proporções
        self.image = pygame.transform.scale(imagem_original, (largura_nova, altura_nova))
        
        # Posiciona o tiro saindo centralizado do bico do jogador
        self.rect = self.image.get_rect()
        self.rect.centerx = x_jogador
        self.rect.bottom = y_jogador  

        self.velocidade = 10
        self.dano = 1

    def update(self):
        # Move o tiro para cima
        self.rect.y -= self.velocidade
        
        # Se o tiro sair da tela, ele se destrói
        if self.rect.y <= 0:
            self.kill()

# Certifique-se de que LARGURA_TELA está importada no topo do seu sprites.py
# Caso não esteja, importe do src.config

class Chefe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(CAMINHO_CHEFE).convert_alpha() 

        escala_chefe = 4

        largura_nave = int(self.image.get_width() * escala_chefe)
        altura_nave = int(self.image.get_height() * escala_chefe)
        self.image = pygame.transform.scale(self.image, (largura_nave, altura_nave))

        self.rect = self.image.get_rect()
        
        self.rect.centerx = LARGURA_TELA // 2
        self.rect.bottom = 0  
        # Status chefe
        self.vida = 30
        self.velocidade = 1

    def update(self):
        self.rect.y += self.velocidade
        
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.vidas = vidas
        self.image = pygame.image.load(CAMINHO_NAVE).convert_alpha()

        escala_nave = 2 
        largura_nave = int(self.image.get_width() * escala_nave)
        altura_nave = int(self.image.get_height() * escala_nave)
        self.image = pygame.transform.scale(self.image, (largura_nave, altura_nave))
        
        # Hitbox
        self.rect = self.image.get_rect()

        posicao_inicial_x = (LARGURA_TELA // 2) - (largura_nave // 2)
        posicao_inicial_y = ALTURA_TELA - altura_nave - 20

        self.rect.x = posicao_inicial_x
        self.rect.y = posicao_inicial_y
        self.velocidade = 5

    def update(self):
        # Movimentação
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]: self.rect.x -= self.velocidade
        if teclas[pygame.K_d]: self.rect.x += self.velocidade
        if teclas[pygame.K_w]: self.rect.y -= self.velocidade
        if teclas[pygame.K_s]: self.rect.y += self.velocidade

        # Bordas da tela
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > LARGURA_TELA: self.rect.right = LARGURA_TELA
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > ALTURA_TELA: self.rect.bottom = ALTURA_TELA

class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.vida = 2
        self.velocidade = 1

        self.image = pygame.image.load(CAMINHO_INIMIGO).convert_alpha()

        escala_inimigo = 2 
        largura_inimigo = int(self.image.get_width() * escala_inimigo)
        altura_inimigo = int(self.image.get_height() * escala_inimigo)
        self.image = pygame.transform.scale(self.image, (largura_inimigo, altura_inimigo))
        
        self.rect = self.image.get_rect()

    def update(self):
        # Mover para baixo
        self.rect.y += self.velocidade
        # Chegar ao fim da tela
        if self.rect.top > ALTURA_TELA:
            self.kill()
        
class BarraDeVida(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.vida = vidas
        
        img = pygame.image.load(CAMINHO_VIDA_CHEIA).convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * 5), int(img.get_height() * 5)))

        self.rect = self.image.get_rect()
        
        self.rect.x = 20
        self.rect.y = 330

    def update(self, vidas):
        if vidas == 3:
            img_nova = pygame.image.load(CAMINHO_VIDA_CHEIA).convert_alpha()
        elif vidas == 2:
            img_nova = pygame.image.load(CAMINHO_23_VIDA).convert_alpha()
        elif vidas == 1:
            img_nova = pygame.image.load(CAMINHO_13_VIDA).convert_alpha()
        else:
            img_nova = pygame.image.load(CAMINHO_VIDA_VAZIA).convert_alpha()
        
        self.image = pygame.transform.scale(img_nova, (int(img_nova.get_width() * 5), int(img_nova.get_height() * 5)))
            

