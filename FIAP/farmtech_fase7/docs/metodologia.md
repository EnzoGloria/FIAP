# Metodologia

## Metodologia de integração

A integração foi feita por módulos independentes, cada um representando um conteúdo da Fase 7. O `app.py` atua como orquestrador do dashboard, chamando funções de sensores, banco, IA, voz, alertas, visão computacional, segurança e gráficos.

## Uso de dados simulados

O projeto usa CSVs e geração aleatória controlada para simular sensores agrícolas. Essa decisão permite rodar localmente sem ESP32 físico, sem APIs pagas e sem conta AWS.

## Justificativa técnica

- Streamlit acelera a criação do dashboard.
- Plotly gera gráficos interativos.
- SQLite permite persistência local simples.
- Módulos separados aproximam a solução de uma arquitetura de microsserviços.
- Simulações preservam o conteúdo conceitual sem criar dependências externas.

## Limitações

- A previsão LSTM é simulada e não treina uma rede neural real.
- A voz usa placeholders, sem captura de áudio real.
- A AWS é representada por simulação local.
- A visão computacional classifica imagens de forma simulada.
- Os dados não vêm de sensores reais.

## Evolução futura

- Integrar ESP32 real via MQTT ou API HTTP.
- Treinar LSTM com TensorFlow ou PyTorch.
- Criar endpoints FastAPI para cada microsserviço.
- Usar AWS IoT Core, Lambda, SNS, SQS e CloudWatch reais.
- Usar Amazon Rekognition, SageMaker, Transcribe e Polly.
- Implementar autenticação, autorização e auditoria.

