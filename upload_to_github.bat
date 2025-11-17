@echo off
REM GitHub Upload Script for image-cropper-gui
REM This script will initialize Git and push to GitHub

setlocal enabledelayedexpansion

echo ====================================
echo GitHub Upload Script
echo ====================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Git found. Proceeding with upload...
echo.

REM Set variables
set GITHUB_USER=simondarnell
set GITHUB_REPO=image-cropper-gui
set GITHUB_URL=https://%GITHUB_USER%:mollysusandarnell^!@github.com/%GITHUB_USER%/%GITHUB_REPO%.git

REM Initialize Git
echo [1/5] Initializing Git repository...
git init
if errorlevel 1 exit /b 1

REM Configure user
echo [2/5] Configuring Git user...
git config user.name "Simon Darnell"
git config user.email "simon@example.com"
if errorlevel 1 exit /b 1

REM Add all files
echo [3/5] Adding files...
git add .
if errorlevel 1 exit /b 1

REM Create commit
echo [4/5] Creating commit...
git commit -m "Initial commit: Batch image cropper GUI application with standalone Windows executable"
if errorlevel 1 exit /b 1

REM Add remote and push
echo [5/5] Pushing to GitHub...
git remote add origin %GITHUB_URL%
if errorlevel 1 (
    echo Remote may already exist, removing and re-adding...
    git remote remove origin
    git remote add origin %GITHUB_URL%
)

git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed. Please check:
    echo - Internet connection
    echo - GitHub repository exists and is empty
    echo - Credentials are correct
    echo.
    pause
    exit /b 1
)

echo.
echo ====================================
echo SUCCESS! Project uploaded to GitHub
echo ====================================
echo Repository: https://github.com/%GITHUB_USER%/%GITHUB_REPO%
echo.
pause
