@echo off
setlocal

:: Check Python version
for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do set pyver=%%a
if "%pyver%"=="3.11.7" (
    echo Found Python 3.11.7
) else (
    echo Python 3.11.7 is required. Please install it from https://www.python.org/downloads/release/python-3117/
    exit /b 1
)

:: Check for default values in appsettings.json
set "defaultsFound=0"
findstr /c:"\"AccessToken\": \"your_personal_access_token_here\"" appsettings.json > nul && (echo Make sure AccessToken is updated from the default value. && set "defaultsFound=1")
findstr /c:"\"ProjectId\": \"your_project_id_here\"" appsettings.json > nul && (echo Make sure ProjectId is updated from the default value. && set "defaultsFound=1")
findstr /c:"\"isSelfManaged\": false" appsettings.json > nul || (echo Make sure isSelfManaged is correctly set. && set "defaultsFound=1")
findstr /c:"\"selfManagedUrl\": \"\"" appsettings.json > nul || (echo Make sure selfManagedUrl is correctly set. && set "defaultsFound=1")

if "%defaultsFound%"=="1" (
    echo One or more default values are not updated in appsettings.json. Please update them before proceeding.
    exit /b 1
)

:: Install GitPython
echo Installing GitPython...
python -m pip install GitPython

echo Done.
endlocal
