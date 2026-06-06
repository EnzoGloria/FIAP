def reconhecer_fala_placeholder(audio_path: str | None = None) -> str:
    """Placeholder para futura integracao STT, como Amazon Transcribe."""
    if audio_path:
        return f"Audio recebido em {audio_path}. Transcricao simulada: verificar irrigacao do talhao."
    return "Comando simulado: verificar irrigacao do talhao."


def sintetizar_voz_placeholder(texto: str) -> str:
    """Placeholder para futura integracao TTS, como Amazon Polly."""
    return f"Sintese de voz simulada: {texto}"


def interpretar_comando_agricola(comando: str) -> dict:
    comando_normalizado = comando.lower()
    acao = "consulta"
    if "irrig" in comando_normalizado:
        acao = "irrigacao"
    elif "alerta" in comando_normalizado:
        acao = "alertas"

    return {
        "comando": comando,
        "acao_detectada": acao,
        "status": "preparado_para_integracao_futura",
    }

