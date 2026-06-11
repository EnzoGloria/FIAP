from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
SCRIPTS_DIR = ROOT_DIR / "scripts"


def gerar_dados_clima_fallback() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    dias = pd.date_range(start="2025-01-01", end="2026-06-01")
    n = len(dias)
    np.random.seed(42)
    temperatura = 25 + 5 * np.sin(np.arange(n) * 2 * np.pi / 365) + np.random.normal(0, 2, n)
    umidade = 70 + 15 * np.cos(np.arange(n) * 2 * np.pi / 365) + np.random.normal(0, 5, n)
    precipitacao = np.random.exponential(1 / 0.2, n) * (umidade > 70)
    
    df_clima = pd.DataFrame({"data": dias, "temperatura": temperatura, "umidade": umidade, "precipitacao": precipitacao})
    df_clima.to_csv(DATA_DIR / "clima_historico.csv", index=False)
    
    matriz_cor = df_clima[["temperatura", "umidade", "precipitacao"]].corr()
    matriz_cor.to_csv(DATA_DIR / "clima_correlacao.csv", index=True)


def executar_scripts_r() -> tuple[pd.DataFrame, pd.DataFrame]:
    try:
        subprocess.run(["Rscript", str(SCRIPTS_DIR / "clima.R")], check=True, cwd=str(ROOT_DIR), capture_output=True)
        subprocess.run(["Rscript", str(SCRIPTS_DIR / "analise.R")], check=True, cwd=str(ROOT_DIR), capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        gerar_dados_clima_fallback()

    df_clima = pd.read_csv(DATA_DIR / "clima_historico.csv")
    df_clima["data"] = pd.to_datetime(df_clima["data"])
    df_correlacao = pd.read_csv(DATA_DIR / "clima_correlacao.csv", index_col=0)
    
    return df_clima, df_correlacao
