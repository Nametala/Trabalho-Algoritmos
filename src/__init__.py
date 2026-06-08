import pygame

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x_jogador, y_jogador, local_arquivo): 
        super().__init__()
        super().__init__()
        
        # Carrega o laser único do Piskel
        imagem_original = pygame.image.load(local_arquivo).convert_alpha()
        
        # Define a escala do projétil
        escala_laser = 5
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