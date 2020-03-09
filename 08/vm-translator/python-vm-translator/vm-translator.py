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
                function_instruction, init_code


class Parser:

    # path is type list<args>
    def __init__(self, path):

        if(path[0].endswith(".vm")):
            self.files = path
            self.file_name = path[0].split(".")[0] + ".asm"
        else:
            self.files = [path[0] + f for f in os.walk(path[0]).__next__()[2] if f.endswith(".vm")]
            self.file_name = path[0] + path[0].split("/")[-2] + ".asm"

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
            

    def get_new_filename(self):
        return self.file_name

    def get_parsed_lines(self):
        return self.lines



class Translator():

    def __init__(self, parser):
        self.parser = parser
        self.lines = parser.get_parsed_lines()
        self.file_name = parser.get_new_filename()

        self.num_of_function_calls = 0
        self.inside_function = False
        self.curr_function = ""


    def push_instruction(self, line, random):
        segment = line[1]
        position = int(line[2]) + 5 if segment == "temp" else line[2]
        position = int(line[2]) + 16 if segment == "static" else position

        translated_line = push_instruction[segment].replace("{random}", random)
        translated_line = translated_line.replace("{position}", str(position))
        this_that = "THIS" if line[2] == "0" else "THAT"
        translated_line = translated_line.replace("{THIS_THAT}", this_that)
        return translated_line

    def pop_instruction(self, line, random):
        segment = line[1]
        position = int(line[2]) + 5 if segment == "temp" else line[2]
        position = int(line[2]) + 16 if segment == "static" else position

        translated_line = pop_instruction[segment].replace("{random}", random)
        translated_line = translated_line.replace("{position}", str(position))
        this_that = "THIS" if line[2] == "0" else "THAT"
        translated_line = translated_line.replace("{THIS_THAT}", this_that)
        return translated_line


    def define_label(self, line):
        label_name = line[1] if not self.inside_function else self.curr_function + "$" + line[1] 
        translated_line = branching_instruction["label"].replace("{label-name}", label_name)
        return translated_line


    def define_goto(self, line):
        label_name = line[1] if not self.inside_function else  self.curr_function + "$" + line[1]
        translated_line = branching_instruction["goto"].replace("{label-name}", label_name)
        return translated_line


    def define_if_goto(self, line):
        label_name = line[1] if not self.inside_function else  self.curr_function + "$" + line[1]
        translated_line = branching_instruction["if-goto"].replace("{label-name}", label_name)
        return translated_line


    def define_function(self, line):
            function_name = line[1]
            num_locals = int(line[2])

            init_locals = ""
            if(num_locals):
                for _ in range(num_locals):
                    init_locals += self.push_instruction(["push", "constant", "0"], "0")

            translated_line = function_instruction["function"].replace("{function-name}", function_name)
            translated_line = translated_line.replace("{N-LCL}", init_locals)
            return translated_line


    def call_function(self, line):
        function_name = line[1]
        return_address = line[1] + "-RET-" + str(self.num_of_function_calls)
        self.num_of_function_calls += 1
        num_args = line[2]

        translated_line = function_instruction["call"].replace("{return-address}", return_address)
        translated_line = translated_line.replace("{function-name}", function_name)
        translated_line = translated_line.replace("{num-args}", num_args)
        return translated_line


    def call_return(self, line):
        return function_instruction["return"]


    def init_bootstrap(self):
        return init_code


    def translate(self):
        with open(self.file_name, "w") as f:
            # bootstrap code (initinitalize sp and call Sys.init) 
            # comment out the 2 lines below when run test for programFlow
            f.write(self.init_bootstrap())
            f.write(self.call_function(["call", "Sys.init", "0"]))

            for line in self.lines:
                translation = self.translate_line(line)
                f.write(translation)

        print("Wrote: %d VM instructions to %s" %(len(self.lines), self.file_name))


    def translate_line(self, line):
        print(line)
        random = str(uuid.uuid1())

        try:
            if line[0].upper() == "PUSH":
                return self.push_instruction(line, random)

            if line[0].upper() == "POP":
                return self.pop_instruction(line, random)

            if line[0].upper() == "LABEL":
                return self.define_label(line)

            if line[0].upper() == "GOTO":
                return self.define_goto(line)

            if line[0].upper() == "IF-GOTO":
                return self.define_if_goto(line)

            if line[0].upper() == "FUNCTION":
                self.curr_function = line[1]
                self.inside_function = True
                return self.define_function(line)

            if line[0].upper() == "CALL":
                return self.call_function(line)

            if line[0].upper() == "RETURN":
                return self.call_return(line)

            return arithmetic_ops[line[0]].replace("{random}", random)

        except Exception as e:
            traceback.print_exc()
            sys.stderr.write("Error: Wrong instruction %s\n" %line[0])
            sys.exit()



def main():
    if not(len(sys.argv) == 2):
        sys.stderr.write("Usage: vm-translator <file_name.vm>\n\tvm-translator <dir_name>/\n")
        sys.exit(2)

    parser = Parser(sys.argv[1:])
    Translator(parser).translate()


if __name__ == "__main__":
    main()

