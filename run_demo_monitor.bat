@echo off
chcp 65001 >nul
title BrandHub Docs Portal & Selenium Live Demo Monitor
cd /d "%~dp0"
echo ================================================================================
echo   KHOI DONG BRANDHUB DOCS PORTAL VA SELENIUM LIVE DEMO MONITOR
echo   - Docs Portal ^& Live Demo UI : http://localhost:5180/demo-monitor?mode=auto
echo   - Bàn điều khiển HTML (:3999) : http://localhost:3999
echo   - Local Test Target          : http://localhost:3000
echo   - Production Target          : https://brandhub.id.vn
echo ================================================================================

netstat -ano | findstr ":3999 " | findstr "LISTENING" >nul
if errorlevel 1 (
    echo [1/2] Dang khoi dong Selenium Monitor Server tren cong :3999...
    start "BrandHub Selenium Monitor (:3999)" cmd /k "python -X utf8 scripts/demo/selenium_demo_monitor.py"
) else (
    echo [1/2] Selenium Monitor Server da san sang tren cong :3999.
)

netstat -ano | findstr ":5180 " | findstr "LISTENING" >nul
if errorlevel 1 (
    echo [2/2] Dang khoi dong Vite Docs Portal tren cong :5180...
    start "" cmd /c "timeout /t 3 /nobreak >nul & start \"\" \"http://localhost:5180/demo-monitor?mode=auto\""
    npm run dev -- --port 5180
) else (
    echo [2/2] Docs Portal da san sang tren cong :5180. Dang mo giao dien...
    start "" "http://localhost:5180/demo-monitor?mode=auto"
)
