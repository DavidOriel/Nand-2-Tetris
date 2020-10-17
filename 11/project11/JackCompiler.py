import sys
import os
import CompilationEngine


def main():
    """
    main class, here we will get the input from the input line and run the program on the input
    :return: none
    """
    userinput = sys.argv[1]
    if os.path.isdir(userinput):
        if not userinput.endswith("/"):
            userinput+= "/"
        files = os.listdir(userinput)
        for file in files:
            if file.endswith("jack"):
                filename = file.split(".")[0]
                comp = CompilationEngine.CompilationEngine(userinput+file,userinput+filename+".vm")
                comp.compileClass()
    elif os.path.isfile(userinput):
        userinput = userinput.split(".")[0]
        comp = CompilationEngine.CompilationEngine(userinput +".jack",userinput + ".vm")
        comp.compileClass()
    else:
        return




if __name__ =="__main__":
    main()

