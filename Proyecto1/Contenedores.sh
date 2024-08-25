#!/bin/bash

# Lista de imágenes de alto y bajo consumo
ALTO_CONSUMO=("redis" "progrium/stress")
BAJO_CONSUMO=("alpine")  # Solo una imagen de bajo consumo

# Función para crear contenedores
crear_contenedores() {
    local cantidad=$1
    for i in $(seq 1 $cantidad)
    do 
        # Generar un nombre aleatorio para el contenedor
        CONTAINER_NAME=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 8)

        # Generar un número aleatorio entre 0 y 1
        RANDOM_NUM=$((RANDOM % 2))

        if [ $RANDOM_NUM -eq 0 ]; then
            # Seleccionar aleatoriamente una imagen de alto consumo
            IMAGE=${ALTO_CONSUMO[$((RANDOM % ${#ALTO_CONSUMO[@]}))]}
        else
            # Seleccionar la única imagen de bajo consumo
            IMAGE=${BAJO_CONSUMO[0]}
        fi

        # Crear el contenedor con la imagen seleccionada
        sudo docker run -d --name $CONTAINER_NAME $IMAGE sleep infinity
        echo "Contenedor creado: $CONTAINER_NAME con la imagen $IMAGE"
    done
}

# Bucle infinito para el ciclo de eliminación y creación
while true
do
    # Crear los primeros 10 contenedores
    echo "Creando los primeros 10 contenedores..."
    crear_contenedores 10

    # Pausa de 10 segundos
    echo "Esperando 20 segundos..."
    sleep 20

    # Eliminar los contenedores creados
    echo "Eliminando los contenedores creados..."
    sudo docker rm -f $(sudo docker ps -aq)

    # Repetir el proceso creando 10 nuevos contenedores
done
