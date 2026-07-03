# Databricks notebook source
# MAGIC %sql
# MAGIC -- Célula 1: Criar a "gaveta" (Schema) da camada Gold
# MAGIC CREATE SCHEMA IF NOT EXISTS pulsecity.gold;
# MAGIC
# MAGIC -- Célula 2: Definir o contexto de uso do Databricks
# MAGIC USE CATALOG pulsecity;
# MAGIC USE SCHEMA gold;
# MAGIC
# MAGIC -- Célula 3: Criar a View Analítica Gold com Janelas de Tempo e Regras de Negócio
# MAGIC CREATE OR REPLACE VIEW pulsecity.gold.traffic_metrics_5min AS
# MAGIC SELECT 
# MAGIC     sensor_id,
# MAGIC     -- Janela de tempo de 5 minutos baseada no horário real do evento do sensor
# MAGIC     window(event_timestamp, '5 minutes').start AS window_start,
# MAGIC     window(event_timestamp, '5 minutes').end AS window_end,
# MAGIC     
# MAGIC     -- Métricas Analíticas agregadas por sensor e por janela
# MAGIC     SUM(vehicle_count) AS total_vehicles,
# MAGIC     ROUND(AVG(average_speed_kmh), 1) AS avg_speed_kmh,
# MAGIC     ROUND(AVG(co2_level_ppm), 0) AS avg_co2_level,
# MAGIC     
# MAGIC     -- Regra de Negócio: Se a média de CO2 passar de 450 ppm, gera um alerta crítico (1)
# MAGIC     CASE 
# MAGIC         WHEN AVG(co2_level_ppm) > 450 THEN 1 
# MAGIC         ELSE 0 
# MAGIC     END AS is_critical_co2_alert,
# MAGIC     
# MAGIC     -- Metadado de auditoria: guarda quando a consulta foi atualizada
# MAGIC     CURRENT_TIMESTAMP() AS updated_at
# MAGIC FROM pulsecity.silver.traffic
# MAGIC GROUP BY 
# MAGIC     sensor_id, 
# MAGIC     window(event_timestamp, '5 minutes');
# MAGIC