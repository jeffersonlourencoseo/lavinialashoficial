@echo off
cd /d "%~dp0"
echo Gerando o site...
python build\build.py
echo.
echo Abrindo http://localhost:8080  (feche esta janela para parar o servidor)
start "" http://localhost:8080
python -m http.server 8080 --directory site --bind 127.0.0.1
