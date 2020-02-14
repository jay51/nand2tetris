
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
        @PUSH_RESULT
        0;JMP

(NOT_EQUAL)
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
        some ops
    """,
    "lt": """
        some ops
    """,
    "and": """
        some ops
    """,
    "or": """
        some ops
    """,
    "not": """
        some ops
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
        @{}
        some stuff
    """,
    "that": """
        @{}
        some stuff
    """,
    "this": """
        @{}
        some stuff
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
        @{}
        some stuff
    """,
    "that": """
        @{}
        some stuff
    """,
    "this": """
        @{}
        some stuff
    """
}
