@echo off
title Vernacular AI - Push to GitHub
echo ======================================================================
echo           VERNACULAR AI - 1-CLICK GITHUB PUSH WIZARD
echo ======================================================================
echo.

cd /d "%~dp0"

echo [*] Checking Git installation...
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Git is not installed or not found in PATH.
    echo Please install Git from https://git-scm.com/ and try again.
    pause
    exit /b 1
)

echo [*] Staging all project files...
git add .

echo [*] Creating commit...
git commit -m "feat: Vernacular AI Multi-Lingual Platform (51 Languages, Cinema Dub Studio, Offline Engine, Academic Report Generator)"

echo.
echo ======================================================================
echo  GitHub Remote Setup
echo ======================================================================
echo If you haven't created a GitHub repository yet:
echo   1. Go to https://github.com/new
echo   2. Create a new repository named "Vernacular_AI" (Do NOT check initialize with README)
echo   3. Copy your repository HTTPS URL (e.g. https://github.com/YOUR_USERNAME/Vernacular_AI.git)
echo ======================================================================
echo.

set /p REPO_URL="Paste your GitHub repository URL: "

if "%REPO_URL%"=="" (
    echo [!] No URL entered. Changes have been committed locally.
    echo You can push manually anytime using: git push -u origin main
    pause
    exit /b 0
)

echo.
echo [*] Configuring remote origin: %REPO_URL%...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [*] Setting branch to main...
git branch -M main

echo [*] Pushing to GitHub (origin main)...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo  SUCCESS! Your project has been pushed to GitHub successfully!
    echo ======================================================================
) else (
    echo.
    echo [!] Push encountered an error. Please check your GitHub credentials or URL.
    echo You can also run: git push -u origin main
)

echo.
pause
