from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def calcular_metricas(sensores: pd.DataFrame, alertas: pd.DataFrame | None = None) -> dict:
    if sensores.empty:
        sensores = pd.DataFrame(
            [{"umidade": 35.0, "temperatura": 29.0, "consumo_agua": 1200.0, "status_irrigacao": "Adequada"}]
        )

    total_alertas = 0 if alertas is None or alertas.empty else len(alertas)
    status = sensores.iloc[-1].get("status_irrigacao", "Adequada")

    return {
        "umidade_media": round(float(sensores["umidade"].mean()), 2),
        "temperatura_media": round(float(sensores["temperatura"].mean()), 2),
        "consumo_agua": round(float(sensores["consumo_agua"].sum()), 2),
        "numero_alertas": int(total_alertas),
        "status_irrigacao": status,
    }


def grafico_umidade(sensores: pd.DataFrame):
    return px.line(
        sensores,
        x="timestamp",
        y="umidade",
        color="talhao",
        markers=True,
        title="Serie temporal de umidade por talhao",
    )


def grafico_temperatura(sensores: pd.DataFrame):
    return px.bar(
        sensores.tail(20),
        x="talhao",
        y="temperatura",
        color="cultura",
        title="Temperatura recente por talhao",
    )


def grafico_fluxo_integracao():
    etapas = ["Sensor", "Banco de Dados", "IA", "Dashboard", "Alerta", "Recomendacao"]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(len(etapas))),
            y=[1] * len(etapas),
            mode="markers+text+lines",
            text=etapas,
            textposition="top center",
            marker=dict(size=22, color=["#2E7D32", "#1565C0", "#6A1B9A", "#00838F", "#C62828", "#EF6C00"]),
            line=dict(width=3, color="#455A64"),
        )
    )
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)
    fig.update_layout(title="Fluxo final da solucao FarmTech", height=320, margin=dict(l=20, r=20, t=60, b=20))
    return fig

