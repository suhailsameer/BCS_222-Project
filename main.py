from projectClass import ProjectLexer

lexer = ProjectLexer().get_lexer()
sample_input = "hello"
tokens = lexer.lex(sample_input)

for token in tokens:
    print(token)
