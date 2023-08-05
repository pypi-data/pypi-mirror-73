import subprocess

def Execute_App(Paths):
    cmd=subprocess.run(Paths,capture_output=True)
    stdout=cmd.stdout.decode()
    stderr=cmd.stderr.decode()
    return (stdout,stderr)