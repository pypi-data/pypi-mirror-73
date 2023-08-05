from pathlib import Path
import subprocess

def Generate_SearchJDK():
    text="""
@echo off
setlocal
::- Test for the registry location  
SET VALUE=CurrentVersion
SET KEY_1="HKLM\SOFTWARE\JavaSoft\Java Development Kit"
SET KEY_2=HKLM\SOFTWARE\JavaSoft\JDK
SET REG_1=reg.exe
SET REG_2="C:\Windows\sysnative\\reg.exe"
SET REG_3="C:\Windows\syswow64\\reg.exe"

SET KEY=%KEY_1%
SET REG=%REG_1%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

SET KEY=%KEY_2%
SET REG=%REG_1%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

::- %REG_2% is for 64-bit installations, using "C:\Windows\sysnative"
SET KEY=%KEY_1%
SET REG=%REG_2%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

SET KEY=%KEY_2%
SET REG=%REG_2%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

::- %REG_3% is for 32-bit installations on a 64-bit system, using "C:\Windows\syswow64"
SET KEY=%KEY_1%
SET REG=%REG_3%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

SET KEY=%KEY_2%
SET REG=%REG_3%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

:_set_value
FOR /F "tokens=2,*" %%a IN ('%REG% QUERY %KEY% /v %VALUE%') DO (
    SET JDK_VERSION=%%b
)
SET KEY=%KEY%\%JDK_VERSION%
SET VALUE=JavaHome
FOR /F "tokens=2,*" %%a IN ('%REG% QUERY %KEY% /v %VALUE%') DO (
    SET JAVAHOME=%%b
)
ECHO "%JAVAHOME%"
SETX JAVA_HOME "%JAVAHOME%"
SETX Path "%JAVAHOME%bin"
    """
    f = open("Search JDK.bat", "w+")
    text=text.strip()
    f.write(text)
    f.close()

def Generate_SearchJRE():
    text="""
@echo off
setlocal
::- Test for the registry location  
SET VALUE=CurrentVersion
SET KEY_1="HKLM\SOFTWARE\JavaSoft\Java Runtime Environment"
SET KEY_2=HKLM\SOFTWARE\JavaSoft\Java Runtime Environment
SET REG_1=reg.exe
SET REG_2="C:\Windows\sysnative\\reg.exe"
SET REG_3="C:\Windows\syswow64\\reg.exe"

SET KEY=%KEY_1%
SET REG=%REG_1%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

SET KEY=%KEY_2%
SET REG=%REG_1%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

::- %REG_2% is for 64-bit installations, using "C:\Windows\sysnative"
SET KEY=%KEY_1%
SET REG=%REG_2%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

SET KEY=%KEY_2%
SET REG=%REG_2%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

::- %REG_3% is for 32-bit installations on a 64-bit system, using "C:\Windows\syswow64"
SET KEY=%KEY_1%
SET REG=%REG_3%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

SET KEY=%KEY_2%
SET REG=%REG_3%
%REG% QUERY %KEY% /v %VALUE% 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

:_set_value
FOR /F "tokens=2,*" %%a IN ('%REG% QUERY %KEY% /v %VALUE%') DO (
    SET JRE_VERSION=%%b
)
SET KEY=%KEY%\%JRE_VERSION%
SET VALUE=JavaHome
FOR /F "tokens=2,*" %%a IN ('%REG% QUERY %KEY% /v %VALUE%') DO (
    SET JREHOME=%%b
)
ECHO "%JREHOME%"
SETX JRE_HOME "%JREHOME%"
    """
    f = open("Search JRE.bat", "w+")
    text=text.strip()
    f.write(text)
    f.close()

def getJDKLocation():
    Generate_SearchJDK()
    cmd=subprocess.run("Search JDK.bat",capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    stdout = stdout[stdout.index('"'):stdout.rindex('"')]
    stdout = stdout.replace('"', '')
    return (stdout,stderr)

def getJRELocation():
    Generate_SearchJRE()
    cmd=subprocess.run("Search JRE.bat",capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    stdout = stdout[stdout.index('"'):stdout.rindex('"')]
    stdout = stdout.replace('"', '')
    return (stdout, stderr)
