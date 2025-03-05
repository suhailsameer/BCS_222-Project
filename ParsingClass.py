from pyparsing import Word, alphas, nums, oneOf, Group, Forward, Suppress, ZeroOrMore, Literal, Optional, infixNotation, opAssoc, ParseException

# Define basic elements
identifier = Word(alphas, alphas + nums + "_").setName("identifier")
integer = Word(nums).setName("integer")
float_num = Word(nums) + '.' + Word(nums)
number = float_num | integer

# Operators
operator = oneOf("+ - * /")
assignment = Suppress("=").setName("'='")
semicolon = Literal(";").suppress().setName("';'")
lbrace = Literal("{").suppress().setName("'{'")
rbrace = Literal("}").suppress().setName("'}'")
lparen = Literal("(").suppress().setName("'('")
rparen = Literal(")").suppress().setName("')'")

# Variable declaration
data_type = oneOf("int float").setName("data type")
declaration = Group(data_type + identifier + semicolon)

# Expressions
operand = identifier | number
expression = infixNotation(operand, [(operator, 2, opAssoc.LEFT)])

# Assignment statement
assignment_stmt = Group(identifier + assignment + expression + semicolon)

# Print statement
valid_functions = {"print"}
print_stmt = Group(Literal("print") + lparen + identifier + rparen + semicolon)

# If statement
condition = Group(lparen + expression + rparen)
if_block = Forward()
if_stmt = Group(Literal("if") + condition + lbrace + if_block + rbrace)

# Program structure
statement = Forward()
statement <<= declaration | assignment_stmt | print_stmt | if_stmt
if_block <<= ZeroOrMore(statement)
program = ZeroOrMore(statement)

def parse_code(code):
    lines = code.strip().split("\n")
    for i, line in enumerate(lines, start=1):
        try:
            parsed_result = program.parseString(line, parseAll=True)
            # If parsing is successful, print the set of tokens
            print(f"Tokens for line {i}: {set(parsed_result)}")
        except ParseException as pe:
            error_msg = f"Syntax Error at line {i}: "
            if "data type" in str(pe.parserElement):
                error_msg += f"Invalid data type in '{line.strip()}'. Check variable declaration syntax."
            elif "';'" in str(pe.parserElement):
                error_msg += f"Missing semicolon in '{line.strip()}'. Did you forget a ';'?"
            elif "identifier" in str(pe.parserElement):
                error_msg += f"Unknown identifier in '{line.strip()}'. Check for typos or undeclared variables."
            elif "'('" in str(pe.parserElement) or "')'" in str(pe.parserElement):
                error_msg += f"Mismatched parentheses in '{line.strip()}'. Ensure '(' and ')' are correctly placed."
            elif "'{'" in str(pe.parserElement) or "'}'" in str(pe.parserElement):
                error_msg += f"Mismatched braces in '{line.strip()}'. Ensure '{{' and '}}' are correctly placed."
            elif "if" in line.strip().split()[0]:
                error_msg += f"Malformed if statement in '{line.strip()}'. Check parentheses and braces."
            else:
                expected_token = pe.pstr[pe.loc:pe.loc+10].split()[0] if pe.loc < len(pe.pstr) else "(end of input)"
                error_msg += f"Unexpected token '{expected_token}' in '{line.strip()}'."
            print(error_msg)
        except Exception as e:
            print(f"Unexpected Error at line {i}: {e}")

# Example valid and invalid snippets
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
if a > 0 { print(a); }
"""

print("Testing valid code:")
parse_code(valid_code)

print("\nTesting invalid code:")
parse_code(invalid_code)
