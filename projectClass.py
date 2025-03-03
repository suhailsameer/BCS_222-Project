from rply import LexerGenerator

class ProjectLexer:
    def __init__(self):
        self.lexer = LexerGenerator()
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
        self.lexer.add('SUBTRACTION',r'-')
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
        self.lexer.add('IDENTIFIERS',r'[a-zA-Z_][a-zA-Z0-9_]*') # Identifiers should start with a letter or underscore and can have numbers, letters, and underscores after
        # Numbers
        self.lexer.add('NUMBER',r'\d+(\.\d+)?') # Matches any number including float, does not match if no number present before decimal point (eg, .5)
        # String
        self.lexer.add('STRING',r'"[^"]*"')

        # Ignore Whitespaces
        self.lexer.ignore(r'\s+')

    def get_lexer(self):
        self.add_tokens()
        return self.lexer.build()

