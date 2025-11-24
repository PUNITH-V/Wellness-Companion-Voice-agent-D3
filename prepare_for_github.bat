@echo off
echo ========================================
echo Preparing Project for GitHub Upload
echo ========================================
echo.

echo Step 1: Checking for files to remove...
echo.

if exist "backend\test_notion_fetch.py" (
    echo [FOUND] backend\test_notion_fetch.py - This should be deleted
    choice /C YN /M "Delete backend\test_notion_fetch.py"
    if errorlevel 2 goto skip1
    if errorlevel 1 (
        del "backend\test_notion_fetch.py"
        echo [DELETED] backend\test_notion_fetch.py
    )
) else (
    echo [OK] backend\test_notion_fetch.py not found
)
:skip1

echo.
if exist "livekit.zip" (
    echo [FOUND] livekit.zip - This should be deleted
    choice /C YN /M "Delete livekit.zip"
    if errorlevel 2 goto skip2
    if errorlevel 1 (
        del "livekit.zip"
        echo [DELETED] livekit.zip
    )
) else (
    echo [OK] livekit.zip not found
)
:skip2

echo.
echo Step 2: Verifying .gitignore exists...
if exist ".gitignore" (
    echo [OK] .gitignore found
) else (
    echo [ERROR] .gitignore not found!
    pause
    exit /b 1
)

echo.
echo Step 3: Checking for sensitive files...
echo.

if exist "backend\.env" (
    echo [WARNING] backend\.env exists - Make sure it's in .gitignore
) else (
    echo [OK] backend\.env not found
)

if exist "frontend\.env.local" (
    echo [WARNING] frontend\.env.local exists - Make sure it's in .gitignore
) else (
    echo [OK] frontend\.env.local not found
)

if exist "backend\wellness_log.json" (
    echo [WARNING] backend\wellness_log.json exists - Make sure it's in .gitignore
) else (
    echo [OK] backend\wellness_log.json not found
)

echo.
echo Step 4: Verifying example files exist...
if exist "backend\.env.example" (
    echo [OK] backend\.env.example found
) else (
    echo [ERROR] backend\.env.example not found!
)

if exist "frontend\.env.example" (
    echo [OK] frontend\.env.example found
) else (
    echo [ERROR] frontend\.env.example not found!
)

echo.
echo ========================================
echo Preparation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: git init
echo 2. Run: git add .
echo 3. Run: git status (verify no .env files are staged)
echo 4. Run: git commit -m "Initial commit"
echo 5. Create repo on GitHub
echo 6. Run: git remote add origin YOUR_REPO_URL
echo 7. Run: git push -u origin main
echo.
pause
