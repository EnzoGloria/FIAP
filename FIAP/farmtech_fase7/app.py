from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.algoritmo_genetico import otimizar_irrigacao
from modules.alertas_aws import avaliar_alerta_sensor
from modules.banco import consultar_alertas, consultar_sensores, criar_banco, inserir_alerta, inserir_leitura
from modules.dashboard_utils import calcular_metricas, grafico_fluxo_integracao, grafico_temperatura, grafico_umidade
from modules.previsao_lstm import classificar_risco_umidade, prever_umidade_futura
from modules.seguranca import analisar_postura_blue_team, gerar_logs_seguranca
from modules.sensores import SensorAgricola, gerar_leituras_simuladas
from modules.visao_computacional import analisar_imagem_lavoura
from modules.voz import interpretar_comando_agricola, reconhecer_fala_placeholder, sintetizar_voz_placeholder


ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"


st.set_page_config(page_title="FarmTech Solutions - FIAP Fase 7", layout="wide")


@st.cache_data
def carregar_csv(nome: str) -> pd.DataFrame:
    caminho = DATA_DIR / nome
    if caminho.exists():
        return pd.read_csv(caminho)
    return pd.DataFrame()


def carregar_dados_sensores() -> pd.DataFrame:
    sensores = carregar_csv("sensores.csv")
    if sensores.empty:
        sensores = pd.DataFrame(gerar_leituras_simuladas())
    return sensores


def carregar_alertas() -> pd.DataFrame:
    alertas = carregar_csv("historico_alertas.csv")
    if alertas.empty:
        alertas = pd.DataFrame(
            [
                {
                    "origem": "FarmTech",
                    "severidade": "Baixa",
                    "mensagem": "Ambiente operacional sem alertas criticos.",
                    "timestamp": "2026-05-17T08:00:00-03:00",
                }
            ]
        )
    return alertas


def exibir_cards(metricas: dict) -> None:
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Umidade media", f"{metricas['umidade_media']:.1f}%")
    col2.metric("Temperatura media", f"{metricas['temperatura_media']:.1f} C")
    col3.metric("Consumo de agua", f"{metricas['consumo_agua']:.0f} L")
    col4.metric("Alertas", metricas["numero_alertas"])
    col5.metric("Irrigacao", metricas["status_irrigacao"])


def tela_visao_geral(sensores: pd.DataFrame, plantio: pd.DataFrame, alertas: pd.DataFrame) -> None:
    st.header("Visao Geral")
    exibir_cards(calcular_metricas(sensores, alertas))
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grafico_umidade(sensores), use_container_width=True)
    with col2:
        st.plotly_chart(grafico_temperatura(sensores), use_container_width=True)
    st.subheader("Plantio monitorado")
    st.dataframe(plantio, use_container_width=True)


def tela_dados_agricolas(sensores: pd.DataFrame, plantio: pd.DataFrame) -> None:
    st.header("Dados Agricolas")
    st.write("Base consolidada com plantio, sensores, talhoes e culturas.")
    st.dataframe(plantio, use_container_width=True)
    fig = px.pie(plantio, names="cultura", values="area_hectares", title="Distribuicao de area por cultura")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Leituras agricolas")
    st.dataframe(sensores, use_container_width=True)


def tela_iot_sensores(sensores: pd.DataFrame) -> None:
    st.header("IoT e Sensores")
    st.write("Simulacao de sensores agricolas com POO inspirada em ESP32.")

    if st.button("Gerar leitura ESP32 simulada", type="primary"):
        leitura = SensorAgricola.simular().para_dict()
        inserir_leitura(leitura)
        st.success("Leitura gravada no SQLite.")
        st.json(leitura)

    st.plotly_chart(grafico_umidade(sensores), use_container_width=True)
    st.dataframe(sensores.tail(15), use_container_width=True)


def tela_banco_dados() -> None:
    st.header("Banco de Dados")
    criar_banco()
    sensores_db = consultar_sensores()
    alertas_db = consultar_alertas()

    st.write("Persistencia local SQLite para leituras de sensores e alertas operacionais.")
    col1, col2 = st.columns(2)
    col1.metric("Registros de sensores", len(sensores_db))
    col2.metric("Alertas persistidos", len(alertas_db))
    st.subheader("Tabela sensores")
    st.dataframe(sensores_db, use_container_width=True)
    st.subheader("Tabela alertas")
    st.dataframe(alertas_db, use_container_width=True)


def tela_ia_lstm(sensores: pd.DataFrame) -> None:
    st.header("IA Preditiva LSTM")
    st.write("Previsao temporal simulada de umidade futura, representando o uso de RNN/LSTM sem treino pesado local.")
    passos = st.slider("Horizonte de previsao em horas", min_value=6, max_value=24, value=12)
    previsao = prever_umidade_futura(sensores["umidade"], passos=passos)
    previsao["risco"] = previsao["umidade_prevista"].apply(classificar_risco_umidade)

    fig = px.line(previsao, x="periodo", y="umidade_prevista", markers=True, color="risco", title="Previsao de umidade futura")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(previsao, use_container_width=True)


def tela_algoritmo_genetico(sensores: pd.DataFrame) -> None:
    st.header("Algoritmo Genetico")
    ultima = sensores.iloc[-1]
    umidade = st.number_input("Umidade atual (%)", value=float(ultima["umidade"]))
    temperatura = st.number_input("Temperatura atual (C)", value=float(ultima["temperatura"]))

    resultado = otimizar_irrigacao(umidade, temperatura)
    st.metric("Melhor volume de irrigacao", f"{resultado['melhor_volume_litros']} L")
    st.write(resultado["recomendacao"])

    historico = pd.DataFrame(resultado["historico"])
    fig = px.line(historico, x="geracao", y="score", markers=True, title="Evolucao do score por geracao")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(historico, use_container_width=True)


def tela_voz_inteligente() -> None:
    st.header("Voz Inteligente")
    st.write("Tela preparada para STT/TTS. Em uma evolucao AWS, STT pode usar Amazon Transcribe e TTS pode usar Amazon Polly.")
    comando = st.text_input("Comando de voz simulado", value="Verificar irrigacao do talhao")
    transcricao = reconhecer_fala_placeholder()
    interpretacao = interpretar_comando_agricola(comando)
    resposta = sintetizar_voz_placeholder("A irrigacao sera avaliada conforme umidade e previsao.")

    st.subheader("STT - Speech to Text")
    st.info(transcricao)
    st.subheader("Interpretacao")
    st.json(interpretacao)
    st.subheader("TTS - Text to Speech")
    st.success(resposta)


def tela_alertas_aws(sensores: pd.DataFrame) -> None:
    st.header("Alertas AWS")
    ultima = sensores.iloc[-1]
    alerta = avaliar_alerta_sensor(float(ultima["umidade"]), float(ultima["temperatura"]))

    if st.button("Simular SNS/SQS/Lambda/CloudWatch", type="primary"):
        inserir_alerta(alerta)
        st.success("Alerta simulado e persistido no SQLite.")

    st.json(alerta)
    etapas = pd.DataFrame(
        [
            {"servico": "SNS", "papel": "Publicar notificacao"},
            {"servico": "SQS", "papel": "Enfileirar eventos"},
            {"servico": "Lambda", "papel": "Processar regra de alerta"},
            {"servico": "CloudWatch", "papel": "Registrar log e metrica"},
        ]
    )
    st.dataframe(etapas, use_container_width=True)


def tela_visao_computacional() -> None:
    st.header("Visao Computacional")
    st.write("Analise de alta fidelidade usando YOLO (Mock) com imagens de validacao.")
    
    pasta_imagens = ROOT_DIR / "images"
    arquivos_imagem = []
    if pasta_imagens.exists():
        arquivos_imagem = [f.name for f in pasta_imagens.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]
    
    if arquivos_imagem:
        imagem_selecionada = st.selectbox("Selecione uma imagem da lavoura:", arquivos_imagem)
        caminho_imagem = pasta_imagens / str(imagem_selecionada)
        st.image(str(caminho_imagem), caption=str(imagem_selecionada), use_container_width=True)
        
        if st.button("Executar Analise YOLO", type="primary"):
            resultado = analisar_imagem_lavoura(str(caminho_imagem))
            
            col1, col2 = st.columns(2)
            col1.metric("Diagnostico", resultado["classe"])
            col2.metric("Confianca", f"{resultado['confianca'] * 100:.1f}%")
            
            if resultado["classe"] == "Saudavel":
                st.success(resultado["recomendacao"])
            elif resultado["classe"] == "Anomalia Desconhecida":
                st.warning(resultado["recomendacao"])
            else:
                st.error(resultado["recomendacao"])
            
            st.json(resultado)
    else:
        st.warning("Nenhuma imagem encontrada na pasta images/. Adicione imagens (.jpg, .jpeg, .png) para testar.")


def tela_seguranca() -> None:
    st.header("Seguranca")
    logs = gerar_logs_seguranca()
    analise = analisar_postura_blue_team(logs)

    col1, col2, col3 = st.columns(3)
    col1.metric("Firewall", analise["firewall"])
    col2.metric("Tentativas suspeitas", analise["tentativas_suspeitas"])
    col3.metric("Risco atual", analise["risco"])

    st.subheader("Logs de seguranca")
    st.dataframe(pd.DataFrame(logs), use_container_width=True)
    st.subheader("Boas praticas Blue Team")
    for pratica in analise["boas_praticas"]:
        st.write(f"- {pratica}")


def tela_integracao_final() -> None:
    st.header("Integracao Final")
    st.write("Fluxo consolidado da Fase 7.")
    st.plotly_chart(grafico_fluxo_integracao(), use_container_width=True)
    st.success("Sensor -> Banco de Dados -> IA -> Dashboard -> Alerta -> Recomendacao")


def tela_conclusao() -> None:
    st.header("Conclusao")
    st.write(
        "A FarmTech Solutions consolida as fases anteriores em uma arquitetura local, extensivel e preparada "
        "para evoluir com IA temporal, voz, otimizacao genetica, microsservicos, AWS e praticas Blue Team."
    )
    st.markdown(
        """
        **Proximos passos**

        - Treinar LSTM real com historico maior.
        - Integrar Amazon Transcribe, Polly, Rekognition e SNS.
        - Publicar microsservicos com Docker e CloudFormation.
        - Ampliar controles de seguranca, logs e resposta a incidentes.
        """
    )


def main() -> None:
    sensores = carregar_dados_sensores()
    plantio = carregar_csv("plantio.csv")
    alertas = carregar_alertas()

    st.sidebar.title("FarmTech Solutions")
    pagina = st.sidebar.radio(
        "Menu",
        [
            "Visao Geral",
            "Dados Agricolas",
            "IoT e Sensores",
            "Banco de Dados",
            "IA Preditiva LSTM",
            "Algoritmo Genetico",
            "Voz Inteligente",
            "Alertas AWS",
            "Visao Computacional",
            "Seguranca",
            "Integracao Final",
            "Conclusao",
        ],
    )

    st.sidebar.caption("FIAP Fase 7 - Dashboard consolidado")

    if pagina == "Visao Geral":
        tela_visao_geral(sensores, plantio, alertas)
    elif pagina == "Dados Agricolas":
        tela_dados_agricolas(sensores, plantio)
    elif pagina == "IoT e Sensores":
        tela_iot_sensores(sensores)
    elif pagina == "Banco de Dados":
        tela_banco_dados()
    elif pagina == "IA Preditiva LSTM":
        tela_ia_lstm(sensores)
    elif pagina == "Algoritmo Genetico":
        tela_algoritmo_genetico(sensores)
    elif pagina == "Voz Inteligente":
        tela_voz_inteligente()
    elif pagina == "Alertas AWS":
        tela_alertas_aws(sensores)
    elif pagina == "Visao Computacional":
        tela_visao_computacional()
    elif pagina == "Seguranca":
        tela_seguranca()
    elif pagina == "Integracao Final":
        tela_integracao_final()
    elif pagina == "Conclusao":
        tela_conclusao()


if __name__ == "__main__":
    main()

