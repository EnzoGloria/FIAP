from __future__ import annotations

from random import choice, uniform


def analisar_imagem_lavoura(imagem_nome: str = "amostra_lavoura.jpg") -> dict:
    classe = choice(["Saudavel", "Deficiencia hidrica", "Possivel praga", "Baixo vigor"])
    recomendacoes = {
        "Saudavel": "Manter monitoramento preventivo.",
        "Deficiencia hidrica": "Aumentar prioridade de irrigacao.",
        "Possivel praga": "Realizar vistoria e avaliar manejo integrado.",
        "Baixo vigor": "Verificar nutricao, solo e compactacao.",
    }
    return {
        "imagem": imagem_nome,
        "classe": classe,
        "confianca": round(uniform(0.74, 0.97), 2),
        "recomendacao": recomendacoes[classe],
        "servico_aws_futuro": "Amazon Rekognition ou SageMaker endpoint",
    }

