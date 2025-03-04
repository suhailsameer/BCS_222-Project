from projectClass import ProjectParser

parser = ProjectParser()
sample_input = """
int x;
x = 5 * 2 + 10 / 2;
print("Hello World");
s = "String"; 
if x > 5 {
    print(s)
    }
"""
tokens = parser.get_lexer().lex(sample_input)
#result= parser.parse_tokens(tokens)
for token in tokens:
    print(token)