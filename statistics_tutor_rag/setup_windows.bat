@echo off
setlocal
cd /d "%~dp0"

echo Creating a Python virtual environment...
py -3.11 -m venv .venv
if errorlevel 1 (
  echo.
  echo Python 3.11 was not found. Install 64-bit Python 3.11 and try again.
  pause
  exit /b 1
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Core installation complete.
echo To add optional FAISS acceleration, run:
echo   .venv\Scripts\python -m pip install -r requirements-faiss.txt
echo.
echo Next, install Ollama and run:
echo   ollama pull llama3.2
echo   ollama pull all-minilm
pause
