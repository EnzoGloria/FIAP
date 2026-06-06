from __future__ import annotations

import pandas as pd


def prever_umidade_futura(serie_umidade: list[float] | pd.Series, passos: int = 12) -> pd.DataFrame:
    """Simula uma previsao temporal inspirada em RNN/LSTM sem exigir treino pesado local."""
    valores = pd.Series(serie_umidade, dtype="float64").dropna()
    if valores.empty:
        valores = pd.Series([35.0, 34.2, 33.7, 32.9], dtype="float64")

    tendencia = valores.tail(8).diff().mean()
    if pd.isna(tendencia):
        tendencia = -0.25

    ultima = float(valores.iloc[-1])
    previsoes = []
    for passo in range(1, passos + 1):
        ajuste_sazonal = 0.8 if passo % 6 == 0 else 0
        prevista = max(18, min(55, ultima + tendencia * passo + ajuste_sazonal))
        previsoes.append({"periodo": f"+{passo}h", "umidade_prevista": round(prevista, 2)})

    return pd.DataFrame(previsoes)


def classificar_risco_umidade(umidade_prevista: float) -> str:
    if umidade_prevista < 28:
        return "Alto"
    if umidade_prevista < 34:
        return "Medio"
    return "Baixo"

