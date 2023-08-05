from pathlib import Path
import subprocess
import os

def DeleteFile(File):
    str=""
    if ".py" in File:
        str=File
    else:
        str=File+".py"
    my_file = Path(str)
    if my_file.is_file():
        os.remove(str)
        return True
    else:
        return False