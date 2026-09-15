@echo off
echo Adding firewall rule for GRC Agent (port 7860)...
netsh advfirewall firewall add rule name="GRC Agent 7860" dir=in action=allow protocol=TCP localport=7860
echo.
echo Done! Firewall rule added successfully.
echo.
echo GRC Agent is now accessible at:
echo   http://10.126.142.71:7860  (Wi-Fi IP)
echo   http://10.114.80.73:7860   (VPN IP)
echo.
echo Login: admin / grc2026
echo.
pause
