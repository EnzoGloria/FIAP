# FarmTech Solutions - FIAP Fase 7 (Consolidação)

## Contexto do Projeto
Este projeto é a entrega final (Fase 7) de uma sprint acadêmica da FIAP. O objetivo é consolidar os desenvolvimentos das Fases 1 a 6 em um sistema unificado de Gestão para o Agronegócio.

- **Fase 1:** Análise estatística meteorológica usando R.
- **Fase 2:** Banco de Dados Relacional (MER/DER) estruturado (SQLite/SQL).
- **Fase 3:** IoT e Automação (Mocks de sensores e lógicas para ESP32).
- **Fase 4:** Dashboard Interativo em Streamlit com Scikit-Learn.
- **Fase 5:** Serviço de mensageria real na AWS (boto3) disparando e-mails/SMS via Amazon SNS.
- **Fase 6:** Visão Computacional com YOLO para monitoramento de saúde da plantação usando imagens estáticas locais.

## Diretrizes e Restrições de Arquitetura
1. **Sem Over-Engineering:** A orquestração é feita inteiramente pelo **Streamlit** (UI/botões) e via **terminal (subprocess)**. É proibido o uso de frameworks web backend (FastAPI, Flask) ou mensagerias pesadas locais (Celery, RabbitMQ).
2. **Orquestração Assíncrona Nativa:** 
   - Uso de `subprocess` para chamar scripts em R e inferências do YOLO.
   - Uso de `threading` para requisições de rede (como AWS boto3) para não bloquear a thread principal do Streamlit.
3. **Regra de Clean Code (Estrita):** Os arquivos do projeto (`.py` e `.R`) **NÃO PODEM CONTER NENHUM COMENTÁRIO** (linhas iniciadas com `#`).

## Metas da Fase 7
- Integrar todos os códigos/serviços numa única pasta (`FIAP/farmtech_fase7`).
- Atualizar a interface do Streamlit para ter botões que disparem os serviços reais das fases passadas, abandonando simulações (mocks).
- Integrar chamadas do Boto3 (AWS SNS) para alertar os gestores, utilizando a infraestrutura criada na Fase 5.
- Preparar a estrutura final para documentação no GitHub, espelhando fielmente o diretório local do VS Code.

## O Que Já Foi Feito
- **Revisão e Diagnóstico Arquitetural:** Identificou-se que o código atual estava atuando majoritariamente com "mocks", sem integrações reais (falta do `rpy2`/R e inferências de visão computacional vazias).
- **Refatoração AWS SNS (`modules/alertas_aws.py`):**
  - O mock `simular_envio_alerta` foi removido.
  - Implementada a função `enviar_alerta_sns` conectando via `boto3`.
  - Implementada a função `disparar_alerta_background` usando a biblioteca `threading` nativa para evitar bloqueio no dashboard do Streamlit.
  - Atualizado o `app.py` para refletir as mudanças nas importações, removendo referências a funções deletadas.
  - Garantida a regra de Clean Code estrita (sem comentários nos arquivos reescritos).

## Próximos Passos (To-Do)
- [ ] **Integração Fase 1 (R):** Trazer/criar o script de análise meteorológica em R para dentro do projeto e acioná-lo via `subprocess` (ou biblioteca de ponte se necessário, porém seguindo a regra de não haver over-engineering).
- [ ] **Integração Fase 6 (Visão Computacional - YOLO):** Trocar os *mocks* (baseados em `random.choice`) no arquivo `visao_computacional.py` por código real de inferência (carregando tensores/modelos, preferencialmente `ultralytics`), analisando imagens estáticas de uma pasta.
- [ ] **Ajuste na UI (Streamlit):** Conectar de forma final os botões do dashboard aos respectivos processamentos (R e YOLO).
- [ ] **Revisão Final Clean Code:** Garantir que 100% da base não possui comentários.

## Status Atual do Projeto - Fase 5 Concluída

- **Módulo `modules/alertas_aws.py`**: Totalmente implementado e validado. Contém integração assíncrona usando `threading` e tratamento de exceções robusto com `botocore.exceptions`.
- **Validação de Infraestrutura**: O Amazon SNS foi configurado com o tópico `farmtech-alertas` e uma assinatura de e-mail foi confirmada com sucesso.
- **Teste de Integração**: Realizado teste pontual forçando severidade máxima (Umidade: 15.0, Temperatura: 45.0) via interpretador interativo do Python. O disparo foi executado com sucesso e o e-mail de alerta crítico foi recebido na caixa de entrada.
- **Próximo Passo**: Iniciar a Fase 6 (Visão Computacional / YOLO), conectando a interface do Streamlit (`app.py`) ao módulo `modules/visao_computacional.py` para processar imagens estáticas da lavoura.