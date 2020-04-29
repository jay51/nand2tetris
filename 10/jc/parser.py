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
        for var in self.subroutine_dec:
            print(var)



class VarDec():
    def __init__(self, access_modifier, var_type, var_name):
        self.access_modifier = access_modifier
        self.type = var_type
        self.name = var_name

    def __str__(self):
        return "Var({}, {}, {})".format(self.access_modifier, self.type, self.name)



class Parser():

    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = self.lexer.token()


    def consume(self, t):
        if self.curr_token.type == t:
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

        var_dec_ast = self.parse_var_dec()
        subroutine_dec_ast = self.parse_subroutine_dec()

        self.consume("SYMBOL")

        return Unite(unite_name, var_dec_ast, subroutine_dec_ast)




    # ('static' | 'field') type identifer(',' identifer)* ';'
    def parse_var_dec(self):
        declarations = []

        while(self.curr_token.value in ("static", "field")):
            access_mod = self.curr_token.value
            self.consume("KEYWORD")
            var_type = self.curr_token.value
            self.consume("KEYWORD")
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




    def parse_subroutine_dec(self):
        pass





    def parse(self):
        return self.parse_unite()



         
        
