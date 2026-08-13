@echo off
title DDW-X COMMAND & CONTROL (C2) DASHBOARD
echo ===============================================================================
echo   DDW-X COMMAND & CONTROL (C2) - ZERO-KNOWLEDGE INTELLIGENCE SUITE
echo ===============================================================================
echo  [*] Launching Threaded C2 Web API Server on port 8080...
echo  [*] Web Dashboard URL: http://127.0.0.1:8080
echo -------------------------------------------------------------------------------
python src/core/api/ddwx_api.py --port 8080
pause
