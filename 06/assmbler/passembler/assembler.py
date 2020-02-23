#!/usr/bin/python

import collections
import sys
from const import COMP, PREDEFINED_MEM, JUMP, DEST



class Parser():
    # iter of all free memory starting from 16 to address of SCREEN
    free_addresses = iter(range(16, PREDEFINED_MEM['SCREEN']-1))

    def __init__(self, filename):
        self.filename = filename
        # when adding to self.variables you will get the next avlable address
        self.variables = collections.defaultdict(Parser.next_address)

        f = open(filename)
        self.labels = dict()
        self.lines = self.parse(f)
        f.close()

    
    def parse(self, f):
        """ parse lines in file & recorde labels"""
        lines = []
        for line in f:
            _line = line.split("//")[0].strip()
            if _line.startswith("("):  # is a label
                label_name = _line[1:-1]
                self.labels[label_name] = len(lines)  # line number / address of label
            elif _line:
                lines.append(_line)
            # else: it's just a whitespace/comment line (ignore)
        return lines

    @staticmethod
    def next_address():
        return next(Parser.free_addresses) # get the next address

    def resolve_symbol(self, symbol):
        """ return memory address of symbol"""
        if symbol in self.labels:
            return self.labels[symbol]
        if symbol in PREDEFINED_MEM:
            return PREDEFINED_MEM[symbol]

        return self.variables[symbol]  # autoincrement default

    def assemble_line(self, line):
        if line.startswith("@"):
            return AInstruction(line, parser=self)
        else:
            return CInstruction(line)


    def write_to_file(self, opcode):
        with open(self.filename.replace("asm", "hack"), "w") as f:
            for binary_op in opcode:
                f.write(binary_op.__str__() + "\n")


    def assemble_binary(self, write_to_file=True):
        opcode = map(self.assemble_line, self.lines)
        if write_to_file: self.write_to_file(opcode)
        else: return opcode



class AInstruction():
    def __init__(self, code, parser):
        try:
            # if selecting memory like (@14034)
            self.address = int(code[1:])
        except ValueError:
            # if selecting memory like (@SCREEN)
            self.address = parser.resolve_symbol(code[1:])

    def __str__(self):
        return "0{:0>15b}".format(self.address)


class CInstruction():
    def __init__(self, code):
        self.dest, rest = code.split("=") if "=" in code else ("", code)
        self.comp, self.jump = rest.split(";") if ";" in rest else (rest, "")

    def __str__(self):
        return "111{}{}{}".format(COMP[self.comp], DEST[self.dest],
                                  JUMP[self.jump])


if "__main__" == __name__:

    if len(sys.argv) < 2:
        print("Usage: assembler <file_name>")
        exit(1)

    input_file = sys.argv[1]
    binary_ops = Parser(input_file).assemble_binary()

