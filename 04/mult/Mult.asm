// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

	@R2  	// here the outcome will be stored
	M = 0
	@R0 	//first number 
	D = M
	@i      // i represent the number of time we will add the other number to itself
	M = D
(LOOP)
	@i
	D = M
	@END     // jump if the loop has ended
	D; JEQ
	@i
	M = M-1

	@R1      // the second number will be added to itself
	D=M
	@R2
	M = M+D

	@LOOP
	0 ; JMP

(END)
	@END
	0; JMP

