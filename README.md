# Previsão de lotação da academia com LSTM

Previsão da lotação de uma academia universitária na próxima hora com uma rede LSTM, a partir do dataset [Crowdedness at the Campus Gym](https://www.kaggle.com/datasets/nsrose7224/crowdedness-at-the-campus-gym). O trabalho compara três configurações de histórico (janelas contínuas de 24h e de 168h e uma janela dilatada) e avalia a melhor delas contra a persistência e contra referências sazonais.

## Notebook final

[`notebooks/02_previsao_lotacao_lstm.ipynb`](notebooks/02_previsao_lotacao_lstm.ipynb) é a entrega. Ele segue o pipeline da lauda: preparação dos dados, análise exploratória, janelas, referências, treino, escolha da janela, avaliação no teste e conclusão.

## Como executar no Google Colab

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GabrielcMiranda/gym-crowndedness-forecasting/blob/main/notebooks/02_previsao_lotacao_lstm.ipynb)

1. Em *Ambiente de execução > Alterar o tipo de ambiente de execução*, escolha uma GPU.
2. Use *Ambiente de execução > Executar tudo*.

O notebook baixa e valida o dataset sozinho, sem credenciais do Kaggle, e todas as bibliotecas que ele usa já vêm no Colab. O treino das três configurações leva poucos minutos em uma GPU T4. Uma nova execução pode alterar levemente os valores do treino.

## Como executar localmente

Requisito: [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python scripts/ingest_dataset.py
uv run jupyter lab notebooks/02_previsao_lotacao_lstm.ipynb
```

O script de ingestão baixa o dataset público, confere a integridade do arquivo e o salva em `data/raw/data.csv`.

Sem GPU, o treino completo fica muito lento. Para uma verificação rápida, defina `FAST_RUN=1` antes de abrir o notebook. Com isso o treino usa 1 semente e no máximo 2 épocas, e os resultados não valem para a entrega.

## Verificação do notebook

```bash
uv run python scripts/check_notebook.py notebooks/02_previsao_lotacao_lstm.ipynb
```

O verificador falha se houver comentário ou docstring no código, célula não executada, célula com erro, marcador pendente ou problema de limpeza fora do padrão de título, código que revela o problema e código que o corrige.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `notebooks/02_previsao_lotacao_lstm.ipynb` | Notebook final entregue |
| `notebooks/03_experimentos_lstm.ipynb` | Experimentos que definiram os hiperparâmetros, as entradas e as sementes, no recorte final do treino |
| `notebooks/01_validacao_dataset.ipynb` | Validação inicial do dataset, anterior à correção do preenchimento e das horas com poucas leituras |
| `scripts/ingest_dataset.py` | Download e validação do dataset |
| `scripts/check_notebook.py` | Verificador de qualidade dos notebooks |
