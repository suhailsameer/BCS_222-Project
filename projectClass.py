from rply import LexerGenerator
from rply import ParserGenerator

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
        self.lexer.add('IDENTIFIERS',r'[a-zA-Z_][a-zA-Z0-9_]*') # Identifiers should start with a letter or underscore and can have numbers, letters, and underscores after
        # Numbers
        self.lexer.add('NUMBER',r'\d+(\.\d+)?') # Matches any number including float, does not match if no number present before decimal point (eg, .5)
        # String
        self.lexer.add('STRING',r'"[^"]*"')

        # Ignore Whitespaces
        self.lexer.ignore(r'\s+')

    def parse_tokens(self):
        pG=ParserGenerator(
                        ['PRINT','IF','INT','FLOAT','STRING','ADD','SUBTRACT', # Token names
                        'MULTIPLY','DIVIDE','GREATER','LESSER','EQUALTO','NOTEQUAL'
                        'OPENBRACE','CLOSINGBRACE','OPENPAREN','CLOSEPAREN','SEMICOLON',
                        'COLON','IDENTIFIERS','NUMBER','STRING'
                        ],
                        precedence=[
                        ('left',['ADD','SUBTRACTION']),
                        ('left',['MULTIPLY','DIVIDE']),
                        ('left',['GREATER','LESSER','EQUALTO','NOTEQUAL'])
                        ]
                        )
        @pG.production('expression: expression ADD factor')
        @pG.production('expression: expression SUBTRACT factor')
        def expression_binary_as(p):
            left = p[0]
            right = p[0]
            if p[1].gettokentype()=='ADD':
                return p[0] + p[2]
            if p[1].gettokentype()=='SUBTRACT':
                return p[0] - p[2]
            
        
        @pG.production('expression: expression MULTIPLY term')
        @pG.production('expression: expression DIVIDE term')
        def expression_binary_md(p):
            left = p[0]
            right = p[0]
            if p[1].gettokentype()=='MULTIPLY':
                return p[0] * p[2]
            if p[1].gettokentype()=='DIVIDE':
                return p[0] / p[2]

    def get_lexer(self):
        self.add_tokens()
        return self.lexer.build()

