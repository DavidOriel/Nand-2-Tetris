import sys
import os

# Constant tables for binary values for instructions.
comp = {'0': '0101010', '1': '0111111','-1': '0111010', 'D': '0001100', 'A': '0110000', '!D': '0001101',
        '!A': '0110001', '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
        'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
        'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010',
        'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000', 'D|M': '1010101'}

dest = {None: '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}

jump = {None: '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

shift = {'D<<': '0110000', 'D>>': '0010000', 'A<<': '0100000', 'A>>': '0000000', 'M<<': '1100000', 'M>>': '1000000'}


# Main method that checks if the given argument is a folder or a file, verifies that is it an asm file,
# And runs the program in the following order: Parse file, add symbols, and generate to binary code.
def main():
    files = []
    if os.path.isdir(sys.argv[1]):
        path = os.path.abspath(sys.argv[1])+'\\'
        for filename in os.listdir(path):
            if filename.endswith('.asm'):
                files.append(filename)
    elif str(sys.argv[1]).endswith('.asm'):
        path = ''
        files.append(str(sys.argv[1]))
    else:
        return
    for file in files:
        with open(file, 'r') as f:
            lines = parser(f)
        symbols = SymbolTable(lines)
        output = code(lines, symbols)
        outname = str(file).replace('asm', 'hack')
        with open(path+outname, 'w') as f:
            for out in output:
                f.write(out+'\n')


# The parser gets the arguments from the user or the filename, removes spaces, tabs, \n's, comments and returns
# a list with all lines separated by cells.
def parser(f):
    file = []
    lines = []
    for line in f:
        file.append(line)
    for line in file:
        line = line.replace(" ", "")
        line = line.replace("  ", "")
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        line = line.split('//')[0]
        if line:
            lines.append(line)
    return lines


# A code method that gets the parsed lines of the file and the symbols dictionary, and does the following:
# Checks if the instruction is an A or a C command.
# If it's an A: simply adds the address to the output as a binary number. If the address exist in the symbols table,
# it adds the corresponding value of it to the output.
# If it's a C: splits the instruction to comp, dest and jump. checks if the instruction is a shift or not and defines
# the first 3 digits according to the condition result. than gets the corresponding values from the dictionary according
# to the instruction. returns an output that contains string of binary numbers that represents the instructions in
# hack lang.
def code(lines, symbols):
    out = []
    for line in lines:
        if line.startswith('@', 0, 1):
            temp = line.strip('@')
            if temp in symbols:
                val = '{0:016b}'.format(symbols.get(temp))
            else:
                val = '{0:016b}'.format(int(temp))
            out.append(val)
        elif not line.startswith('(', 0, 1):
            ins1 = line.split('=')
            ins2 = ins1[len(ins1)-1].split(';')
            if ins2[0] in shift:
                val = '101'
                val += shift.get(ins2[0])
            else:
                val = '111'
                val += comp.get(ins2[0])
            if len(ins1) == 1:
                val += dest.get(None)
            else:
                val += dest.get(ins1[0])
            if len(ins2) == 1:
                val += jump.get(None)
            else:
                val += jump.get(ins2[1])
            out.append(val)
    return out


# The SymbolTable method gets the lines array and does the following:
# in the first for loop, it goes over the lines and finds addresses pointer (the ones with the parentheses) and
# gives them the correct value according to their line number. In the second for loop, it finds all the variables
# and adds them to the dictionary. At the end, returns an updated symbols table.
def SymbolTable(lines):
    symboltable = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8,
                   'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
                   'SCREEN': 16384, 'KBD': 24576, 'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4}
    counter = 0
    for line in lines:
        if line.startswith('(', 0, 1):
            temp = line.strip('()')
            symboltable[temp] = counter
        else:
            counter += 1
    counter = 16
    for line in lines:
        temp = line.strip('@')
        if line.startswith('@', 0, 1) and temp not in symboltable and not temp.isdigit():
            symboltable[temp] = counter
            counter += 1
    return symboltable


if __name__ == "__main__":
    main()
