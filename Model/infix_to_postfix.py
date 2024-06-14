def infix_to_postfix(expression):
    """
    Конвертує інфіксний вираз у постфіксний.
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    right_associative = {'^'}
    functions = {'sin', 'cos', 'tan', 'tg', 'cot', 'ctg', 'asin', 'arcsin', 'acos', 'arccos',
                 'atan', 'arctan', 'arctg', 'acot', 'arcctg', 'arccot', 'sinh', 'sh', 'cosh',
                 'ch', 'tanh', 'th', 'coth', 'cth', 'sqrt', 'ln', 'lg', 'log', 'abs', 'niga'}

    def has_higher_precedence(op1, op2):
        return (precedence.get(op1, 0) > precedence.get(op2, 0) or 
                (precedence.get(op1, 0) == precedence.get(op2, 0) and op1 not in right_associative))

    output = []
    operators = []
    if 'log' in expression:
        expression = expression.replace(', ', ' ')
    tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()
    
    for token in tokens:
        if is_num(token) or (token.isalpha() and token not in functions):  # Якщо операнд число або змінна
            output.append(token)
        elif token in functions:
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Видалити '(' зі стеку
            if operators and operators[-1] in functions:
                output.append(operators.pop())
        else:  # Якщо оператор
            while (operators and operators[-1] != '(' and has_higher_precedence(operators[-1], token)):
                output.append(operators.pop())
            operators.append(token)

    while operators:
        output.append(operators.pop())

    return ' '.join(output)

def is_num(token):
    try:
        float(token)
        return True
    
    except ValueError:
        return False