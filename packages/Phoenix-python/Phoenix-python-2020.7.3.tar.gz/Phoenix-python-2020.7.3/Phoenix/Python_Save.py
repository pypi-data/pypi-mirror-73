from pathlib import Path
import subprocess

def Save_Py(Text,Paths):
    Paths = Paths + ".py"
    f=open(Paths,"w+",encoding="utf-8")
    f.write(Text)
    my_file = Path(Paths)
    if my_file.is_file():
        return True
    else:
        return False
