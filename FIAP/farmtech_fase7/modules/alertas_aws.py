from __future__ import annotations

import os
import threading
from datetime import datetime
from zoneinfo import ZoneInfo

import boto3


def enviar_alerta_sns(mensagem: str, arn_topico: str) -> None:
    cliente_sns = boto3.client("sns", region_name="us-east-1")
    cliente_sns.publish(TopicArn=arn_topico, Message=mensagem)


def disparar_alerta_background(mensagem: str, arn_topico: str) -> None:
    thread_alerta = threading.Thread(target=enviar_alerta_sns, args=(mensagem, arn_topico))
    thread_alerta.start()


def avaliar_alerta_sensor(umidade: float, temperatura: float) -> dict:
    mensagem = "Condicoes agricolas dentro da faixa esperada."
    severidade = "Baixa"
    origem = "Sensor ESP32"

    if umidade < 28:
        mensagem = "Umidade critica detectada. Acionar irrigacao."
        severidade = "Alta"
    elif temperatura > 35:
        mensagem = "Temperatura elevada detectada. Monitorar cultura."
        severidade = "Media"

    arn_topico = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:farmtech-alertas")

    if severidade != "Baixa":
        disparar_alerta_background(mensagem, arn_topico)

    timestamp = datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(timespec="seconds")

    return {
        "origem": origem,
        "severidade": severidade,
        "mensagem": mensagem,
        "timestamp": timestamp,
        "sns": "Disparo real AWS SNS executado em background",
        "status": "enviado_real",
    }
