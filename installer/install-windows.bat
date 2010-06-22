REM @echo on
@echo off

REM "%VARIABLE%"
REM Set InstallDir=%C:\Synthesis
Set InstallDir=%1
REM mkdir "%InstallDir%\src"
REM mkdir "%InstallDir%\Python25"
REM mkdir "%InstallDir%\PostgreSQL"
REM mkdir "%InstallDir%\GnuPG"
xcopy /EQR "%CD%\buildout\src\synthesis" "%InstallDir%\src"
xcopy /EQR "%CD%\buildout\packages\win32\Python25" "%InstallDir%\Python25"
xcopy /EQR "%CD%\buildout\packages\win32\pythoncom25.dll" "C:\windows\system32\"
xcopy /EQR "%CD%\buildout\packages\win32\pywintypes25.dll" "C:\windows\system32\"
xcopy /EQR "%CD%\buildout\packages\win32\python25.dll" "C:\windows\system32\"
xcopy /EQR "%CD%\buildout\packages\win32\msvcr71.dll" "C:\windows\system32\"

REM "%CD%\buildout\packages\win32\postgresql-8.3.10-1-windows.exe" --mode unattended --prefix %InstallDir%\PostgreSQL --superpassword mypassword

REM "%CD%\buildout\packages\win32\gnupg-w32cli-1.4.10b.exe" /S /C="%CD%\buildout\packages\win32\gnupg.ini" /D=%InstallDir%\GnuPG
echo "Incoming variable is: " 
echo %1%

echo %InstallDir%

cd buildout
%InstallDir%\Python25\python.exe bootstrap.py
REM pause

"%CD%\bin\buildout"

REM pause

copy %CD%\bin\*.exe %InstallDir%\src\python.exe
copy %CD%\bin\buildout-script.py %InstallDir%\src\python-script.py
copy %InstallDir%\GnuPG\gpg.exe %InstallDir%\src\

REM pause

set PGPASSWORD=mypassword
%InstallDir%\PostgreSQL\bin\createdb.exe -U postgres synthesis

REM pause