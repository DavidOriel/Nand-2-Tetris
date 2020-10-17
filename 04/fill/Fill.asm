// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// 
 
(LOOP)
    @8191 	// the number of pixels we need to draw in the screen, 256*512/16 
	D = A
	@R1     // our conter
	M = D
	@KBD    // get keyboard input
	D=M
	@WHITE  // jump to white
	D; JEQ
	@BLACK  // jump to black
	0; JMP
		
(WHITE)
	@R0
	M=0
	@DRAW
	0; JMP

(BLACK)
	@R0
	M=-1
	@DRAW
	0; JMP

	
(DRAW)
	@R1
	D = M
	@addr 
	M = D
	@SCREEN   // get the screen address
	D=A
	@addr     // current address of the pixel
	M= M+D
	@R0       // contains the input from the keyboard
	D=M
 	@addr     // draw
	A=M
	M=D
	@R1
	D = M-1
	M = D
	@DRAW
	D; JGE
	@LOOP
	0; JMP
	
	
	
