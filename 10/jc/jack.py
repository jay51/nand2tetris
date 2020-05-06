from lexer import lexer
import sys
from parser import Parser




class NodeVisitor():
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        # print("visit type is : %s" %visitor)
        return visitor(node)


    def generic_visit(self, node):
        raise Exception("no visit_{} method found".format(type(node).__name__))




class CodeGen(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.table = {}


    def visit_Unite(self, node):
        print("<class>")
        print(self.visit(node.unite_name))

        for var_node in node.var_dec:
            print("<class VarDec>")
            self.visit(var_node)
            print("</class VarDec>")

        # for routine in node.subroutine_dec:
            # self.visit(routine)
        print("</class>")



    def visit_VarDec(self, node):
        print("\t", self.visit(node.access_modifier))
        print("\t", self.visit(node.type))
        print("\t", self.visit(node.name))



    def visit_KeyWrod(self, node):
        return "<keyword> {} </keyword>".format(node.value)

    def visit_Identifier(self, node):
        return "<identifier> {} </identifier>".format(node.value)

    def visit_String(self, node):
        return "<string> {} </string>".format(node.value)

    def visit_Int(self, node):
        return "<int> {} </int>".format(node.value)




    def run(self):
        if self.tree:
            return self.visit(self.tree)











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
    

def stage_three(lexer):
    parser = Parser(lexer)
    AST = parser.parse()
    code_gen = CodeGen(AST)
    code_gen.run()



def get_files():
    pass

# tokenize
def main():
    with open(sys.argv[1], "r") as f:
        source_code = f.read()

    lexer.input(source_code)
    # stage_two(lexer)
    stage_three(lexer)

    # stage_one(source_code)





if __name__ == "__main__":
    exit(main())
