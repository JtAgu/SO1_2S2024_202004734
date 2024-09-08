from fastapi import FastAPI # type: ignore
import os
import json
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
