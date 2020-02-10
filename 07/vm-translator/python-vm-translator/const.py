
arithmetic_ops = {
    "add": """
// SP--
        @SP
        M=M-1   

// JUMP INTO LOCATION AT SP
        A=M 
// SET D = RAM[A]
        D=M 
        
// STORE D IN R12
        @R12
        M=D 

// SP--
        @SP
        M=M-1 

// JUMP INTO LOCATION AT SP
        A=M     
// SET D = RAM[A]
        D=M     

// ADD THE TWO NUMBERS 
        @R12
        D=D+M   

// STORE BACK ON STACK
        @SP
        A=M
        M=D

// SP++
        @SP
        M=M+1
    """,
    "neg": """
        some ops
    """,
    "eq": """
        some ops
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
        @{}
        some stuff
    """,

    "temp": """
        @{}
        some stuff
    """,
    "static": """
        @{}
        some stuff
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
        @{}
        some stuff
    """,
    "static": """
        @{}
        some stuff
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
