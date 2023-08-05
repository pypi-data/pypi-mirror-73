from pathlib import Path
import subprocess

def ExecutePy(File,Paths):
    Command=""
    if Paths=="":
        Command = "python "+ File
    else :
        Paths = "\""+Paths+"\\"+File+"\""
        Command = "python " + Paths
    cmd=subprocess.run(Command,capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    return (stdout,stderr)
