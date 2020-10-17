@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=D
//write operator command
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
//handling lt
@SP
AM=M-1
D= M
@R13
M=-1
@POSITIVE11
D;JGT
@R13
M=0
(POSITIVE11)
@SP
A=M-1
D=M
@R15
M =D
@R14
M=-1
@POSITIVE21
D;JGT
@R14
M=0
(POSITIVE21)
@R13
D=M
@R14
D=D-M
@R15
M=D
@NOPROBLEM1
D;JEQ
@HANDLEPLUS1
D;JGT
@SP
A=M-1
M=-1
@END1
0;JMP
(HANDLEPLUS1)
@SP
A=M-1
M=0
@END1
0; JMP
(NOPROBLEM1)
@SP
A=M
D=M
@SP
A=M-1
D=D-M
M =0
@END1
D;JGT
@SP
A = M-1
M=-1
(END1)
@SP
A = M
M=0
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=D
//write operator command
//handling lt
@SP
AM=M-1
D= M
@R13
M=-1
@POSITIVE12
D;JGT
@R13
M=0
(POSITIVE12)
@SP
A=M-1
D=M
@R15
M =D
@R14
M=-1
@POSITIVE22
D;JGT
@R14
M=0
(POSITIVE22)
@R13
D=M
@R14
D=D-M
@R15
M=D
@NOPROBLEM2
D;JEQ
@HANDLEPLUS2
D;JGT
@SP
A=M-1
M=-1
@END2
0;JMP
(HANDLEPLUS2)
@SP
A=M-1
M=0
@END2
0; JMP
(NOPROBLEM2)
@SP
A=M
D=M
@SP
A=M-1
D=D-M
M =0
@END2
D;JGT
@SP
A = M-1
M=-1
(END2)
@SP
A = M
M=0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=D
//write operator command
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@SP
AM=M-1
D= M
@R13
M=-1
@POSITIVE13
D;JGT
@R13
M=0
(POSITIVE13)
@SP
A=M-1
D=M
@R15
M =D
@R14
M=-1
@POSITIVE23
D;JGT
@R14
M=0
(POSITIVE23)
@R13
D=M
@R14
D=D-M
@R15
M=D
@NOPROBLEM3
D;JEQ
@HANDLEPLUS3
D;JGT
@SP
A=M-1
M=0
@END3
0;JMP
(HANDLEPLUS3)
@SP
A=M-1
M=-1
@END3
0; JMP
(NOPROBLEM3)
@SP
A=M
D=M
@SP
A=M-1
D=D-M
M =-1
@END3
D;JGT
@SP
A = M-1
M=0
(END3)
@SP
A = M
M=0
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=D
//write operator command
@SP
AM=M-1
D= M
@R13
M=-1
@POSITIVE14
D;JGT
@R13
M=0
(POSITIVE14)
@SP
A=M-1
D=M
@R15
M =D
@R14
M=-1
@POSITIVE24
D;JGT
@R14
M=0
(POSITIVE24)
@R13
D=M
@R14
D=D-M
@R15
M=D
@NOPROBLEM4
D;JEQ
@HANDLEPLUS4
D;JGT
@SP
A=M-1
M=0
@END4
0;JMP
(HANDLEPLUS4)
@SP
A=M-1
M=-1
@END4
0; JMP
(NOPROBLEM4)
@SP
A=M
D=M
@SP
A=M-1
D=D-M
M =-1
@END4
D;JGT
@SP
A = M-1
M=0
(END4)
@SP
A = M
M=0
