@echo off
echo Starting Andalusian Champions League Website...
python app.py
timeout /t 2 >nul
start http://127.0.0.1:5000
pause
