from lexer import tokens


class Unite():
    def __init__(self, unite_name, var_dec, subroutine_dec):
        self.unite_name = unite_name
        self.var_dec = var_dec
        self.subroutine_dec = subroutine_dec
    
    def print_var_dec_ast(self):
        for var in self.var_dec:
            print(var)

    def print_subroutine_dec_ast(self):
        for routine in self.subroutine_dec:
            print(routine)
            for param in routine.param_list:
                print(param)

            for stat in routine.routine_body:
                print(stat)

            print("-------------")


    def __str__(self):
        return "Unit({},  {},  {})".format(self.unite_name, self.var_dec, self.subroutine_dec)

    __repr__ = __str__


class Obj():
    def __init__(self, name,  properity):
        self.name = name
        self.properity = properity

    def __str__(self):
        return "Obj({}, {})".format(self.name, self.properity)

    __repr__ = __str__


class Return():
    def __init__(self, ret_value):
        self.ret_value = ret_value

    def __str__(self):
        return "Return({})".format(self.ret_value)

    __repr__ = __str__


class DoCall():
    def __init__(self, id, arg_list):
        self.id = id
        self.arg_list = arg_list

    def __str__(self):
        return "DoCall({}, {})".format(self.id, self.arg_list)

    __repr__ = __str__


class BinOp():
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return "BinOp({}, {}, {})".format(self.left, self.op, self.right)

    __rper__ = __str__



class UnaryOp():
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __str__(self):
        return "UnaryOp({}, {})".format(self.op, self.expr)

    __rper__ = __str__




class VarDec():
    def __init__(self, access_modifier, var_type, var_name):
        self.access_modifier = access_modifier
        self.type = var_type
        self.name = var_name

    def __str__(self):
        return "Var({}, {}, {})".format(self.access_modifier, self.type, self.name)

    __repr__ = __str__



class Array():
    def __init__(self, name, idx):
        self.name = name
        self.idx = idx

    def __str__(self):
        return "Array({}, {})".format(self.name, self.idx)

    __repr__ = __str__


class VarDef():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "DefVar({}->{})".format(self.left, self.right)

    __repr__ = __str__


class SubroutineDec():
    def __init__(self, routine_type, ret_type, routine_name, param_list, body):
        self.routine_type = routine_type
        self.ret_type = ret_type
        self.routine_name = routine_name
        self.param_list = param_list
        self.routine_body = body

    def __str__(self):
        return "{} {}({}, {}) -> {}".format(
                self.routine_type,
                self.ret_type,
                self.routine_name,
                self.param_list,
                self.routine_body[0]
                )

    __repr__ = __str__


class IfStatement():
    def __init__(self, expression, body):
        self.expression = expression
        self.body = body

    def __str__(self):
        return "IF({}, {})".format(self.expression, self.body)

    __repr__ = __str__


class WhileStatement():
    def __init__(self, expression, body):
        self.expression = expression
        self.body = body

    def __str__(self):
        return "While({}, {})".format(self.expression, self.body)

    __repr__ = __str__


class String():
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

    def __str__(self):
        return "String({})".format(self.value)

    __repr__ = __str__


class Int():
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

    def __str__(self):
        return "Int({})".format(self.value)

    __repr__ = __str__


class KeyWrod():
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

    def __str__(self):
        return "KeyWrod({})".format(self.value)

    __repr__ = __str__

class Identifier():
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

    def __str__(self):
        return "Identifier({})".format(self.value)

    __repr__ = __str__


class Param():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Param({} {})".format(self.type, self.value)

    __repr__ = __str__


class NoOp():
    pass



class Parser():

    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = self.lexer.token()


    def consume(self, t):
        if self.curr_token.type in t:
            self.curr_token = self.lexer.token()
        else:
            self.error(t)
        

    def error(self, t):
        raise Exception("TOKEN %s don't match current token %s" %(t, self.curr_token))


    # class ClassName '{' VarDec* subroutineDec* '}'
    def parse_unite(self):
        self.consume("KEYWORD")
        unite_name = self.expression()
        self.consume("SYMBOL")

        var_dec_ast = self.parse_class_var_dec()
        subroutine_dec_ast = self.parse_subroutine_dec()

        self.consume("SYMBOL")
        return Unite(unite_name, var_dec_ast, subroutine_dec_ast)



    # ('static' | 'field') type identifer(',' identifer)* ';'
    def parse_class_var_dec(self):
        return self.var_dec(("static", "field"))


    def parse_subroutine_var_dec(self):
        return self.var_dec("var")

    def var_dec(self, keywords):
        declarations = []

        while(self.curr_token.value in keywords):
            access_mod = self.expression()
            var_type = self.expression()
            var_name = self.expression()
            declarations.append(VarDec(access_mod, var_type, var_name))

            while(self.curr_token.value == ","):
                self.consume("SYMBOL")
                var_name = self.expression()
                declarations.append(VarDec(access_mod, var_type, var_name))
                
            self.consume("SYMBOL")

        return declarations



    def parse_arg_list(self):
        arg_list = []
        self.consume("SYMBOL")
        arg_list.append(self.expression())
        while(self.curr_token.value == ","):
            self.consume("SYMBOL")
            arg_list.append(self.expression())

        self.consume("SYMBOL")
        return arg_list



    def parse_param_list(self):
        param_list = []
        self.consume("SYMBOL")
        if self.curr_token.type in ("KEYWORD", "ID"):
            param_type = self.curr_token.value
            self.consume(("KEYWORD", "ID")) # param type
            param_name = self.curr_token.value
            param_list.append(Param(param_type, param_name))
            self.consume("ID")

            while(self.curr_token.value == ","):
                self.consume("SYMBOL")

                param_type = self.curr_token.value
                self.consume(("KEYWORD", "ID")) # param type
                param_name = self.curr_token.value
                param_list.append(Param(param_type, param_name))
                self.consume("ID")

        self.consume("SYMBOL")
        return param_list




    def factor(self):

        token = self.curr_token

        if(self.curr_token.value in ("+", "-")):
            self.consume("SYMBOL")
            node = UnaryOp(token, self.factor())
            return node

        if(self.curr_token.type == "INTEGER"):
            self.consume("INTEGER")
            return Int(token)

        if(self.curr_token.value == "("):
            self.consume("SYMBOL")
            node = self.expr()
            self.consume("SYMBOL")
            return node

        else:
            node = self.expression()
            return node



    def term(self):
        node = self.factor()
        while(self.curr_token.value in ("*", "/")):
            token = self.curr_token
            self.consume("SYMBOL")

            node = BinOp(node, token, self.factor())
        return node




    def expr(self):
        node = self.term()
        while(self.curr_token.value in ("+", "-", ">", "<")):
            token = self.curr_token
            self.consume("SYMBOL")

            node = BinOp(left=node, op=token, right=self.term())

        return node



    def expression(self):

        if self.curr_token.type == "STRING":
            return self.parse_string()
        if self.curr_token.type == "INTEGER":
            return self.parse_int()
        if self.curr_token.type == "KEYWORD":
            return self.parse_keyword()

        if self.curr_token.type == "ID":
            tok = self.curr_token
            self.consume("ID")

            if self.curr_token.value == "[": # array indexing
                return self.parse_array(tok)

            if self.curr_token.value == "(": # function call
                return self.parse_func_call(tok)

            if self.curr_token.value == ".": # class call
                return self.parse_method_call(tok)

                
            return Identifier(tok)

        # not yet Implemented!
        return NoOp()







    def parse_array(self, tok):
       self.consume("SYMBOL")
       idx = self.expr()
       self.consume("SYMBOL")
       return Array(tok.value, idx)


    def parse_string(self):
       token = self.curr_token
       self.consume("STRING")
       return String(token)


    def parse_int(self):
       token = self.curr_token
       self.consume("INTEGER")
       return Int(token)


    def parse_keyword(self):
        token = self.curr_token
        self.consume("KEYWORD")
        return KeyWrod(token)


    # (constructor | method | function) (void | type) identifier '(' prameterList ')'
    # '{' varDec* statments '}'
    def parse_subroutine_dec(self):
        subroutines = []
        while(self.curr_token.value in ("constructor", "method", "function")):
            routine_type = self.expression()
            ret_type = self.expression()
            routine_name = Identifier(self.curr_token)
            self.consume("ID")
            param_list = self.parse_param_list()
            self.consume("SYMBOL") # {
            routine_body = [ *self.parse_subroutine_var_dec(), *self.parse_statements() ]
            self.consume("SYMBOL") # }

            subroutines.append(
                SubroutineDec(
                    routine_type,
                    ret_type,
                    routine_name,
                    param_list,
                    routine_body
                )
            )

        return subroutines



    def parse_statements(self):
        statements = []
        # TODO: handle when we have somthing that's not any fo the following
        while(self.curr_token.value in ("let", "if", "while", "do", "return")):
            statements.append(self.parse_statement())
            
        return statements


    def parse_statement(self):
        if self.curr_token.value == "let":
            self.consume("KEYWORD")
            return self.parse_let()
        
        if self.curr_token.value == "if":
            self.consume("KEYWORD")
            return self.parse_if()


        if self.curr_token.value == "while":
            self.consume("KEYWORD")
            return self.parse_while()


        if self.curr_token.value == "do":
            self.consume("KEYWORD")
            return self.parse_do()

        if self.curr_token.value == "return":
            self.consume("KEYWORD")
            return self.parse_return()

        # I think invalid statemnet
        return NoOp()


    def parse_let(self):
        left = self.expression()

        self.consume("SYMBOL")
        right = self.expr()
        self.consume("SYMBOL") #;
        return VarDef(left, right)


    def parse_if(self):
        self.consume("SYMBOL")
        if_expr = self.expr()
        self.consume("SYMBOL")
        self.consume("SYMBOL") #{
        body = self.parse_statements()
        self.consume("SYMBOL") #}
        return IfStatement(if_expr, body)
        


    def parse_while(self):
        self.consume("SYMBOL")
        while_expr = self.expr()
        self.consume("SYMBOL")
        self.consume("SYMBOL") #{
        body = self.parse_statements()
        self.consume("SYMBOL") #}
        return WhileStatement(while_expr, body)


    def parse_do(self):
        expr = self.expression()
        self.consume("SYMBOL") #;
        return expr


    def parse_func_call(self, tok):
        self.consume("SYMBOL")
        arg_list = []
        arg_list.append(self.expr())
        while(self.curr_token.value == ","):
            self.consume("SYMBOL")
            arg_list.append(self.expr())

        self.consume("SYMBOL")
        return DoCall(Identifier(tok), arg_list)



    def parse_method_call(self, tok):
        self.consume("SYMBOL")
        properity = self.expression()
        return Obj(tok.value, properity)


    def parse_return(self):
        ret = self.expression()
        self.consume("SYMBOL")
        return Return(ret)



    def parse(self):
        return self.parse_unite()



