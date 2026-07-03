# Databricks notebook source
# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS pulsecity.bronze.traffic;
# MAGIC DROP TABLE IF EXISTS pulsecity.silver.traffic;

# COMMAND ----------

# Remove as pastas ocultas de schemas e checkpoints para o Spark começar do zero
dbutils.fs.rm("/Volumes/pulsecity/bronze/stage_volume/_schemas/", recurse=True)
dbutils.fs.rm("/Volumes/pulsecity/bronze/stage_volume/_checkpoints/", recurse=True)


# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG pulsecity;
# MAGIC CREATE SCHEMA IF NOT EXISTS bronze;
# MAGIC USE SCHEMA bronze;
# MAGIC
# MAGIC -- No padrão de mercado com Auto Loader, NÃO criamos a tabela com "CREATE TABLE" antes.
# MAGIC -- Deixamos o próprio writeStream criar a tabela Delta sozinho na primeira execução.
# MAGIC
# MAGIC

# COMMAND ----------

query_bronze = spark.readStream \
    .format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .option("cloudFiles.schemaLocation", "/Volumes/pulsecity/bronze/stage_volume/_schemas/traffic") \
    .load("/Volumes/pulsecity/bronze/stage_volume/json_stream")

# O writeStream cria a tabela automaticamente com o schema perfeito extraído do JSON
query_bronze.writeStream \
    .format("delta") \
    .outputMode("append") \
    .trigger(availableNow=True) \
    .option("checkpointLocation", "/Volumes/pulsecity/bronze/stage_volume/_checkpoints/traffic") \
    .toTable("pulsecity.bronze.traffic")
