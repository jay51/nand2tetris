arithmetic_ops = {
"add":"""
// ADD TWO NUMBERS 
        @SP
        D=M-1
        M=D
        A=M
        D=M 
        @R13
        M=D
        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R14
        M=D
        @R13
        D=M
        @R14
        D=D+M
        @SP
        A=M
        M=D
        D=A+1
        @SP
        M=D
// ADD TWO NUMBERS/
        """,
"sub": """
// SUB TWO NUMBERS
              @SP
        D=M-1
        M=D
        A=M
        D=M
        @R14
        M=D

        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R13
        M=D

        @R13
        D=M
        @R14
        D=D-M

        @SP
        A=M
        M=D
        D=A+1
        @SP
        M=D
// SUB TWO NUMBERS/
        """,
"neg": """
// NEG INSTRUCTION
        @SP
        D=M-1
        M=D
        A=M
        D=-M

        @SP
        A=M
        M=D
        D=A+1
        @SP
        M=D
// NEG INSTRUCTION/
        """,
"eq": """
// EQ INSTRUCTION
        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R13
        M=D

        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R14
        M=D

        @R13
        D=M
        @R14
        D=D-M
        @{random}.NOT_EQUAL
        D;JNE

        D=-1
        @{random}.PUSH_RESULT
        1;JMP

        ({random}.NOT_EQUAL)
        D=0

        ({random}.PUSH_RESULT)
        @SP
        A=M
        M=D
        D=A+1
        @SP
        M=D
// EQ INSTRUCTION/
        """,
"gt": """
// GT INSTRUCTION
        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R14
        M=D

        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R13
        M=D

        @R13
        D=M
        @R14
        D=D-M
        @{random}.GREATER_THAN
        D;JGT

        D=0
        @{random}.PUSH_RESULT
        1;JMP

        ({random}.GREATER_THAN)
        D=-1

        ({random}.PUSH_RESULT)
        @SP
        A=M
        M=D
        D=A+1
        @SP
        M=D
// GT INSTRUCTION/
        """,
"lt": """
// LT INSTRUCTION
        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R14
        M=D

        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R13
        M=D

        @R13
        D=M
        @R14
        D=D-M
        @{random}.LESS_THAN
        D;JLT

        D=0
        @{random}.PUSH_RESULT
        1;JMP

        ({random}.LESS_THAN)
        D=-1

        ({random}.PUSH_RESULT)
        @SP
        A=M
        M=D
        D=A+1
        @SP
        M=D
// LT INSTRUCTION/
        """,
"and": """
// AND INSTRUCTION
        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R13
        M=D

        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R14
        M=D

        @R13
        D=M
        @R14
        D=D&M

        @SP
        A=M
        M=D
        D=A+1
        @SP
        M=D
// AND INSTRUCTION/
        """,
"or": """
// OR INSTRUCTION
        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R13
        M=D

        @SP
        D=M-1
        M=D
        A=M
        D=M
        @R14
        M=D

        @R13
        D=M
        @R14
        D=D|M

        @SP
        A=M
        M=D
        D=A+1
        @SP
        M=D
// OR INSTRUCTION/
        """,
"not": """
// NOT INSTRUCTION
        @SP
        D=M-1
        M=D
        A=M
        D=!M

        @SP
        A=M
        M=D
        D=A+1
        @SP
        M=D
// NOT INSTRUCTION/
        """
}



pop_instruction = {
"local": """
// POP LOCAL
        @{position}
        D=A
        @LCL
        D=D+M   
        @R12
        M=D     

        @SP
        M=M-1
        A=M
        D=M

        @R12
        A=M
        M=D
// POP LOCAL/
        """,
"argument": """
// POP ARGUMENT
        @{position}
        D=A
        @ARG
        D=D+M   

        @R12
        M=D     
        @SP
        M=M-1
        A=M
        D=M

        @R12
        A=M
        M=D
// POP ARGUMENT/
        """,
"temp": """
// POP TEMP
        @SP
        M=M-1
        A=M
        D=M
        @{position}
        M=D
// POP TEMP/
        """,
        "static": """
// POP STATIC
        @SP
        M=M-1
        A=M
        D=M
        @{static-var}
        M=D
// POP STATIC/
        """,
"pointer": """
// POP POINTER
        @SP
        M=M-1
        A=M
        D=M

        @{THIS_THAT}
        M=D
// POP POINTER/
        """,
"that": """
// POP THAT
        @{position}
        D=A
        @THAT
        D=D+M
        @R13
        M=D

        @SP
        M=M-1
        A=M
        D=M
        @R13
        A=M
        M=D
// POP THAT/
        """,
"this": """
// POP THIS
        @{position}
        D=A
        @THIS
        D=D+M

        @R13
        M=D
        @SP
        M=M-1
        A=M
        D=M

        @R13
        A=M
        M=D
// POP THIS/
        """
}




push_instruction = {
"local": """
// PUSH LOCAL
        @{position}
        D=A     
        @LCL
        A=D+M
        D=M

        @SP
        A=M
        M=D
        @SP
        M=M+1
// PUSH LOCAL/
        """,
"argument": """
// PUSH ARGUMENT
        @{position}
        D=A
        @ARG
        A=D+M   
        D=M

        @SP
        A=M
        M=D

        @SP
        M=M+1
// PUSH ARGUMENT/
        """,
"temp": """
// POP TEMP
        @SP
        M=M-1
        A=M
        D=M
        @{position}
        M=D
// POP TEMP/
        """,
"constant": """
// PUSH CONSTANT
        @{position}
        D=A
        @SP
        A=M
        M=D

        @SP
        M=M+1
// PUSH CONSTANT/
        """,
"temp": """
// PUSH TEMP
        @{position}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
// PUSH TEMP/
        """,
"static": """
// PUSH STATIC
        @{static-var}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
// PUSH STATIC/
        """,
"pointer": """
// PUSH POINTER
        @{THIS_THAT}
        D=M

        @SP
        A=M
        M=D
        @SP
        M=M+1 
// PUSH POINTER/
        """,
"that": """
// PUSH THAT
        @{position}
        D=A
        @THAT
        A=D+M
        D=M


        @SP
        A=M
        M=D
        @SP
        M=M+1
// PUSH THAT/
        """,
"this": """
// PUSH THIS
        @{position}
        D=A
        @THIS
        A=D+M
        D=M

        @SP
        A=M
        M=D
        @SP
        M=M+1
// PUSH THIS/
        """
}


branching_instruction = {
"label": """
// DEFINE LABEL
        ({label-name})
// DEFINE LABEL/
        """,
"goto": """
// GOTO LABEL
        @{label-name}
        0;JMP
// GOTO LABEL/
        """,
"if-goto": """
// IF-GOTO LABEL
        @SP
        M=M-1
        A=M
        D=M
        @{label-name}
        D;JNE
// IF-GOTO LABEL/
"""
}


function_instruction = {
"return": """
// CALL RETURN
    // SAVE LCL TO R13
        @LCL
        D=M
        @R13
        M=D

    // SAVE RETURN ADDRESS TO R14
        @5
        A=D-A
        D=M
        @R14
        M=D

    // set arg to hold return value
        @SP
        M=M-1
        A=M
        D=M
        @ARG
        A=M
        M=D

    // RESET STACK POINTER
        @ARG
        D=M+1
        @SP
        M=D

    // RESET THAT
        @R13
        A=M-1
        D=M
        @THAT
        M=D

    // RESET THIS
        @R13
        D=M
        @2
        A=D-A
        D=M
        @THIS
        M=D

    // RESET ARG
        @R13
        D=M
        @3
        A=D-A
        D=M
        @ARG
        M=D

    // RESET LCL
        @R13
        D=M
        @4
        A=D-A
        D=M
        @LCL
        M=D

    // RETURN
        @R14
        A=M
        0;JMP
// CALL RETURN/
        """,
"call": """
// CALL FUNCTION
        @{return-address}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1

    // PUSH LCL, ARG, THIS, THAT
        @LCL
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1

        @ARG
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1

        @THIS
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1

        @THAT
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1

    // LCL = SP
        @SP
        D=M
        @LCL
        M=D

    // ARG = SP-n-5
        @SP
        D=M
        @{num-args}
        D=D-A
        @5
        D=D-A
        @ARG
        M=D

    // GO TO FUNCTION
        @{function-name}
        0;JMP

    ({return-address})
// CALL FUNCTION/
        """,
"function": """
// DEFINE FUNCTION
        ({function-name})
        {N-LCL}
// DEFINE FUNCTION/
        """
}


init_code = """
        @256
        D=A
        @SP
        M=D
"""

