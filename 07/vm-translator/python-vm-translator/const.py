
arithmetic_ops = {
    "add": """
        @SP
        M=M-1   // SP--
        A=M     // jump into location at SP
        D=M     // D = RAM[A] 5
        
        @R12
        M=D     // store first item on stack

        @SP
        M=M-1   // SP--
        A=M     // jump into location at SP
        D=M     // D = RAM[A] 5
        
        @R12
        D=D+M   // add the two items on the stack


        @SP     // store back on stack
        A=M     // jump to location of SP
        M=D     // RAM[*SP] = D

        @SP
        M=M+1   // SP++
    """,
    "sub": """
        some ops
    """
}

pop_instruction = {
    "local": """
        @%s
        D=A
        @LCL
        D=D+M   // D = LCL+i
        
        @R12
        M=D     // RAM[R0] = D
        
        @SP
        M=M-1   // SP--
        A=M     // jump into location at SP
        D=M     // D = RAM[A] 5
        
        @R12
        A=M     // jump to location at LCL+i
        M=D     // LCL[i] = D
    """,
    "argument": """
        @%s
        some stuff
    """,

    "temp": """
        @%s
        some stuff
    """,
    "static": """
        @%s
        some stuff
    """,
    "pointer": """
        @%s
        some stuff
    """,
    "that": """
        @%s
        some stuff
    """,
    "this": """
        @%s
        some stuff
    """

}


push_instruction = {
    "local": """
        @%s
        D=A     // D=i

        @LCL
        A=D+M   // A=LCL+i jump to that memory
        D=M     // D=LCL[i]

        @SP
        A=M     // jump to location of SP
        M=D     // RAM[*SP] = D

        @SP
        M=M+1   // SP++

    """,

    "constant": """
        @%s
        D=A     // store n in D

        @SP
        A=M     // jump to location of SP
        M=D     // RAM[*SP] = D

        @SP
        M=M+1   // SP++
    """,
    "temp": """
        @%s
        some stuff
    """,
    "static": """
        @%s
        some stuff
    """,
    "pointer": """
        @%s
        some stuff
    """,
    "that": """
        @%s
        some stuff
    """,
    "this": """
        @%s
        some stuff
    """
}
