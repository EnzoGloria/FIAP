# FarmTech Solutions - FIAP Fase 7

## Objetivo

Construir um sistema integrado em Python + Streamlit que consolida as Fases 1 a 6 em um dashboard funcional, incorporando os temas da Fase 7: consolidação de sistemas, RNN/LSTM, voz, algoritmos genéticos, AWS, microsserviços, IA como serviço, ESP32 com POO e segurança Blue Team.

## Problema resolvido

Produtores e equipes técnicas precisam acompanhar dados agrícolas, sensores, alertas e recomendações em um único ambiente. Sem integração, decisões de irrigação, segurança e monitoramento ficam dispersas.

## Solução proposta

A FarmTech Solutions centraliza dados simulados de sensores e plantio, persiste eventos em SQLite, exibe gráficos Plotly, simula IA preditiva, otimização por algoritmo genético, voz inteligente, visão computacional, alertas AWS e segurança operacional.

## Tecnologias usadas

- Python
- Streamlit
- Pandas
- Plotly
- SQLite
- CSV
- Simulações de AWS SNS, SQS, Lambda e CloudWatch

## Relação com cada capítulo da Fase 7

- Consolidação de sistema: integração das funcionalidades em um único dashboard.
- RNN/LSTM: previsão simulada de umidade futura por série temporal.
- Reconhecimento e síntese de voz: placeholders para STT/TTS.
- Algoritmos genéticos: otimização do volume de irrigação.
- AWS SNS/SQS/Lambda/CloudWatch: simulação de alertas e observabilidade.
- Microsserviços e CloudFormation: arquitetura proposta em documentação.
- IA como serviço na AWS: preparação para Rekognition, SageMaker, Transcribe e Polly.
- POO com ESP32: classe `SensorAgricola`.
- Segurança cibernética / Blue Team: logs, firewall, tentativas suspeitas e boas práticas.

## Estrutura de pastas

```bash
farmtech_fase7/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── sensores.csv
│   ├── plantio.csv
│   └── historico_alertas.csv
├── database/
│   └── farmtech.db
├── modules/
│   ├── sensores.py
│   ├── banco.py
│   ├── previsao_lstm.py
│   ├── voz.py
│   ├── algoritmo_genetico.py
│   ├── alertas_aws.py
│   ├── visao_computacional.py
│   ├── seguranca.py
│   └── dashboard_utils.py
├── docs/
│   ├── arquitetura.md
│   ├── metodologia.md
│   ├── roteiro_video.md
│   └── divisao_tarefas.md
└── images/
```

## Como instalar

```bash
pip install -r requirements.txt
```

## Como executar

```bash
streamlit run app.py
```

## Explicação das telas

- Visão Geral: cards principais e gráficos de umidade e temperatura.
- Dados Agrícolas: plantio, culturas, áreas e leituras.
- IoT e Sensores: geração de leitura simulada com classe `SensorAgricola`.
- Banco de Dados: consulta SQLite de sensores e alertas.
- IA Preditiva LSTM: previsão simulada de umidade futura.
- Algoritmo Genético: busca do melhor volume de irrigação.
- Voz Inteligente: preparação para STT/TTS.
- Alertas AWS: simulação de SNS, SQS, Lambda e CloudWatch.
- Visão Computacional: classificação simulada de imagem da lavoura.
- Segurança: logs, firewall, tentativas suspeitas e Blue Team.
- Integração Final: fluxo Sensor -> Banco -> IA -> Dashboard -> Alerta -> Recomendação.
- Conclusão: síntese da solução e próximos passos.

## Próximos passos

- Usar dados reais de sensores ESP32.
- Treinar um modelo LSTM real com histórico maior.
- Integrar AWS real com credenciais seguras.
- Containerizar módulos como microsserviços.
- Criar infraestrutura CloudFormation.
- Expandir segurança com autenticação, auditoria e resposta a incidentes.

## Integrantes do grupo

- Integrante 1 - RM
- Integrante 2 - RM
- Integrante 3 - RM
- Integrante 4 - RM
- Integrante 5 - RM

