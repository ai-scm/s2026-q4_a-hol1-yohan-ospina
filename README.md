# HandsOnLab 1: AWS Data Engineering Pipeline (S3 + Lambda + Glue + Athena)

---

## Descripción del Proyecto

Este proyecto documenta la implementación de un **Pipeline Serverless de Procesamiento y Analítica de Datos** en Amazon Web Services (AWS) desarrollado durante el HandsOnLab 1 (HOL 1) del programa de Semilleros Blend360.

El flujo toma datos semiestructurados/no estructurados en formato CSV, los transforma mediante computación serverless en registros independientes JSON, rastrea su esquema de manera automática y habilita consultas analíticas en SQL estándar.

---

## Arquitectura del Pipeline

```
  ┌────────────────────────────────┐
  │   Amazon S3 (Input Bucket)     │
  │   100_users.csv                │
  └───────────────┬────────────────┘
                  │
                  ▼
  ┌────────────────────────────────┐
  │       AWS Lambda (Python)      │
  │ bld_tseed_Workshop_yohan_ospina│
  └───────────────┬────────────────┘
                  │
                  ▼
  ┌────────────────────────────────┐
  │   Amazon S3 (Output Bucket)    │
  │   yohan_ospina/                │
  └───────────────┬────────────────┘
                  │
                  ▼
  ┌────────────────────────────────┐
  │   AWS Glue Crawler & Catalog   │
  │   Inferia de Esquema           │
  └───────────────┬────────────────┘
                  │
                  ▼
  ┌────────────────────────────────┐
  │         Amazon Athena          │
  │   Consultas SQL Interactivas   │
  └────────────────────────────────┘
```

---

## Componentes e Implementación

### 1. Almacenamiento Inicial (Amazon S3 Input)
* **Bucket origen:** `bld-tseed-workshop-input-semillero-2026-q4-a`
* **Subcarpeta:** `yohan_ospina/`
* **Archivo de entrada:** Dataset CSV de 100 registros.

### 2. Procesamiento Serverless (AWS Lambda)
* **Nombre de la función:** `bld-tseed-workshop-yohan-ospina`
* **Runtime:** Python 3
* **Configuración:**
  * **Timeout:** Incrementado a 2 minutos.
* **Lógica:** El script `lambda_function.py` lee el archivo CSV de entrada, parsea cada fila utilizando `pandas` y exporta **100 archivos JSON independientes** en la subcarpeta del bucket de salida.

### 3. Almacenamiento Transformado (Amazon S3 Output)
* **Bucket destino:** `bld-tseed-workshop-output-semillero-2026-q4-a`
* **Subcarpeta:** `yohan_ospina/`
* **Estructura generada:** 100 archivos estructurados (`fila_1.json`, `fila_2.json`, ..., `fila_100.json`).

### 4. Catalogación Automática (AWS Glue)
* **Crawler:** `bld-tseed-workshop-yohan-ospina`
* **Data Source:** `s3://bld-tseed-workshop-output-semillero-2026-q4-a/yohan_ospina/`
* **Database Target:** `bld-tseed-workshop`
* **Resultado:** Inferencia automática del esquema (columnas como `age`, `languages`, `education`, etc.) y creación de la tabla analítica.

### 5. Consultas Analíticas (Amazon Athena)
Ejecución de sentencias SQL sobre los archivos JSON indexados en el Data Catalog:

```sql
-- Consulta general
SELECT * 
FROM "BLDTC Workshop"."bld_tseed_workshop_output_yohan_ospina" 
LIMIT 10;

-- Consulta con filtro demográfico y conversión de tipo (Casting)
SELECT name, age, languages 
FROM "BLDTC Workshop"."bld_tseed_workshop_output_yohan_ospina"
WHERE CAST(age AS INT) > 35 AND languages LIKE '%English%';
```
