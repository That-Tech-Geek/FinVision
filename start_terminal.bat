@echo off
echo Starting FinVision Terminal (Monolithic Mode)...

:: Check for backend .env
if not exist backend\.env (
    echo [WARNING] backend/.env not found!
)

:: Check for frontend .env
if not exist frontend\.env (
    echo [WARNING] frontend/.env not found!
)

:: Start Backend
start cmd /k "cd backend && python main.py"
echo Backend starting on port 8085...

:: Start Frontend
start cmd /k "cd frontend && npm run dev -- --port 8081"
echo Frontend starting on port 8081...

echo All systems initialized. Terminal is ready.
