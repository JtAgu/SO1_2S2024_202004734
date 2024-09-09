from fastapi import FastAPI, HTTPException # type: ignore
import os
import json
from typing import Dict, Any
from pydantic import BaseModel
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

app = FastAPI()

class LogProcess(BaseModel):
    pid: int
    container_id: str
    name: str
    memory_usage: float
    cpu_usage: float
    vcz: float
    rss: float
    date: str
    time: str


class system_info(BaseModel):
    processes: List[LogProcess]
    total_ram: int
    free_ram: int
    uso_ram: int

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/logs")
def post_logs(logs_proc: List[LogProcess]):
    logs_file = 'code/logs/logs.json'
    print(logs_proc)
    try:
        os.makedirs(os.path.dirname(logs_file), exist_ok=True)  # Crea directorios intermedios si no existen
    except Exception as e:
        return {"received": False, "error": f"Error creating directory: {str(e)}"}


    # Checamos si existe el archivo logs.json
    try:

        if os.path.exists(logs_file):
            # Leemos el archivo logs.json
            with open(logs_file, 'r') as file:
                existing_logs = json.load(file)
        else:
            # Sino existe, creamos una lista vacía
            existing_logs = []

        # Agregamos los nuevos logs a la lista existente
        new_logs = [log.dict() for log in logs_proc]
        existing_logs.extend(new_logs)

        # Escribimos la lista de logs en el archivo logs.json
        with open(logs_file, 'w') as file:
            json.dump(existing_logs, file, indent=4)

        return {"received": True, "error": None}

    except Exception as e:
        # Si ocurre un error, devolvemos un mensaje de error
        return {"received": False, "error": str(e)}


@app.post("/logs_mem")
def post_logs(logs_proc: Dict[str, Any]):
    logs_file = 'code/logs/logs_m.json'
    print(logs_proc)
    try:
        os.makedirs(os.path.dirname(logs_file), exist_ok=True)  # Crea directorios intermedios si no existen
    except Exception as e:
        return {"received": False, "error": f"Error creating directory: {str(e)}"}


    # Checamos si existe el archivo logs.json
    try:
        total_ram = logs_proc.get("total_ram", 0)
        free_ram = logs_proc.get("free_ram", 0)
        uso_ram = logs_proc.get("uso_ram", 0)

        logs_data = {
            "total_ram": total_ram,
            "free_ram": free_ram,
            "uso_ram": uso_ram,
        }

        # Write data to JSON file, overwriting existing data
        with open(logs_file, 'w') as file:
            json.dump(logs_data, file, indent=4)
        
        return {"received": True, "error": None}

    except Exception as e:
        # Si ocurre un error, devolvemos un mensaje de error
        return {"received": False, "error": str(e)}


@app.get("/ram")
def get_graphic_ram():
    logs_file = 'code/logs/logs_m.json'
    
    # Verificar si el archivo existe
    try:

        if os.path.exists(logs_file):
            # Leer el archivo JSON
            with open(logs_file, 'r') as file:
                existing_logs = json.load(file)
        else:
            existing_logs=[]


        print(existing_logs)
        # Convertir el contenido a un DataFrame de pandas
        df = pd.DataFrame([existing_logs])
        print(df)
        # Extraer los datos de memoria, asegurándose de que sean escalares y no NaN
        if df.empty:
            raise HTTPException(status_code=500, detail="DataFrame is empty")

        total_ram = df['total_ram'].iloc[0] if 'total_ram' in df.columns and not pd.isna(df['total_ram'].iloc[0]) else 0
        free_ram = df['free_ram'].iloc[0] if 'free_ram' in df.columns and not pd.isna(df['free_ram'].iloc[0]) else 0
        uso_ram = df['uso_ram'].iloc[0] if 'uso_ram' in df.columns and not pd.isna(df['uso_ram'].iloc[0]) else 0

        # Imprimir los valores para depuración
        print(f"total_ram: {total_ram}, free_ram: {free_ram}, uso_ram: {uso_ram}")

        # Crear el gráfico de pastel
        plt.figure(figsize=(8, 8))
        plt.pie(
            [total_ram - uso_ram, uso_ram, free_ram],
            labels=['Available RAM', 'Used RAM', 'Free RAM'],
            autopct='%1.1f%%',
            startangle=140
        )
        plt.title('Memory Usage Distribution')

        # Guardar el gráfico como archivo
        output_file = 'code/logs/memory_usage_pie_chart.png'
        plt.savefig(output_file)
        plt.close()
        
        # Verificar que el archivo ha sido creado
        file_exists = os.path.exists(output_file)
        print(f"File exists after saving: {file_exists}")

        # Retornar respuesta
        return {"message": "Pie chart created successfully", "file": output_file}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chart: {str(e)}")


@app.get("/cpu")
def get_graphic_cpu():
    logs_file = 'code/logs/logs.json'
    # Checamos si existe el archivo logs.json
    if os.path.exists(logs_file):
        # Leemos el archivo logs.json
        with open(logs_file, 'r') as file:
            existing_logs = json.load(file)
    else:
        # Sino existe, creamos una lista vacía
        existing_logs = []

    print(existing_logs)
    # Escribimos la lista de logs en el archivo logs.json
    df = pd.DataFrame(existing_logs)

    # Combinar 'date' y 'time' en un solo campo datetime
    df['timestamp'] = pd.to_datetime(df['time'])

    # Agrupar por timestamp y sumar los valores de cpu_usage
    df_grouped = df.groupby('timestamp')['cpu_usage'].sum().reset_index()

    # Ordenar por timestamp
    df_grouped = df_grouped.sort_values('timestamp')

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df_grouped['timestamp'], df_grouped['cpu_usage'], marker='o', linestyle='-', color='b', label='CPU Usage')
    plt.xlabel('Time')
    plt.ylabel('CPU Usage')
    plt.title('CPU Usage Over Time')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)  # Rotar etiquetas de tiempo para mejor visualización
    plt.tight_layout()       # Ajustar el diseño para que todo el texto sea visible
    
    # Guardar el gráfico como archivo
    output_file = '/code/logs/cpu_usage.png'
    plt.savefig(output_file)
    plt.close()

    return {"received": output_file}



    return {"received": output_file}

@app.get("/memory")
def get_graphic_memory():
    logs_file = 'code/logs/logs.json'
    # Checamos si existe el archivo logs.json
    if os.path.exists(logs_file):
        # Leemos el archivo logs.json
        with open(logs_file, 'r') as file:
            existing_logs = json.load(file)
    else:
        # Sino existe, creamos una lista vacía
        existing_logs = []

    df = pd.DataFrame(existing_logs)

    # Combinar 'date' y 'time' en un solo campo datetime
    df['timestamp'] = pd.to_datetime(df['time'])

    # Agrupar por timestamp y sumar los valores de memory_usage
    df_grouped = df.groupby('timestamp')['memory_usage'].sum().reset_index()

    # Ordenar por timestamp
    df_grouped = df_grouped.sort_values('timestamp')

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df_grouped['timestamp'], df_grouped['memory_usage'], marker='o', linestyle='-', color='b', label='Memory Usage')
    plt.xlabel('Time')
    plt.ylabel('Memory Usage')
    plt.title('Memory Usage Over Time')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)  # Rotar etiquetas de tiempo para mejor visualización
    plt.tight_layout()       # Ajustar el diseño para que todo el texto sea visible
    
    # Guardar el gráfico como archivo
    output_file = '/code/logs/memory_usage.png'
    plt.savefig(output_file)
    plt.close()
    
    return {"received": output_file}
