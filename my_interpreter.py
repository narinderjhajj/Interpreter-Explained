# Tokens
PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, NUMBER, EOF = ('add','sub','mul','div','(',')','number', 'EOF')

#Generate Tokens
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value =value

    def __represent__(self):
        return 'Token({type},{value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__represent__()

#Creating Lexer - defining the tokens from the input
class Lexer(object):
    def __init__(self, input):
        self.input = input
        self.pos = 0
        self.cur_tok = self.input[self.pos]

    def nextToken(self):
        self.pos += 1
        #to iterate through all the tokens
        if self.pos > len(self.input) - 1:
            self.cur_tok =  None
        else:
            self.cur_tok = self.input[self.pos]

    def ignoreWS(self):
        while self.cur_tok is not None and self.cur_tok.isspace():
            self.nextToken()

    def number(self):
        tmp = ''
        while self.cur_tok is not None and self.cur_tok.isdigit():
            tmp += self.cur_tok
            self.nextToken()
            return int(tmp)

    def error(self):
        raise Exception('Invalid Syntax')

    def getTokens(self):
        while self.cur_tok is not None:
            if self.cur_tok.isdigit():
                return Token(NUMBER, self.number())
            if self.cur_tok == '+':
                self.nextToken()
                return Token(PLUS, '+')
            if self.cur_tok == '-':
                self.nextToken()
                return Token(MINUS, '-')
            if self.cur_tok == '*':
                self.nextToken()
                return Token(MUL, '*')
            if self.cur_tok == '/':
                self.nextToken()
                return Token(DIV, '/')
            if self.cur_tok == '(':
                self.nextToken()
                return Token(LPAREN, '(')
            if self.cur_tok == ')':
                self.nextToken()
                return Token(RPAREN, ')')
            if self.cur_tok.isspace():
                self.ignoreWS()
                continue
            self.error()
        return Token(EOF, None)

#Creating an AST out of the parsed input (lexer)
#the input was broken down into recognizable tokens using Lexer
#The tokens will be analysed by Parser to create an AST
class AST(object):
    pass
class BinaryOp(AST):
    def __init__(self, left, op,right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Unary(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.curr = self.lexer.getTokens()


    def error(self):
        raise Exception('Invalid Syntax')

    def matchToken(self, type_):
        if self.curr.type == type_:
            self.curr = self.lexer.getTokens()

        else:
            self.error()
    def factor(self):
        """ ?factor: NUMBER   -> number
         | "-" atom         -> neg
         | NAME             -> var
         | "(" sum ")"""
        token = self.curr
        if token.type == NUMBER:
            self.matchToken(NUMBER)
            return Unary(token)
        elif token.type == LPAREN:
            self.matchToken(LPAREN)
            node = self.expr()
            self.matchToken(RPAREN)
            return node
    def term(self):
        """ ?term: factor
        | term "*" factor  -> mul
        | term "/" factor  -> div
        """
        node = self.factor()
        while self.curr.type in (MUL,DIV):
            token = self.curr
            if token.type == MUL:
                self.matchToken(MUL)
            elif token.type == DIV:
                self.matchToken(DIV)
            node = BinaryOp(left=node, op= token, right=self.factor())
        return node

    def expr(self):
        """ ?expr: term
        | expr "+" term   -> add
        | expr "-" term   -> sub"""

        node = self.term()
        while self.curr.type in (PLUS, MINUS):
            token = self.curr
            if token.type == PLUS:
                self.matchToken(PLUS)
            elif token.type == MINUS:
                self.matchToken(MINUS)
            node = BinaryOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        return self.expr()

#Interpreter - interprets the AST  created by the parser into concrete syntax tree
#calculates the operators

class iterator(object):

    def visit(self, node):
        method = 'visit_'+ type(node).__name__
        visitor = getattr(self, method, self.novisit)
        return visitor(node)

    def novisit(self, node):
        raise Exception('Nos visit_ method'.format(type(node).__name__))

class Interpreter(iterator):

    def __init__(self, parser):
        self.parser = parser

    def visit_BinaryOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)


    def visit_Unary(self,node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def printAST(self):
        #TO-DO
        pass

def main():
    while True:
        try:
            text = input('lark>')
        except EOFError:
            break

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        value = interpreter.interpret()
        print('Result', value)




if __name__== '__main__':
    main()

