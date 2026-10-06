import json
import boto3
import csv
import io

# Se inicializa el cliente de S3 fuera del handler para aprovechar 
# la reutilización de conexiones en invocaciones en caliente (warm starts).
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Definición de variables de entorno/rutas
    input_bucket = "bld-tseed-workshop-input-semillero-2026-q4-a"
    # Nota: Si el archivo no tiene extensión en S3, deja el nombre exacto. 
    # Si tiene extensión, asegúrate de añadir '.csv' al final de esta variable.
    input_key = "sample_users.csv" 
    
    output_bucket = "bld-tseed-workshop-output-semillero-2026-q4-a"
    output_folder = "yohan_ospina/"
    
    try:
        # Paso 1: Extraer (Leer) el archivo del bucket de origen
        response = s3_client.get_object(Bucket=input_bucket, Key=input_key)
        
        # Se decodifica el archivo asumiendo codificación UTF-8
        csv_content = response['Body'].read().decode('utf-8')
        
        # Paso 2: Transformar (Parsear el CSV)
        # csv.DictReader convierte automáticamente cada fila en un diccionario 
        # usando la primera fila del CSV como las llaves (nombres de las columnas).
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        # Paso 3: Cargar (Escribir cada fila como un JSON individual)
        # Se usa enumerate para llevar un conteo y darle un nombre único a cada JSON
        archivos_creados = 0
        
        for index, row in enumerate(csv_reader, start=1):
            # Convertir el diccionario de la fila a un string JSON
            json_data = json.dumps(row, ensure_ascii=False)
            
            # Construir la ruta de destino: yohan_ospina/fila_1.json, yohan_ospina/fila_2.json...
            output_key = f"{output_folder}fila_{index}.json"
            
            # Guardar en S3
            s3_client.put_object(
                Bucket=output_bucket,
                Key=output_key,
                Body=json_data,
                ContentType='application/json'
            )
            archivos_creados += 1
            
            # Condición de seguridad para asegurar que solo sean 100 filas,
            # en caso de que el archivo real sea más largo de lo esperado.
            if archivos_creados == 100:
                break
                
        return {
            'statusCode': 200,
            'body': json.dumps(f'Proceso completado. Se crearon {archivos_creados} archivos JSON en la carpeta {output_folder}.')
        }
        
    except Exception as e:
        print(f"Error grave durante el procesamiento: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error en la ejecución: {str(e)}')
        }