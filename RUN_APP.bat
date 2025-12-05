@echo off
echo Starting FarmOG Station...
cd /d "%~dp0"
streamlit run app/app.py
pause
