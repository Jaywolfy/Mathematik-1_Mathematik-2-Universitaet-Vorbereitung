@echo off
rem ==========================================================================
rem  Python-Vorkurs-Lernquiz - Start fuer Windows (Doppelklick)
rem  Sucht Python 3.10+ (py -3, python, python3 und die ueblichen
rem  Installationsordner) und startet vorkurs_quiz.py.
rem  Alle Parameter werden weitergereicht, z. B.:  Start.bat --terminal
rem  Hinweis: Diese Datei braucht Windows-Zeilenenden (CRLF) und nur ASCII.
rem ==========================================================================
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title Python-Vorkurs-Lernquiz
set "INSTALLIERT="

:suchen
set "PY="
call :pruefe py -3
if defined PY goto starten
call :pruefe python
if defined PY goto starten
call :pruefe python3
if defined PY goto starten
rem Nach einer frischen Installation kennt dieses Fenster den neuen PATH noch
rem nicht. Deshalb auch direkt in den ueblichen Installationsordnern suchen.
call :pruefe "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" -3
if defined PY goto starten
if exist "%SystemRoot%\py.exe" call :pruefe "%SystemRoot%\py.exe" -3
if defined PY goto starten
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*" "%ProgramFiles%\Python3*") do (
    if not defined PY if exist "%%~fD\python.exe" call :pruefe "%%~fD\python.exe"
)
if defined PY goto starten
goto keinpython

:starten
rem "call", damit auch Python-Starter funktionieren, die selbst .bat-Dateien sind
call %PY% vorkurs_quiz.py %*
set "CODE=%ERRORLEVEL%"
if "%CODE%"=="0" goto ende
echo.
echo   Das Programm wurde mit Fehlercode %CODE% beendet.
echo   Die Meldung oben hilft bei der Fehlersuche (siehe auch LIESMICH.md).
pause
:ende
endlocal & exit /b %CODE%

rem --------------------------------------------------------------------------
rem  :pruefe BEFEHL [ARGUMENTE]  - setzt PY, wenn BEFEHL ein Python >= 3.10 ist.
rem  Der Windows-Platzhalter "python.exe" (App-Ausfuehrungsalias, oeffnet nur
rem  den Microsoft Store) liefert hier einen Fehlercode und wird so uebergangen.
:pruefe
call %* -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if "%ERRORLEVEL%"=="0" set "PY=%*"
exit /b 0

rem --------------------------------------------------------------------------
:keinpython
echo.
echo   ==============================================================
echo    Python-Vorkurs-Lernquiz
echo   ==============================================================
echo.
if defined INSTALLIERT goto nachinstallation
set "ALT="
call py --version >nul 2>&1
if "%ERRORLEVEL%"=="0" set "ALT=1"
call python --version >nul 2>&1
if "%ERRORLEVEL%"=="0" set "ALT=1"
if defined ALT goto zualt
echo   Python wurde auf diesem Computer nicht gefunden.
set "PLATZHALTER="
for /f "delims=" %%P in ('where python 2^>nul') do (
    echo %%P| find /i "WindowsApps" >nul && set "PLATZHALTER=1"
)
if not defined PLATZHALTER goto anbieten
echo.
echo   Hinweis: Der Befehl "python" ist hier nur ein Platzhalter von Windows
echo   (App-Ausfuehrungsalias, er oeffnet nur den Microsoft Store). Das ist
echo   kein echtes Python.
goto anbieten
:zualt
echo   Python ist installiert, aber die Version ist zu alt.
:anbieten
echo   Dieses Lernquiz braucht Python 3.10 oder neuer.
echo.
where winget >nul 2>&1
if errorlevel 1 goto ohnewinget
echo   Python 3.12 kann jetzt automatisch installiert werden
echo   (mit dem Windows-Paketmanager winget, dauert 1-3 Minuten).
echo.
choice /c JN /n /m "  Python 3.12 jetzt installieren? [J/N]: "
if errorlevel 2 goto ohnewinget
echo.
call winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
if not "%ERRORLEVEL%"=="0" goto wingetfehler
set "INSTALLIERT=1"
echo.
echo   Installation fertig - ich suche Python noch einmal ...
goto suchen

:wingetfehler
echo.
echo   Die automatische Installation hat leider nicht geklappt
echo   (Fehlercode %ERRORLEVEL%).
goto ohnewinget

:nachinstallation
echo   Python wurde installiert, ist in diesem Fenster aber noch nicht
echo   bekannt. Bitte schliesse dieses Fenster und doppelklicke Start.bat
echo   noch einmal. Klappt es dann immer noch nicht: Computer neu starten.
echo.
pause
exit /b 1

:ohnewinget
echo.
echo   Bitte installiere Python von:  https://www.python.org/downloads/
echo   WICHTIG: Beim Installieren das Haekchen "Add python.exe to PATH" setzen!
echo   Danach Start.bat noch einmal doppelklicken.
echo.
choice /c JN /n /m "  Download-Seite jetzt im Browser oeffnen? [J/N]: "
if errorlevel 2 goto abbruch
start "" "https://www.python.org/downloads/"
:abbruch
echo.
pause
exit /b 1
