@echo off
chcp 65001 >nul
title BrandHub Docs Portal & Selenium Live Demo Monitor
cd /d "%~dp0"
echo ================================================================================
echo   KHOI DONG BRANDHUB DOCS PORTAL VA SELENIUM LIVE DEMO MONITOR
echo   - Docs Portal & Live Demo UI : http://localhost:5180/demo-monitor
echo   - Selenium Control Server    : http://localhost:3999
echo   - Local Test Target          : http://localhost:5173
echo   - Production Target          : https://brandhub.id.vn
echo ================================================================================

start "BrandHub Selenium Monitor (:3999)" cmd /k "python -X utf8 scripts/demo/selenium_demo_monitor.py"
start "" "http://localhost:5180/demo-monitor"
npm run dev
