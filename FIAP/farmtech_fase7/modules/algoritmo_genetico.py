from __future__ import annotations

from random import randint, sample


def avaliar_irrigacao(volume_litros: int, umidade_atual: float, temperatura: float) -> float:
    alvo = 38
    ganho_umidade = volume_litros / 120
    penalidade_excesso = max(0, volume_litros - 2200) * 0.015
    penalidade_calor = max(0, temperatura - 32) * 0.8
    umidade_estimativa = umidade_atual + ganho_umidade - penalidade_calor
    return abs(alvo - umidade_estimativa) + penalidade_excesso


def otimizar_irrigacao(umidade_atual: float, temperatura: float, geracoes: int = 18, tamanho_populacao: int = 16) -> dict:
    """Algoritmo genetico simples para sugerir volume de irrigacao em litros."""
    populacao = [randint(600, 2600) for _ in range(tamanho_populacao)]
    historico = []

    for geracao in range(1, geracoes + 1):
        ranqueados = sorted(
            [(avaliar_irrigacao(volume, umidade_atual, temperatura), volume) for volume in populacao],
            key=lambda item: item[0],
        )
        melhor_score, melhor_volume = ranqueados[0]
        historico.append({"geracao": geracao, "volume": melhor_volume, "score": round(melhor_score, 3)})

        elite = [volume for _, volume in ranqueados[:4]]
        nova_populacao = elite.copy()
        while len(nova_populacao) < tamanho_populacao:
            pai, mae = sample(elite, 2)
            filho = int((pai + mae) / 2) + randint(-120, 120)
            nova_populacao.append(max(400, min(3000, filho)))
        populacao = nova_populacao

    return {
        "melhor_volume_litros": historico[-1]["volume"],
        "score": historico[-1]["score"],
        "historico": historico,
        "recomendacao": "Aplicar volume otimizado e reavaliar sensores apos o ciclo de irrigacao.",
    }

