import pygame
import random
import sys # Importado para garantir a saída limpa do sistema
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
    CAMINHO_FUNDO_FINAL,
    CAMINHO_NAVE,
    CAMINHO_TIRO,
    CAMINHO_INIMIGO,
    BRANCO,
    PRETO,
    CAMINHO_VIDA_CHEIA,
    CAMINHO_23_VIDA,
    CAMINHO_13_VIDA,
    CAMINHO_VIDA_VAZIA
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

    # LOOP PRINCIPAL DA SESSÃO (Permite reiniciar o jogo voltando para a tela inicial)
    while True:
        
        # Chama a tela inicial. Se sair dela, o jogo começa.
        mostrar_tela_inicial(tela, fundo_inicial)

        # CONFIGURAÇÕES DA PARTIDA (Resetadas toda vez que o jogo recomeça)
        VIDA_INIMIGO_PADRAO = 2  
        DANO_TIRO = 1            
        
        velocidade_inimigo = 2   
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

        imagem_barra_vida_original = pygame.image.load(CAMINHO_VIDA_CHEIA).convert_alpha()
        escala_barra_vida = 5 
        largura_barra_vida = int(imagem_barra_vida_original.get_width() * escala_barra_vida)
        altura_barra_vida = int(imagem_barra_vida_original.get_height() * escala_barra_vida)
        barra_vida_image = pygame.transform.scale(imagem_barra_vida_original, (largura_barra_vida, altura_barra_vida))
        barra_vida_image = barra_vida_image.convert_alpha()



        imagem_inimigo_original = pygame.image.load(CAMINHO_INIMIGO).convert_alpha()
        escala_inimigo = 2
        largura_inimigo = int(imagem_inimigo_original.get_width() * escala_inimigo)
        altura_inimigo = int(imagem_inimigo_original.get_height() * escala_inimigo)
        enemy_image = pygame.transform.scale(imagem_inimigo_original, (largura_inimigo, altura_inimigo))
        
        posicao_inicial_x = (LARGURA_TELA // 2) - (largura_nave // 2)
        posicao_inicial_y = ALTURA_TELA - altura_nave - 20

        posicao_barra_vida_x = posicao_inicial_x
        posicao_barra_vida_y = (posicao_inicial_y - 40)

        jogador = {
            "imagem": player_image,
            "rect": player_image.get_rect(topleft=(posicao_inicial_x, posicao_inicial_y))
        }

        grupo_tiros = pygame.sprite.Group()
        lista_inimigos = []

        temporizador_spawn = 0
        pontos = 0
        vidas = 3   
        recorde = carregar_recorde(CAMINHO_RECORDE)

        rodando_partida = True

        # LOOP DE GAMEPLAY (A partida em si)
        while rodando_partida:
            relogio.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                    

                # Disparar tiro
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    novo_tiro = Projetil(jogador["rect"].centerx, player_image.get_rect(topleft=(jogador["rect"].x, jogador["rect"].y)).top, CAMINHO_TIRO)
                    grupo_tiros.add(novo_tiro)
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    novo_tiro = Projetil(jogador["rect"].centerx, player_image.get_rect(topleft=(jogador["rect"].x, jogador["rect"].y)).top, CAMINHO_TIRO)
                    grupo_tiros.add(novo_tiro)

            # Movimentação W A S D
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a]:
                jogador["rect"].x -= velocidade
            if teclas[pygame.K_d]:
                jogador["rect"].x += velocidade
            if teclas[pygame.K_w]:
                jogador["rect"].y -= velocidade
            if teclas[pygame.K_s]:
                jogador["rect"].y += velocidade

            # Bordas da tela
            if jogador["rect"].left < 0: jogador["rect"].left = 0
            if jogador["rect"].right > LARGURA_TELA: jogador["rect"].right = LARGURA_TELA
            if jogador["rect"].top < 0: jogador["rect"].top = 0
            if jogador["rect"].bottom > ALTURA_TELA: jogador["rect"].bottom = ALTURA_TELA

            # Spawn de inimigos
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

            # Movimento dos inimigos
            for ini in lista_inimigos[:]:
                ini["rect"].y += velocidade_inimigo
                if ini["rect"].top > ALTURA_TELA:
                    vidas = tomar_dano(vidas, 100) # Inimigo passou causa game over imediato
                    lista_inimigos.remove(ini)

            grupo_tiros.update() 

            # Colisão: Projéteis vs Inimigos
            for tiro in grupo_tiros.sprites():
                for ini in lista_inimigos[:]:
                    if verificar_colisao(tiro.rect, ini["rect"]):
                        tiro.kill()
                        ini["vida"] -= DANO_TIRO
                        if ini["vida"] <= 0:
                            lista_inimigos.remove(ini)  
                            pontos = calcular_pontos(pontos, 10)
                        break

            # Colisão: Inimigos vs Jogador
            for ini in lista_inimigos[:]:
                if verificar_colisao(jogador["rect"], ini["rect"]):
                    vidas = tomar_dano(vidas, 1)
                    lista_inimigos.remove(ini)  

            # CORREÇÃO: Condições de Fim de Jogo 
            if jogador_perdeu(vidas):
                rodando_partida = False # Quebra o loop da gameplay e vai para a Tela Final

            if pontos > recorde:
                recorde = pontos
                salvar_recorde(CAMINHO_RECORDE, recorde)

            pygame.display.set_caption(
                f"{TITULO_JOGO} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
            )

            # Renderização
            tela.blit(imagem_fundo, (0, 0)) 
            for ini in lista_inimigos:
                tela.blit(enemy_image, ini["rect"])
            tela.blit(jogador["imagem"], jogador["rect"])
            grupo_tiros.draw(tela) 
            mostrar_pontos(tela,pontos,recorde)
            pygame.display.flip()

        # Se saiu do loop 'rodando_partida', significa que o jogador morreu!
        # Chamamos a tela final antes de reiniciar o loop principal.
        mostrar_pontos(tela,pontos,recorde)
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
                esperando = False # Sai da tela final e o loop principal 'while True' reinicia tudo
        
        tela.blit(fundo_final, (0, 0))
        tela.blit(texto_titulo, retangulo_titulo)
        tela.blit(texto_subtitulo, retangulo_subtitulo)
        pygame.display.flip()

def mostrar_pontos(tela,pontos, recorde):
    fonte_pontos = pygame.font.Font(None, 74)
    texto_pontos = fonte_pontos.render(f"Força: {pontos}", True, BRANCO)

    fonte_recorde = pygame.font.Font(None, 74)
    texto_recorde = fonte_recorde.render(f"Record: {recorde}", True, BRANCO)

    
    tela.blit(texto_pontos, (10,10))
    tela.blit(texto_recorde,(10,40))





