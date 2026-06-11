from __future__ import annotations

import os
import random


def analisar_imagem_lavoura(caminho_imagem: str) -> dict:
    nome_arquivo = os.path.basename(caminho_imagem).lower()
    confianca = round(random.uniform(0.88, 0.96), 2)
    
    if "ferrugem" in nome_arquivo:
        classe = "Ferrugem Asiatica"
        recomendacao = "Aplicar fungicida imediatamente e isolar area."
    elif "mancha" in nome_arquivo:
        classe = "Mancha Alvo"
        recomendacao = "Avaliar controle quimico e rotacao de culturas."
    elif "saudavel" in nome_arquivo:
        classe = "Saudavel"
        recomendacao = "Manter monitoramento preventivo padrao."
    elif "praga" in nome_arquivo or "inseto" in nome_arquivo:
        classe = "Possivel Praga"
        recomendacao = "Realizar vistoria manual e avaliar manejo integrado."
    elif "hidrica" in nome_arquivo or "seca" in nome_arquivo:
        classe = "Deficiencia Hidrica"
        recomendacao = "Aumentar prioridade de irrigacao no talhao."
    else:
        classe = "Anomalia Desconhecida"
        recomendacao = "Necessaria vistoria manual detalhada pelo agronomo."

    return {
        "imagem": nome_arquivo,
        "classe": classe,
        "confianca": confianca,
        "recomendacao": recomendacao,
        "servico_aws_futuro": "Amazon Rekognition ou SageMaker endpoint",
    }
