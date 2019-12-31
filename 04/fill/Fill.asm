// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm



(START)
	// row=256, pixels per row=512, register is 16bit; 
	// (256x512)/16 = 8192 screen ratio
	@8192
	D=A
	@numScreenRegistersToPaint
	M=D

	// Set the value of var currentScreenRegister to 
	// the first register of the screen
	@SCREEN
	D=A
	@currentScreenRegister
	M=D

	// Set D to the value of keyboard. 0=No press, 1=press

	@KBD
	D=M

	// set paint color to white
	@SETWHITE
	D; JEQ

	// set paint color to black
	@SETBLACK
	0; JMP

(SETWHITE)
	@color
	M=0 // set the 16bit reg to 0 which is 0000... in binary
	// so all bits/pixels in that reg will be 0(white)

	@PAINT
	0;JMP


(SETBLACK)
	@color
	M=-1 // set the 16bit reg to -1 which is 1111... in binary
	// so all bits/pixels in that reg will be 1(black)

	@PAINT
	0;JMP

// Paint the screem
(PAINT)
	// Set D to value of color
	@color
	D=M

	// Set the value of A to the screen register number 
	// and set the reg to color (0 white; -1 black)
	@currentScreenRegister
	A=M
	M=D

	// Add one to currentScreenRegister (move to next reg)
	@currentScreenRegister
	M=M+1

	// Subtract 1 from numScreenRegistersToPaint
	@numScreenRegistersToPaint
	M=M-1
	D=M

	// if numScreenRegistersToPaint is 0, go to start program
	@START
	D; JEQ

	// if numScreenRegistersToPaint is not 0, continue painting
	@PAINT
	0; JMP
