


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
        @{position}
        M=D
// POP STATIC/
        """,
"pointer": """
// POP POINTER

        @{position}
        D=A
        D=D-1
        @{random}-THIS-SEGMENT
        D;JNE

        @{random}-THAT-SEGMENT
        0;JMP

        ({random}-THIS-SEGMENT)
        @SP
        M=M-1
        A=M
        D=M
        @THIS
        M=D


        ({random}-THAT-SEGMENT)
        @SP
        M=M-1
        A=M
        D=M
        @THAT
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
        @{position}
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
        @{position}
        D=A
        D=D-1
        @{random}-THIS-SEGMENT
        D;JNE

        ({random}-THAT-SEGMENT)
        @THAT
        D=M
        @{random}-POINTER.PUSH_RESULT
        0;JMP

        ({random}-THIS-SEGMENT)
        @THIS
        D=M


        ({random}-POINTER.PUSH_RESULT)
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
