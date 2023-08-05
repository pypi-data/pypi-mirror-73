from pathlib import Path
import subprocess
import os

def CompileJava(VE,File,Paths):
    if VE!="javac":
        VE = "\"" + VE + "\""
    UTF="\""+"UTF-8"+"\""
    Command=VE+" -encoding "+UTF+" -sourcepath src "+File+" -d "+Paths+""
    if Paths=="":
        Command = VE+" -encoding " + UTF + " -sourcepath src " + File + ""
    else :
        File="\""+Paths+File+"\""
        Command = VE+" -encoding " + UTF + " -sourcepath src " + File + ""
    cmd=subprocess.run(Command,capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    return (stdout,stderr)

def ExecuteJava(VE,File,Paths):
    if VE!="java":
        VE = "\"" + VE + "\""
    Command=VE+" -cp "+Paths+" "+File
    if Paths=="":
        Command = VE+" -cp . "+ File
    else :
        File="\""+File+"\""
        Paths = "\""+Paths+"\\"+"\""
        Command = VE+" -cp " + Paths + " " + File
    cmd=subprocess.run(Command,capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    return (stdout,stderr)
