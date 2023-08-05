from pathlib import Path
import subprocess

def ExecuteJava(VE,File,Paths):
    if VE!="python":
        VE = "\"" + VE + "\""
    Command=""
    if Paths=="":
        Command = VE+" "+ File
    else :
        Paths = "\""+Paths+"\\"+File+"\""
        Command = VE+" " + Paths
    cmd=subprocess.run(Command,capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    return (stdout,stderr)