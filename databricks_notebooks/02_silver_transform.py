# Databricks notebook source
# MAGIC %sql
# MAGIC USE CATALOG pulsecity;
# MAGIC CREATE SCHEMA IF NOT EXISTS silver;
# MAGIC USE SCHEMA silver;
# MAGIC

# COMMAND ----------

spark.readStream.table("pulsecity.bronze.traffic").createOrReplaceTempView("v_bronze_stream")

silver_sql_query = spark.sql("""
    SELECT 
        UPPER(sensor_id) AS sensor_id,
        CAST(timestamp AS TIMESTAMP) AS event_timestamp,
        CAST(vehicle_count AS INT) AS vehicle_count,
        CAST(average_speed_kmh AS DOUBLE) AS average_speed_kmh,
        CAST(co2_level_ppm AS INT) AS co2_level_ppm,
        CAST(timestamp AS DATE) AS event_date,
        CURRENT_TIMESTAMP() AS processed_at
    FROM v_bronze_stream
    WHERE sensor_id IS NOT NULL 
      AND vehicle_count >= 0
""")

# Deixamos o Spark criar a tabela Silver automaticamente para evitar mismatch
silver_sql_query.writeStream \
    .format("delta") \
    .outputMode("append") \
    .trigger(availableNow=True) \
    .option("checkpointLocation", "/Volumes/pulsecity/bronze/stage_volume/_checkpoints/silver_traffic") \
    .toTable("pulsecity.silver.traffic")
