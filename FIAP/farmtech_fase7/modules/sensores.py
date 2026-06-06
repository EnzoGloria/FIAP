from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from random import uniform
from zoneinfo import ZoneInfo


@dataclass
class SensorAgricola:
    """Representa um sensor agricola inspirado no uso com ESP32."""

    sensor_id: str
    talhao: str
    cultura: str
    umidade: float
    temperatura: float
    consumo_agua: float
    luminosidade: float
    timestamp: str

    @classmethod
    def simular(cls, sensor_id: str = "ESP32-001", talhao: str = "Talhao A", cultura: str = "Soja") -> "SensorAgricola":
        umidade = round(uniform(24, 46), 2)
        temperatura = round(uniform(23, 37), 2)
        consumo_agua = round(uniform(850, 1800), 2)
        luminosidade = round(uniform(520, 980), 2)

        return cls(
            sensor_id=sensor_id,
            talhao=talhao,
            cultura=cultura,
            umidade=umidade,
            temperatura=temperatura,
            consumo_agua=consumo_agua,
            luminosidade=luminosidade,
            timestamp=datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(timespec="seconds"),
        )

    def status_irrigacao(self) -> str:
        if self.umidade < 30:
            return "Irrigar agora"
        if self.umidade < 36:
            return "Monitorar"
        return "Adequada"

    def para_dict(self) -> dict:
        dados = asdict(self)
        dados["status_irrigacao"] = self.status_irrigacao()
        return dados


def gerar_leituras_simuladas(quantidade: int = 48) -> list[dict]:
    culturas = ["Soja", "Milho", "Cafe"]
    talhoes = ["Talhao A", "Talhao B", "Talhao C"]
    leituras = []

    for indice in range(quantidade):
        sensor = SensorAgricola.simular(
            sensor_id=f"ESP32-{indice % 3 + 1:03d}",
            talhao=talhoes[indice % len(talhoes)],
            cultura=culturas[indice % len(culturas)],
        )
        leituras.append(sensor.para_dict())

    return leituras

