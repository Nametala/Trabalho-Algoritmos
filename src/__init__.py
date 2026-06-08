import pygame

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x_jogador, y_jogador):
        super().__init__()
        # 1. Criamos uma superfície retangular simples (largura: 6px, altura: 15px)
        self.image = pygame.Surface((6, 15))
        
        # 2. Pintamos o tiro de vermelho neon para destacar bem na tela
        self.image.fill((255, 0, 0)) 
        
        # 3. Definimos o rect e posicionamos na ponta da nave
        self.rect = self.image.get_rect()
        self.rect.centerx = x_jogador
        self.rect.top = y_jogador
        
        self.velocidade = 10

    def update(self):
        # Move para cima
        self.rect.y -= self.velocidade
        
        # Se sair da tela, elimina o objeto
        if self.rect.y <= 0:
            self.kill()