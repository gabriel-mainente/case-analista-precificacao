@echo off
echo Iniciando configuracao do ambiente...

if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

:: Ativa o ambiente virtual
call venv\Scripts\activate

:: Instala as dependencias
echo Instalando dependencias...
pip install -r requirements.txt

:: Executa a automacao/dashboard
echo Iniciando dashboard...
streamlit run app.py