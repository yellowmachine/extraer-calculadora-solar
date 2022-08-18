import ply.lex as lex
import sys
import string

vars = string.ascii_letters

reserved = {
    'IF': 'IF', 'AND': 'AND', 'OR': 'OR', 'SUM': 'SUM', 'AVERAGE': 'AVERAGE', 'SUMIF': 'SUMIF',
    'INT': 'INT', 'ROUNDUP': 'ROUNDUP', 'COUNTIF': 'COUNTIF', 'MAX': 'MAX', 'SUMIFS': 'SUMIFS',
    'MIN': 'MIN', 'COUNT': 'COUNT', 'MATCH': 'MATCH', 'INDEX': 'INDEX'
}

tokens = [
   'NUMBER',
   'NUMBERPERCENT',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'LBRACKET',
   'RBRACKET',
   'NOTEQUAL',
   'EQUAL',
   'ID',
   'SEMICOLON',
   'LESSTHAN',
   'LESSTHANEQUAL',
   'GREATERTHAN',
   'GREATERTHANEQUAL',
   'LITERALSTRING',
   'INTEGER'
] + list(reserved.values())


t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
#t_EQUAL   = r'='
t_IF      = r'IF'
#t_SEMICOLON = r';'
t_LITERALSTRING = r'("[^"]*")'
t_LESSTHAN = r'<'
t_LESSTHANEQUAL = r'<='
t_GREATERTHAN = r'>'
t_GREATERTHANEQUAL = r'>='

def t_NOTEQUAL(t):
    r'<>'
    t.value = "!="
    return t

def t_EQUAL(t):
    r'='
    t.value = "=="
    return t

def t_SEMICOLON(t):
    r';'
    t.value = ","
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_NUMBERPERCENT(t):
    r'[+-]?(\d*\.)?\d+%'
    t.value = str(float(t.value[:-1])/100)
    return t

#integer = re.compile(r'^\d+$')

def t_NUMBER(t):
    r'[-]?(\d*\.)?\d+'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    sys.exit()

lexer = lex.lex()
def translate(data):
    skip_token = False
    lexer.input(data)
    result = ""
    while True:
        tok = lexer.token()
        if not tok:
            break
        
        result = result + str(tok.value)

    return result