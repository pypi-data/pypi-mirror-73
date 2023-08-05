import os
from Phoenix import Java_Execute,VE_Java_Execute
from Phoenix import Java_Save,Java_Delete

def Execute_App(Paths,VE_Path,VE=False):
    Paths="\""+Paths+"\""
    #Paths = "\"" + Paths + "\""
    Text="import java.io.BufferedReader;\nimport java.io.IOException;\nimport java.io.InputStreamReader;\n\npublic class RunApp {\n"+"public static void main(String args[]){\n"+"try {\nRuntime p = Runtime.getRuntime();\np.exec("+Paths+");\n} catch (IOException ex) \n{ex.printStackTrace();}\n"+"}}"
    Java_Save.Save_Java(Text, "RunApp")
    if(VE == True):
        VE_Java_Execute.CompileJava(VE_Path + "javac.exe", "RunApp.java", "")
        VE_Java_Execute.ExecuteJava(VE_Path + "java.exe", "RunApp", "")
    else:
        Java_Execute.CompileJava("RunApp.java", "")
        Java_Execute.ExecuteJava("RunApp", "")
    Java_Delete.DeleteFile("RunApp")

#Execute_App("D:\\\Projects\\\Python\\\Phoenix--Lang\\\Phoenix\\\\temp.exe")