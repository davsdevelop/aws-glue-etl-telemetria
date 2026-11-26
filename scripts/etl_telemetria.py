from pyspark.context import SparkContext
from awsglue.context import GlueContext  # type: ignore
from pyspark.sql import functions as F

# 1. Inicializar contexto oficial de AWS Glue + Spark
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Rutas dentro del contenedor
INPUT_PATH = "/home/glue_user/workspace/data/raw/telemetria_equipos.csv"
OUTPUT_PATH = "/home/glue_user/workspace/data/processed/telemetria_parquet"

print(">>> [EXTRACT] Leyendo CSV crudo...")
df_raw = (
    spark.read.option("header", "true")
    .option("inferSchema", "false")
    .csv(INPUT_PATH)
)

print(">>> [RAW] Vista previa antes de limpiar:")
df_raw.show(5, truncate=False)

# 2. Transformaciones: limpieza de espacios, casteo de tipos y columna calculada
print(">>> [TRANSFORM] Limpiando textos y calculando consumo_kwh...")
df_clean = (
    df_raw
    .withColumn("id_equipo", F.trim(F.col("id_equipo")))
    .withColumn("zona", F.trim(F.col("zona")))
    .withColumn("voltaje_v", F.col("voltaje_v").cast("double"))
    .withColumn("corriente_a", F.col("corriente_a").cast("double"))
    .withColumn("horas_operacion", F.col("horas_operacion").cast("double"))
    .withColumn("fecha", F.to_date(F.col("fecha"), "yyyy-MM-dd"))
    .withColumn(
        "consumo_kwh",
        F.round((F.col("voltaje_v") * F.col("corriente_a") / 1000.0) * F.col("horas_operacion"), 2)
    )
)

print(">>> [PROCESSED] Vista previa después de transformar:")
df_clean.printSchema()
df_clean.show(truncate=False)

# 3. Carga en formato columnar Parquet
print(f">>> [LOAD] Escribiendo archivos Parquet en {OUTPUT_PATH}...")
df_clean.coalesce(1).write.mode("overwrite").parquet(OUTPUT_PATH)

print(">>> [OK] Pipeline ETL finalizado con éxito.")