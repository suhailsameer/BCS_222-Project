from pyparsing import *
import re

# Define tokens
integer = Keyword("int")
floating = Keyword("float")
print_keyword = Keyword("print")
if_keyword = Keyword("if")
identifier = Word(alphas, alphanums)
number = Regex(r'\d+(\.\d*)?')
plus = Literal("+")
minus = Literal("-")
equals = Literal("=")
semicolon = Literal(";")
open_paren = Literal("(")
close_paren = Literal(")")
open_brace = Literal("{")
close_brace = Literal("}")
greater_than = Literal(">")
less_than = Literal("<")
equals_equals = Literal("==")
not_equals = Literal("!=")

# Define grammar
declaration = (integer("type") + identifier("variable_name") + semicolon("semicolon")).set_name("declaration")
expression = Forward()
term = identifier | number
expression << term + ZeroOrMore((plus | minus) + term)
assignment = (identifier("variable") + equals("equals") + expression("value") + semicolon("semicolon")).set_name("assignment")
print_statement = (print_keyword("print_keyword") + open_paren("open_paren") + expression("expression") + close_paren("close_paren") + semicolon("semicolon")).set_name("print_statement")
condition = (identifier("condition_variable") + (greater_than | less_than | equals_equals | not_equals)("condition_operator") + number("condition_value")).set_name("condition")
statement_list = Forward()
if_statement = (if_keyword("if_keyword") + open_paren("open_paren") + condition("condition") + close_paren("close_paren") + open_brace("open_brace") + statement_list("statement_list") + close_brace("close_brace")).set_name("if_statement")
statement = declaration | assignment | print_statement | if_statement
statement_list << ZeroOrMore(statement)
program = OneOrMore(statement)

# Enhanced Error Handling
def parse_code(code):
    try:
        program.parseString(code, parseAll=True)
        return "Valid syntax."
    except ParseException as e:
        error_msg = f"Syntax error at line {e.lineno}, column {e.col}: "
        found_token = e.token if hasattr(e, 'token') else ""
        expected_tokens = e.parserElement.name if hasattr(e.parserElement, 'name') else str(e.parserElement)

        if "if" in code and not re.search(r'if\s*\(', code):
            return error_msg + "Missing parentheses around 'if' condition."
        elif found_token == "":
            return error_msg + "Unexpected end of input. Possible missing semicolon or closing brace."
        elif found_token == "{":
            return error_msg + "Unexpected '{'. Possible missing 'if' condition or misplaced block."
        elif found_token == "}":
            return error_msg + "Unexpected '}'. Possible missing opening brace '{'."
        elif found_token == "(":
            return error_msg + "Unexpected '('. Possible missing 'if' keyword or misplaced parentheses."
        elif found_token == ")":
            return error_msg + "Unexpected ')'. Possible missing opening parenthesis '('."
        elif found_token == ";":
            return error_msg + "Unexpected ';'. Possible misplaced semicolon or missing statement before it."
        elif found_token.isalnum():
            return error_msg + f"Unexpected identifier '{found_token}'. Possible missing keyword or incorrect syntax."
        elif "Expecting" in expected_tokens:
            expected_tokens = expected_tokens.split("Expecting")[1].strip()
            return error_msg + f"Expected {expected_tokens}, found '{found_token}'."
        else:
            return error_msg + f"Unexpected token '{found_token}'. Check syntax."

# Code snippets
valid_snippets = [
    "int a; a = 5; print(a);",
    "int x; x = 10 + 5 - 2; print(x);",
    "if (a > 0) { print(a); }",
    "int b; b = 0; if (b < 10) { b = b + 1; print(b); }"
]

invalid_snippets = [
    "a=5",  # Missing semicolon
    "a = 5 print(a);",  # Missing semicolon
    "if a > 0 { print(a); }", # Missing parentheses around condition
]

# Test and output
print("Valid Snippets:")
for snippet in valid_snippets:
    print(f"'{snippet}': {parse_code(snippet)}")

print("\nInvalid Snippets:")
for snippet in invalid_snippets:
    print(f"'{snippet}': {parse_code(snippet)}")
