#!/usr/bin/env bash
# Actualizar los paquetes e instalar dependencias necesarias
apt-get update && apt-get install -y curl gnupg2 apt-transport-https

# Agregar repositorio de Microsoft para ODBC Driver
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Instalar el driver ODBC
apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Limpiar caché para reducir tamaño de la imagen
apt-get clean
