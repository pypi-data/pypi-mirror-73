from pathlib import Path
import subprocess

def Execute_AppX64(Paths):
    cmd=subprocess.run("Elevatex64.exe  "+Paths,capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    return (stdout,stderr)

def Execute_AppX32(Paths):
    cmd=subprocess.run("Elevatex32.exe  "+Paths,capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    return (stdout,stderr)

