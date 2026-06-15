# Testes

* Colisão da Nave com asteróide
* Colisão do projétil com o asteróide
* Perda de vida
* Pontuação aumentando corretamente
* Movimentação multidirecional

## Arquivos

- `test_logica.py`: valida funcoes puras de logica em `src/funcoes.py`.

## Como executar

```bash
python -m pytest
```

## Boas praticas

- Crie testes para toda regra de pontuacao, vidas e condicoes de fim de jogo.
- Prefira funcoes pequenas e testaveis no modulo `src/funcoes.py`.
