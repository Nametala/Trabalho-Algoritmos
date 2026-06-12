import pygame
from src.config import CAMINHO_CHEFE, LARGURA_TELA

def pegar_sprite(local_arquivo, x, y, width, height, scale=1.0):
    """Carrega uma imagem e recorta um pedaço específico dela (spritesheet)."""
    imagem_completa = pygame.image.load(local_arquivo).convert_alpha()
    
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
    def __init__(self, x_jogador, y_jogador, local_arquivo):
        super().__init__()
        
        # Carrega o laser único do Piskel
        imagem_original = pygame.image.load(local_arquivo).convert_alpha()
        
        # Define a escala do projétil (Ajuste aqui se quiser mudar o tamanho do tiro)
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

    def update(self):
        # Move o tiro para cima
        self.rect.y -= self.velocidade
        
        # Se o tiro sair da tela, ele se destrói
        if self.rect.y <= 0:
            self.kill()

class Chefe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Carrega a imagem do chefe
        self.image_original = pygame.image.load(CAMINHO_CHEFE).convert_alpha()
        
        # TAMANHO CHEFE
        self.tamanho = (400, 400)
        self.image = pygame.transform.scale(self.image_original, self.tamanho)
        
        self.rect = self.image.get_rect()
        
        # Posiciona no meio do eixo X e um pouco acima da tela (para entrar deslizando)
        self.rect.centerx = LARGURA_TELA // 2
        self.rect.bottom = 0 
        
