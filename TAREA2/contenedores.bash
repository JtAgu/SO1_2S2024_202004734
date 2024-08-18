#!/bin/bash

for i in {1..10}
do 
    CONTAINER_NAME=$(head /dev/urandom | tr -dc A-Za-z0-9|head -c 8)
    docker run -d --name $CONTAINER_NAME alpine sleep infinity
    echo "Contnedor creado: " $CONTAINER_NAME
done
