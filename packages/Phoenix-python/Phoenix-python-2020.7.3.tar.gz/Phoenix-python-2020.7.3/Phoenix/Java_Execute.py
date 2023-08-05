from pathlib import Path
import subprocess

def CompileJava(File,Paths):
    UTF="\""+"UTF-8"+"\""
    Command="javac -encoding "+UTF+" -sourcepath src "+File+" -d "+Paths+""
    if Paths=="":
        Command = "javac -encoding " + UTF + " -sourcepath src " + File + ""
    else :
        File="\""+Paths+File+"\""
        Command = "javac -encoding " + UTF + " -sourcepath src " + File + ""
    cmd=subprocess.run(Command,capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    return (stdout,stderr)

def ExecuteJava(File,Paths):
    Command="java -cp "+Paths+" "+File
    if Paths=="":
        Command = "java -cp . "+ File
    else :
        File="\""+File+"\""
        Paths = "\""+Paths+"\\"+"\""
        Command = "java -cp " + Paths + " " + File
    cmd=subprocess.run(Command,capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    return (stdout,stderr)

#x=CompileJava("App_RuntimeAdmin.java","")
#print(x)