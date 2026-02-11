@echo off
chcp 65001 >nul

REM Criar venv se nao existir
IF NOT EXIST .venv (
    py -m venv .venv 
)

REM Ativar venv no CMD
CALL .\.venv\Scripts\activate.bat

REM Garantir pip atualizado
python -m pip install --upgrade pip

REM Instalar dependencias declaradas
IF EXIST requirements.txt.txt (
    pip install -r requirements.txt.txt
)

REM Instalar dependencias adicionais usadas no projeto
pip install watchdog Pillow reportlab openpyxl XlsxWriter

REM Iniciar o bot com watchdog
python run_bot_with_watchdog.py

pause
