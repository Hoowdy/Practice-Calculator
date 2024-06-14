import re

def brackets_check(expression):
    """
    Перевіряє правильність розстановки дужок у виразі.
    Якщо розстановка дужок правильна, повертає True.
    Інакше піднімає виключення з повідомленням про помилку.
    """
    stack = []
    for symbol in expression:
        if symbol == '(':
            stack.append('(')
        elif symbol == ')':
            if stack and stack[-1] == '(':
                stack.pop()
            else:
                stack.append(')')
    if stack:
        raise Exception('Помилка в скобочній послідовності')
    return True

def convert_constx_to_const_x(expr):
    """
    Перетворює вирази виду 'constx' у 'const * x' та 'xconst' у 'x * const'.
    """
    def replace_constx(match):
        const = match.group(1)
        x = match.group(2)
        return f"{const} * {x}"

    def replace_xconst(match):
        x = match.group(1)
        const = match.group(2)
        return f"{x} * {const}"

    pattern1 = r"(\d+)([a-zA-Z])"
    pattern2 = r"([a-zA-Z])(\d+)"
    expr = re.sub(pattern1, replace_constx, expr)
    expr = re.sub(pattern2, replace_xconst, expr)
    return expr

def seperate_from_barackets(expression):
    """
    Додає множення між закритою дужкою і наступним числом чи змінною.
    """
    result = ""
    i = 0
    while i < len(expression):
        if expression[i] == ')' and i + 1 < len(expression) and expression[i + 1].isalnum():
            result += ") * "
        else:
            result += expression[i]
        i += 1
    return result

def separate_var_from_func(expr):
    """
    Розділяє змінні і функції, коли вони записуються разом.   
    """
    functions = ['sin', 'cos', 'tan', 'tg', 'cot', 'ctg', 'asin', 'arcsin', 'acos', 'arccos',
                 'atan', 'arctan', 'arctg', 'acot', 'arcctg', 'arccot', 'sinh', 'sh', 'cosh',
                 'ch', 'tanh', 'th', 'coth', 'cth', 'sqrt', 'ln', 'lg', 'log', 'abs', 'pi', 'niga']

    # Sort functions by length in descending order to match longer names first
    functions.sort(key=len, reverse=True)

    new_expr = ""
    i = 0
    while i < len(expr):
        match = re.match(f"({'|'.join(functions)})", expr[i:])
        if match:
            func = match.group(0)
            if i > 0 and (expr[i-1].isdigit() or expr[i-1].isalpha() or expr[i-1] == ')'):
                new_expr += '*'
            new_expr += func
            i += len(func)
            if i < len(expr) and expr[i] == '(':
                balance = 1
                new_expr += '('
                i += 1
                while balance > 0 and i < len(expr):
                    if expr[i] == '(':
                        balance += 1
                    elif expr[i] == ')':
                        balance -= 1
                    new_expr += expr[i]
                    i += 1
        else:
            if i > 0 and ((expr[i].isalpha() and expr[i-1].isalpha()) or (expr[i].isalpha() and expr[i-1].isdigit()) or (expr[i] == '(' and expr[i-1].isdigit())):
                new_expr += '*'
            new_expr += expr[i]
            i += 1

    return new_expr

def separate_with_spaces(expr):
    """
    Розділяє оператори пробілами, крім випадків, коли оператор '-' використовується для позначення від'ємного числа.
    """
    operators = ['+', '-', '*', '/', '^']   
    result = ""
    i = 0
    while i < len(expr):
        if expr[i] in operators:  
            # Перевіряємо чи є '-'
            if expr[i] == '-':
                # Якщо перед '-' нічого немає або є оператор чи відкрита дужка, то це від'ємне число
                if i == 0 or expr[i - 1] in operators + ['(', ' ']:
                    result += expr[i]
                else:
                    result += f" {expr[i]} "
            else:
                result += f" {expr[i]} "
        else:
            result += expr[i]
        i += 1
    return result

def mult_sign_between_brackts(expression):
    """
    Додає знак множення між дужками.
    """
    return re.sub(r'(\))(\()', r'\1*\2', expression)
    
def separate_variables(expr):
    """
    Розділяє змінні, які не є математичними функціями, на окремі змінні з оператором множення.
    """
    functions = {'sin', 'cos', 'tan', 'tg', 'cot', 'ctg', 'asin', 'arcsin', 'acos', 'arccos',
                 'atan', 'arctan', 'arctg', 'acot', 'arcctg', 'arccot', 'sinh', 'sh', 'cosh',
                 'ch', 'tanh', 'th', 'coth', 'cth', 'sqrt', 'ln', 'lg', 'log', 'abs', 'pi', 'niga'}
    
    variables = re.findall(r'[a-zA-Z]+', expr)
    for var in variables:
        if var not in functions:
            expr = re.sub(r'\b' + var + r'\b', ' * '.join(list(var)), expr)
    return expr

def process_expression(expr):
    """
    Обробляє вираз:
    1. Перевіряє правильність дужок.
    2. Перетворює вирази виду 'constx' у 'const * x'.
    3. Додає множення між закритою дужкою і наступним числом чи змінною.
    4. Розділяє змінні і функції, коли вони записуються разом.
    5. Розділяє оператори пробілами, крім випадків, коли оператор '-' використовується для позначення від'ємного числа.
    6. Додає знак множення між дужками.
    7. Розділяє змінні, які не є математичними функціями, на окремі змінні з оператором множення.
    """
    expression1 = expr.replace(',', '.') 
    expression2 = expression1.replace('. ', ', ') # це щоб не змінювало кому в записі звичайного логорифма

    brackets_check(expression2)
    sep_constX = convert_constx_to_const_x(expression2)
    sep_var_brackts = seperate_from_barackets(sep_constX)
    sep_var_funcs = separate_var_from_func(sep_var_brackts)
    sep_expr = separate_with_spaces(sep_var_funcs)
    sep_brackts = mult_sign_between_brackts(sep_expr)
    converted_expression = separate_variables(sep_brackts)

    print(f'Converted expression: {converted_expression}')
        
    return converted_expression