import ply.lex as lex
import sys


keywords = (
    "let", "if", "return", "class", "method", "function", "string"
    "var", "static", "constructor", "int", "field", "true", "false",
    "else", "null", "this", "void", "char", "while", "do", "boolean"
)

tokens = keywords + (
   "SYMBOL", "INTEGER", "STRING", "ID", "NEWLINE", "COMMENT"
)

t_ignore = " \t"

def t_ID(t):
    r"[A-Za-z][A-Za-z0-9]*"
    if t.value in keywords:
        t.type = t.value
    return t


def t_NEWLINE(t):
    r"\n"
    t.lexer.lineno += 1


def t_COMMENT(t):
    r"(//.* | /\*\*.*\*/)"
    # print("comment ---- ", t.value)
    pass


t_SYMBOL     = r"[\{\}\(\)\[\]\.\,\;\+\-\*\/\&\|\<\>\=\~]"
t_INTEGER   = r"\d+"
t_STRING    = r"\".*?\""


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)



# ---------- UTILS ----------

def get_files():
    pass

# Tokenize
def main():

    with open(sys.argv[1], "r") as f:
        source_code = f.read()

    lexer = lex.lex(debug=0)
    lexer.input(source_code)
    tok = lexer.token()
    while tok:
        print("token: %s, value: %s" %(tok.type, tok.value))
        tok = lexer.token()



if __name__ == "__main__":
    exit(main())
