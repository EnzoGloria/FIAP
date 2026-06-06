# Arquitetura

## Arquitetura lógica

A solução é organizada em três camadas:

- Coleta: sensores simulados com POO representando ESP32.
- Processamento: módulos Python para banco, IA, alertas, voz, visão e segurança.
- Apresentação: dashboard Streamlit com gráficos Plotly.

## Fluxo de dados

1. Sensor ESP32 gera leitura de umidade, temperatura, consumo de água e luminosidade.
2. Dados são persistidos em SQLite e também podem ser lidos de CSV.
3. Módulo LSTM simulado prevê umidade futura.
4. Algoritmo genético sugere volume otimizado de irrigação.
5. Dashboard exibe indicadores e gráficos.
6. Alertas são simulados em fluxo SNS -> SQS -> Lambda -> CloudWatch.
7. Segurança monitora logs e postura Blue Team.

## Microsserviços propostos

- `sensor-service`: recebe leituras IoT.
- `database-service`: centraliza persistência.
- `prediction-service`: executa previsão LSTM.
- `optimization-service`: roda algoritmo genético.
- `alert-service`: integra SNS, SQS e Lambda.
- `security-service`: coleta logs e gera métricas Blue Team.
- `dashboard-service`: apresenta dados ao usuário.

## Simulação AWS

O projeto não exige AWS real. A simulação representa:

- SNS para publicação de notificações.
- SQS para fila de eventos.
- Lambda para processamento serverless.
- CloudWatch para logs e métricas.
- Rekognition ou SageMaker como evolução de visão computacional.
- Transcribe e Polly como evolução de voz.

## Segurança

A arquitetura considera controles Blue Team:

- MFA para acesso administrativo.
- Segmentação de rede IoT.
- Logs centralizados.
- Monitoramento de anomalias.
- Backup e resposta a incidentes.
- Menor privilégio para credenciais futuras de cloud.

