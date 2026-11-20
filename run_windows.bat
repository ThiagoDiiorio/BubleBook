@echo off
setlocal
cd /d "%~dp0"
title Buble Book - Servidor local

if not exist ".venv\Scripts\python.exe" (
    echo Criando ambiente Python...
    py -3 -m venv .venv
    if errorlevel 1 (
        echo Nao foi possivel criar o ambiente. Verifique se o Python 3 esta instalado.
        pause
        exit /b 1
    )
)

if not exist ".venv\installed.flag" (
    echo Instalando dependencias pela primeira vez...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo A instalacao falhou. Confira sua conexao com a internet.
        pause
        exit /b 1
    )
    type nul > ".venv\installed.flag"
)

echo Iniciando Buble Book em http://127.0.0.1:5000 ...
start "" cmd /c "ping 127.0.0.1 -n 3 >nul & start http://127.0.0.1:5000"
".venv\Scripts\python.exe" app.py
pause
