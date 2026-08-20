@echo off
chcp 65001 >nul
cd /d "C:\Users\T1UKLL7\Desktop\Workstation\employee agent"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\start_demo.ps1"
pause