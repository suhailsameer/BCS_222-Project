from projectClass import ProjectLexer

lexer = ProjectLexer().get_lexer()
sample_input = "if (x=5): a=10+5;"
tokens = lexer.lex(sample_input)

for token in tokens:
    print(token)
