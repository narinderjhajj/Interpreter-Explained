# Interpreter-Explained
This is a implementation of a simple interpreter in Python that executes the mathematical expression for four basic operations: addition, subtraction, multiplication and division. The expression
for the operation will be provided by the user.
The project is based on creating of
grammar in a text file. In order to build one
I referred to Python’s built in parser library
called Lark that provides a structure called
Lark grammar to define grammar rules. Once
the grammar rules established we can then
implement a lexer and a parser that would
generate a data structure for the
interpreter to process.
