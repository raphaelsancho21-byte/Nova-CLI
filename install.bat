@echo off
setlocal
where py >nul 2>nul
if not errorlevel 1 (
  set "RUNNER=py -3"
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Instale Python 3 antes de continuar: https://www.python.org/downloads/
    exit /b 1
  )
  set "RUNNER=python"
)
set "DIR=%LOCALAPPDATA%\NovaCLI"
if not exist "%DIR%" mkdir "%DIR%"
copy /y "%~dp0nova.py" "%DIR%\nova.py" >nul
> "%DIR%\Nova.cmd" echo @echo off
>> "%DIR%\Nova.cmd" echo %RUNNER% "%%LOCALAPPDATA%%\NovaCLI\nova.py" %%*
echo.
echo Nova CLI instalada em %DIR%.
echo Adicione a pasta abaixo ao PATH do usuario se ainda nao estiver:
echo %DIR%
echo.
echo Para usar imediatamente: "%DIR%\Nova.cmd"
echo Para habilitar o comando Nova em qualquer CMD, execute:
echo powershell -NoProfile -Command "$p=[Environment]::GetEnvironmentVariable('Path','User');if(($p -split ';') -notcontains '%DIR%'){[Environment]::SetEnvironmentVariable('Path',($p.TrimEnd(';')+';%DIR%'),'User')}"
echo Depois feche e abra novamente o CMD.
endlocal
