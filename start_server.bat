@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting V2 Standoff Server...
echo.
echo MongoDB must be running on localhost:27017
echo WebSocket endpoint: ws://localhost:25505
echo HTTP endpoint:      http://localhost:25506
echo.
python server.py
pause
