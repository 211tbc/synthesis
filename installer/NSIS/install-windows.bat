@echo on

REM "%VARIABLE%"
REM Set InstallDir=%C:\Synthesis
Set InstallDir=%APP_HOME%
mkdir "%InstallDir%\src"
mkdir "%InstallDir%\Python25"
mkdir "%InstallDir%\PostgreSQL"
mkdir "%InstallDir%\GnuPG"
xcopy /EQR "%CD%\buildout\src\synthesis" "%InstallDir%\src"
xcopy /EQR "%CD%\buildout\packages\win32\Python25" "%InstallDir%\Python25"
xcopy /EQR "%CD%\buildout\packages\win32\pythoncom25.dll" "C:\windows\system32\"
xcopy /EQR "%CD%\buildout\packages\win32\pywintypes25.dll" "C:\windows\system32\"
xcopy /EQR "%CD%\buildout\packages\win32\python25.dll" "C:\windows\system32\"
xcopy /EQR "%CD%\buildout\packages\win32\msvcr71.dll" "C:\windows\system32\"

"%CD%\buildout\packages\win32\postgresql-8.3.10-1-windows.exe" --mode unattended --prefix %InstallDir%\PostgreSQL --superpassword mypassword

"%CD%\buildout\packages\win32\gnupg-w32cli-1.4.10b.exe" /S /C="%CD%\buildout\packages\win32\gnupg.ini" /D=%InstallDir%\GnuPG

cd buildout
"%InstallDir%\Python25\python.exe" bootstrap.py
"%CD%\bin\buildout"

copy "%CD%\bin\.exe" "%InstallDir%\src\python.exe"
copy "%CD%\bin\-script.py" "%InstallDir%\src\python-script.py"
copy "%InstallDir%\GnuPG\gpg.exe" "%InstallDir%\src\"

set PGPASSWORD=mypassword
"%InstallDir%\PostgreSQL\bin\createdb.exe" -U postgres synthesis
