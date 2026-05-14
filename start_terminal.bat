@echo off
echo Starting FinVision Terminal (Monolithic Mode)...

:: Check for backend .env
if not exist server\.env (
    echo [WARNING] server/.env not found!
)

:: Start Backend
start cmd /k "cd server && venv\Scripts\activate && python main.py"
echo Backend starting on port 8085...

:: Start Frontend
start cmd /k "npm run dev:frontend"
echo Frontend starting on port 8081...

echo All systems initialized. Terminal is ready.
