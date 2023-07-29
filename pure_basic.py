from lark import Lark

from PureBasic import my_interpreter


def runCalculator(text):
    # Run program
    lexer = my_interpreter.Lexer(text)
    parse = my_interpreter.Parser(lexer)
    interpreter = my_interpreter.Interpreter(parse)
    value = interpreter.interpret()
    print('Result=', value)


def printAst(text):
    grammer_file = open("pure_basic_grammar.txt", "r")
    grammar = grammer_file.read()
    grammer_file.close()
    parser = Lark(grammar, parser='lalr')
    ast = parser.parse(text)
    print(ast.pretty())
