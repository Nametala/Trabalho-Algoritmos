import pygame
import random
from src.sprites import Projetil

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
    CAMINHO_FUNDO,
    CAMINHO_NAVE,
    CAMINHO_TIRO,
    CAMINHO_INIMIGO
)

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
)
from src.dados import (
    salvar_recorde,
    carregar_recorde,
)


def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""
    pygame.init()
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    rodando = True

    #  CONFIGURAÇÕES CUSTOMIZÁVEIS 
    VIDA_INIMIGO_PADRAO = 2  # vida de todos os inimigos
    DANO_TIRO = 1            # Quanto de vida cada tiro tira do inimigo
    
    velocidade_inimigo = 2   # Velocidade de descida dos inimigos
    velocidade = 5           # Velocidade de movimento do jogador
    frequencia_spawn_min = 30    # Parametro do spawn de inimigos
    frequencia_spawn_max = 90 # Parametro do spawn de inimigos
    frequencia_spawn = random.randint(frequencia_spawn_min, frequencia_spawn_max) # Randomiza o spawn de inimigos

    # Jogador
    imagem_nave_original = pygame.image.load(CAMINHO_NAVE).convert_alpha()
    escala_nave = 2 
    largura_nave = int(imagem_nave_original.get_width() * escala_nave)
    altura_nave = int(imagem_nave_original.get_height() * escala_nave)
    player_image = pygame.transform.scale(imagem_nave_original, (largura_nave, altura_nave))
    player_image.set_colorkey((0, 0, 0))
    player_image = player_image.convert_alpha()

    # Inimigo
    imagem_inimigo_original = pygame.image.load(CAMINHO_INIMIGO).convert_alpha()
    escala_inimigo = 2
    largura_inimigo = int(imagem_inimigo_original.get_width() * escala_inimigo)
    altura_inimigo = int(imagem_inimigo_original.get_height() * escala_inimigo)
    enemy_image = pygame.transform.scale(imagem_inimigo_original, (largura_inimigo, altura_inimigo))
    
    # Fundo
    imagem_original = pygame.image.load(CAMINHO_FUNDO).convert()
    imagem_fundo = pygame.transform.scale(imagem_original, (LARGURA_TELA, ALTURA_TELA))

    # 2. CONFIGURANDO OS ELEMENTOS 
    # Ponto inicial do jogador (centralizado embaixo)
    posicao_inicial_x = (LARGURA_TELA // 2) - (largura_nave // 2)
    posicao_inicial_y = ALTURA_TELA - altura_nave - 20

    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=(posicao_inicial_x, posicao_inicial_y))
    }

    grupo_tiros = pygame.sprite.Group()
    lista_inimigos = []

    temporizador_spawn = 0
    pontos = 0

    vidas = 3   # Vidas
    if vidas < 0:
        vidas = 0
    recorde = carregar_recorde(CAMINHO_RECORDE)

    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            # ESPAÇO (Disparar tiro)
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                novo_tiro = Projetil(jogador["rect"].centerx, player_image.get_rect(topleft=(jogador["rect"].x, jogador["rect"].y)).top, CAMINHO_TIRO)
                grupo_tiros.add(novo_tiro)

        # W A S D
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            jogador["rect"].x -= velocidade
        if teclas[pygame.K_d]:
            jogador["rect"].x += velocidade
        if teclas[pygame.K_w]:
            jogador["rect"].y -= velocidade
        if teclas[pygame.K_s]:
            jogador["rect"].y += velocidade

        # Restrição das bordas da tela para o jogador
        if jogador["rect"].left < 0:
            jogador["rect"].left = 0
        if jogador["rect"].right > LARGURA_TELA:
            jogador["rect"].right = LARGURA_TELA
        if jogador["rect"].top < 0:
            jogador["rect"].top = 0
        if jogador["rect"].bottom > ALTURA_TELA:
            jogador["rect"].bottom = ALTURA_TELA

        # SISTEMA DE GERAÇÃO E MOVIMENTO DOS INIMIGOS 
        temporizador_spawn += 1
        if temporizador_spawn >= frequencia_spawn:
            temporizador_spawn = 0
            
            # Todos os inimigos nascem EXCLUSIVAMENTE no topo, variando apenas a posição X
            x_spawn = random.randint(0, LARGURA_TELA - largura_inimigo)
            y_spawn = -altura_inimigo

            novo_inimigo = {
                "rect": enemy_image.get_rect(topleft=(x_spawn, y_spawn)),
                "vida": VIDA_INIMIGO_PADRAO  # Atribui a quantidade de vida atual configurada
            }
            lista_inimigos.append(novo_inimigo)

        # Atualiza a posição dos inimigos apenas para baixo (eixo Y)
        for ini in lista_inimigos[:]:
            ini["rect"].y += velocidade_inimigo
            
            # SE O INIMIGO PASSAR DO FINAL DA TELA: O jogador perder
            if ini["rect"].top > ALTURA_TELA:
                vidas = tomar_dano(vidas, 100)
                lista_inimigos.remove(ini)

        # Atualiza a movimentação física dos tiros ativos
        grupo_tiros.update() 

        #  VERIFICAÇÃO DE COLISÕES 
        # Colisão: Projéteis contra Inimigos
        for tiro in grupo_tiros.sprites():
            for ini in lista_inimigos[:]:
                if verificar_colisao(tiro.rect, ini["rect"]):
                    tiro.kill()  # O tiro some imediatamente
                    
                    # Aplica o dano na nave inimiga
                    ini["vida"] -= DANO_TIRO
                    
                    # Se a vida do inimigo zerar ou ficar negativa, ele explode de verdade
                    if ini["vida"] <= 0:
                        lista_inimigos.remove(ini)  
                        pontos = calcular_pontos(pontos, 10)
                    break

        # Colisão: Inimigos contra o Jogador (Colisão direta no espaço)
        for ini in lista_inimigos[:]:
            if verificar_colisao(jogador["rect"], ini["rect"]):
                vidas = tomar_dano(vidas, 1)
                lista_inimigos.remove(ini)  

        # Condições de Fim de Jogo e Atualização do Recorde
        if jogador_perdeu(vidas):
            rodando = False

        if pontos > recorde:
            recorde = pontos
            salvar_recorde(CAMINHO_RECORDE, recorde)

        pygame.display.set_caption(
            f"{TITULO_JOGO} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
        )

        #  RENDERIZAÇÃO (DESENHO) 
        tela.blit(imagem_fundo, (0, 0)) 
        
        for ini in lista_inimigos:
            tela.blit(enemy_image, ini["rect"])
            
        tela.blit(jogador["imagem"], jogador["rect"])
        grupo_tiros.draw(tela) 

        pygame.display.flip()

    pygame.quit()