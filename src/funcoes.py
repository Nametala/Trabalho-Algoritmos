import pygame
import sys
from src.config import ALTURA_TELA, LARGURA_TELA, SOM_MORTE, TITULO_JOGO
from src.sprites import Inimigo, Chefe

def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)


# isso aqui ta regulando o jogo de acordo com o seu nivel, a cada 500 pontos aumenta velocidade vida e frequencia dos inimigos
def calcular_dificuldade(pontos, frequencia_base=200):
    nivel = pontos // 1000

    velocidade = min(1 + nivel * 0.3, 4) #velocidade max = 4
    vida_inimigo = min(2 + nivel // 2, 8) #vida max = 8
    vida_chefe = 20 + nivel * 10 #aumento na vida do chefe
    frequencia_spawn = max(frequencia_base - nivel * 5, 200) #frequencia max = 200

    return velocidade, vida_inimigo, vida_chefe, frequencia_spawn

def mostrar_pontos(tela, pontos, recorde, fonte):
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    texto_recorde = fonte.render(f"Recorde: {recorde}", True, (255, 255, 255))
    tela.blit(texto_pontos, (20, 20))
    tela.blit(texto_recorde, (20, 55))

def mostrar_tela_final(tela, fundo_final, fonte_grande, fonte_pequena):
    som_perdeu = pygame.mixer.Sound(SOM_MORTE)
    som_perdeu.play()
    
    
    texto_titulo = fonte_grande.render("O IMPÉRIO VENCEU", True, (255, 255, 255))
    texto_subtitulo = fonte_pequena.render("PRESSIONE ESPAÇO PARA REINICIAR", True, (255, 255, 255))
    
    retangulo_titulo = texto_titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 80))
    retangulo_subtitulo = texto_subtitulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 40))
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando = False
        
        tela.blit(fundo_final, (0, 0))
        tela.blit(texto_titulo, retangulo_titulo)
        tela.blit(texto_subtitulo, retangulo_subtitulo)
        pygame.display.flip()

def spawn_padroes_inimigos(grupo_inimigos, tipo, LARGURA_TELA, vida=2, velocidade=1):
    margem = 25

    if tipo == 1:
        for i in range(5):
            ini = Inimigo(vida, velocidade)
            largura = ini.rect.width
            passo_x = (LARGURA_TELA - 2 * margem - largura) / 4
            ini.rect.x = margem + i * passo_x
            ini.rect.y = -40
            grupo_inimigos.add(ini)

    elif tipo == 2:
        offsets = [
            (0,    -40), (-160, -90), (160, -90), (-320, -140), (320, -140),
        ]
        for dx, y in offsets:
            ini = Inimigo(vida, velocidade)
            ini.rect.centerx = LARGURA_TELA // 2 + dx
            ini.rect.y = y
            grupo_inimigos.add(ini)

    elif tipo == 3:
        for i in range(5):
            ini = Inimigo(vida, velocidade)
            largura = ini.rect.width
            passo_x = (LARGURA_TELA - 2 * margem - largura) / 4
            ini.rect.x = margem + i * passo_x
            ini.rect.y = -80 + i * 10
            grupo_inimigos.add(ini)

    elif tipo == 4:
        for i in range(5):
            ini = Inimigo(vida, velocidade)
            largura = ini.rect.width
            passo_x = (LARGURA_TELA - 2 * margem - largura) / 4
            ini.rect.x = LARGURA_TELA - margem - largura - i * passo_x
            ini.rect.y = -80 + i * 10
            grupo_inimigos.add(ini)

    # fila diagonal direita -> esquerda 
    elif tipo == 4:
        for i in range(5):
            ini = Inimigo()
            largura = ini.rect.width
            passo_x = (LARGURA_TELA - 2 * margem - largura) / 4
            ini.rect.x = LARGURA_TELA - margem - largura - i * passo_x
            ini.rect.y = -80 + i * 10
            grupo_inimigos.add(ini)

def mostrar_tela_inicial(tela, fundo_inicial, fonte_grande, fonte_pequena):
    texto_titulo = fonte_grande.render(TITULO_JOGO, True, (255, 255, 255))
    texto_subtitulo = fonte_pequena.render("PRESSIONE ESPAÇO PARA INICIAR", True, (255, 255, 255))
    
    retangulo_titulo = texto_titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 60))
    retangulo_subtitulo = texto_subtitulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 40))
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando = False
        
        tela.blit(fundo_inicial, (0, 0))
        tela.blit(texto_titulo, retangulo_titulo)
        tela.blit(texto_subtitulo, retangulo_subtitulo)
        pygame.display.flip()