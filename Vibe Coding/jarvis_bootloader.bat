@echo off
TITLE Jarvis Core Bootloader
cd /d "%~dp0"

echo [JARVIS] Booting internal cognitive modules...
start /min cmd /c "uvicorn jarvis.server:app"

echo [JARVIS] Booting visual rendering HUD...
start /min cmd /c "npm run dev"

echo [JARVIS] Synchronizing...
timeout /t 4 /nobreak

echo [JARVIS] Projecting to desktop...
start chrome --app=http://localhost:5173 --autoplay-policy=no-user-gesture-required

exit
