# AGENTE.md — Contexto y Memoria del Proyecto

## 1. Propósito del Proyecto
Proyecto demostrativo de portafolio (origen: práctica de diplomatura en Data Science) que implementa un pipeline ETL utilizando **AWS Glue (PySpark)** en un entorno 100% local mediante la imagen oficial de Docker `amazon/aws-glue-libs`.

## 2. Arquitectura y Flujo
1. **Ingesta (Raw):** Archivo CSV crudo en `data/raw/telemetria_equipos.csv`.
2. **Transformación (AWS Glue / PySpark):**
   - Lectura mediante `GlueContext` / `SparkSession`.
   - Limpieza de espacios en blanco (`trim`) en columnas de texto (`id_equipo`, `zona`).
   - Casteo explícito de tipos numéricos (`double`) y fecha (`date`).
   - Generación de columna calculada:
     `consumo_kwh = round((voltaje_v * corriente_a / 1000) * horas_operacion, 2)`
3. **Almacenamiento (Processed):** Escritura en formato columnar **Parquet** en `data/processed/`.
4. **Validación:** Consultas analíticas con **Spark SQL** directamente sobre los archivos `.parquet`.

## 3. Estructura del Repositorio
- `data/raw/`: Datos crudos de entrada (CSV).
- `data/processed/`: Datos transformados de salida (Parquet).
- `scripts/`: Scripts PySpark de AWS Glue y validación SQL.
- `docs/captures/`: Evidencia visual de ejecución para el README.
- `docker-compose.yml`: Definición del contenedor oficial de AWS Glue.
- `requirements.txt`: Dependencias Python de referencia (`pyspark==3.3.0`).

## 4. Reglas para el Agente (OpenCode)
- Mantener el código compatible con AWS Glue 4.0 (PySpark).
- No requerir credenciales ni servicios pagos de AWS; todo debe ejecutarse localmente en Docker.
- Usar rutas relativas dentro del contenedor (`/home/glue_user/workspace/...`).
- Documentar los cambios y mantener el código limpio y comentado en español.

## 5. Estado de Fases
- [x] Fase 1: Repositorio, dataset CSV crudo y `AGENTE.md`.
- [x] Fase 2: Configuración de Docker (`amazon/aws-glue-libs`).
- [x] Fase 3: Script ETL en PySpark y generación de `.parquet`.
- [x] Fase 4: Validación con Spark SQL y capturas.
- [ ] Fase 5: Diagrama, README Case Study. (Avanzada: diagrama Mermaid,
      instrucciones y resultados en README. Pendiente: tarjeta de portafolio.)
