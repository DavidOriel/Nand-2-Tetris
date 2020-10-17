

symbols = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R1O': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4
}

dest = {
    'null': ' 000',
    'M': '001',
    'D': '010',
    'MD':'011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AND':'111',
}
jumps= {
    'null' :' 000',
    'JGT' : "001",
    'JEQ' : '010',
    'JGE' : ' 011',
    'JLT' : '100',
    'JNE' : '101',
    'JLE' : ' 110',
    'JMP' : '111',

}
comp = {
    '0' : '101010',
    '1' : '111111',
    '-1' : '111010',
    'D': '001100',
    'A': '110000',
    '!D': '001101',
    '!A': '110001',
    '-D': '001111',
    '-A': '110011',
    'D+1':'011111',
    'A+1':'110111',
    'D-1':'001110',
    'A-1':'110010',
    'D+A': '000010',
    'D-A':'010011',
    'A-D':'000111',
    'D&A': '000000',
    'D!A': '010101'
}



def readfile(file):
    f = open("file", "r")
    return f

def remove_comments(line):
    line = line.split("//")[0]
    return line

def read_and_order(f):
    hack_instructions = []
    while True:
        x = f.readline()
        if x == "\n":
            continue
        x = "".join(x.split())
        x = remove_comments(x)
        hack_instructions.append(x)
        if not x:
            break
    return hack_instructions

