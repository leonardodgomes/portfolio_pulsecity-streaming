# Backlog do Projeto: SmartCity Streaming Pipeline

Este backlog representa o planejamento ágil para o desenvolvimento do portfólio de engenharia de dados.

## Sprint 1: Setup do Ambiente e Infraestrutura Básica
- [ ] **Task 1.1:** Instalar e configurar a nova Databricks CLI v0.200+ localmente na máquina.
- [ ] **Task 1.2:** Autenticar a CLI com o Databricks Community Edition usando o Workspace URL e Token.
- [ ] **Task 1.3:** Criar a estrutura de pastas local (`/scripts`, `/notebooks`, `/dashboard`) e inicializar o repositório Git.
- [ ] **Task 1.4:** Desenvolver o script gerador de JSONs (`generator.py`) usando a biblioteca `faker`.

## Sprint 2: Engenharia de Dados com Spark SQL (Medallion Architecture)
- [ ] **Task 2.1:** Configurar o `readStream` em formato Delta mapeando a pasta de stage para a camada **Bronze**.
- [ ] **Task 2.2:** Desenvolver o notebook de transformação em Spark SQL para a camada **Silver** (tipagem de dados, limpeza de nulos, cast de timestamps).
- [ ] **Task 2.3:** Criar agregados em tempo real na camada **Gold** usando Spark SQL para calcular médias de velocidade e tráfego por sensor a cada 5 minutos.
- [ ] **Task 2.4:** Configurar os checkpoints de streaming no DBFS para garantir a tolerância a falhas.

## Sprint 3: Visualização de Dados e Deploy Final
- [ ] **Task 3.1:** Conectar o Power BI Desktop ao cluster do Databricks Community via driver Spark/Hive/ODBC.
- [ ] **Task 3.2:** Desenvolver o Dashboard no Power BI com métricas de tráfego e alertas de CO2 em tempo real.
- [ ] **Task 3.3:** Finalizar a documentação do projeto no `README.md` incluindo o diagrama da arquitetura.
