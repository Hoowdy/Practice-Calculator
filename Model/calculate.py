import math, cmath
from typing import Any
from .prc import process_expression
from .infix_to_postfix import infix_to_postfix, is_num

class Calc:

    FUNCTIONS = ['sin', 'cos', 'tan', 'tg', 'cot', 'ctg', 'asin', 'arcsin', 'acos', 'arccos',
                     'atan', 'arctan', 'arctg', 'acot', 'arcctg', 'arccot', 'sinh', 'sh', 'cosh',
                     'ch', 'tanh', 'th', 'coth', 'cth', 'sqrt', 'ln', 'lg', 'log', 'abs']

    def __init__(self):
        self.expression = None
        self._variables = {}
        self.stack_trace = None

    @property
    def variables(self) -> dict[str, Any]:
        return self._variables

    def evaluate(self, expression : str = None, variables : dict[str, Any] = None):
        """
        Evaluates the expression without variable substitution.
        """
        _expression = self.expression
        if expression:
            _expression, self.stack_trace = infix_to_postfix(process_expression(expression))
            self._variables = {}
        if not _expression:
            return
        tokens = _expression.split()
        stack = []

        for token in tokens:
            if token in "+-*/^":
                right = stack.pop()
                left = stack.pop()
                result = self.apply_operator(token, left, right)
                stack.append(result)

            elif token in self.FUNCTIONS:
                if token == 'log':
                    operand = [stack.pop(), stack.pop()]
                else:
                    operand = stack.pop()
                result = self.apply_function(token, operand)
                stack.append(result)

            elif token.isalpha():
                if token in variables:
                    stack.append(variables[token])
                    self._variables[token] = variables[token]
                elif token in self._variables.keys():
                    stack.append(self._variables[token])
                else:
                    stack.append(token)
                    self._variables[token] = token
            else:
                try:
                    stack.append(float(token))
                except ValueError:
                    stack.append(token)

        if expression:
            self.expression, self.stack_trace = infix_to_postfix(stack[0])

        return stack[0], self.stack_trace

    def apply_operator(self, operator, left, right):
        """
        Applies the operator to two operands.
        """
        if not (is_num(left) and is_num(right)):
            return f"({left} {operator} {right})"
        if operator == '+':
            return float(left) + float(right)
        elif operator == '-':
            return float(left) - float(right)
        elif operator == '*':
            return float(left) * float(right)
        elif operator == '/':
            if float(right) == 0:
                raise ValueError('Undefined: Division by zero')
            return float(left) / float(right)
        elif operator == '^':
            return float(left) ** float(right)
    
    def apply_function(self, function, operand):
        """
        Applies the mathematical function to the operand.
        """
        if not is_num(operand):
            return f"{function}({operand})"
        
        elif function == 'sin':
            return math.sin(operand)
        
        elif function == 'cos':
            return math.cos(operand)
        
        elif function == 'tan' or function == 'tg':
            if math.isclose(math.cos(operand), 0, abs_tol=1e-15):
                raise ValueError('Undefined')
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
                raise ValueError("The value is too large.")
            elif operand < -710:
                raise ValueError("The value is too small.")
            else:
                return cmath.sinh(operand).real
        
        elif function == 'cosh' or function == 'ch':
            if operand > 710:
                raise ValueError("The value is too large.")
            elif operand < -710:
                raise ValueError("The value is too small.")
            else:
                return cmath.cosh(operand).real
        
        elif function == 'tanh' or function == 'th':
            return cmath.tanh(operand).real
        
        elif function == 'coth' or function == 'cth':
            return 1 / cmath.tanh(operand).real
        
        elif function == 'sqrt':
            if operand < 0:
                raise ValueError('Undefined: Square root of negative number.')
            return cmath.sqrt(operand).real
        
        elif function == 'log':
            if isinstance(operand, list):
                base, value = operand
                if value <= 0:
                    raise ValueError('Undefined: Log of non-positive number.')
                if base <= 0:
                    raise ValueError('Undefined: Log with base less than or equal to zero.')
                if base == 1:
                    raise ValueError("Underfined: Log base equal to one.")
                return math.log(value, base)
            
        elif function == 'ln':
            if operand <= 0:
                raise ValueError('Undefined: Log of negative number.')
            return cmath.log(operand).real
        
        elif function == 'lg':
            if operand <= 0:
                raise ValueError('Undefined: Log of negative number.')
            return cmath.log10(operand).real
        
        elif function == 'abs':
            return abs(operand)
    
    # def substitute_variables(self, variables):
    #     """
    #     Substitutes variable values into the expression and evaluates the result.
    #     """
    #     substituted_expression = self.original_expression
        
    #     # Substitute variable values into the original expression
    #     for var, value in variables.items():
    #         substituted_expression = substituted_expression.replace(var, str(value))
        
    #     # Evaluate the substituted expression
    #     return self.evaluate(substituted_expression)