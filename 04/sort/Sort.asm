// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Sort.asm

	
	@R15
	D = M
	@END
	D ; JEQ
	@length
	M = D
	@j
	M = 1
	
(OUTLOOP)

	@j
	D = M
	@length
	D = D - M
	@END
	D ;JGE
	
	@length
	D = M
	@j
	D = D - M
	@innerlength
	M = D
	@i  
	M = 0
	
(INNERLOOP) 				// the inner loop
	@i 				//i is the index of the inner loop
	M = M +1
	D = M
	@innerlength	
	D = D- M
	@SETIN
	D; JGT
	@R14
	D = M
	@i
	D = D - M
	@R15
	D = D + M
	@first
	M = D
	A = D
	D = M
	@first
	A = M -1
	D = D- M
	@SWITCH			// jump to switch if yes, if its bellow zero
	D; JGE
	@INNERLOOP           // jump to set if we dont need to switch
	0; JMP
	
(SWITCH)           // here we will switch between the numbers 
	@first
	A = M
	D = M
	@temp
	M = D
	@first
	A = M -1
	D = M
	@first
	A = M
	M = D
	@temp
	D = M
	@first
	A = M -1
	M = D
	@INNERLOOP
	0; JMP

(SETIN) // here we will update the outer loop index
	@j
	M = M+1
	@OUTLOOP
	0; JMP
		

(END)
	@END
	
