import pygame
import random
import sys
from src.sprites import Projetil, Chefe, Player, Inimigo, BarraDeVida

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CAMINHO_RECORDE,
    CAMINHO_FUNDO,
    CAMINHO_FUNDO_FINAL,
    CAMINHO_TIRO,
    BRANCO,
    SOM_MORTE,
    TIRO_SOM,
    EXPLOSAO_BOSS,
    EXPLOSAO_INIMIGO,
    THEME,
    THEME_BOSS,
    FONTE,
    DANO_TOMADO
    
)

TAMANHO = (LARGURA_TELA, ALTURA_TELA)

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    verificar_colisao,
    tomar_dano,
)
from src.dados import (
    salvar_recorde,
    carregar_recorde,
)



def executar_jogo():
    pygame.init()
    pygame.mixer.init()

    #cache para a musica nao travar
    pygame.mixer.set_num_channels(16)
    canal_musica = pygame.mixer.Channel(0)

    som_tema_normal = pygame.mixer.Sound(THEME)
    som_tema_boss = pygame.mixer.Sound(THEME_BOSS)

    som_tema_normal.set_volume(0.025)
    som_tema_boss.set_volume(0.5)

    # Configuracao das fontes
    fonte_grande = pygame.font.Font(FONTE, 42)
    fonte_pequena = pygame.font.Font(FONTE, 24)
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    
    relogio = pygame.time.Clock()

    imagem_original = pygame.image.load(CAMINHO_FUNDO).convert()
    imagem_fundo = pygame.transform.scale(imagem_original, (LARGURA_TELA, ALTURA_TELA))

    fundo_inicial = pygame.image.load(CAMINHO_FUNDO).convert()
    fundo_inicial = pygame.transform.scale(fundo_inicial, TAMANHO)

    fundo_final = pygame.image.load(CAMINHO_FUNDO_FINAL).convert()
    fundo_final = pygame.transform.scale(fundo_final, TAMANHO)

    while True:

        # CORREÇÃO: Passando os dois parâmetros de fonte que a função agora exige
        mostrar_tela_inicial(tela, fundo_inicial, fonte_grande, fonte_pequena)

        canal_musica.play(som_tema_normal, loops=-1, fade_ms=1000)
        
        frequencia_spawn_min = 30    
        frequencia_spawn_max = 90 
        frequencia_spawn = random.randint(frequencia_spawn_min, frequencia_spawn_max) 

        jogador = Player()
        barra_vida = BarraDeVida()

        chefe = None
        chefe_ativo = False 
        mensagem_chefe = False
        tempo_fim_aviso = 0
        
        grupo_tiros = pygame.sprite.Group()
        grupo_inimigos = pygame.sprite.Group()

        temporizador_spawn = 0
        pontos = 0
        vidas = 3
        recorde = carregar_recorde(CAMINHO_RECORDE)

        rodando_partida = True
        
        tempo_inicio_partida = pygame.time.get_ticks()
        
        proximo_spawn_chefe = 10000 # Primeiro spawn

        while rodando_partida:
            relogio.tick(FPS)
            
            temporizador = pygame.time.get_ticks() - tempo_inicio_partida

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if (evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE) or evento.type == pygame.MOUSEBUTTONDOWN:
                    
                    tiro_som = pygame.mixer.Sound(TIRO_SOM)
                    tiro_som.set_volume(0.04)
                    tiro_som.play(maxtime=2000)
                    tiro_som.play()
                    
                    novo_tiro = Projetil(jogador.rect.centerx, jogador.rect.top, CAMINHO_TIRO)
                    grupo_tiros.add(novo_tiro)

            jogador.update()

            if temporizador >= proximo_spawn_chefe and not chefe_ativo: 
                chefe = Chefe()
                chefe_ativo = True
                mensagem_chefe = True 
                tempo_fim_aviso = temporizador + 3000
                canal_musica.play(som_tema_boss, loops=-1, fade_ms=1000)
            
            if chefe is not None:
                chefe.update()
                
                if chefe.rect.top > ALTURA_TELA:
                    vidas = tomar_dano(vidas, 100)
                    chefe = None
                    chefe_ativo = False
                    proximo_spawn_chefe = temporizador + 30000 # tempo spawn boss
                    canal_musica.play(som_tema_normal, loops=-1, fade_ms=1000)

            temporizador_spawn += 1
            if temporizador_spawn >= frequencia_spawn:
                temporizador_spawn = 0
                novo_inimigo = Inimigo()
                novo_inimigo.rect.x = random.randint(0, LARGURA_TELA - novo_inimigo.rect.width)
                novo_inimigo.rect.y = -novo_inimigo.rect.height
                grupo_inimigos.add(novo_inimigo)

            grupo_inimigos.update()
            grupo_tiros.update()
            barra_vida.update(vidas)

            for ini in grupo_inimigos.sprites():
                if ini.rect.top > ALTURA_TELA:
                    vidas = tomar_dano(vidas, 2)
                    ini.kill()


            for tiro in grupo_tiros.sprites():
                for ini in grupo_inimigos.sprites():
                    if verificar_colisao(tiro.rect, ini.rect):
                        tiro.kill()
                        ini.vida -= tiro.dano
                        if ini.vida <= 0:
                            ini_morto_som = pygame.mixer.Sound(EXPLOSAO_INIMIGO)
                            ini_morto_som.set_volume(0.06)

                            ini_morto_som.play()
                            ini.kill()  
                            pontos = calcular_pontos(pontos, 10)
                        break
                
                if chefe is not None and verificar_colisao(tiro.rect, chefe.rect):
                    tiro.kill()
                    chefe.vida -= tiro.dano
                    if chefe.vida <= 0:
                        boss_morto_som = pygame.mixer.Sound(EXPLOSAO_BOSS)
                        boss_morto_som.set_volume(0.2)
                        boss_morto_som.play()
                        chefe = None
                        chefe_ativo = False
                        proximo_spawn_chefe = temporizador + 20000 # Tempo para o spawn do proximo boss
                        canal_musica.play(som_tema_normal, loops=-1, fade_ms=1000)

            for ini in grupo_inimigos.sprites():
                if verificar_colisao(jogador.rect, ini.rect):
                    vidas = tomar_dano(vidas, 1)
                    dano = pygame.mixer.Sound(DANO_TOMADO)
                    dano.play()
                    ini.kill()

            if chefe is not None and verificar_colisao(jogador.rect, chefe.rect):
                vidas = tomar_dano(vidas, 100)
                chefe = None
                chefe_ativo = False

            if jogador_perdeu(vidas):
                rodando_partida = False 
                canal_musica.fadeout(500)

            if pontos > recorde:
                recorde = pontos
                salvar_recorde(CAMINHO_RECORDE, recorde)

            pygame.display.set_caption(
                f"{TITULO_JOGO} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
            )

            tela.blit(imagem_fundo, (0, 0)) 
            
            grupo_inimigos.draw(tela)
            
            if chefe is not None:
                tela.blit(chefe.image, chefe.rect)

            tela.blit(jogador.image, jogador.rect)
            grupo_tiros.draw(tela) 
            tela.blit(barra_vida.image, barra_vida.rect)
            mostrar_pontos(tela, pontos, recorde, fonte_pequena)

            if mensagem_chefe:
                if temporizador < tempo_fim_aviso:
                    # Ajustado para usar a fonte_grande no aviso do Boss
                    texto_aviso = fonte_grande.render("o ImperIo contra ATACA", True, (255, 0, 0)) 
                    rect_aviso = texto_aviso.get_rect(center=(LARGURA_TELA // 2, (ALTURA_TELA // 2 - 150)))
                    tela.blit(texto_aviso, rect_aviso)
                else:
                    mensagem_chefe = False

            pygame.display.flip()

        # Ajustado para passar as duas fontes para a tela de game over também
        mostrar_tela_final(tela, fundo_final, fonte_grande, fonte_pequena)


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


def mostrar_tela_final(tela, fundo_final, fonte_grande, fonte_pequena):
    som_perdeu = pygame.mixer.Sound(SOM_MORTE)
    som_perdeu.play()
    
    # Atualizado para usar fonte_grande no título e fonte_pequena no subtítulo
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


def mostrar_pontos(tela, pontos, recorde, fonte):
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    texto_recorde = fonte.render(f"Recorde: {recorde}", True, (255, 255, 255))
    tela.blit(texto_pontos, (20, 20))
    tela.blit(texto_recorde, (20, 55))