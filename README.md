# PulseCity-Streaming: Pipeline de IoT Urbano E2E com Databricks e Power BI

[![Databricks](https://shields.io)](https://databricks.com)
[![PowerBI](https://shields.io)](https://microsoft.com)
[![Spark SQL](https://shields.io)](https://apache.org)

Este projeto demonstra a criação de uma solução de engenharia de dados ponta a ponta (E2E) para monitoramento de tráfego urbano e poluentes ambientais em tempo real. Utilizando uma arquitetura baseada em eventos simulados (JSON), os dados são orquestrados e processados seguindo a Arquitetura Medallion e disponibilizados para consumo analítico executivo.

---

## Arquitetura de Dados (Medallion)

O pipeline foi estruturado utilizando as melhores práticas do **Unity Catalog** no Databricks:

1. **Geração de Dados**: Script nativo em Python atua como um simulador de sensores IoT urbanos, depositando continuamente arquivos JSON no ecossistema.
2. **Camada Bronze (Raw)**: Ingestão de streaming incremental automatizada via **Auto Loader (`read_files`)**, garantindo suporte nativo a *Schema Evolution*.
3. **Camada Silver (Clean & Enriched)**: Tratamento de qualidade, limpeza de nulos e tipagem estrita de dados (`TIMESTAMP`, `INT`, `DOUBLE`) via **Spark SQL**.
4. **Camada Gold (Analytics)**: Criação de visões de negócio agregadas em janelas temporais de **5 minutos**, injetando lógicas condicionais para deteção de alertas de CO2 críticos.
5. **Visualização**: Consumo otimizado das tabelas finais no Power BI Desktop.

---

## Engineering Mindset: Desafios Técnicos e Soluções

Desenvolver este projeto em um ambiente de computador corporativo restrito exigiu adaptações técnicas fundamentais que demonstram maturidade arquitetural:

* **Contorno de Proxy e Firewall**: A infraestrutura de rede corporativa bloqueava requisições externas via Python devido a falhas de certificação SSL (`CERTIFICATE_VERIFY_FAILED`). **Solução**: O simulador foi portado para rodar nativamente dentro do cluster em nuvem do Databricks, eliminando barreiras locais da máquina de trabalho.
* **Governança com Unity Catalog Volumes**: O uso do antigo DBFS raiz foi descontinuado devido a novas políticas de segurança da plataforma (`[DBFS_DISABLED]`). **Solução**: Toda a área de stage foi migrada para **Volumes Gerenciados** no Unity Catalog (`/Volumes/pulsecity/bronze/stage_volume/`), adotando o padrão de governança mais moderno do mercado.
* **Otimização de Custos e Restrições Serverless**: O cluster gratuito bloqueava streams interativos contínuos que consumiam recursos infinitamente (`Trigger ProcessingTime not supported`). **Solução**: O pipeline foi reconfigurado para rodar no modo **Micro-batch** com o gatilho **`.trigger(availableNow=True)`**, permitindo o processamento incremental e eficiente apenas de novos arquivos antes de desligar o fluxo de forma segura.

---

## Estrutura do Repositório

```text
├── data_generator/
│   └── generator.py        # Código do simulador de sensores IoT
├── databricks_notebooks/
│   ├── 01_bronze_ingestion.py # Ingestão via Auto Loader (Híbrido Python/SQL)
│   ├── 02_silver_transform.py # Limpeza e tipagem explícita (Híbrido Python/SQL)
│   └── 03_gold_aggregation.sql# Visão analítica com Janelas de Tempo (Spark SQL)
├── power_bi/
│   └── dashboard_pulse.pbix   # Relatório com página de pitch e KPIs de negócio
├── BACKLOG.md              # Gerenciamento ágil de features do projeto
└── README.md               # Documentação principal
```

---

## Como Executar o Projeto

1. Execute o notebook `00_generator_sim` no Databricks para começar a depositar os arquivos JSON simulados de Aveiro, Porto, Lisboa e Coimbra no Volume do Unity Catalog.
2. Dispare o notebook `01_bronze_ingestion` para processar a carga bruta incremental.
3. Dispare o notebook `02_silver_transform` para limpar e estruturar os dados.
4. Abra o Power BI Desktop e utilize o conector nativo do Databricks (inserindo o *Server Hostname* e o *HTTP Path* das opções avançadas de JDBC do seu cluster) para consumir os dados diretamente de `pulsecity.gold.traffic_metrics_5min`.

---

## Entrega de Valor (Dashboard Power BI)

O relatório final conta com uma aba executiva de Pitch Técnico e visuais interativos que expõem:
* **KPIs de Alertas de CO2**: Deteção de picos de poluição com formatação condicional baseada na coluna lógica da camada Gold.
* **Gráficos de Tendência**: Análise temporal comparativa entre o volume de carros e a emissão de poluentes.
* **Segmentação por Região**: Filtros dinâmicos para isolar a saúde do tráfego por cidade.
