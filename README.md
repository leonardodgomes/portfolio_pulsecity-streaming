# SmartCity Streaming Pipeline: Databricks & Power BI

Este projeto demonstra a criação de uma solução de engenharia de dados ponta a ponta (E2E) para monitoramento de tráfego urbano e poluentes em tempo real. Utilizando uma arquitetura de streaming baseada em arquivos JSON simulados, os dados são processados usando a Arquitetura Medallion e disponibilizados para consumo analítico.

## Arquitetura do Projeto

1. **Geração de Dados:** Script Python local utilizando a biblioteca `Faker` gera payloads JSON e os envia continuamente para o DBFS via Databricks CLI.
2. **Camada Bronze (Raw):** Ingestão direta dos arquivos JSON em streaming via Structured Streaming (`cloudFiles`).
3. **Camada Silver (Clean):** Limpeza, tipagem de campos e tratamento de dados ausentes utilizando **Spark SQL**.
4. **Camada Gold (Analytics):** Agregações temporais e cálculos de KPIs prontos para o negócio com Spark SQL.
5. **Visualização:** Power BI conectado ao cluster Databricks consumindo as tabelas Delta finais.

## Estrutura do Repositório

```text
├── data_generator/
│   └── generator.py        # Script gerador de carga JSON sintética
├── databricks_notebooks/
│   ├── ingestion_bronze.py # Captura do streaming de arquivos
│   ├── transform_silver.py # Regras de limpeza em Spark SQL
│   └── aggregate_gold.py   # Criação das views de negócio em Spark SQL
├── power_bi/
│   └── dashboard_smartcity.pbix # Arquivo do relatório analítico
├── BACKLOG.md              # Gerenciamento de features e tarefas do projeto
└── README.md               # Documentação principal
```

## Como Executar o Projeto

### Pré-requisitos
* Conta ativa no [Databricks Community Edition](https://databricks.com/).
* Python 3.10+ instalado localmente.
* Databricks CLI instalado.

### Passo 1: Configuração das Variáveis de Ambiente
Configure seu token de acesso do Databricks no seu terminal local:
```bash
export DATABRICKS_HOST="https://databricks.com"
export DATABRICKS_TOKEN="seu_token_aqui"
```

### Passo 2: Iniciar a Geração de Dados
Navegue até a pasta do gerador e execute o script para começar a enviar os eventos simulados em JSON:
```bash
python data_generator/generator.py
```

### Passo 3: Executar os Notebooks no Databricks
Importe e execute os notebooks da pasta `databricks_notebooks/` respeitando a ordem: Bronze -> Silver -> Gold.

## Dashboard Desenvolvido
*[Insira aqui um printscreen do seu painel final do Power BI mostrando os gráficos e alertas criados]*
