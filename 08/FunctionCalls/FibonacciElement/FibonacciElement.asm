@256
D=A
@SP
M=D
@RETURN_SYS.INIT3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(RETURN_SYS.INIT3)
(Main.fibonacci)
@ARG
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
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
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
M =-1
@END1
D;JGT
@SP
A = M-1
M=0
(END1)
@SP
A = M
M=0
@SP
M=M-1
A=M
D=M
@IF_TRUE
D ; JNE
@IF_FALSE
0; JMP
(IF_TRUE)
@ARG
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
@LCL
D = M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
AM = M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D = M
@1
A = D-A
D = M
@THAT
M=D
@R13
D = M
@2
A = D-A
D = M
@THIS
M=D
@R13
D = M
@3
A = D-A
D = M
@ARG
M=D
@R13
D = M
@4
A = D-A
D = M
@LCL
M=D
@R14
A = M
0;JMP
(IF_FALSE)
@ARG
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
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=D
@RETURN_MAIN.FIBONACCI1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_MAIN.FIBONACCI1)
@ARG
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
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=D
@RETURN_MAIN.FIBONACCI2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_MAIN.FIBONACCI2)
@SP
AM=M-1
D=M
A=A-1
D=M+D
M=D
@LCL
D = M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
AM = M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D = M
@1
A = D-A
D = M
@THAT
M=D
@R13
D = M
@2
A = D-A
D = M
@THIS
M=D
@R13
D = M
@3
A = D-A
D = M
@ARG
M=D
@R13
D = M
@4
A = D-A
D = M
@LCL
M=D
@R14
A = M
0;JMP
(Sys.init)
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@RETURN_MAIN.FIBONACCI1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_MAIN.FIBONACCI1)
(WHILE)
@WHILE
0; JMP
