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

# Обчислення без підстановки змінних
try:
    result_without_vars = calc_expr.evaluate()
except ValueError as ex:
    print(ex)
    sys.exit(0)

# Задання значень змінних
variables = {'x': 2, 'y': 0, 'z': 1}
calc_expr.variables = variables

# Підстановка і обрахунок змінних у вираз
try:
    sub_res = calc_expr.substitute_variables(variables)
except ValueError as ex:
    print(ex)
    sys.exit(0)

# Оцінка виразу без підстановки змінних
result_without_vars = calc_expr.evaluate()

# Виведення результатів
if isinstance(result_without_vars, float):
    result_without_vars = round(result_without_vars, 2)
print("Результат без підстановки змінних:", result_without_vars)

if isinstance(sub_res, float):
    sub_res = round(sub_res, 2)
print("Результат з підстановкою змінних:", sub_res)