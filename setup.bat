@echo off
REM Script para configurar y ejecutar el proyecto en Windows
REM Este script configura la BD e instala dependencias

echo ===================================
echo Sistema de Gestion de Restaurante
echo ===================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar si psql (PostgreSQL) está instalado
psql --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: PostgreSQL no está instalado o psql no está en el PATH
    echo Instala PostgreSQL desde: https://www.postgresql.org/download/windows/
    pause
    exit /b 1
)

echo [1] Creando entorno virtual...
if not exist .venv (
    python -m venv .venv
    echo - Entorno virtual creado
) else (
    echo - Entorno virtual ya existe
)

echo.
echo [2] Activando entorno virtual...
call .venv\Scripts\activate.bat
echo - Entorno virtual activado

echo.
echo [3] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo - Dependencias instaladas

echo.
echo [4] Verificando conexion a PostgreSQL...
echo Por favor ingresa la contraseña del usuario postgres cuando se pida
psql -U postgres -c "SELECT version();" >nul 2>&1
if errorlevel 1 (
    echo ERROR: No se puede conectar a PostgreSQL
    echo Asegúrate de que:
    echo - PostgreSQL está instalado y corriendo
    echo - El usuario 'postgres' existe
    pause
    exit /b 1
)
echo - Conexion exitosa

echo.
echo [5] Creando usuario y base de datos...
psql -U postgres -tc "SELECT 1 FROM pg_user WHERE usename = 'joaquin';" | find "1" >nul 2>&1
if errorlevel 1 (
    echo Creando usuario 'joaquin'...
    psql -U postgres -c "CREATE USER joaquin WITH PASSWORD 'saki7089';" >nul 2>&1
) else (
    echo - Usuario 'joaquin' ya existe
)

psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'restaurant_proyect';" | find "1" >nul 2>&1
if errorlevel 1 (
    echo Creando base de datos 'restaurant_proyect'...
    psql -U postgres -c "CREATE DATABASE restaurant_proyect OWNER joaquin;" >nul 2>&1
) else (
    echo - Base de datos 'restaurant_proyect' ya existe
)

echo.
echo [6] Inicializando base de datos...
python init_db.py
if errorlevel 1 (
    echo ERROR: No se pudo inicializar la BD
    pause
    exit /b 1
)

echo.
echo ===================================
echo CONFIGURACION COMPLETADA EXITOSAMENTE
echo ===================================
echo.
echo Para ejecutar la aplicacion:
echo   python Restaurante.py
echo.
pause
