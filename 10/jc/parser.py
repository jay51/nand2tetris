from lexer import tokens


class Unite():
    def __init__(self, unite_name, var_dec, subroutine_dec):
        self.unite_name = unite_name
        # list of var dec
        self.var_dec = var_dec
        # list of subroutine_dec
        self.subroutine_dec = subroutine_dec
    
    def print_var_dec_ast(self):
        for var in self.var_dec:
            print(var)

    def print_subroutine_dec_ast(self):
        for routine in self.subroutine_dec:
            print(routine)
            for param in routine.param_list:
                print(param)

            for var in routine.routine_body[0]:
                print(var)

            print("-------------")



class VarDec():
    def __init__(self, access_modifier, var_type, var_name):
        self.access_modifier = access_modifier
        self.type = var_type
        self.name = var_name

    def __str__(self):
        return "Var({}, {}, {})".format(self.access_modifier, self.type, self.name)



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



class String():
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

    def __str__(self):
        return "String({})".format(self.value)


class Int():
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

    def __str__(self):
        return "Int({})".format(self.value)


class Identifier():
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

    def __str__(self):
        return "Identifier({})".format(self.value)


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
        unite_name = self.curr_token.value
        self.consume("ID")
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
            access_mod = self.curr_token.value
            self.consume("KEYWORD")
            var_type = self.curr_token.value
            self.consume(("KEYWORD", "ID"))
            var_name = self.curr_token.value
            self.consume("ID")
            declarations.append(VarDec(access_mod, var_type, var_name))

            while(self.curr_token.value == ","):
                self.consume("SYMBOL")
                var_name = self.curr_token.value
                self.consume("ID")
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
        self.consume("KEYWORD") # type
        param_list.append(self.expression())
        while(self.curr_token.value == ","):
            self.consume("SYMBOL")
            self.consume("KEYWORD")
            param_list.append(self.expression())

        self.consume("SYMBOL")
        return param_list


    def expression(self):
        if self.curr_token.type == "STRING":
            return self.parse_string()
        if self.curr_token.type == "INTEGER":
            return self.parse_int()
        if self.curr_token.type == "ID":
            return self.parse_identifier()

        # not yet Implemented!
        return NoOp()



    def parse_string(self):
       token = self.curr_token
       self.consume("STRING")
       return String(token)


    def parse_int(self):
       token = self.curr_token
       self.consume("INTEGER")
       return Int(token)


    def parse_identifier(self):
       token = self.curr_token
       self.consume("ID")
       return Identifier(token)


    # (constructor | method | function) (void | type) identifier '(' prameterList ')'
    # '{' varDec* statments '}'
    def parse_subroutine_dec(self):
        subroutines = []
        while(self.curr_token.value in ("constructor", "method", "function")):
            routine_type = self.curr_token.value
            self.consume("KEYWORD")
            ret_type = self.curr_token.value
            self.consume(("KEYWORD", "ID"))
            routine_name = self.curr_token.value
            self.consume("ID")
            param_list = self.parse_param_list()
            self.consume("SYMBOL") # {
            routine_body = [ self.parse_subroutine_var_dec(), self.parse_statements() ]
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
        pass


    def parse_statement(self):
        pass


    def parse(self):
        return self.parse_unite()



