from pathlib import Path
import subprocess
import os

def Generate_SearchPY(PyVer):
    text="""
@echo off
setlocal
set KEY_1="HKLM\SOFTWARE\Python\PythonCore\\"""+PyVer+"""\InstallPath"
set KEY_2="HKLM\SOFTWARE\Python\PythonCore\\"""+PyVer+"""\InstallPath"
set VALUE=Default
SET REG_1=reg.exe
SET REG_2="C:\Windows\sysnative\\reg.exe"
SET REG_3="C:\Windows\syswow64\\reg.exe"

SET KEY=%KEY_1%
SET REG=%REG_1%
%REG% QUERY %KEY% /ve 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

SET KEY=%KEY_2%
SET REG=%REG_1%
%REG% QUERY %KEY% /ve 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

::- %REG_2% is for 64-bit installations, using "C:\Windows\sysnative"
SET KEY=%KEY_1%
SET REG=%REG_2%
%REG% QUERY %KEY% /ve 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

SET KEY=%KEY_2%
SET REG=%REG_2%
%REG% QUERY %KEY% /ve 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

::- %REG_3% is for 32-bit installations on a 64-bit system, using "C:\Windows\syswow64"
SET KEY=%KEY_1%
SET REG=%REG_3%
%REG% QUERY %KEY% /ve 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

SET KEY=%KEY_2%
SET REG=%REG_3%
%REG% QUERY %KEY% /ve 2>nul
IF %ERRORLEVEL% EQU 0 GOTO _set_value

:_set_value
FOR /F "tokens=2,*" %%a IN ('%REG% QUERY %KEY% /ve') DO (SET PYHOME=%%b)
ECHO "%PYHOME%"
SETX PY_HOME %PYHOME%
    """
    f = open("Search Py.bat", "w+")
    text=text.strip()
    f.write(text)
    f.close()

def getPythonLocation():
    cmd=subprocess.run("python --version",capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    text=stdout
    if("Python " in stdout):
        temp=stdout.replace("Python ","")
        temp=temp[0:temp.rindex('.')]
        temp=temp.replace(os.getcwd()+">py --version","")
        temp=temp.strip()
        Generate_SearchPY(temp)
        cmd = subprocess.run("Search Py.bat", capture_output=True)
        stdout = cmd.stdout.decode()
        stderr = cmd.stderr.decode()
        stdout=stdout[stdout.index('"'):stdout.rindex('"')]
        stdout=stdout.replace('"','')
        return (stdout,stderr)
    else:
        text="No Python Path Found"

    return text