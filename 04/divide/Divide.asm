// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Divide.asm
// The idea of the algorithm is to check how many times the divider fits in the divisor, in the power of 
// two's, untill the redundant is smaller then the divisor, and during the proccess we decrement the divisor by 
// the last value of the divider shift.
	@ans
	M = 1
	@R15
	M = 0
	@R13
	D = M
	@n
	M = D
	@R14
	D = M
	@m
	M = D
	@counter
	M = 0
	
(LOOP1)
	@n 
	D = M
	@m
	D = D - M
	@END
	D  ; JLT

(LOOP2)
	@m
	D = M
	@WRITEANS
	D ; JLT
	@n
	D = M
	@m
	D = D - M
	@WRITEANS
	D ; JLE
	@m
	D = M
	@tempm
	M = D
	@m
	M = M<<
	@counter
	M = M + 1
	@LOOP2
	0 ; JMP

(WRITEANS)
	@counter
	M = M - 1
	D = M
	@CONT
	D ; JLE
	@ans
	M = M<<
	@WRITEANS
	0 ; JMP
	
(CONT)
	@ans
	D = M
	M = 1
	@R15
	M = M + D	
	@tempm
	D = M
	@n
	M = M - D
	@R14
	D = M
	@m
	M = D
	@LOOP1
	0 ; JMP	

(END)
	@END
	0 ; JMP