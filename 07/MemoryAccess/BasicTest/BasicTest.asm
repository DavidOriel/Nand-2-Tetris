@10
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@LCL
D=M
@0
A=D+A
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//printing pop1
@21
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@22
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@ARG
D=M
@2
A=D+A
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//printing pop1
@ARG
D=M
@1
A=D+A
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//printing pop1
@36
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@THIS
D=M
@6
A=D+A
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//printing pop1
@42
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@45
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@THAT
D=M
@5
A=D+A
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//printing pop1
@THAT
D=M
@2
A=D+A
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//printing pop1
@510
D=A
@SP
A=M
M=D
@SP
M=M+1
//handling constant
@SP
A=M-1
D=M
@R11
M=D
@SP
M=M-1
//printing pop2 
@LCL
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
//printing push 2
@THAT
D=M
@5
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
//printing push 2
@SP
AM=M-1
D=M
A=A-1
D=M+D
M=D
//write operator command
@ARG
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
//printing push 2
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=D
//write operator command
@THIS
D=M
@6
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
//printing push 2
@THIS
D=M
@6
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
//printing push 2
@SP
AM=M-1
D=M
A=A-1
D=M+D
M=D
//write operator command
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=D
//write operator command
@R11
D=M
@SP
A=M
M=D
@SP
M=M+1
//printing push 1
@SP
AM=M-1
D=M
A=A-1
D=M+D
M=D
//write operator command
