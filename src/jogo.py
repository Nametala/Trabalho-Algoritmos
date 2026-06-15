import pygame
import random
import sys
from src.sprites import Projetil, Chefe # <--- Sua classe original mantida aqui!

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
    CAMINHO_FUNDO,
    CAMINHO_FUNDO_FINAL,
    CAMINHO_NAVE,
    CAMINHO_TIRO,
    CAMINHO_INIMIGO,    
    BRANCO,
    PRETO,
    CAMINHO_VIDA_CHEIA,
    CAMINHO_23_VIDA,
    CAMINHO_13_VIDA,
    CAMINHO_VIDA_VAZIA, 
    CAMINHO_CHEFE
)

TAMANHO = (LARGURA_TELA, ALTURA_TELA)

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

    # Carrega as imagens de fundo uma única vez para poupar memória
    imagem_original = pygame.image.load(CAMINHO_FUNDO).convert()
    imagem_fundo = pygame.transform.scale(imagem_original, (LARGURA_TELA, ALTURA_TELA))

    fundo_inicial = pygame.image.load(CAMINHO_FUNDO).convert()
    fundo_inicial = pygame.transform.scale(fundo_inicial, TAMANHO)

    fundo_final = pygame.image.load(CAMINHO_FUNDO_FINAL).convert()
    fundo_final = pygame.transform.scale(fundo_final, TAMANHO)

    # LOOP PRINCIPAL DO SISTEMA 
    while True:
        
        # Tela inicial
        mostrar_tela_inicial(tela, fundo_inicial)

        # CONFIGURAÇÕES DA PARTIDA 

        # Status dos Inimigos Comuns
        VIDA_INIMIGO_PADRAO = 2  
        velocidade_inimigo = 1  

        # Status do Chefe 
        VIDA_CHEFE_PADRAO = 25
        velocidade_chefe = 1
        tempo_spawn_chefe = 40000 # Tempo de espera spawn chefe
        
        # Outras configurações
        DANO_TIRO = 1            
        velocidade = 5           
        frequencia_spawn_min = 30    
        frequencia_spawn_max = 90 
        frequencia_spawn = random.randint(frequencia_spawn_min, frequencia_spawn_max) 

        # Carregar Personagens
        imagem_nave_original = pygame.image.load(CAMINHO_NAVE).convert_alpha()
        escala_nave = 2 
        largura_nave = int(imagem_nave_original.get_width() * escala_nave)
        altura_nave = int(imagem_nave_original.get_height() * escala_nave)
        player_image = pygame.transform.scale(imagem_nave_original, (largura_nave, altura_nave))
        player_image.set_colorkey((0, 0, 0))
        player_image = player_image.convert_alpha()

        imagem_inimigo_original = pygame.image.load(CAMINHO_INIMIGO).convert_alpha()
        escala_inimigo = 2
        largura_inimigo = int(imagem_inimigo_original.get_width() * escala_inimigo)
        altura_inimigo = int(imagem_inimigo_original.get_height() * escala_inimigo)
        enemy_image = pygame.transform.scale(imagem_inimigo_original, (largura_inimigo, altura_inimigo))
        
        posicao_inicial_x = (LARGURA_TELA // 2) - (largura_nave // 2)
        posicao_inicial_y = ALTURA_TELA - altura_nave - 20

        jogador = {
            "imagem": player_image,
            "rect": player_image.get_rect(topleft=(posicao_inicial_x, posicao_inicial_y))                  
        }

        # Inicialização chefe 
        chefe = None
        chefe_ativo = False 
        mensagem_chefe = False
        tempo_fim_aviso = 0
        # SISTEMA BARRA DE VIDA 
        escala_barra_vida = 5
        vidas = 3   # Quantidade vidas jogador

        def barra_de_vida(caminho):
            img = pygame.image.load(caminho).convert_alpha()
            larg = int(img.get_width() * escala_barra_vida)
            alt = int(img.get_height() * escala_barra_vida)
            return pygame.transform.scale(img, (larg, alt))

        # Variações da barra de vida
        sprites_vida = {
            3: barra_de_vida(CAMINHO_VIDA_CHEIA),
            2: barra_de_vida(CAMINHO_23_VIDA),
            1: barra_de_vida(CAMINHO_13_VIDA),
            0: barra_de_vida(CAMINHO_VIDA_VAZIA)
        }

        posicao_barra_vida_x = 20  
        posicao_barra_vida_y = 330

        barra_vida = {
            "imagem": sprites_vida[3], 
            "rect": sprites_vida[3].get_rect(topleft=(posicao_barra_vida_x, posicao_barra_vida_y))
        }

        grupo_tiros = pygame.sprite.Group()
        lista_inimigos = []

        temporizador_spawn = 0
        pontos = 0
        recorde = carregar_recorde(CAMINHO_RECORDE)

        rodando_partida = True
        
        # Desconta tempo em menus
        tempo_inicio_partida = pygame.time.get_ticks()

        # LOOP DE GAMEPLAY 
        while rodando_partida:
            relogio.tick(FPS)
            
            # Temporizador
            temporizador = pygame.time.get_ticks() - tempo_inicio_partida

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Disparar tiro
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    novo_tiro = Projetil(jogador["rect"].centerx, jogador["rect"].top, CAMINHO_TIRO)
                    grupo_tiros.add(novo_tiro)
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    novo_tiro = Projetil(jogador["rect"].centerx, jogador["rect"].top, CAMINHO_TIRO)
                    grupo_tiros.add(novo_tiro)

            # W A S D
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a]: jogador["rect"].x -= velocidade
            if teclas[pygame.K_d]: jogador["rect"].x += velocidade
            if teclas[pygame.K_w]: jogador["rect"].y -= velocidade
            if teclas[pygame.K_s]: jogador["rect"].y += velocidade

            # Bordas da tela
            if jogador["rect"].left < 0: jogador["rect"].left = 0
            if jogador["rect"].right > LARGURA_TELA: jogador["rect"].right = LARGURA_TELA
            if jogador["rect"].top < 0: jogador["rect"].top = 0
            if jogador["rect"].bottom > ALTURA_TELA: jogador["rect"].bottom = ALTURA_TELA

            # Spawn do chefe
            if temporizador >= tempo_spawn_chefe and not chefe_ativo:
                chefe = Chefe()
                chefe.vida = VIDA_CHEFE_PADRAO # Aplica a vida configurada acima
                # Garante que ele nasça centralizado no topo da tela para entrar deslizando
                chefe.rect.centerx = LARGURA_TELA // 2
                chefe.rect.bottom = 0 
                chefe_ativo = True
                # Mensagem chefe

                mensagem_chefe = True 
                tempo_fim_aviso = temporizador + 3000
            
            if chefe is not None:
                # Move o chefe para baixo usando a velocidade configurada acima
                chefe.rect.y += velocidade_chefe
                chefe.update()
                
                # Chefe chega ao fim da tela
                if chefe.rect.top > ALTURA_TELA:
                    vidas = tomar_dano(vidas, 100)
                    chefe = None

            # Spawn de inimigos comuns
            temporizador_spawn += 1
            if temporizador_spawn >= frequencia_spawn:
                temporizador_spawn = 0
                x_spawn = random.randint(0, LARGURA_TELA - largura_inimigo)
                y_spawn = -altura_inimigo
                novo_inimigo = {
                    "rect": enemy_image.get_rect(topleft=(x_spawn, y_spawn)),
                    "vida": VIDA_INIMIGO_PADRAO  
                }
                lista_inimigos.append(novo_inimigo)

            # Movimento dos inimigos comuns
            for ini in lista_inimigos[:]:
                ini["rect"].y += velocidade_inimigo
                # Inimigo chegar ao fim da tela
                if ini["rect"].top > ALTURA_TELA:
                    vidas = tomar_dano(vidas, 2) 
                    lista_inimigos.remove(ini)

            # Chefe chegar ao fim da tela
            if chefe is not None:
                if chefe.rect.bottom >= ALTURA_TELA:
                    vidas = tomar_dano(vidas, 100) 
                    chefe = None

            grupo_tiros.update() 

            # Colisão: Projéteis com Inimigos e Chefe
            for tiro in grupo_tiros.sprites():
                # Contra inimigos 
                for ini in lista_inimigos[:]:
                    if verificar_colisao(tiro.rect, ini["rect"]):
                        tiro.kill()
                        ini["vida"] -= DANO_TIRO
                        if ini["vida"] <= 0:
                            lista_inimigos.remove(ini)  
                            pontos = calcular_pontos(pontos, 10)
                        break
                # Contra Chefe
                if chefe is not None and verificar_colisao(tiro.rect, chefe.rect):
                    tiro.kill()
                    chefe.vida -= DANO_TIRO
                    if chefe.vida <= 0:
                        chefe = None
                        pontos = calcular_pontos(pontos, 1000) 

            # Colisão com Inimigos
            for ini in lista_inimigos[:]:
                if verificar_colisao(jogador["rect"], ini["rect"]):
                    vidas = tomar_dano(vidas, 1)
                    lista_inimigos.remove(ini)

            # Colisão com Chefe
            if chefe is not None and verificar_colisao(jogador["rect"], chefe.rect):
                vidas = tomar_dano(vidas, 100)
                chefe = None

            # Atualiza interface de vida
            vidas_checadas = max(0, min(vidas, 3))
            barra_vida["imagem"] = sprites_vida[vidas_checadas]

            # Condições de Fim de Jogo 
            if jogador_perdeu(vidas):
                rodando_partida = False 

            if pontos > recorde:
                recorde = pontos
                salvar_recorde(CAMINHO_RECORDE, recorde)

            pygame.display.set_caption(
                f"{TITULO_JOGO} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
            )

            # RENDERIZAÇÃO
            tela.blit(imagem_fundo, (0, 0)) 
            
            # Desenha inimigos comuns
            for ini in lista_inimigos:
                tela.blit(enemy_image, ini["rect"])
            
            # Desenha o Chefe se ele estiver vivo
            if chefe is not None:
                tela.blit(chefe.image, chefe.rect)

            tela.blit(jogador["imagem"], jogador["rect"])
            grupo_tiros.draw(tela) 
            tela.blit(barra_vida["imagem"], barra_vida["rect"])
            mostrar_pontos(tela, pontos, recorde)

            # Desenhar aviso chefe
            if mensagem_chefe:
                if temporizador < tempo_fim_aviso:
                    fonte_aviso = pygame.font.Font(None, 60) 
                    texto_aviso = fonte_aviso.render("O IMPÉRIO CONTRA-ATACA!", True, (255, 0, 0)) 
                    rect_aviso = texto_aviso.get_rect(center=(LARGURA_TELA // 2, (ALTURA_TELA // 2 - 150)))
                    tela.blit(texto_aviso, rect_aviso)
                else:
                    mensagem_chefe = False # Sumir depois de 3 segundos

            pygame.display.flip()

        # Tela final após morte
        mostrar_tela_final(tela, fundo_final)


def mostrar_tela_inicial(tela, fundo_inicial):
    fonte_titulo = pygame.font.Font(None, 74)
    texto_titulo = fonte_titulo.render(TITULO_JOGO, True, BRANCO)

    fonte_subtitulo = pygame.font.Font(None, 36)
    texto_subtitulo = fonte_subtitulo.render("PRESSIONE ESPAÇO PARA INICIAR", True, BRANCO)
    
    retangulo_titulo = texto_titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 40))
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


def mostrar_tela_final(tela, fundo_final):
    fonte_titulo = pygame.font.Font(None, 74)
    texto_titulo = fonte_titulo.render("O IMPÉRIO VENCEU", True, BRANCO)

    fonte_subtitulo = pygame.font.Font(None, 36)
    texto_subtitulo = fonte_subtitulo.render("PRESSIONE ESPAÇO PARA VOLTAR PARA O INÍCIO", True, BRANCO)
    
    retangulo_titulo = texto_titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 210))
    retangulo_subtitulo = texto_subtitulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 160))
    
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


def mostrar_pontos(tela, pontos, recorde):
    fonte_hud = pygame.font.Font(None, 36)
    texto_pontos = fonte_hud.render(f"Pontos: {pontos}", True, BRANCO)
    texto_recorde = fonte_hud.render(f"Recorde: {recorde}", True, BRANCO)
    tela.blit(texto_pontos, (20, 20))
    tela.blit(texto_recorde, (20, 55))