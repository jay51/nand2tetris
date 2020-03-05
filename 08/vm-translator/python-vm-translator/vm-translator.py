#!/usr/bin/env python

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
import traceback
import os
from const import push_instruction, pop_instruction, \
                arithmetic_ops, branching_instruction,\
                function_instruction


class Parser:

    # path is type list<args>
    def __init__(self, path):

        if(len(path) == 1 and path[0].endswith(".vm")):
            self.files = path
            self.file_name =  path[0].split(".")[0] + ".asm"
        else:
            self.files = [path[0] + f for f in os.walk(path[0]).__next__()[2] if f.endswith(".vm")]
            self.file_name =  path[0] + path[0].replace("/", ".asm")


        self.lines = self.parse(self.files)
            


    def parse(self, files):
        lines = []
        for vm_file in files:
            with open(vm_file, "r") as f:
                for line in f:
                    striped_line = line.strip()
                    if striped_line and not striped_line.startswith("//") : # is not a comment or empty line
                        idx = line.find("//") # ignore // if instruction ends with //
                        lines.append(line[:idx].split())

        return lines
            

    def assemble_file(self, func, f_name=None):
        file_name = f_name if f_name else self.file_name
        with open(file_name, "w") as f:
            for line in self.lines:
                f.write(func(line))
        
        print("Wrote: %d VM instructions to %s" %(len(self.lines), file_name))



def vm_translator(line): 
    
    print(line)
    translated_line = ""
    random = str(uuid.uuid1())

    try:
        if line[0].upper() == "PUSH":
            segment = line[1]
            position = int(line[2]) + 5 if segment == "temp" else line[2]
            position = int(line[2]) + 16 if segment == "static" else position

            translated_line = push_instruction[segment].replace("{random}", random)
            translated_line = translated_line.replace("{position}", str(position))
            this_that = "THIS" if line[2] == "0" else "THAT" 
            translated_line = translated_line.replace("{THIS_THAT}", this_that)

        elif line[0].upper() == "POP":
            segment = line[1]
            position = int(line[2]) + 5 if segment == "temp" else line[2]
            position = int(line[2]) + 16 if segment == "static" else position

            translated_line = pop_instruction[segment].replace("{random}", random)
            translated_line = translated_line.replace("{position}", str(position))
            this_that = "THIS" if line[2] == "0" else "THAT" 
            translated_line = translated_line.replace("{THIS_THAT}", this_that)

        elif line[0].upper() == "LABEL":
            label_name = line[1]
            translated_line = branching_instruction["label"].replace("{label-name}", label_name)
            
        elif line[0].upper() == "GOTO":
            label_name = line[1]
            translated_line = branching_instruction["goto"].replace("{label-name}", label_name)

        elif line[0].upper() == "IF-GOTO":
            label_name = line[1]
            translated_line = branching_instruction["if-goto"].replace("{label-name}", label_name)

        elif line[0].upper() == "FUNCTION":
            function_name = line[1]
            num_locals = int(line[2])
            if(num_locals):
                push_zeros_to_stack = """
                @SP
                A=M
                M=0
                @SP
                M=M+1
                """
            else:
                push_zeros_to_stack = ""

            for _ in range(1, num_locals):
                push_zeros_to_stack+= push_zeros_to_stack

            translated_line = function_instruction["function"].replace("{function-name}", function_name)
            translated_line = translated_line.replace("{N-LCL}", push_zeros_to_stack)

        elif line[0].upper() == "CALL":
            function_name = line[0]
            num_of_calls=0
            return_address = line[0] + "-RET-" + str(num_of_calls)
            num_of_calls += 1
            num_args = line[2]

            translated_line = function_instruction["call"].replace("{return-address}", return_address)
            translated_line = translated_line.replace("{function-name}", function_name)
            translated_line = translated_line.replace("{num-args}", num_args)


        elif line[0].upper() == "RETURN":
            translated_line = function_instruction["return"]


        else:
            translated_line = arithmetic_ops[line[0]].replace("{random}", random)

    except Exception as e:
        # print(e)
        traceback.print_exc()
        sys.stderr.write("Error: Wrong instruction %s\n" %line[0])
        sys.exit()

    return translated_line



def main():
    if not(len(sys.argv) == 2):
        sys.stderr.write("Usage: vm-translator <file_name.vm>\n\tvm-translator <dir_name>/\n")
        sys.exit(2)

    Parser(sys.argv[1:]).assemble_file(vm_translator)


if __name__ == "__main__":
    main()

