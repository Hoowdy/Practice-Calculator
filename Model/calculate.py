import math, cmath, numpy
from typing import Any

class Calc:
    """
    Клас для обчислення виразу у постфіксній формі.
    """
    def __init__(self):
        self.expression = None
        self.variables = {}
        self.stack = []
        self.stack_trace = []

    def evaluate(self, expression, variables : dict[str, Any]):
        """
        Обчислює значення виразу. Якщо у виразі є змінні, просить користувача ввести їх значення.
        """
        # Заміна констант 'pi' та 'e' на їх числові значення
        self.expression = expression.replace("pi", str(math.pi)).replace("e", str(math.e)).replace(",", ".").split()
    
        functions = ['sin', 'cos', 'tan', 'tg', 'cot', 'ctg', 'asin', 'arcsin', 'acos', 'arccos',
                     'atan', 'arctan', 'arctg', 'acot', 'arcctg', 'arccot', 'sinh', 'sh', 'cosh',
                     'ch', 'tanh', 'th', 'coth', 'cth', 'sqrt', 'ln', 'lg', 'log', 'abs', 'niga']

        for token in self.expression:
            if token in "+-*/^":
                # Виконуємо операцію з двома останніми операндами на стеку
                right = self.stack.pop()
                left = self.stack.pop()
                result = self.apply_operator(token, left, right)
                self.stack.append(result)
            elif token in functions:
                # Виконуємо функцію для останнього операнда на стеку
                if token == 'log':
                    operand = [self.stack.pop(), self.stack.pop()]
                else:
                    operand = self.stack.pop()
                result = self.apply_function(token, operand)
                self.stack.append(result)
            elif token.isalpha():
                # Обробка змінних, запит значення у користувача, якщо змінна ще не визначена
                if token not in variables:
                    # value = input(f"Введіть значення для змінної {token} (або введіть '{token}', щоб залишити змінну): ")
                    # if value == token:
                    #     self.variables[token] = token
                    # else:
                    #     self.variables[token] = float(value)
                    raise ValueError(f"Value of {token} is not defined")
                self.stack.append(variables[token])
            else:
                # Якщо токен є числом
                self.stack.append(float(token))
            self.stack_trace.append(self.stack[:])
        self.expression = self.stack[0]
        self.stack.clear()
        return self.evaluate_with_variables()

    @staticmethod
    def apply_operator(operator, left, right):
        """
        Застосовує оператор до двох операндів.
        """
        if isinstance(left, str) or isinstance(right, str):
            return f"({left} {operator} {right})"
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise ValueError('Undefined: Division by zero')
            return left / right
        elif operator == '^':
            return left ** right
    
    @staticmethod
    def apply_function(function, operand):
        """
        Застосовує математичну функцію до операнда.
        """
        if isinstance(operand, str):
            return f"{function}({operand})"
        
        elif function == 'sin':
            return math.sin(operand)
        
        elif function == 'cos':
            return math.cos(operand)
        
        elif function == 'tan' or function == 'tg':
            # num = operand / (math.pi /2)
            # if not num % 2 == 0:
            #     raise ValueError('Undefined')
            return math.tan(operand)
        
        elif function == 'cot' or function == 'ctg':
            num = operand / math.pi
            if num == int(num):
                raise ValueError('Undefined')
            return math.cos(operand) / math.sin(operand)
        
        elif function == 'arcsin' or function == 'asin':
            return cmath.asin(operand).real
        
        elif function == 'arccos' or function == 'acos':
            return cmath.acos(operand).real
        
        elif function == 'arctan' or function == 'arctg' or function == 'atan':
            return cmath.atan(operand).real
        
        elif function == 'arccot' or function == 'arcctg' or function == 'acot':
            if operand > 0:
                return (math.pi / 2) - cmath.atan(operand).real
            elif operand < 0:
                return (-math.pi / 2) - cmath.atan(operand).real
            else:
                return math.pi / 2
            
        elif function == 'sinh' or function == 'sh':
            if operand > 710:
                raise ValueError("The value is too big.")
            elif operand < 710:
                raise ValueError("The value is too small.")
            else:
                return cmath.sinh(operand).real
        
        elif function == 'cosh' or function == 'ch':
            if operand > 710:
                raise ValueError("The value is too big.")
            elif operand < 710:
                raise ValueError("The value is too small.")
            else:
                return cmath.cosh(operand).real
        
        elif function == 'tanh' or function == 'th':
            return cmath.tanh(operand).real
        
        elif function == 'coth' or function == 'cth':
            return 1 / cmath.tanh(operand).real
        
        elif function == 'sqrt':
            if operand < 0:
                raise ValueError('Undefined: Square root of negative number')
            return cmath.sqrt(operand).real
        
        elif function == 'log':
            if isinstance(operand, list):
                base, value = operand
                if value <= 0:
                    raise ValueError('Undefined: Log of non-positive number')
                if base <= 0:
                    raise ValueError('Undefined: Log with base less than or equal to zero.')
                if base == 1:
                    raise ValueError("Underfined: Log base equal to one.")
                return math.log(value, base)
            
        elif function == 'ln':
            if operand <= 0:
                raise ValueError('Undefined: Log of negative number')
            return cmath.log(operand).real
        
        elif function == 'lg':
            if operand <= 0:
                raise ValueError('Undefined: Log of negative number')
            return cmath.log10(operand).real
        
        elif function == 'abs':
            return abs(operand)
        
        elif function == 'niga':
            raise Exception('☠☠ nigga why you so black ☠☠')
        
    def evaluate_with_variables(self):
        """
        Обчислює вираз, який може містити змінні.
        """
        if isinstance(self.expression, str):
            return self.expression
        elif isinstance(self.expression, (int, float)):
            return self.expression
        else:
            left = self.evaluate_with_variables(self.expression[0])
            right = self.evaluate_with_variables(self.expression[2])
            operator = self.expression[1]
            if isinstance(left, str) or isinstance(right, str):
                return f"({left} {operator} {right})"
            else:
                return eval(f"{left} {operator} {right}")