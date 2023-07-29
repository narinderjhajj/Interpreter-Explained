import pure_basic

while True:
    print("Press 1 for Calculator")
    print("Press 2 for AST")
    print("Press 3 for built in ASTs")
    text = input('PureBasic > ')
    try:
        if text == "1":
            print("Running Calculator: Enter Expression")
            text = input('PureBasic > ')
            pure_basic.runCalculator(text)
        elif text == "2":
            print("Enter Expression to print its AST")
            text = input('PureBasic > ')
            pure_basic.printAst(text)
        elif text == "3":
            pure_basic.printAst("1+1")
            pure_basic.printAst("1+2-3")
            pure_basic.printAst("1+2-3*2")
            pure_basic.printAst("12/2+2*3")
            pure_basic.printAst("1+2-3-(3)/(23)+2+2")
        else:
            print("Invalid option")
    except Exception as e:
        print(e)

