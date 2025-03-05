from pyparsing import *

identifier = Word(alphas, alphas + nums + "_")
integer = Word(nums)
float_num = Word(nums) + '.' + Word(nums)
number = float_num | integer

operator = oneOf("+ - * /")
assignment = Suppress("=")
semicolon = Suppress(";")
lbrace = Suppress("{")
rbrace = Suppress("}")
lparen = Suppress("(")
rparen = Suppress(")")

data_type = oneOf("int float")
declaration = Group(data_type + identifier + semicolon)

operand = identifier | number
expression = infixNotation(operand, [(operator, 2, opAssoc.LEFT)])

assignment_stmt = Group(identifier + assignment + expression + semicolon)

print_stmt = Group(Literal("print") + lparen + identifier + rparen + semicolon)

statement = Forward()
statement <<= declaration | assignment_stmt | print_stmt

condition = Group(lparen + expression + rparen)
if_block = Group(ZeroOrMore(statement))
if_stmt = Group(Literal("if") + condition + lbrace + if_block + rbrace)

statement <<= declaration | assignment_stmt | print_stmt | if_stmt
program = ZeroOrMore(statement)

def parse_code(code):
    try:
        result = program.parseString(code, parseAll=True)
        print("Valid Syntax:", result.asList())
    except Exception as e:
        print("Syntax Error:", e)

valid_code = """
int a;
a = 5;
a = a + 5;
print(a);
"""

invalid_code = """
inta;
a = 5
printa;
"""

print("Testing valid code:")
parse_code(valid_code)

print("\nTesting invalid code:")
parse_code(invalid_code)
