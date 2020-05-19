import sys
import os
from lexer import lexer
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

        for routine in node.subroutine_dec:
            print("<subroutineDec>")
            self.visit(routine)
            print("</subroutineDec>")

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

    def visit_Param(self, node):
        return "<param> {} {} </param>".format(node.type, node.value)

    def visit_Param(self, node):
        return "<param> {} {} </param>".format(node.type, node.value)

    def visit_VarDec(self, node):
        print("\t\t<varDec>")
        print("\t\t", self.visit(node.access_modifier))
        print("\t\t", self.visit(node.type))
        print("\t\t", self.visit(node.name))
        print("\t\t</varDec>")


    def visit_SubroutineDec(self, node):
        print("\t", self.visit(node.routine_type))
        print("\t", self.visit(node.ret_type))
        print("\t", self.visit(node.routine_name))

        print("<parameterList>")
        for param in node.param_list:
            print("\t", self.visit(param))
        print("</parameterList>")


        print("<subroutineBody>")
        print("\t<statements>")
        #print(node.routine_body)
        for stmt in node.routine_body:
            self.visit(stmt)
        print("\t</statements>")
        print("</subroutineBody>")


    def visit_VarDef(self, node):
        print("<letStatement>")
        print("\t", self.visit(node.left))
        print("\t", self.visit(node.right))
        print("</letStatement>")


    def visit_Obj(self, node):
        print("\t<ObjExpression>")
        print("\t\t", node.name)
        # print("\t\t", node.properity)
        self.visit(node.properity)
        print("\t</ObjExpression>")


    def visit_DoCall(self, node):
        print("\t", self.visit(node.id))
        print("\t<expressionList>")
        for arg in node.arg_list:
            print("\t\t", self.visit(arg))
        print("\t</expressionList>")




    def visit_WhileStatement(self, node):
        print("\t<WhileStatement>")
        print("\t<expression>")
        print("\t\t", self.visit(node.expression))
        print("\t</expression>")

        print("\t<statements>")
        for stmt in node.body:
            self.visit(stmt)
        print("\t</statements>")

        print("\t</WhileStatement>")



    def visit_Array(self, node):
        print("\t<Array>")
        print("\t\t {}[{}]".format(node.name, self.visit(node.idx)))
        print("\t</Array>")


    def visit_Return(self, node):
        print("\t<Return>")
        print("\t\t", self.visit(node.ret_value))
        print("\t</Return>")



    def visit_BinOp(self, node):
        print("\t", self.visit(node.left))
        print("\t <Operator> {} </Operator>".format(node.op.value))
        print("\t", self.visit(node.right))



    def visit_NoOp(self, node):
        pass



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





def main():
    if not len(sys.argv) == 2:
        sys.stderr.write("Usage: jack <file_name.jack>\n\tjack <dir_name>\n")
        sys.exit(2)

    jakc_files = None
    path = sys.argv[1:]

    if(path[0].endswith(".jack")):
        jack_files = path[0].split(".")[0] + ".jack"
    else:
        jack_files = [path[0] + f for f in os.walk(path[0]).__next__()[2] if f.endswith(".jack")]


    vm_files = [ f.replace(".jack", ".vm") for f in jack_files ]
    print(jack_files)
    print(vm_files)





    for source_file in jack_files:
        with open(source_file, "r") as f:
            source_code = f.read()

        lexer.input(source_code)
        # stage_two(lexer)
        stage_three(lexer)

        # stage_one(source_code)





if __name__ == "__main__":
    exit(main())
