import sys
import os

"""
The parser class will clean the given file from tabs, comments and sapces.
"""


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.file = filename
        self.lines = []
        self.clean_file()

    """
    function for cleaning the file
    """

    def clean_file(self):
        for line in self.file:
            if len(line.strip()) > 0:
                self.lines.append(line)
        for line in self.lines:
            line = line.replace(" ", "")
            line = line.replace("  ", "")
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            line = line.split('//')[0]


"""
class for translating a vm file into an asm file
"""


class Writer:
    """
    constructor for the writer class
    """

    def __init__(self, vm_file, file_name):
        parser = Parser(vm_file)
        parser.clean_file()
        self.file_name = file_name.replace(".vm", "")
        self.lines = parser.lines
        self.translation = []
        self.index = 0
        self.funccounter = 0
        self.arythmetic1 = {
            "add": "+",
            "sub": "-",
            "and": "&",
            "or": "|",
        }
        self.arythmetic2 = {
            "neg": "-",
            "not": "!",
        }
        self.jmp_com = {
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT"
        }
        self.destination1 = {
            "pointer": 3,
            "temp": 5
        }

        self.destination2 = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }

    """
    function that managing the translation, sends every line to one of three fucntions, 
    depending on the command
    """

    def handle_commands(self):
        for line in self.lines:
            com_list = line.split()
            first = com_list[0]
            if first == "pop":
                self.handle_pop_command(com_list[1], com_list[2])
            elif first == "push":
                self.handle_push_command(com_list[1], com_list[2])
            elif first in ["if-goto", "label", "goto"]:
                self.handle_specials1(first, com_list[1])
            elif first in ["call", "function"]:
                self.handle_specials2(first, com_list[1], com_list[2])
            elif first == "return":
                self.translation.extend(self.writereturn())
            else:
                self.handle_arithmetic_operators(first)

    """
    handle special calls, function, return , function call, go to and if.
    """
    def handle_specials1(self, command, string):
        if command == "label":
            self.translation.extend(self.writelabel(string))
        elif command == "if-goto":
            self.translation.extend(self.writeif(string))
        else:
            self.translation.extend(self.writegoto(string))

    def handle_specials2(self, command, string, num):
        if command == "call":
            self.translation.extend(self.writecall(string, num))
        else:
            self.translation.extend(self.writefunction(string, num))

    """
    handling pop commands,specially taking care of static command that has a special way of translation
    else sending the line for translation depending on the command. 
    """

    def handle_pop_command(self, dest_name, dest):
        if dest_name == "static":
            self.translation.extend(self.handle_static_pop(dest))
        elif dest_name in self.destination1:  # pointer or temp
            location = str(self.destination1[dest_name] + int(dest))
            self.translation.extend(self.pop1(location))
        elif dest_name in self.destination2:  # lcl, arg, this, that
            self.translation.extend(self.pop2(self.destination2[dest_name], dest))

    """
    first type of translation, taking care of pointers and temps possibilities
    """

    def pop1(self, location):
        return ["@SP", "A=M-1", "D=M", "@" + "R" + location, "M=D", "@SP", "M=M-1"
                ]

    """
    second type of translation, taking care of lcl, arg, this and that possibilities
    """

    def pop2(self, location, dest):
        return ["@" + str(location), "D=M", "@" + str(dest), "A=D+A", "D=A", "@R13", "M=D", "@SP", "AM=M-1",
                "D=M", "@R13", "A=M", "M=D"]

    """
    function for static command
    """

    def handle_static_pop(self, dest):
        return ["@" + self.file_name + "." + str(dest), "D=A", "@R13", "M=D", "@SP", "AM=M-1", "D=M", "@R13", "A=M",
                "M=D"]

    """
    andling push commands,specially taking care of static and constant command that has a 
    special way of translation. else sending the line for translation depending on the command. 
    """

    def handle_push_command(self, dest_name, dest):
        if dest_name == "static":
            self.translation.extend(self.handle_static_push(dest))
        elif dest_name == "constant":
            self.translation.extend(self.handle_constant(dest))
        elif dest_name in self.destination1:
            location = str(self.destination1[dest_name] + int(dest))
            self.translation.extend(self.push1(location))
        elif dest_name in self.destination2:
            self.translation.extend(self.push2(self.destination2[dest_name], dest))

    """
    first type of translation, taking care of pointers and temps possibilities
    """

    def push1(self, location):
        return ["@" + "R" + location, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    """
        second type of translation, taking care of lcl, arg, this and that possibilities
    """

    def push2(self, location, dest):
        return ["@" + str(location), "D=M", "@" + str(dest), "D=D+A", "A=D", "D=M", "@SP", "A=M",
                "M=D", "@SP", "M=M+1"]

    """
    function for static command
    """

    def handle_static_push(self, dest):
        location = self.file_name + "." + str(dest)
        return ["@" + location, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    """
    handling the constant method that can appear only in the the push command
    """

    def handle_constant(self, dest):
        return ["@" + str(dest), "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    """
    in case there is no push or pop command, the line will be an arythmetic operation.
    this function will translate the line. 
    """

    def handle_arithmetic_operators(self, command):
        if command in self.arythmetic1:
            self.translation.extend(self.write_command1(self.arythmetic1[command]))
        elif command in self.arythmetic2:
            self.translation.extend(self.write_command2(self.arythmetic2[command]))
        elif command in self.jmp_com:
            self.translation.extend(self.write_jmp_command(command))

    """
    if the operation is a regular operation
    """

    def write_command1(self, command):
        return ([
            "@SP", "AM=M-1", "D=M", "A=A-1", "D=M" + str(command) + "D", "M=D"
        ])

    """
    if the operation is a "not" or "neg" operation.
    """

    def write_command2(self, command):
        return ([
            "@SP", "A=M-1", "M=" + str(command) + "M"
        ])

    """
    in case of comparison, this function translate a jump command, we are also checking the cases for overflow
    and taking care of them
    """

    def write_jmp_command(self, command):
        self.index += 1
        index = str(self.index)
        dic = {"lt":
                   ["@SP", "AM=M-1", "D=M", "@R13", "M=-1", "@POSITIVE1" + index,
                    "D;JGT", "@R13", "M=0", "(POSITIVE1" + index + ")", "@SP", "A=M-1", "D=M", "@R15", "M =D",
                    "@R14", "M=-1", "@POSITIVE2" + index, "D;JGT", "@R14", "M=0", "(POSITIVE2" + index + ")",
                    "@R13", "D=M", "@R14", "D=D-M", "@R15", "M=D", "@NOPROBLEM" + index, "D;JEQ",
                    "@HANDLEPLUS" + index, "D;JGT", "@SP", "A=M-1", "M=-1",
                    "@END" + index, "0;JMP",  # if minus - x biger then false
                    "(HANDLEPLUS" + index + ")", "@SP", "A=M-1", "M=0",
                    "@END" + index, "0; JMP",  # if plus - y is bigger then true
                    "(NOPROBLEM" + index + ")", "@SP", "A=M", "D=M", "@SP", "A=M-1",
                    "D=D-M", "M =-1", "@END" + index, "D;JGT", "@SP", "A = M-1", "M=0",
                    "(END" + index + ")", "@SP", "A = M", "M=0"],

               "gt": ["@SP", "AM=M-1", "D= M", "@R13", "M=-1", "@POSITIVE1" + index,
                      "D;JGT", "@R13", "M=0", "(POSITIVE1" + index + ")", "@SP", "A=M-1", "D=M", "@R15", "M =D",
                      "@R14", "M=-1", "@POSITIVE2" + index, "D;JGT", "@R14", "M=0", "(POSITIVE2" + index + ")",
                      "@R13", "D=M", "@R14", "D=D-M", "@R15", "M=D", "@NOPROBLEM" + index, "D;JEQ",
                      "@HANDLEPLUS" + index, "D;JGT", "@SP", "A=M-1", "M=0",
                      "@END" + index, "0;JMP",  # if minus - x biger then false
                      "(HANDLEPLUS" + index + ")", "@SP", "A=M-1", "M=-1",
                      "@END" + index, "0; JMP",  # if plus - y is bigger then true
                      "(NOPROBLEM" + index + ")", "@SP", "A=M", "D=M", "@SP", "A=M-1",
                      "D=D-M", "M =0", "@END" + index, "D;JGE", "@SP", "A = M-1", "M=-1",
                      "(END" + index + ")", "@SP", "A = M", "M=0"],

               "eq": ["@SP", "AM=M-1", "D=M", "@R13", "M=-1", "@POSITIVE1" + index, "D;JGT", "@R13", "M=0",
                      "(POSITIVE1" + index + ")", "@SP", "A=M-1", "D=M", "@R14",
                      "M=-1", "@POSITIVE2" + index, "D;JGT", "@R14", "M=0", "(POSITIVE2" + index + ")",
                      "@R13", "D=M", "@R14", "D = D-M", "@R15", "M=D", "@NOPROBLEM" + index, "D;JEQ",
                      "@SP", "A=M-1", "M = 0", "@END" + index, "0;JMP", "(NOPROBLEM" + index + ")", "@SP", "A=M",
                      "D=M", "A=A-1", "D=M-D", "@SP", "A = M-1", "M=-1", "@END" + index, "D;JEQ", "@SP", "A=M-1",
                      "M=0", "(END" + index + ")", "@SP", "A = M", "M = 0"]
               }
        return dic[command]
    """
    saving the location into the stack
    """
    def save_to_stack(self, location):
        return ["@" + location, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    """
    restoring the location from the stack
    """
    def restore_from_stack(self, command, location):
        return ["@R13", "D = M", "@"+str(location),"A = D-A", "D = M", "@"+command, "M=D"]
    """
    function that writes a label in asm
    """
    def writelabel(self, string):
        return ["(" + string + ")"]

    """
    function the writes the goto cammand
    """
    def writegoto(self, string):
        return ["@" + string, "0; JMP"]
    """
    function that writes the if-goto command
    """
    def writeif(self, string):
        return ["@SP", "M=M-1", "A=M", "D=M", "@" + string, "D ; JNE"]
    """
    writes a function in asm file
    """
    def writefunction(self, string, num):
        strlist = ["(" + string + ")"]
        for i in range(int(num)):
            strlist.extend(self.handle_constant("0"))
        return strlist
    """
    function that writes a call to a function command
    """
    def writecall(self, func, num):
        self.funccounter += 1
        const = "RETURN_"+str(func).upper()+str(self.funccounter)
        strlist= ["@" + const, "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        strlist.extend(self.save_to_stack("LCL"))
        strlist.extend(self.save_to_stack("ARG"))
        strlist.extend(self.save_to_stack("THIS"))
        strlist.extend(self.save_to_stack("THAT"))
        strlist.extend(["@" + str(int(num) + 5), "D=A", "@SP", "D=M-D", "@ARG", "M=D", "@SP", "D=M", "@LCL", "M=D",
                        "@"+str(func), "0;JMP", "("+const+")"])
        return strlist
    """
    funciton that writes a return command 
    """
    def writereturn(self):
        strlist = ["@LCL", "D = M", "@R13", "M=D", "@5", "D=D-A", "A=D", "D=M", "@R14", "M=D","@SP", "AM = M-1", "D=M",
                   "@ARG","A=M", "M=D", "@ARG", "D=M", "@SP", "M=D+1"]
        strlist.extend(self.restore_from_stack("THAT", 1))
        strlist.extend(self.restore_from_stack("THIS", 2))
        strlist.extend(self.restore_from_stack("ARG", 3))
        strlist.extend(self.restore_from_stack("LCL", 4))
        strlist.extend(["@R14", "A = M", "0;JMP"])
        return strlist
    """
    function that will be called for writing in the start of any asm translated file 
    """
    def writeinit(self):
        strlist = ["@256", "D=A", "@SP", "M=D"]
        funclist = self.writecall("Sys.init", "0")
        funclist[0] = funclist[0].replace("1", "")
        funclist[-1] = funclist[-1].replace("1", "")
        # strlist.extend(self.writecall("Sys.init", "0"))
        strlist.extend(funclist)
        return strlist

"""
the main function. here we will open the file, read it, translate it using the parser and the writer
and then write the translation into an asm file.
"""


def main():
    files = []
    output = []
    counter = 0
    if os.path.isdir(sys.argv[1]):
        dirname = os.path.basename(sys.argv[1])
        path = os.path.abspath(sys.argv[1])
        outputfile = str(path) + "/" + dirname + ".asm"
        for filename in os.listdir(path + "/"):
            if filename.endswith('.vm'):
                files.append(filename)
    elif str(sys.argv[1]).endswith('.vm'):
        path = ""
        files.append(str(sys.argv[1]))
        outputfile = os.path.abspath(sys.argv[1]).replace('vm', 'asm')
    else:
        return
    for file in files:
        with open(os.path.join(path, file), 'r') as f:
            writer = Writer(f, file)
            writer.handle_commands()
            if counter == 0:
                output.extend(writer.writeinit())
                counter +=1
            output.extend(writer.translation)
            outname = str(file).replace('vm', 'asm')
    with open(outputfile, 'w') as f:
        for out in output:
            f.write(out + '\n')


if __name__ == "__main__":
    main()

