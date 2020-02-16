#!/usr/bin/env python

# Arithmetic/logical commands
# add   x + y
# sub   x - y
# neg   -x
# eq    true if x = y, else false (pops 2 args)
# gt    true if x > y, else false (pops 2 args)
# lt    true if x < y, else false (pops 2 args)
# ...


# variable types:
# - Argument var
# - Local var
# - Staic var

# pointer manipulation:
"""
D = *p      0 |257|p
            1 |102|q
            ..|...|..
            257|23|
 ^
 |
In hack

@p  #select memory at p (0)
A=M #assigne A to 257 (A will jump to memory at 257)
D=M #assign D value of memory at 257 (D=23)


*SP = 17
SP++

 ^
 |
In hack
#D=17
@17
D=A 
#*SP=D
@SP
A=M
M=D
#SP++
@SP
M=M+1

Go to the memory address pointed to by SP and put 17 there.
Increment SP.

##### POP LOCAL i #####
psudo code: addr = LCL + 2, SP--, *addr = *SP

@2
D=A

@LCL
D=D+M # D = LCL+2

@R0
M=D # RAM[R0] = D

@SP
M=M-1 #SP--
A=M # jump into location at SP
D=M # D = RAM[A] 5

@R0
A=M # jump to location at LCL+2
M=D # LCL[2] = D

##### PUSH LOCAL i #####
psudo code: addr = LCL + 2, *addr = *SP, SP++

@2
D=A #D=2

@LCL
A=D+M # A=LCL+2 jump to that memory
D=M # D=LCL[2]

@SP
A=M # jump to location of SP
M=D # RAM[*SP] = D

@SP
M=M+1 # SP++
"""

# Stack machine:
# - SP stored in RAM[0] and points to the next avaliable location on stack
# - Stack base addr = 256; stack starts incrementing from address 256
# - LCL will hold the base address of the local segment
# - ? case insensitive


# REGISTER
# RAM[0]  SP -> stack pointer;
# RAM[1]  LCL -> pointes to base of current vm function local segment;
# RAM[2]  ARG -> pointes to base of current vm function argument segment;
# RAM[3]  THIS -> pointes to base of current this segment (within the heap);
# RAM[4]  THAT -> pointes to base of current that segment (within the heap);


# RAM[5-12] -> holds the contents of the temp segment;
# RAM[13-15] -> can be used by the vm as general purpose regisers
# RAM[16-255] -> Static variables 
# RAM[2040-16483] -> HEAP (store objects and arrarys)


import sys
import uuid
from const import push_instruction , pop_instruction , arithmetic_ops


class Parser:

    def __init__(self, file_name):
        self.file_name = file_name

        with open(file_name, "r") as f:
            self.lines = self.parse(f)
                


    def parse(self, f):
        lines = []
        for line in f:
            if line.strip() and not line.strip().startswith("//") : # is not a comment or empty line
                idx = line.find("//")
                lines.append(line[:idx].split())

        return lines
            

    def assemble_file(self, func, f_name=None):
        file_name = f_name if f_name else self.file_name.split(".")[0] + ".asm"
        with open(file_name, "w") as f:
            for line in self.lines:
                f.write(func(line))
        
        print("Wrote: %d lines to %s" %(len(self.lines), file_name))





def vm_translator(line):
    
    print(line)
    translated_line = ""
    random = str(uuid.uuid1())

    try:
        if line[0].upper() == "PUSH":
            segment = line[1]
            position = line[2] + 5 if line[1] == "temp" else line[2]
            position = line[2] + 16 if line[1] == "static" else line[2]

            translated_line = push_instruction[segment].replace("{random}", random)
            translated_line = push_instruction[segment].replace("{position}", position)

        elif line[0].upper() == "POP":
            segment = line[1]
            position = line[2] + 5 if line[1] == "temp" else line[2]
            position = line[2] + 16 if line[1] == "static" else line[2]

            translated_line = pop_instruction[segment].replace("{random}", random)
            translated_line = pop_instruction[segment].replace("{position}", position)
            
        else:
            translated_line = arithmetic_ops[line[0]].replace("{random}", random)

    except Exception as e:
        print(e)
        sys.stderr.write("Error: Wrong instruction %s" %line[0])
        sys.exit()

    return translated_line



def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: vm-translator <file_name.vm>")
        sys.exit(2)

    Parser(sys.argv[1]).assemble_file(vm_translator)


if __name__ == "__main__":
    main()

