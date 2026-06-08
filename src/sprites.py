import pygame

def pegar_sprite(local_arquivo, x, y, width, height, scale=1):
    """Corta um único elemento de uma spritesheet e remove o fundo usando canal Alpha."""
    
    # 1. Carrega a imagem mantendo a transparência original (.png com canal alpha)
    # Se for usar BMP/fundo preto fixo, mantenha apenas .convert()
    sheet = pygame.image.load(local_arquivo).convert_alpha()

    # 2. Cria uma superfície vazia QUE ACEITA TRANSPARÊNCIA (SRCALPHA)
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # 3. Copia o pedaço da folha para a nossa nova imagem
    image.blit(sheet, (0, 0), (x, y, width, height))
    
    # 4. Configuração da transparência inteligente
    # Se o pixel (0,0) for preto ou cinza de fundo (em imagens sem alpha real):
    cor_do_fundo = image.get_at((0, 0))
    # Se a cor detectada não for transparente, força o colorkey nela
    if cor_do_fundo[3] > 0: 
        image.set_colorkey(cor_do_fundo)
    
    # 5. Aplica o redimensionamento, se houver
    if scale != 1:
        novo_largura = int(width * scale)
        novo_altura = int(height * scale)
        image = pygame.transform.scale(image, (novo_largura, novo_altura))
        
    return image

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x_jogador, y_jogador):
        super().__init__()
        
        # Criamos uma superfície temporária de 6x15 pixels pintada de vermelho
        self.image = pygame.Surface((6, 15))
        self.image.fill((255, 0, 0)) 
        
        # Configura o retângulo de posicionamento
        self.rect = self.image.get_rect()
        self.rect.centerx = x_jogador
        self.rect.top = y_jogador
        
        self.velocidade = 10

    def update(self):
        # Move o tiro para cima
        self.rect.y -= self.velocidade
        
        # Se sair da tela, se auto-destrói
        if self.rect.y <= 0:
            self.kill()