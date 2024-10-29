import json
from random import randrange
from locust import HttpUser, between, task

debug = False

def printDebug(msg):
    if debug:
        print(msg)

class Reader:
    def __init__(self):
        self.array = []

    def pickRandom(self):
        length = len(self.array)
        if length > 0:
            random_index = randrange(0, length - 1) if length > 1 else 0
            return self.array.pop(random_index)
        else:
            print(">> Reader: No encontramos ningún valor o registro en el archivo.")
            return None

    def load(self):
        print(">> Reader: Estamos iniciando la lectura del archivo de datos.")
        try:
            with open("olimpiadas.json", 'r') as data_file:
                self.array = json.load(data_file)
        except Exception as error:
            print(f'>> Reader: No se cargaron los datos, error: {error}')

class MessageTraffic(HttpUser):
    wait_time = between(0.1, 0.9)
    reader = Reader()
    reader.load()

    def on_start(self):
        printDebug(">> MessageTraffic: Iniciamos el envío de tráfico")

    @task
    def PostMessage(self):
        random_data = self.reader.pickRandom()
        if random_data is not None:
            printDebug(json.dumps(random_data))
            if random_data["faculty"] == "Ingenieria":
                self.client.post("https://34.36.176.35/ingenieria", json=random_data)
            else:
                self.client.post("/students", json=random_data)
        else:
            print(">> MessageTraffic: Envío de tráfico a finalizado, no hay más registros para enviar.")
            self.stop()

    @task
    def GetMessages(self):
        self.client.get("/")
