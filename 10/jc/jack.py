from lexer import lexer
import sys
from parser import Parser


def stage_one(source_code):
    lexer.input(source_code)
    tok = lexer.token()
    print("<Tokens>")
    while tok:
        # print("token: %s, value: %s" %(tok.type, tok.value))
        print("\t<%s> %s </%s>" %(tok.type, tok.value, tok.type))
        tok = lexer.token()
    print("</Tokens>")


def stage_two(lexer):
    parser = Parser(lexer)
    AST = parser.parse()
    AST.print_var_dec_ast()
    AST.print_subroutine_dec_ast()
    



def get_files():
    pass

# tokenize
def main():
    with open(sys.argv[1], "r") as f:
        source_code = f.read()

    lexer.input(source_code)
    stage_two(lexer)

    # stage_one(source_code)





if __name__ == "__main__":
    exit(main())
