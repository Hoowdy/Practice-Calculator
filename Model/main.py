import infix_to_postfix
import prc
import calculate
import sys

#вводимо, oпрацьовуєм вираз та переводимо в ОПЗ
expression = input('введіть вираз: ')
process_expression = prc.process_expression(expression)
postfix_expression = infix_to_postfix.infix_to_postfix(process_expression)
print(postfix_expression)

#вираховуєм результат
calc_expr = calculate.Calc(postfix_expression)

#вивід результату
try:
    result = calc_expr.evaluate()
except ValueError as nigga: # "Во всем негры виноваты" - Олексій Кузьмін-Гітлер
    print(nigga)
    sys.exit(0)

if isinstance(result, float):
    result = round(result, 2)
    print(result)
else:
    print(result)


