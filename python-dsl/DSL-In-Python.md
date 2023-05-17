# Introduction

Domain-Specific Languages, or DSLs, are specialized programming languages designed to solve specialized problems within a specific domain. DSLs provide a concise and expressive syntax that is tailored to address the specific needs and challenges of a given problem. DSLs empower developers to express complex concepts and operations in an intuitive manner. Through using DSLs, developers can focus on the problem at hand without dealing with unnecessary details.

There are several advantages to creating a DSL in Python. Python's flexibility and expressiveness make it ideal for hosting a domain-specific language. It's rich ecosystem of libraries and tools provides a solid foundation for creating unique and specialize DSLs that can integrate seamlessly with existing codebases.

In this article, we will explore the process of implementing a simple DSL in Python. We're explore the core concepts, examine the necessary components, and guide you through the basic steps of implementing your own DSL. By the end, you will have a clear understanding of how to design, implement, and utilize DSLs to improve your Python applications!

# Understanding DSLs

DSLs are specialized languages designed to address complex problems in a simple and intuitive manner for specific domains. They offer a concise syntax tailored to the particular needs of the application. This approach brings several advantages, such as improved readability, expressiveness, extendibility, and ease of use.

## Internal vs External DSLs

There are two categories of DSLs, internal DSLs and external DSLs.

### Internal DSLs

Internal DSLs are hosted within a language itself and leverage the syntactical features of its host language to define a specialized syntax. These DSLs leverage the flexibility and expressiveness of its host language and as a result are relatively easy to implement.

### External DSLs

External DSLs, on the other hand, define their own syntax and grammar which stands alone from a host language. These require a dedicated parser and interpreter to properly handle the parsing and execution of the language. Advantages of external DSLs include providing more control over the design and more flexibility, but at the disadvantage of increase complexity of implementation.

### Design Principles in Creating DSLs

There are certain design principles to follow when creating DSLs. Following these principles ensures that a DSL is intuitive to use, expressive, and efficient in its execution.

1. Simplicity: The DSL should define a clear and concise syntax that is easy to understand and fits within the problem domain.
2. Expressiveness: A DSL should strive to capture the problem domain well, defining the operations and concepts necessary to achieve the specified results.
3. Readability: DSLs should be readable by developers who write and maintain the codebase. Using meaningful keywords and consistent naming conventions ensures a clear and readable design.
4. Compositionality: Composition of DSL constructs allows building of complex and meaningful components from simpler ones, thus promoting code reuse.
5. Error Handling: Proper error handling is essential to ensure data integrity and inform users of your DSL when errors occur and how to respond to them.

# Setting up Your DSL Environment

In order to implement your DSL, it is necessary to properly set up your environment to support its development. This involves choosing the appropriate libraries and tools that will enable you to create and execute your DSL.

## Choosing Libraries

Python offers a number of libraries for creating DSLs. One option is `ply`.

`ply` is an implementation of the lex and yacc parsing tools for Python and enables the creation of lexers and parser in Python. It provides a clear way to define grammar rules and handle tokenization and parsing of your DSL code. By utilizing `ply` , you can easily define the structure and behavior of your DSL.

## Installation

Provided you have `pip` installed, installing `ply` is as easy as running the following command:

```bash
pip install ply
```



With `ply` installed you are now ready to define the syntax for building and interpreting your DSL!

# Define the DSL Syntax

Defining the syntax of the DSL you wish to implement is a critical step in the implementation. Identifying the language constructs, keywords, and expressions that will comprise your DSL is necessary in order to understand how you will implement it. By designing a clear syntax, you will enable your users to express their intensions clearly and accurately.

### Identifying the Syntax

First identify the problem domain and understand the operation and concepts necessary to support your DSL. You will have to consider what actions, conditions, and calculations the user of your DSL will want to perform. For example, let us suppose we want to create a simple DSL for defining vectors, matrices, and carrying out simple operations such as vector addition and matrix multiplication. You might define the DSL as follows:

```
vector v1 = [1, 2, 3]
vector v2 = [4, 5, 6]
matrix m1 = [[1, 2], [3, 4]]
matrix m2 = [[5, 6], [7, 8]]

vector v3 = v1 + v2
matrix m3 = m1 * m2
```


This defines a very simple DSL for defining vectors and matrices and carrying out simple operations. We will enforce certain constraints in the design of our DSL using the `numpy` language to handle addition and multiplication operations and enforce shape constraints.

### Creating Grammar Rules

Once you have a clear understanding of the syntax you want to utilize, you can proceed to define grammar rules in `ply`. These rules specify the structure and semantics of what constitutes a valid expression the DSL.

Using `ply`, we define token names and regular expressions to tokenize the incoming input stream. You would also define grammar rules that define how these tokens can be combined to form valid code expressions. 

First, let us import the necessary libraries we will need to use.

```python
import ply.lex as lex
import ply.yacc as yacc

import numpy as np
```

Next, we'll need to define our tokens

```python
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
```

We declare a variable store for storing our variables. It is a simple dictionary at the moment, but can be expanded to be a more elaborate object as the DSL demands.

```python
# Variables
variables = {}
```

Next we define some tokens for things like newlines, our print statement, our vector and matrix declarations, and our identifiers.

```python
# Token definition for newline, print, vector and 
# matrix identifiers, generic identifiers, and numbers
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
```

We want to be able to define a program for our DSL, essentially a series of statements that can be executed in sequence. We define the structure of the grammar as a comment and define how we want to handle the statement within the code. Here we just pass for now.

```python
# ---- PROGRAM ----
def p_program(p):
    '''program : program statement
               | statement'''
    pass
```

Now we want to focus on how we handle parsing vectors. We need to be able to assign a vector to a variable and store that variable in the variable table.

First, let's focus on the assignment portion: `vector v1 = <expression>`

```python
def p_statement_vector_assignment(p):
    'statement : VECTOR_ID EQUALS expression'
    variable_name = p[1].split()[1]
    variables[variable_name] = p[3]
    p[0] = (variable_name, p[3])
```

Here we define a statement that is defined as `VECTOR_ID` token, an `EQUALS` token, and an `<expression>`. We take the token at p[1], corresponding to `VECTOR_ID`, and split it to obtain the variable name. In the above example, that would be `v1`. We then assign `variables[variable_name]` to the value of `<expression>`. We then assign p[0] as a tuple of `(variable name, value)`.

From here, we can define our `vector` expression as a series of functions. They are define as follows:

```python
def p_vectordef(p):
    'expression : LBRACKET vector_values RBRACKET'
    p[0] = np.array(p[2])

def p_vector_values_single(p):
    'vector_values : NUMBER'
    p[0] = [p[1]]

def p_vector_values_multiple(p):
    'vector_values : NUMBER COMMA vector_values'
    p[0] = [p[1]] + p[3]
```



The overview of this code is as follows. `p_vectordef`is an expression that looks at statements in the form of [ `<vector_values>` ] . `p_vector_values_single` handles single values, in this case, just a number. Finally, `p_vector_values_multiple` handles multiple values, in the form of `1, 2, 3, 4`. Notice how we reference `vector_values` from within `P_vector_values_multiple`? This allows it to recursively call itself until it terminates at a `NUMBER` token.

With this code in place, we can now parse and store statements in the form of `vector v1 = [1, 2, 3]`.

Matrices are defined similarly, with a few additional functions to handle rows and row values.

```python
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
```

The above code allows us to parse matrices in the form of `matrix m1 = [[a1, b1, c1,....,z1], [a2, b2, c2...,z2], ...., [an, bn, cn, ....zn]]`.

With this in place, we can now define some operations, such as addition and matrix multiplication. We can also define a print statement to print the values of our variables.

First, we have to define an expression for retrieving `IDENTIFIERS` from the variable table.

```python
def p_expression_identifier(p):
    'expression : IDENTIFIER'
    variable_name = p[1]
    if variable_name in variables:
        p[0] = variables[variable_name]
    else:
        print(f"Error: Variable '{variable_name}' not in variable table")
```

Here if we encounter a `IDENTIFIER` token, we look to see if the variable identified by `IDENTIFIER` is in the variable identifier. If it is we retrieve its value and store it in `p[0]` else we print an error message.

Addition and multiplication are straight forward as well, with multiplication using numpy's `matmul` method:

```python
def p_expression_add(p):
    'expression : expression PLUS expression'
    p[0] = p[1] + p[3]

def p_expression_multiply(p):
    'expression : expression MULTIPLY expression'
    p[0] = np.matmul(p[1],p[3])

```

Likewise, the `print` statement can be easily defined as well.

```python
def p_statement_print(p):
    'statement : PRINT LPAREN IDENTIFIER RPAREN'
    variable_name = p[3]
    if variable_name in variables:
        print(variables[variable_name])
    else:
        print(f"Error: Variable '{variable_name}' not in variable table")
```

Here we parse statements in the form of `print(<IDENTIFIER>)`. We retrieve `IDENTIFIER` and look it up in the variable table. If it is present, we print the value of that variable, otherwise, we print an error message.

We conclude with a simple error handler:

```python
def p_error(p):
    print("Syntax error: ", p)
```

To run the program, we build the lexer and parser.

```
# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()
```

And define our DSL code:

```python
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
```

Finally, we can call the `parse` method on the `parser` object on `dsl_code` to see the output of our program.

```python
parser.parse(dsl_code)
```

With that, we have a fully functionally DSL in Python

# Conclusion

In this article, we explored domain-specific languages. We examined two types of DSLs, internal and DSL, as well as the criteria that defines a good DSL. Furthermore, we looked at the advantages of creating a DSL for domain specific problems. We then dived into the process of designing and implementing a DSL using the Ply librarying, which provides lexing and parsing capabilities in the Python language.

We begun by defining the tokens of our DSL. These form the basic building blocks of the language, such as numbers, identifiers, and keywords like `vector` and `matrix`. We leveraged regular expressions to define token rules and used Ply's lexer tok tokenize our sample DSL code.

We then proceeded to design our grammar rules to define the syntactical and semantic structure of our language. We created rules for declaring vectors and matrices and assigning them to variables. Next, we proceeded to define operations for performing addition and matrix multiplication on the variables we stored, as well as an operation for a print statement. Through parsing the code, we construct an abstract syntax tree (AST) that represents the structure of the DSL code.

By learning how to implement a DSL in Python and how to leverage the Ply library, you know have the necessary knowledge and tools to create your own domain specific languages. Whether it is for data engineering, rule-based systems, game design, or other use cases, a well-constructed DSL can greatly facilitate the development of software and applications, enhancing productivity and code expressiveness.

Now it's time to apply what you've learning and start exploring the possibilities of building your own DSLs! With these tools at your disposal, you have the flexibility and power to create powerful DSLs and improve the way you tackle complex problems across a wide variety of domains.

Thank you, and happy DSL development!



















