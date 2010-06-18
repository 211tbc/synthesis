; example1.nsi
;
; This script is perhaps one of the simplest NSIs you can make. All of the
; optional settings are left to their default settings. The installer simply 
; prompts the user asking them where to install, and drops a copy of example1.nsi
; there. 

;--------------------------------

; The name of the installer
Name "Synthesis HMIS XML/CSV Format Conversion Tool"
Caption "Synthesis HMIS XML/CSV Format Conversion Tool Installation"

;Icon "${NSISDIR}\Contrib\Graphics\Icons\nsis1-install.ico"

Icon "Y:\installer\NSIS\system-installer.ico"


; The file to write
OutFile "Synthesis.exe"

SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
BGGradient 000000 800000 FFFFFF
InstallColors FF8080 000030
XPStyle on

; The default installation directory
InstallDir "$PROGRAMFILES\Synthesis"

; Request application privileges for Windows Vista
RequestExecutionLevel user

LicenseText "The MIT License"
LicenseData "MITLicense.txt"

;--------------------------------

; Pages

Page license
Page components
Page directory
Page instfiles
;Page custom customPage "" "Installing Foundation Tools...Please wait."
UninstPage uninstConfirm
UninstPage instfiles


;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

    ; put msvcrt in sys32 folder
    SetOutPath $SYSDIR
    ;File msvcr71.dll

  ; Set output path to the installation directory.
    SetOutPath $INSTDIR
  
  ; Put file there
  File Y:\installer\install-windows.bat
  File synthesis.bat
  File system-software-update.png
  File system-software-install.png
  
  StrCpy $R0 "$INSTDIR"
  System::Call 'Kernel32::SetEnvironmentVariableA(t, t) i("APP_HOME", R0).r0'
  ;messagebox mb_ok 'Scott Env. Variable set?$R0'
  
  ;nsExec::Exec  '"$INSTDIR\install-windows.bat"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Synthesis" "DisplayName" "Synthesis (remove only)"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Synthesis" "UninstallString" '"$INSTDIR\bt-uninst.exe"'
  
  ; Create the desktop shortcut
  ;$DESKTOP
  ; Directories to Create
  CreateDirectory $INSTDIR\src
  CreateDirectory $INSTDIR\src\conf
  CreateDirectory $INSTDIR\src\xsd\versions\406
  CreateDirectory $INSTDIR\src\UsedFiles
  CreateDirectory $INSTDIR\src\OutputFiles
  CreateDirectory $INSTDIR\src\FailedFiles
  CreateDirectory $INSTDIR\src\errcatalog
  Call "CopySRC"
  
  CreateDirectory $INSTDIR\Python25
  Call "GetPython25"
  
  Call "GetWX"
  Call "GetWxPython"
  
  CreateDirectory $INSTDIR\PostgreSQL
  Call "InstPG"
  
  CreateDirectory $INSTDIR\GnuPG
  Call "InstGNUPG"
  
  CreateDirectory $INSTDIR\buildout
  Call "CpyBuildOut"
  
  Call "Launch_win32_bat"
  
  WriteUninstaller "bt-uninst.exe"
  
SectionEnd ; end the section

UninstPage uninstConfirm
UninstPage instfiles

;!define JAVA_HOME "d:\JDK1.5"

 
Section "Install APR Report Generator"
    File APR.xlsx
SectionEnd

Section "Start Synthesis Processing"

    MessageBox MB_YESNO "Would you like to start Synthesis Processing Now?" IDYES true
    
    true:
      Exec '$INSTDIR\synthesis.bat'
      
      
SectionEnd

Section "Make shortcuts (desktop, All Programs)"

  SectionIn 1 2 3
  Call CSC

SectionEnd

; Uninstaller

UninstallText "This will uninstall Synthesis. Hit next to continue."
UninstallIcon "${NSISDIR}\Contrib\Graphics\Icons\nsis1-uninstall.ico"

Section "Uninstall"

  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Synthesis"
  DeleteRegKey HKLM "SOFTWARE\Synthesis"
  Delete "$INSTDIR\bt-uninst.exe"
  Delete "$INSTDIR\APR.xlsx"
  Delete '$INSTDIR\install-windows.bat'
  Delete '$INSTDIR\synthesis.bat'
  ;Delete "$INSTDIR\test.ini"
  Delete "$SMPROGRAMS\Synthesis\*.*"
  RMDir "$SMPROGRAMS\Synthesis"
  
  
  Delete $INSTDIR\src\*.py
  Delete $INSTDIR\src\*.pyc
  
  
  ; - remove directories
  RMDir /r $INSTDIR\src
  RMDir /r $INSTDIR\Python25
  RMDir /r $INSTDIR\PostgreSQL
  RMDir /r $INSTDIR\GnuPG
  
  RMDir /r "$INSTDIR"

  IfFileExists "$INSTDIR" 0 NoErrorMsg
    MessageBox MB_OK "Note: $INSTDIR could not be removed!" IDOK 0 ; skipped if file doesn't exist
  NoErrorMsg:

SectionEnd

Function "CSC"
  
  ;CreateDirectory "$SMPROGRAMS\Synthesis"
  SetOutPath $INSTDIR ; for working directory
  ;CreateShortCut "$SMPROGRAMS\Big NSIS Test\Uninstall BIG NSIS Test.lnk" "$INSTDIR\bt-uninst.exe" ; use defaults for parameters, icon, etc.
  ; this one will use notepad's icon, start it minimized, and give it a hotkey (of Ctrl+Shift+Q)
  CreateShortCut "$DESKTOP\Synthesis.lnk" "$INSTDIR\synthesis.bat" "" "Y:\installer\NSIS\system-software-update.ico" 0 SW_SHOWMINIMIZED CONTROL|SHIFT|Q
  ;CreateShortCut "$SMPROGRAMS\Big NSIS Test\TheDir.lnk" "$INSTDIR\" "" "" 0 SW_SHOWMAXIMIZED CONTROL|SHIFT|Z

FunctionEnd

Function "CopySRC"

    SetOutPath $INSTDIR\src
    File /nonfatal /x *.xml Y:\src\*.py
    File /nonfatal Y:\src\fileConverter.ini
    
    ; Update the ini with the right folder for the application
    WriteINIStr "$INSTDIR\src\fileConverter.ini" "filelocations" "input_processing" "$INSTDIR\InputFiles"

    File /nonfatal Y:\src\configurationEditor2.xrc
    
    
    SetOutPath $INSTDIR\src\conf
    File /nonfatal /x *.xml /x *.py~ Y:\src\conf\*
    
    ; copy the schemas to xsd folder
    SetOutPath $INSTDIR\src\xsd\versions
    File /nonfatal /x *.py Y:\xsd\*.xsd
    
    SetOutPath $INSTDIR\src\xsd\versions\406
    File /nonfatal /x *.py Y:\xsd\versions\406\*.xsd
    
    ; set path back to base of install tree
    SetOutPath $INSTDIR\src

FunctionEnd

Function "GetWX"
    ;Banner::show "HMIS XML Data Conversion Tool Installation Continuing..."
    ;http://downloads.sourceforge.net/project/wxwindows/2.8.11/wxMSW-2.8.11-Setup.exe?use_mirror=voxel
    Call ConnectInternet ;Make an internet connection (if no connection available)
    
    StrCpy $2 "$INSTDIR\wxMSW-2.8.11-Setup.exe"
    ;NSISdl::download http://downloads.sourceforge.net/project/pywin32/pywin32/Build%20214/pywin32-214.win32-py2.5.exe?use_mirror=superb-sea2 pywin32-214.win32-py2.5.exe
    
    StrCpy $3 "http://downloads.sourceforge.net/project/wxwindows/2.8.11/wxMSW-2.8.11-Setup.exe?use_mirror=voxel"
    DetailPrint "HMIS XML Data Conversion Tool Installation Continuing..."
    NSISdl::download $3 $2
    Pop $0
    ;MessageBox MB_OK "Download Return is: $0"; skipped if file doesn't exist
    StrCmp $0 "success" successDL
    SetDetailsView show
    ;DetailPrint "download failed: $0"
    ;Abort
  successDL:
    ;MessageBox MB_OK "Installing... $2"; skipped if file doesn't exist
    StrCpy $4 '$2 /SILENT /DIR="$INSTDIR\wx"'
    ;MessageBox MB_OK "Installing with command: $4"; skipped if file doesn't exist
    ExecWait $4
    
FunctionEnd

Function "GetWxPython"
    ;Banner::show "HMIS XML Data Conversion Tool Installation Continuing..."
    ;http://downloads.sourceforge.net/project/wxpython/wxPython/2.8.11.0/wxPython2.8-win32-unicode-2.8.11.0-py25.exe?use_mirror=hivelocity
    ; (not this one) http://downloads.sourceforge.net/project/wxwindows/2.8.11/wxMSW-2.8.11-Setup.exe?use_mirror=voxel
    Call ConnectInternet ;Make an internet connection (if no connection available)
    
    StrCpy $2 "$INSTDIR\wxPython2.8-win32-unicode-2.8.11.0-py25.exe"
    ;NSISdl::download http://downloads.sourceforge.net/project/pywin32/pywin32/Build%20214/pywin32-214.win32-py2.5.exe?use_mirror=superb-sea2 pywin32-214.win32-py2.5.exe
    StrCpy $3 "http://downloads.sourceforge.net/project/wxpython/wxPython/2.8.11.0/wxPython2.8-win32-unicode-2.8.11.0-py25.exe?use_mirror=hivelocity"
    DetailPrint "HMIS XML Data Conversion Tool Installation Continuing..."
    NSISdl::download $3 $2
    Pop $0
    ;MessageBox MB_OK "Download Return is: $0"; skipped if file doesn't exist
    StrCmp $0 "success" successDL
    SetDetailsView show
    ;DetailPrint "download failed: $0"
    ;Abort
  successDL:
    ;MessageBox MB_OK "Installing... $2"; skipped if file doesn't exist
    StrCpy $4 '$2 /SILENT /DIR="$INSTDIR\python25\Lib\site-packages"'
    ;MessageBox MB_OK "Installing with command: $4"; skipped if file doesn't exist
    ExecWait $4
    
FunctionEnd

Function "GetPython25"

    ;Banner::show "HMIS XML Data Conversion Tool Installation Continuing..."
    
    Call ConnectInternet ;Make an internet connection (if no connection available)
    
    StrCpy $2 "$INSTDIR\python-2.5.msi"
    ;NSISdl::download http://downloads.sourceforge.net/project/pywin32/pywin32/Build%20214/pywin32-214.win32-py2.5.exe?use_mirror=superb-sea2 pywin32-214.win32-py2.5.exe
    StrCpy $3 "http://www.python.org/ftp/python/2.5/python-2.5.msi"
    DetailPrint "HMIS XML Data Conversion Tool Installation Continuing..."
    NSISdl::download $3 $2
    Pop $0
    ;MessageBox MB_OK "Download Return is: $0"; skipped if file doesn't exist
    StrCmp $0 "success" successDL
    SetDetailsView show
    ;DetailPrint "download failed: $0"
    ;Abort
  successDL:
    ;MessageBox MB_OK "Installing... $2"; skipped if file doesn't exist
    StrCpy $4 'msiexec /passive /i "$2" TARGETDIR="$INSTDIR\python25"'
    ;MessageBox MB_OK "Installing with command: $4"; skipped if file doesn't exist
    ExecWait $4
    ;Delete $2
  
    ;Call GetWinampInstPath
    ;Pop $0
    ;StrCmp $0 "" skip
    ;StrCpy $INSTDIR $0
  
    
FunctionEnd

Function "get pyWin32"

    ;

    
    ; (not this one) http://downloads.sourceforge.net/project/wxwindows/2.8.11/wxMSW-2.8.11-Setup.exe?use_mirror=voxel
    Call ConnectInternet ;Make an internet connection (if no connection available)
    
    StrCpy $2 "$INSTDIR\pywin32-214.win32-py2.5.exe"
    ;NSISdl::download http://downloads.sourceforge.net/project/pywin32/pywin32/Build%20214/pywin32-214.win32-py2.5.exe?use_mirror=superb-sea2 pywin32-214.win32-py2.5.exe
    StrCpy $3 "http://downloads.sourceforge.net/project/pywin32/pywin32/Build%20214/pywin32-214.win32-py2.5.exe?use_mirror=superb-sea2"
    DetailPrint "HMIS XML Data Conversion Tool Installation Continuing..."
    NSISdl::download $3 $2
    Pop $0
    ;MessageBox MB_OK "Download Return is: $0"; skipped if file doesn't exist
    StrCmp $0 "success" successDL
    SetDetailsView show
    ;DetailPrint "download failed: $0"
    ;Abort
  successDL:
    ;MessageBox MB_OK "Installing... $2"; skipped if file doesn't exist
    StrCpy $4 '$2 /SILENT /DIR="$INSTDIR\python25\Lib\site-packages"'
    ;MessageBox MB_OK "Installing with command: $4"; skipped if file doesn't exist
    ExecWait $4

FunctionEnd

Function "InstPG"

    ; "%CD%\buildout\packages\win32\postgresql-8.3.10-1-windows.exe" --mode unattended --prefix %InstallDir%\PostgreSQL --superpassword mypassword
    SetOutPath $INSTDIR
    StrCpy $1 "postgresql-8.3.10-1-windows.exe"
    File postgresql-8.3.10-1-windows.exe
    
    StrCpy $4 '$1 --mode unattended --prefix "$INSTDIR\PostgreSQL" --superpassword mypassword'
    ;MessageBox MB_OK "Installing with command: $4"; skipped if file doesn't exist (do this to debug a failed installer)
    ExecWait $4

FunctionEnd

Function "InstGNUPG"
    ;"%CD%\buildout\packages\win32\gnupg-w32cli-1.4.10b.exe" /S /C="%CD%\buildout\packages\win32\gnupg.ini" /D=%InstallDir%\GnuPG
    SetOutPath $INSTDIR
    StrCpy $1 "gnupg-w32cli-1.4.10b.exe"
    File gnupg-w32cli-1.4.10b.exe
    File gnupg.ini
    
    StrCpy $4 '$1 /S /C=gnupg.ini /D="$INSTDIR"\GnuPG'
    ;MessageBox MB_OK "Installing with command: $4"; skipped if file doesn't exist(do this to debug a failed installer)
    ExecWait $4
    
FunctionEnd

Function "CpyBuildOut"

    SetOutPath $INSTDIR\buildout
    File /nonfatal /r Y:\installer\buildout\*.*
    
FunctionEnd

Function "Launch_win32_bat"
    
    SetOutPath $INSTDIR
    StrCpy $1 'install-windows.bat "$INSTDIR"'
    ;MessageBox MB_OK "Running BAT file with command: $1"; skipped if file doesn't exist(do this to debug a failed installer)
    ; passing it in a parm
    ; trying to make is silent
    ;ExecWait $1
    ExecShell "open" $1 SW_HIDE
    
FunctionEnd

Function ConnectInternet

  Push $R0
    
    ClearErrors
    Dialer::AttemptConnect
    IfErrors noie3
    
    Pop $R0
    StrCmp $R0 "online" connected
      MessageBox MB_OK|MB_ICONSTOP "Cannot connect to the internet."
      Quit
    
    noie3:
  
    ; IE3 not installed
    MessageBox MB_OK|MB_ICONINFORMATION "Please connect to the internet now."
    
    connected:
  
  Pop $R0
  
FunctionEnd
