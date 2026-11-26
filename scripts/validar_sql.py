from pyspark.sql import SparkSession

# Inicializar SparkSession en modo silencioso para salida limpia
spark = SparkSession.builder.appName("ValidacionSQL_Telemetria").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

PARQUET_PATH = "/home/glue_user/workspace/data/processed/telemetria_parquet"

# Leer el archivo Parquet generado por el ETL y registrarlo como tabla SQL
df_parquet = spark.read.parquet(PARQUET_PATH)
df_parquet.createOrReplaceTempView("telemetria_equipos")

print("\n=== 1. CONSUMO TOTAL Y PROMEDIO POR ZONA (kWh) ===")
spark.sql("""
    SELECT
        zona,
        COUNT(*) AS registros,
        ROUND(SUM(consumo_kwh), 2) AS consumo_total_kwh,
        ROUND(AVG(consumo_kwh), 2) AS consumo_promedio_kwh
    FROM telemetria_equipos
    GROUP BY zona
    ORDER BY consumo_total_kwh DESC
""").show(truncate=False)

print("=== 2. TOP 3 EQUIPOS DE MAYOR CONSUMO ===")
spark.sql("""
    SELECT
        id_equipo,
        zona,
        ROUND(SUM(horas_operacion), 1) AS total_horas,
        ROUND(SUM(consumo_kwh), 2) AS consumo_total_kwh
    FROM telemetria_equipos
    GROUP BY id_equipo, zona
    ORDER BY consumo_total_kwh DESC
    LIMIT 3
""").show(truncate=False)

spark.stop()