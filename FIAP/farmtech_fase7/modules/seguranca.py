from __future__ import annotations

from datetime import datetime
from random import choice, randint
from zoneinfo import ZoneInfo


def gerar_logs_seguranca(quantidade: int = 12) -> list[dict]:
    eventos = [
        ("INFO", "Login administrativo validado com MFA"),
        ("INFO", "Backup local concluido"),
        ("WARN", "Tentativa de acesso fora do horario habitual"),
        ("WARN", "Muitas requisicoes para endpoint de sensores"),
        ("CRITICO", "Tentativa suspeita de autenticacao no dashboard"),
    ]

    logs = []
    for indice in range(quantidade):
        nivel, mensagem = choice(eventos)
        logs.append(
            {
                "id": indice + 1,
                "timestamp": datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(timespec="seconds"),
                "nivel": nivel,
                "origem": f"10.0.0.{randint(2, 240)}",
                "mensagem": mensagem,
            }
        )
    return logs


def analisar_postura_blue_team(logs: list[dict]) -> dict:
    criticos = sum(1 for log in logs if log["nivel"] == "CRITICO")
    avisos = sum(1 for log in logs if log["nivel"] == "WARN")
    firewall = "Ativo"
    risco = "Alto" if criticos else "Medio" if avisos >= 3 else "Baixo"

    return {
        "firewall": firewall,
        "tentativas_suspeitas": criticos + avisos,
        "risco": risco,
        "boas_praticas": [
            "Aplicar MFA para usuarios administrativos",
            "Registrar logs em servico centralizado",
            "Segmentar rede IoT e rede administrativa",
            "Monitorar anomalias com alertas automatizados",
            "Manter backups e plano de resposta a incidentes",
        ],
    }

