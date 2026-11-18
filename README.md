# Previsão de lotação da academia com LSTM

Previsão da próxima observação da lotação de uma academia universitária com uma rede LSTM, a partir do dataset [Crowdedness at the Campus Gym](https://www.kaggle.com/datasets/nsrose7224/crowdedness-at-the-campus-gym).

## Como executar localmente

Requisito: [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python scripts/ingest_dataset.py
uv run jupyter lab notebooks/01_validacao_dataset.ipynb
```

O script de ingestão não precisa de credenciais do Kaggle. Ele baixa o dataset público, confere a integridade do arquivo e o salva em `data/raw/data.csv`.

## Como executar no Google Colab

Abra `notebooks/01_validacao_dataset.ipynb` no Colab e execute todas as células. O notebook baixa e valida o dataset sozinho.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `scripts/ingest_dataset.py` | Download e validação do dataset |
| `notebooks/01_validacao_dataset.ipynb` | Validação do dataset, análise exploratória e treino básico da LSTM |
