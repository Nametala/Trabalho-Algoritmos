# Proposta Inicial do Jogo

Jogo estilo Nave destruindo e desviando de naves inimigas.

## 1. Nome provisório do jogo

Spaceshi.py

## 2. Integrantes do grupo

- Arthur Reis Nametala
- Gustavo Fernandes Vieira

## 3. Tipo de jogo

Jogo estilo Nave destruindo e desviando de naves inimigos e chefe.

## 4. Descrição geral do jogo

Nave controlada pelo jogador que dispara contra asteróides enquanto tenta evitá-los. O jogadore deve mover a nave horizontalmente para desviar dos obstáculos enquanto a nave causa dano para destruí-los.

## 5. Objetivo do jogador

Sobreviver o máximo de tempo possível enquanto desvia de asteróides.

## 6. Regras principais

O jogador terá apenas 3 de vida, e ao tocar qualquer inimigo, a nave será danificada e o jogador perde vidas. A pontuação será baseada no tempo sobrevivido, ficando mais difícil a cada segundo e portanto aumentando sua pontuação progressivamente.

- Regra 1: Apenas 3 de vida
- Regra 2: A nave pode destruir asteróides com projéteis
- Regra 3: A pontuação escala progressivamente com o tempo sobrevivido
- Regra 4: Se um inimigo alcançar o final o dano é dobrado
- Regra 5: Contato direto com o chefe, ou caso ele alcance o fim, é fim de jogo

## 7. Condição de vitória

O objetivo é se superar a cada tentativa, buscando maiores pontuações a cada vez.

## 8. Condição de derrota ou encerramento

O jogador perde ao ter contato com qualquer inimigo durante o jogo ou ao deixar algum inimigo alcançar o fim da tela. Quando o jogador nao tiver mais vidas restantes, é fim de jogo.

## 9. Elementos previstos no jogo

* Nave
* Inimigo
* Chefe
* Projétil
* Background
* Pontuação

## Jogador ou elemento principal

Nave

## Obstáculos, inimigos ou desafios

Naves inimigas e nave chefe

## Itens, alvos ou objetos de interação

Projétil

## Pontuação, vidas, tempo ou progresso

Vida e pontuações.

## 10. Controles previstos

- Tecla A: mover para esquerda
- Tecla D: mover para direita
- Espaço/Botão direito do mouse: Atirar
- ESC: Sair do jogo/Pause

## 11. Organização inicial do código

- `main.py`: inicia o jogo;
- `src/jogo.py`: contém o loop principal;
- `src/config.py`: guarda configurações como tamanho da tela e cores;
- `src/funcoes.py`: contém funções auxiliares;
- `src/dados.py`: contém funções de leitura e escrita de arquivos.

## 12. Recursos externos previstos

* Fontes Personalizadas
* Tutoriais
* Sons
* Imagens
* Sprites.

## 13. Principais dificuldades esperadas

- movimentação do jogador;
- colisão entre objetos;
- controle de tempo;
- criação da pontuação;
- organização do código;
- uso do GitHub;
- testes;
- exibição de textos na tela.
- manipulação de sprites;
- aumento de dificuldade progressivo;

## 14. Escopo mínimo para a entrega final

Nave com movimentação multidirecional que pode desviar de inimigos com colisão própria e um sistema de pontuação simples.

## 15. Possíveis melhorias, caso haja tempo

- tela inicial;
- sons;
- aumento de dificuldade;
- ranking;
- animações simples;
- melhorias da nave (dano, vida, etc);
- personalização da nave (estético);
- menu de pausa.
