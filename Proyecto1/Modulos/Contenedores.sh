#!/bin/bash

# Lista de imágenes de alto y bajo consumo
ALTO_CONSUMO=("redis" "alpine/stress")
BAJO_CONSUMO=("alpine" "busybox")

# Función para crear contenedores
crear_contenedores() {
    # Generar un nombre aleatorio para el contenedor
    CONTAINER_NAME=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 8)

    # Generar un número aleatorio entre 0 y 1
    RANDOM_NUM=$((RANDOM % 2))

    if [ $RANDOM_NUM -eq 0 ]; then
        # Seleccionar aleatoriamente una imagen de alto consumo
        IMAGE=${ALTO_CONSUMO[$((RANDOM % ${#ALTO_CONSUMO[@]}))]}
    else
        # Seleccionar la única imagen de bajo consumo
        IMAGE=${BAJO_CONSUMO[$((RANDOM % ${#BAJO_CONSUMO[@]}))]}
    fi

    # Crear el contenedor con la imagen seleccionada
    sudo docker run -d --name $CONTAINER_NAME $IMAGE sleep infinity
    echo "Contenedor creado: $CONTAINER_NAME con la imagen $IMAGE"
}

# Bucle infinito para el ciclo de eliminación y creación
sudo insmod sysinfo_202004734.ko
while true; do
    echo "Creando contenedores..."
    for i in {1..10};do
        crear_contenedores
    done
    echo "Esperando los 30s..."
    sleep 55
done
sudo rmmod sysinfo_202004734.ko

