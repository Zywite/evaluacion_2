#!/bin/bash

# Script para configurar y ejecutar el proyecto en Linux/Mac
# Este script configura la BD e instala dependencias

echo "==================================="
echo "Sistema de Gestion de Restaurante"
echo "==================================="
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    exit 1
fi

# Verificar si psql (PostgreSQL) está instalado
if ! command -v psql &> /dev/null; then
    echo "ERROR: PostgreSQL no está instalado"
    echo "Instala PostgreSQL con: sudo apt-get install postgresql postgresql-contrib (en Ubuntu/Debian)"
    exit 1
fi

echo "[1] Creando entorno virtual..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "- Entorno virtual creado"
else
    echo "- Entorno virtual ya existe"
fi

echo ""
echo "[2] Activando entorno virtual..."
source .venv/bin/activate
echo "- Entorno virtual activado"

echo ""
echo "[3] Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi
echo "- Dependencias instaladas"

echo ""
echo "[4] Verificando conexion a PostgreSQL..."
psql -U postgres -c "SELECT version();" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: No se puede conectar a PostgreSQL"
    echo "Asegúrate de que PostgreSQL está corriendo:"
    echo "- sudo systemctl start postgresql (en Linux)"
    echo "- brew services start postgresql (en Mac)"
    exit 1
fi
echo "- Conexion exitosa"

echo ""
echo "[5] Creando usuario y base de datos..."
psql -U postgres -tc "SELECT 1 FROM pg_user WHERE usename = 'joaquin';" | grep -q 1
if [ $? -ne 0 ]; then
    echo "Creando usuario 'joaquin'..."
    psql -U postgres -c "CREATE USER joaquin WITH PASSWORD 'saki7089';" > /dev/null 2>&1
else
    echo "- Usuario 'joaquin' ya existe"
fi

psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'restaurant_proyect';" | grep -q 1
if [ $? -ne 0 ]; then
    echo "Creando base de datos 'restaurant_proyect'..."
    psql -U postgres -c "CREATE DATABASE restaurant_proyect OWNER joaquin;" > /dev/null 2>&1
else
    echo "- Base de datos 'restaurant_proyect' ya existe"
fi

echo ""
echo "[6] Inicializando base de datos..."
python init_db.py
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo inicializar la BD"
    exit 1
fi

echo ""
echo "==================================="
echo "CONFIGURACION COMPLETADA EXITOSAMENTE"
echo "==================================="
echo ""
echo "Para ejecutar la aplicacion:"
echo "  python Restaurante.py"
echo ""
