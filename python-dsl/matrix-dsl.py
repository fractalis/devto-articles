import ply.lex as lex
import ply.yacc as yacc

import numpy as np

# Token definitions
tokens = (
        'IDENTIFIER',
        'NUMBER',
        'VECTOR_ID',
        'VECTOR',
        'MATRIX_ID',
        'MATRIX',
        'PLUS',
        'MULTIPLY',
        'LPAREN',
        'RPAREN', 
        'LBRACKET',
        'RBRACKET',
        'COMMA', 
        'EQUALS',
        'PRINT')

# Ignored characters
t_ignore = ' \t'

# Token regular expressions
t_PLUS = r'\+'
t_MULTIPLY = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','

# Variables
variables = {}

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_PRINT(t):
    r'print'
    t.type = 'PRINT'
    return t

def t_VECTOR_ID(t):
    r'vector\s+[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_MATRIX_ID(t):
    r'matrix\s+[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'IDENTIFIER'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# ---- PROGRAM ----
def p_program(p):
    '''program : program statement
               | statement'''
    pass

# ----- VECTOR -----

def p_statement_vector_assignment(p):
    'statement : VECTOR_ID EQUALS expression'
    variable_name = p[1].split()[1]
    variables[variable_name] = p[3]
    p[0] = (variable_name, p[3])

#def p_expression_vector(p):
#    'expression : VECTOR'
#    p[0] = p[1]

def p_vectordef(p):
    'expression : LBRACKET vector_values RBRACKET'
    p[0] = np.array(p[2])

def p_vector_values_single(p):
    'vector_values : NUMBER'
    p[0] = [p[1]]

def p_vector_values_multiple(p):
    'vector_values : NUMBER COMMA vector_values'
    p[0] = [p[1]] + p[3]

# ----- END VECTOR -----

# ----- MATRIX -----
def p_statement_matrix_assignment(p):
    'statement : MATRIX_ID EQUALS expression'
    variable_name = p[1].split()[1]
    variables[variable_name] = p[3]
    p[0] = (variable_name, p[3])

def p_expression_matrix(p):
    'expression : MATRIX'
    p[0] = p[1]

def p_matrix(p):
    'expression : LBRACKET matrix_rows RBRACKET'
    p[0] = np.array(p[2])

def p_matrix_rows_single(p):
    'matrix_rows : row'
    p[0] =[p[1]]

def p_matrix_rows_multiple(p):
    'matrix_rows : row COMMA matrix_rows'
    p[0] = [p[1]] + p[3]

def p_row(p):
    'row : LBRACKET row_values RBRACKET'
    p[0] = p[2]

def p_row_values(p):
    'row_values : NUMBER'
    p[0] = [p[1]]

def p_row_values_multiple(p):
    'row_values : NUMBER COMMA row_values'
    p[0] = [p[1]] + p[3]

# ----- END MATRIX -----

# ----- OPERATIONS -----

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    variable_name = p[1]
    if variable_name in variables:
        p[0] = variables[variable_name]
    else:
        print(f"Error: Variable '{variable_name}' not in variable table")

def p_expression_add(p):
    'expression : expression PLUS expression'
    p[0] = p[1] + p[3]

def p_expression_multiply(p):
    'expression : expression MULTIPLY expression'
    p[0] = np.matmul(p[1],p[3])

def p_statement_print(p):
    'statement : PRINT LPAREN IDENTIFIER RPAREN'
    variable_name = p[3]
    if variable_name in variables:
        print(variables[variable_name])
    else:
        print(f"Error: Variable '{variable_name}' not in variable table")

# ----- END OPERATIONS -----

# ----- ERROR HANDLING -----

def p_error(p):
    print("Syntax error: ", p)

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Parsing and executing DSL code
dsl_code = """
vector v1 = [1, 2, 3]
vector v2 = [4, 5, 6]
print(v1)
print(v2)

matrix m1 = [[1, 2], [3, 4], [5, 6]]
matrix m2 = [[5, 6, 7], [7, 8, 9]]

print(m1)
print(m2)

vector v3 = v1 + v2
matrix m3 = m1 * m2

print(v3)
print(m3)
"""

#ast = []
#for line in dsl_code.strip().split('\n'):
#    ast.append(parser.parse(line))
#
#print(ast)
parser.parse(dsl_code)

