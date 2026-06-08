import pygame
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
    CAMINHO_TIRO
)

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
)
from src.sprites import pegar_sprite
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

    # Carregando as imagens do jogo
    imagem_nave_original = pygame.image.load(CAMINHO_NAVE).convert_alpha()
    escala_nave = 2 
    largura_nave = int(imagem_nave_original.get_width() * escala_nave)
    altura_nave = int(imagem_nave_original.get_height() * escala_nave)
    player_image = pygame.transform.scale(imagem_nave_original, (largura_nave, altura_nave))

    # Para remover o fundo preto (torna a cor preta transparente):
    player_image.set_colorkey((0, 0, 0))
    player_image = player_image.convert_alpha()
    
    # Gema pequena: usando tamanho 64x64
    gem_image    = pegar_sprite(CAMINHO_SPRITES, x=900, y=690, width=200, height=200, scale=0.5)

    # Morcego: usando tamanho 180x120 por causa das asas abertas
    bat_image    = pegar_sprite(CAMINHO_SPRITES, x=905, y=1060, width=200, height=130, scale=0.5)
    
    # O ponto inicial da nave
    posicao_inicial_x = (LARGURA_TELA // 2) - (largura_nave // 2)
    posicao_inicial_y = ALTURA_TELA - altura_nave - 20

    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=(posicao_inicial_x, posicao_inicial_y))
    }

    gema = {
        "imagem": gem_image,
        "rect": gem_image.get_rect(topleft=(500, 300))
    }
    
    inimigo = {
        "imagem": bat_image,
        "rect": bat_image.get_rect(topleft=(200, 500))
    }
    
    # Criando o grupo de tiros controlado pelo jogo
    grupo_tiros = pygame.sprite.Group()

    velocidade = 5
    pontos = 0
    vidas = 3
    recorde = carregar_recorde(CAMINHO_RECORDE)

    # Carrega e redimensiona o fundo UMA vez antes do loop começar
    imagem_original = pygame.image.load(CAMINHO_FUNDO).convert()
    imagem_fundo = pygame.transform.scale(imagem_original, (LARGURA_TELA, ALTURA_TELA))

    # Loop principal: processa entrada, atualiza estado e renderiza a cena.
    while rodando:
        relogio.tick(FPS)


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            # ESPAÇO (tiro)
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                novo_tiro = Projetil(jogador["rect"].centerx, jogador["rect"].top, CAMINHO_TIRO)
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

        # Limitando o jogador rigidamente dentro das bordas internas da tela
        if jogador["rect"].left < 0:
            jogador["rect"].left = 0
        if jogador["rect"].right > LARGURA_TELA:
            jogador["rect"].right = LARGURA_TELA
        if jogador["rect"].top < 0:
            jogador["rect"].top = 0
        if jogador["rect"].bottom > ALTURA_TELA:
            jogador["rect"].bottom = ALTURA_TELA
        
        # Atualiza a posição de todos os projéteis ativos
        grupo_tiros.update() 

        # Verificação de colisão com a Gema
        if verificar_colisao(jogador["rect"], gema["rect"]):
            pontos = calcular_pontos(pontos, 10)
            gema["rect"].x += 80
            gema["rect"].y += 50
            if gema["rect"].x > LARGURA_TELA - gema["rect"].width: 
                gema["rect"].x = 50
            if gema["rect"].y > ALTURA_TELA - gema["rect"].height: 
                gema["rect"].y = 50

        # Verificação de colisão com o Inimigo
        if verificar_colisao(jogador["rect"], inimigo["rect"]):
            vidas = tomar_dano(vidas, 1)
            inimigo["rect"].x += 80
            inimigo["rect"].y += 50
            if inimigo["rect"].x > LARGURA_TELA - inimigo["rect"].width: 
                inimigo["rect"].x = 50
            if inimigo["rect"].y > ALTURA_TELA - inimigo["rect"].height: 
                inimigo["rect"].y = 50

        # Regras de fim de jogo e recorde
        if jogador_perdeu(vidas):
            rodando = False

        if pontos > recorde:
            recorde = pontos
            salvar_recorde(CAMINHO_RECORDE, recorde)

        pygame.display.set_caption(
            f"{TITULO_JOGO} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
        )

       
        # Desenha o fundo da galáxia cobrindo toda a tela
        tela.blit(imagem_fundo, (0, 0)) 
        
        # Desenha os personagens e objetos usando as chaves corretas do dicionário
        tela.blit(gema["imagem"], gema["rect"])
        tela.blit(inimigo["imagem"], inimigo["rect"])
        tela.blit(jogador["imagem"], jogador["rect"])
        
        # Desenha todos os tiros na tela de uma vez só
        grupo_tiros.draw(tela) 

        # Atualiza a tela com tudo o que foi desenhado neste frame
        pygame.display.flip()

    pygame.quit()