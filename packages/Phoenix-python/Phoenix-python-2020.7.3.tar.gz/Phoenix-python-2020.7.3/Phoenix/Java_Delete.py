from pathlib import Path
import subprocess
import os

def DeleteClass(File):
    str=""
    if ".class" in File:
        str=File
    else:
        str=File+".class"
    my_file = Path(str)
    if my_file.is_file():
        os.remove(str)
        return True
    else:
        return False

def DeleteJava(File):
    str=""
    if ".java" in File:
        str=File
    else:
        str=File+".java"
    my_file = Path(str)
    if my_file.is_file():
        os.remove(str)
        return True
    else:
        return False

def DeleteFile(File):
    a=DeleteJava(File)
    b=DeleteClass(File)
    if a==True&b==True:
        return True
    else:
        return False

#DeleteFile("NewClass")