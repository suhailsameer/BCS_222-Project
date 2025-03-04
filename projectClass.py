from rply import LexerGenerator
from rply import ParserGenerator
from rply.errors import ParsingError

class ProjectParser:
    def __init__(self):
        self.lexer = LexerGenerator()
        #self.parser = self.parse_tokens()
        self.variables={}
    def add_tokens(self):
        # 1) Keywords
        # print
        self.lexer.add('PRINT',r'print')
        # if
        self.lexer.add('IF',r'if')
        # int
        self.lexer.add('INT',r'int')
        # float
        self.lexer.add('FLOAT',r'float')
        # string
        self.lexer.add('STRING',r'string')

        # 2) Arithmetic Operations
        # Assignment
        self.lexer.add('ASSIGNMENT',r'=')
        # Add
        self.lexer.add('ADD',r'\+')
        # Subtract
        self.lexer.add('SUBTRACT',r'-')
        # Multiply
        self.lexer.add('MULTIPLY',r'\*')
        # Divide
        self.lexer.add('DIVIDE',r'\/')

        # 3) Conditional Operations
        # Greater Than (>)
        self.lexer.add('GREATER',r'>')
        # Lesser than (<)
        self.lexer.add('LESSER',r'<')
        # Equal To (==)
        self.lexer.add('EQUALTO',r'==')
        # Not Equal To (!=)
        self.lexer.add('NOTEQUAL',r'!=')

        # 4} Punctuations
        # Opening brace
        self.lexer.add('OPENBRACE',r'\{')
        # Closing brace
        self.lexer.add('CLOSINGBRACE',r'\}')
        # Opening parentheses
        self.lexer.add('OPENPAREN',r'\(')
        # Closing parentheses
        self.lexer.add('CLOSINGPAREN',r'\)')
        # Semicolon
        self.lexer.add("SEMICOLON",r';')
        # Colon
        self.lexer.add("COLON",r':')

        # Identifiers
        self.lexer.add('IDENTIFIER',r'[a-zA-Z_][a-zA-Z0-9_]*') # Identifiers should start with a letter or underscore and can have numbers, letters, and underscores after
        # Numbers
        self.lexer.add('NUMBER',r'\d+(\.\d+)?') # Matches any number including float, does not match if no number present before decimal point (eg, .5)
        # String
        self.lexer.add('STRING',r'"[^"]*"')

        # Ignore Whitespaces
        self.lexer.ignore(r'\s+')

    def parse_tokens(self):
        pG=ParserGenerator(
                        ['INT','FLOAT','STRING','ASSIGNMENT','ADD','SUBTRACT', # Token names
                        'MULTIPLY','DIVIDE','GREATER','LESSER','EQUALTO','NOTEQUAL'
                        'OPENBRACE','CLOSINGBRACE','OPENPAREN','CLOSEPAREN','SEMICOLON',
                        'COLON','IDENTIFIER','NUMBER','STRING'
                        ],
                        precedence=[                                            # Precedence of operator - Bottom to Top
                        ('left',['ADD','SUBTRACTION']),
                        ('left',['MULTIPLY','DIVIDE']),
                        ('left',['GREATER','LESSER','EQUALTO','NOTEQUAL'])
                        ]
                        )
        @pG.production("program : statement program")
        @pG.production('program : statement')
        def program(p):
            return [p[0]] + (p[1] if len(p) > 1 else [])

        
        @pG.production('statement : declaration')
        @pG.production('statement : assignment')
        @pG.production('statement : if')
        @pG.production('statement : print')
        def statement(p):
            return p[0]

        @pG.production('declaration : INT IDENTIFIER SEMICOLON')
        @pG.production('declaration : FLOAT IDENTIFIER SEMICOLON')
        @pG.production('declaration : STRING IDENTIFIER SEMICOLON')
        def declaration(p):
            if p[2] != ';':
                raise Exception("Error: Semicolon missing at end")
            var_name=p[1].getstr()
            var_type=p[0].getstr()
            if var_type == "int":
                self.variables[var_name] = ("int", 0)
            elif var_type == "float":
                self.variables[var_name] = ("float", 0.0)
            elif var_type == "string":
                self.variables[var_name] = ("string", "")
            return f"Declared variable of type {var_type}"
        
        @pG.production('assignment : IDENTIFER ASSIGNMENT expression SEMICOLON')
        def assignment(p):
            if p[3] != ';':
                raise Exception("Error: Semicolon missing at end")

            var_name = p[0].getstr()
            var_value = p[2]
            if var_name not in self.variables:
                raise Exception("Undeclared variable!")
            actual_type = self.variables[var_name][0]
            try:
                if actual_type == 'int':
                    if isinstance(var_value, float) or (isinstance(var_value, str) and '.' in var_value):
                        raise Exception(f"Error: Cannot assign float value '{var_value}' to integer variable '{var_name}'.")
                    var_value = int(var_value)  # Ensure integer assignment
                elif actual_type == "float":
                    var_value = float(var_value)  # Convert int → float if needed

                elif actual_type == "string":
                    if not isinstance(var_value, str) or not var_value.startswith('"'):
                        raise Exception(f"Error: Cannot assign non-string value to string variable '{var_name}'.")
            except ValueError:
                raise Exception(f"Error: Type is not correct")
            self.variables[var_name] = (actual_type,var_value)
            return f"Assign {var_value} to {var_name}"
            
        @pG.production('print : print OPENPAREN expression CLOSEPAREN SEMICOLON')
        def print_statement(p):
            if p[4] != ';':
                raise Exception("Error: Semicolon missing at end")

            expr_value = p[2]  
            if isinstance(expr_value, str) and expr_value in self.variables:
                expr_value = self.variables[expr_value][1]  # Get stored value
            # If it's a string literal, just print it directly
            if isinstance(expr_value, str) and expr_value.startswith('"') and expr_value.endswith('"'):
                expr_value = expr_value[1:-1]  # Remove surrounding quotes

            # Ensure variable is initialized before printing
            if expr_value is None:
                raise Exception("Error: Attempt to print an uninitialized variable.")

            return f"Print: {expr_value}"

        @pG.production('expression : expression ADD factor')
        @pG.production('expression : expression SUBTRACT factor')
        def expression_binary_as(p):
            left = p[0]
            right = p[0]
            if p[1].gettokentype()=='ADD':
                return p[0] + p[2]
            if p[1].gettokentype()=='SUBTRACT':
                return p[0] - p[2]
            
        @pG.production('expression : term')
        def expression_term(p):
            return p[0]    
        
        @pG.production('term : term MULTIPLY factor')
        @pG.production('term : term DIVIDE factor')
        def expression_binary_md(p):
            left = p[0]
            operator = p[1].getstr()
            right = p[2]

            # Handle variable usage before assignment
            if isinstance(left, str) and left in self.variables:
                if self.variables[left] is None:
                    raise Exception(f"Error: Variable '{left}' is uninitialized!")
                left = self.variables[left]

            if isinstance(right, str) and right in self.variables:
                if self.variables[right] is None:
                    raise Exception(f"Error: Variable '{right}' is uninitialized!")
                right = self.variables[right]

            # Ensure operands are valid numbers
            try:
                left_val = float(left) if '.' in str(left) else int(left)
                right_val = float(right) if '.' in str(right) else int(right)
            except ValueError:
                raise Exception(f"Error: Invalid operands '{left}' and '{right}' for '{operator}' operation.")

            # Division by zero check
            if operator == '/' and right_val == 0:
                raise Exception("Error: Division by zero!")

            return (operator, left_val, right_val)

        
        @pG.production('term : factor')
        def term_factor(p):
            return p[0]
        
        @pG.production('factor : NUMBER')
        @pG.production('factor : IDENTIFIER')
        @pG.production('factor : STRING_LITERAL')
        def factor(p):
            return p[0].getstr()

        return pG.build()

    def get_lexer(self):
        self.add_tokens()
        return self.lexer.build()
    
    def parse(self,tokens):
        try:
            #lexer=self.get_lexer()
            parsed_results = self.parser.parse(iter(tokens))
        except Exception as e:
            return str(e)


