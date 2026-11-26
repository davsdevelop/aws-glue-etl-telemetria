# Pipeline ETL con AWS Glue 4.0 (PySpark) y Docker

![AWS Glue](https://img.shields.io/badge/AWS%20Glue-4.0-FF9900?style=flat&logo=amazonaws&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-3.3-E25A1C?style=flat&logo=apachespark&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Local%20Dev-2496ED?style=flat&logo=docker&logoColor=white)
![Parquet](https://img.shields.io/badge/Format-Parquet%20(Snappy)-50ABF1?style=flat)

Pipeline ETL desarrollado como práctica de diplomatura en Data Science para procesar telemetría energética de equipos industriales. Utiliza la imagen oficial de **AWS Glue (`amazon/aws-glue-libs`)** en Docker para desarrollar, transformar y validar datos localmente antes de su despliegue en la nube.

---

## Arquitectura del Flujo

```mermaid
flowchart LR
    A[("CSV Crudo<br/>data/raw/telemetria_equipos.csv")] --> B["AWS Glue 4.0 (Docker)<br/>scripts/etl_telemetria.py"]
    B --> C{"Transformaciones PySpark<br/>• trim() en textos<br/>• Casteo double / date<br/>• Cálculo consumo_kwh"}
    C --> D[("Parquet (Snappy)<br/>data/processed/")]
    D --> E["Validación Analítica<br/>Spark SQL (validar_sql.py)"]
```

---

## Transformación: Antes vs. Después

**Datos crudos (`telemetria_equipos.csv`):** espacios inconsistentes en textos, tipos como `string` y sin métrica energética.

| id_equipo | zona | voltaje_v | corriente_a | horas_operacion | fecha |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `  EQ-101 ` | `  Planta Norte  ` | `220` | `12.5` | `8.0` | `2026-10-01` |
| `EQ-102  ` | `Planta Sur   ` | `220` | `15.0` | `6.5` | `2026-10-01` |

**Datos procesados (`Parquet`):** textos normalizados, tipos estrictos (`double`, `date`) y columna derivada `consumo_kwh = round((voltaje_v * corriente_a / 1000) * horas_operacion, 2)`.

| id_equipo | zona | voltaje_v | corriente_a | horas_operacion | fecha | consumo_kwh |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `EQ-101` | `Planta Norte` | `220.0` | `12.5` | `8.0` | `2026-10-01` | **22.0** |
| `EQ-102` | `Planta Sur` | `220.0` | `15.0` | `6.5` | `2026-10-01` | **21.45** |

---

## Estructura del Proyecto

```text
.
├── data/
│   ├── raw/
│   │   └── telemetria_equipos.csv       # Dataset de entrada con espacios sucios
│   └── processed/
│       └── telemetria_parquet/          # Salida columnar Parquet (Snappy)
├── docs/
│   └── captures/                        # Capturas de evidencia de ejecución
├── scripts/
│   ├── etl_telemetria.py                # Job ETL en PySpark / AWS Glue
│   └── validar_sql.py                   # Consultas analíticas con Spark SQL
├── docker-compose.yml                   # Contenedor oficial amazon/aws-glue-libs
├── requirements.txt                     # Dependencias de referencia local
└── README.md
```

---

## Cómo ejecutar el proyecto localmente

Requiere únicamente **Docker** y **Docker Compose**.

```bash
# 1. Levantar el contenedor oficial de AWS Glue 4.0
docker compose up -d

# 2. Ejecutar el job ETL (CSV -> Parquet)
docker compose exec glue-local /home/glue_user/spark/bin/spark-submit /home/glue_user/workspace/scripts/etl_telemetria.py

# 3. Ejecutar validación analítica con Spark SQL
docker compose exec glue-local /home/glue_user/spark/bin/spark-submit /home/glue_user/workspace/scripts/validar_sql.py

# 4. Detener el entorno al finalizar
docker compose down
```

---

## Resultados

Consumo agregado por zona (12 registros procesados):

| Zona | Registros | Consumo total (kWh) | Consumo promedio (kWh) |
| :--- | ---: | ---: | ---: |
| Planta Sur | 4 | 168.59 | 42.15 |
| Planta Norte | 4 | 121.92 | 30.48 |
| Bodega Central | 4 | 86.88 | 21.72 |

Top 3 equipos por consumo acumulado:

| Equipo | Zona | Horas operadas | Consumo total (kWh) |
| :--- | :--- | ---: | ---: |
| EQ-105 | Planta Sur | 17.5 | 121.09 |
| EQ-103 | Planta Norte | 19.5 | 78.47 |
| EQ-102 | Planta Sur | 14.5 | 47.50 |

---

## Evidencia de Ejecución

<details>
<summary><strong>1. Ejecución del Job ETL en PySpark (Antes y Después)</strong></summary>
<br>
<p><strong>Datos crudos (RAW):</strong></p>
<img src="docs/captures/01_etl_raw.png" alt="Datos crudos RAW" width="100%">
<br><br>
<p><strong>Datos transformados (PROCESSED):</strong></p>
<img src="docs/captures/02_etl_processed.png" alt="Datos procesados PROCESSED" width="100%">
</details>

<details>
<summary><strong>2. Generación de archivos columnares Parquet (Snappy)</strong></summary>
<br>
<img src="docs/captures/03_salida_parquet.png" alt="Salida Parquet" width="100%">
</details>

<details>
<summary><strong>3. Validación analítica con Spark SQL</strong></summary>
<br>
<img src="docs/captures/04_validacion_sql.png" alt="Validación Spark SQL" width="100%">
</details>



## Arquitectura del Flujo

<p align="center">
  <img src="docs/captures/arquitectura_etl.png" alt="Arquitectura ETL AWS Glue Local vs Nube" width="100%">
</p>