from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATABASE_DIR = ROOT_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "farmtech.db"


def conectar(caminho: Path = DATABASE_PATH) -> sqlite3.Connection:
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(caminho)


def criar_banco(caminho: Path = DATABASE_PATH) -> None:
    with conectar(caminho) as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS sensores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                talhao TEXT NOT NULL,
                cultura TEXT NOT NULL,
                umidade REAL NOT NULL,
                temperatura REAL NOT NULL,
                consumo_agua REAL NOT NULL,
                luminosidade REAL NOT NULL,
                status_irrigacao TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origem TEXT NOT NULL,
                severidade TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )


def inserir_leitura(leitura: dict, caminho: Path = DATABASE_PATH) -> None:
    criar_banco(caminho)
    with conectar(caminho) as conexao:
        conexao.execute(
            """
            INSERT INTO sensores (
                sensor_id, talhao, cultura, umidade, temperatura, consumo_agua,
                luminosidade, status_irrigacao, timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                leitura["sensor_id"],
                leitura["talhao"],
                leitura["cultura"],
                leitura["umidade"],
                leitura["temperatura"],
                leitura["consumo_agua"],
                leitura["luminosidade"],
                leitura["status_irrigacao"],
                leitura["timestamp"],
            ),
        )


def inserir_alerta(alerta: dict, caminho: Path = DATABASE_PATH) -> None:
    criar_banco(caminho)
    with conectar(caminho) as conexao:
        conexao.execute(
            "INSERT INTO alertas (origem, severidade, mensagem, timestamp) VALUES (?, ?, ?, ?)",
            (alerta["origem"], alerta["severidade"], alerta["mensagem"], alerta["timestamp"]),
        )


def consultar_sensores(caminho: Path = DATABASE_PATH) -> pd.DataFrame:
    criar_banco(caminho)
    with conectar(caminho) as conexao:
        return pd.read_sql_query("SELECT * FROM sensores ORDER BY id DESC", conexao)


def consultar_alertas(caminho: Path = DATABASE_PATH) -> pd.DataFrame:
    criar_banco(caminho)
    with conectar(caminho) as conexao:
        return pd.read_sql_query("SELECT * FROM alertas ORDER BY id DESC", conexao)

