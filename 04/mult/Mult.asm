// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@i
M=0
@R2
M=0

(LOOP)
	@R0 	// load first R0
	D=M 	// set D=R0
	@i	// load counter
	D=D-M	// D=counter - R0
	@END	// load the bread addr
	D;JEQ 	// if D==0,then break
	@R1 	// load second R1
	D=M 	// D=R1
	@R2	// load R2
	M=D+M	// set R2=R2+R1
	@i	// The rest increment i(counter)
	M=M+1
	@LOOP
	0;JMP
(END)
	@END
	0;JMP

