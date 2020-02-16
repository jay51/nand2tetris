

// TODO: 
//  refactore the pointer segemnt (pass this and that using python)
//  generate a rendom number with each label


arithmetic_ops = {
    "add": """
// SP--
        @SP
        M=M-1   

// JUMP INTO LOCATION AT SP
        A=M 
// SET D = RAM[A]
        D=M 
        
// STORE D IN R13
        @R13
        M=D 

// SP--
        @SP
        M=M-1 

// JUMP INTO LOCATION AT SP
        A=M     
// SET D = RAM[A]
        D=M     

// ADD THE TWO NUMBERS 
        @R13
        D=D+M   

// STORE BACK ON STACK
        @SP
        A=M
        M=D

// SP++
        @SP
        M=M+1
    """,
    "sub": """
// SP--
        @SP
        M=M-1   

// JUMP INTO LOCATION AT SP
        A=M 
// SET D = RAM[A]
        D=M 
        
// STORE D IN R13, DON'T USE TEMP
        @R13
        M=D 

// SP--
        @SP
        M=M-1 

// JUMP INTO LOCATION AT SP
        A=M     
// SET D = RAM[A]
        D=M     

// SUB THE TWO NUMBERS 
        @R13
        D=M-D   

// STORE BACK ON STACK
        @SP
        A=M
        M=D

// SP++
        @SP
        M=M+1
    """,
    "neg": """
        @SP
        M=M-1
        A=M

// NEG INSTRUCTION
        D=-M

// STORE BACK ON STACK
        @SP
        A=M
        M=D
// SP++
        @SP
        M=M+1 
    """,
    "eq": """
    
// SP--
        @SP
        M=M-1   

// JUMP INTO LOCATION AT SP
        A=M 
// SET D = RAM[A]
        D=M 
        
// STORE D IN R13, DON'T USE TEMP
        @R13
        M=D 

// SP--
        @SP
        M=M-1 

// JUMP INTO LOCATION AT SP
        A=M     
// SET D = RAM[A]
        D=M     

        @R13
        D=D-M

// JUMP TO NOT_EQUAL IF D != 0
        @NOT_EQUAL
        D;JNE


// JUMP IF EQUAL
        D=-1
        @PUSH_RESULT
        0;JMP


        ({}-NOT_EQUAL)
        D=0


        (PUSH_RESULT)
// STORE BACK ON STACK
        @SP
        A=M
        M=D
// SP++
        @SP
        M=M+1
    """,
    "gt": """
    
// SP--
        @SP
        M=M-1   

// JUMP INTO LOCATION AT SP
        A=M 
// SET D = RAM[A]
        D=M 
        
// STORE D IN R13, DON'T USE TEMP
        @R13
        M=D 

// SP--
        @SP
        M=M-1 

// JUMP INTO LOCATION AT SP
        A=M     
// SET D = RAM[A]
        D=M     

        @R13
        D=D-M

// JUMP IF D > 0
        @GREATER-THAN
        D;JGT


        D=0
        @PUSH_RESULT
        0;JMP

        (GREATER-THAN)
        D=-1


        (PUSH_RESULT)
// STORE BACK ON STACK
        @SP
        A=M
        M=D
// SP++
        @SP
        M=M+1

    """,
    "lt": """

// SP--
        @SP
        M=M-1   

// JUMP INTO LOCATION AT SP
        A=M 
// SET D = RAM[A]
        D=M 
        
// STORE D IN R13, DON'T USE TEMP
        @R13
        M=D 

// SP--
        @SP
        M=M-1 

// JUMP INTO LOCATION AT SP
        A=M     
// SET D = RAM[A]
        D=M     

        @R13
        D=D-M

// JUMP IF D < 0
        @LESS-THAN
        D;JLT


        D=0
        @PUSH_RESULT
        0;JMP

        (LESS-THAN)
        D=-1


        (PUSH_RESULT)
// STORE BACK ON STACK
        @SP
        A=M
        M=D
// SP++
        @SP
        M=M+1

    """,
    "and": """

// SP--
        @SP
        M=M-1   

// JUMP INTO LOCATION AT SP
        A=M 
// SET D = RAM[A]
        D=M 
        
// STORE D IN R13, DON'T USE TEMP
        @R13
        M=D 

// SP--
        @SP
        M=M-1 

// JUMP INTO LOCATION AT SP
        A=M     
// SET D = RAM[A]
        D=M     

        @R13
        D=D&M

// STORE BACK ON STACK
        @SP
        A=M
        M=D
// SP++
        @SP
        M=M+1
    """,
    "or": """

// SP--
        @SP
        M=M-1   

// JUMP INTO LOCATION AT SP
        A=M 
// SET D = RAM[A]
        D=M 
        
// STORE D IN R13, DON'T USE TEMP
        @R13
        M=D 

// SP--
        @SP
        M=M-1 

// JUMP INTO LOCATION AT SP
        A=M     
// SET D = RAM[A]
        D=M     

        @R13
        D=D|M

// STORE BACK ON STACK
        @SP
        A=M
        M=D
// SP++
        @SP
        M=M+1
    """,
    "not": """

// SP--
        @SP
        M=M-1   

// JUMP INTO LOCATION AT SP
        A=M 
// SET D = RAM[A]
        D=M 
        
// STORE D IN R13, DON'T USE TEMP
        @R13
        M=D 

// SP--
        @SP
        M=M-1 

// JUMP INTO LOCATION AT SP
        A=M     
// SET D = RAM[A]
        D=M     

        @R13
        D=!M

// STORE BACK ON STACK
        @SP
        A=M
        M=D
// SP++
        @SP
        M=M+1
    """
}




pop_instruction = {
    "local": """
// D = LCL+i
        @{}
        D=A
        @LCL
        D=D+M   
        
// SET RAM[R12] = D
        @R12
        M=D     

// SP--
        @SP
        M=M-1
// JUMP INTO LOCATION AT SP
        A=M
// D = RAM[A]
        D=M
        
// JUMP TO LOCATION AT LCL+i
        @R12
        A=M
// LCL[i] = D
        M=D
    """,
    "argument": """
// D = ARG+i
        @{}
        D=A
        @ARG
        D=D+M   
        
// SET RAM[R12] = D
        @R12
        M=D     

// SP--
        @SP
        M=M-1
// JUMP INTO LOCATION AT SP
        A=M
// D = RAM[A]
        D=M
        
// JUMP TO LOCATION AT ARG+i
        @R12
        A=M
// ARG[i] = D
        M=D
    """,
    "temp": """
// SP--
        @SP
        M=M-1
// JUMP INTO LOCATION AT SP
        A=M
// D = RAM[A]
        D=M

// TEMP+i = D
        @{}
        M=D
    """,
    "static": """
// SP--
        @SP
        M=M-1
// JUMP INTO LOCATION AT SP
        A=M
// D = RAM[A]
        D=M

// STATIC+i = D
        @{}
        M=D
    """,
    "pointer": """

// i = 0(THIS) OR i = 1(THAT)
        @{}
        D=A
// IF i = 0; (i - 1) != 0 ELSE (i - 1) == 0
        D=D-1
        @THIS.SEGMENT
// IF i == 0 JUMP TO THIS.SEGMENT
        D;JNE

// IF ABOVE CODE DOSEN'T JUMP THAN JUMP TO THAT.SEGMENT
        @THAT.SEGMENT
        0;JMP


        (THIS.SEGMENT)
// SP--
        @SP
        M=M-1
        A=M
        D=M
        
        @THIS
        M=D


        (THAT.SEGMENT)
// SP--
        @SP
        M=M-1
        A=M
        D=M
        
        @THAT
        M=D
    """,
    "that": """
        @{}
        D=A

        @THAT
        D=D+M

        @R13
        M=D

// SP--
        @SP
        M=M-1

        A=M
        D=M

// STORE VALUE ON STACK IN  i+THAT (RAM[i+THAT]=*SP)
        @R13
        A=M
        M=D

    """,
    "this": """
        @{}
        D=A

        @THIS
        D=D+M

        @R13
        M=D

// SP--
        @SP
        M=M-1

        A=M
        D=M

// STORE VALUE ON STACK IN  i+THIS (RAM[i+THIS]=*SP)
        @R13
        A=M
        M=D
    """

}




push_instruction = {
    "local": """
// D=i
        @{}
        D=A     

// A=LCL+i JUMP TO THAT MEMORY AND STORE VALUE IN D
        @LCL
        A=D+M
        D=M

// JUMP TO LOCATION OF SP
        @SP
        A=M

// SET RAM[*SP] = D
        M=D

// SP++
        @SP
        M=M+1

    """,
    "constant": """
// D=i
        @{}
        D=A

// JUMP TO LOCATION OF SP AND STORE i THERE
        @SP
        A=M
        M=D

// SP++
        @SP
        M=M+1
    """,
    "temp": """
// D = TEMP+i
        @{}
        D=M

// JUMP INTO LOCATION AT SP
        @SP
        A=M
        M=D
// SP++
        @SP
        M=M+1
    """,
    "static": """
// D = STATIC+i
        @{}
        D=M

// JUMP INTO LOCATION AT SP
        @SP
        A=M
        M=D
// SP++
        @SP
        M=M+1
    """,
    "pointer": """
// i = 0(THIS) OR i = 1(THAT)
        @{}
        D=A
// IF i = 0; (i - 1) != 0 ELSE (i - 1) == 0
        D=D-1
        @THIS.SEGMENT
// IF i == 0 JUMP TO THIS.SEGMENT
        D;JNE

        (THAT.SEGMENT)
        @THAT
        D=M
        @POINTER.PUSH_RESULT
        0;JMP


        (THIS.SEGMENT)
        @THIS
        D=M


        (POINTER.PUSH_RESULT)
// STORE BACK ON STACK
        @SP
        A=M
        M=D
// SP++
        @SP
        M=M+1 
    """,
    "that": """
        @{}
        D=A

        @THAT
        A=D+M
        D=M


        @SP
        A=M
        M=D
        
// SP++
        @SP
        M=M+1
    """,
    "this": """
        @{}
        D=A

        @THIS
        A=D+M
        D=M


        @SP
        A=M
        M=D
        
// SP++
        @SP
        M=M+1
    """
}
