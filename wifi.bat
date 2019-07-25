@echo off
pause
mode 1000
title wifi
cls
:a
set /p wifiname=SSID:
netsh wlan show profiles %wifiname% key=clear
goto a