@echo off
setlocal
where py >nul 2>nul
if not errorlevel 1 (
 set "RUNNER=py -3"
) else (
 where python >nul 2>nul
 if errorlevel 1 (
  echo Instale Python 3 em https://www.python.org/downloads/
  exit /b 1
 )
 set "RUNNER=python"
)
set "DIR=%LOCALAPPDATA%\NovaCLI"
if not exist "%DIR%" mkdir "%DIR%"
copy /y "%~dp0nova.py" "%DIR%\nova.py" >nul
> "%DIR%\Nova.cmd" echo @echo off
>> "%DIR%\Nova.cmd" echo %RUNNER% "%%LOCALAPPDATA%%\NovaCLI\nova.py" %%*
powershell -NoProfile -ExecutionPolicy Bypass -Command "$d=$env:LOCALAPPDATA+'\NovaCLI';$p=[Environment]::GetEnvironmentVariable('Path','User');if(($p -split ';') -notcontains $d){[Environment]::SetEnvironmentVariable('Path',($p.TrimEnd(';')+';'+$d).TrimStart(';'),'User')}"
if errorlevel 1 echo Aviso: configure o PATH manualmente para %DIR%
echo Instalado. Feche e reabra o CMD e digite Nova
endlocal
