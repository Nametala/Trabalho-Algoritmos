# Spaceshi.py

Integrantes do grupo

- Arthur Reis Nametala
- Gustavo Fernandes Vieira

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

O jogo consiste em uma nave que se move horizontalmente e atira. Objetivo do jogador é sobreviver o máximo de tempo possível enquanto desvia e destrói os asteróides no caminho.

## Objetivo do jogador

Desviar e destruir asteróides no caminho.

## Regras do jogo

- O jogador se movimenta usando A e D, e atira usando SPACEBAR
- A pontuação aumenta gradativamente em relação ao tempo
- Colidir com um obstáculo reduz a quantidade de vidas.
- A partida termina quando o jogador perde todas as vidas.

## Controles

- Tecla A: mover para esquerda
- Tecla D: mover para direita
- Espaço: Atirar
- ESC: Sair do jogo/Pause

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
