from pathlib import Path
import subprocess

def Save_Java(Text,Paths):
    Paths = Paths + ".java"
    f=open(Paths,"w+",encoding="utf-8")
    f.write(Text)
    my_file = Path(Paths)
    if my_file.is_file():
        return True
    else:
        return False

def SetClass(Source):
    Source="\""+Source+"\""
    cmd=subprocess.run("SETX Libpath "+Source,capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    return (stdout,stderr)

def DeleteClass():
    cmd = subprocess.run("REG delete HKCU\Environment /F /V Libpath", capture_output=True)
    stdout = cmd.stdout.decode()
    stderr = cmd.stderr.decode()
    return (stdout,stderr)

def GenerateClassPath(JDKPath,JREPath):
    text=""
    if (JDKPath == JREPath):
        text="""robocopy "%Libpath%" "<JAVA_PATH>jre\lib\ext" *jar /e"""
        text=text.replace('<JAVA_PATH>',JREPath)
    else:
        text="""
        robocopy "%Libpath%" "<JDK_PATH>jre\lib\ext" *jar /e
        robocopy "%Libpath%" "<JRE_PATH>lib\ext" *jar /e
        """
        text = text.replace('<JDK_PATH>', JDKPath)
        text = text.replace('<JRE_PATH>', JREPath)

    f=open("ClassPath.bat","w+",encoding="utf-8")
    f.write(text)
    f.close()


def CopyLibx32(Folder,JDK_Path,JRE_PATH):
    SetClass(Folder)
    GenerateClassPath(JDK_Path,JRE_PATH)
    cmd=subprocess.run("Elevatex32.exe  "+"ClassPath.bat",capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    DeleteClass(Folder)
    return (stdout,stderr)

def CopyLibx64(Folder,JDK_Path,JRE_PATH):
    SetClass(Folder)
    GenerateClassPath(JDK_Path, JRE_PATH)
    cmd=subprocess.run("Elevatex64.exe  "+"ClassPath.bat",capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    DeleteClass(Folder)
    return (stdout,stderr)




