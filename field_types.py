from datetime import date


def int_field(operator: str, const: str, null_allowed: bool):
    """
    Створює замикання, функцію яка запам'ятовує значення параметрів
    та використовує їх для перевірки значення деякого числа.

    :param operator: оператор порівняння ">, <, =, !"
    :param const: число, яке буде запам'ятоване
    :param null_allowed: чи є допустимими значення None
    :return: функція, яка порівнює число із раніше запам'ятованим
    """

    const = int(const)

    def cmp(variable: str):
        if variable is None:
            return null_allowed

        variable = int(variable)

        return {
            '>': lambda x: x > const,
            '<': lambda x: x < const,
            '=': lambda x: x == const,
            '!': lambda x: x != const,
        }[operator](variable)
    return cmp


def str_field(operator: str, const: str, null_allowed: bool):
    """
    Створює замикання, функцію яка запам'ятовує значення параметрів
    та використовує їх для перевірки значення деякого рядка.

    :param operator: оператор порівняння ">, <, =, !, contains"
    :param const: рядок, який буде запам'ятовано
    :param null_allowed: чи є допустимими значення None
    :return:
    """

    def cmp(variable: str):
        if variable is None:
            return null_allowed

        return {
            '>': lambda x: x > const,
            '<': lambda x: x < const,
            '=': lambda x: x == const,
            '!': lambda x: x != const,
            'contains': lambda x: x.count(const) > 0,
        }[operator](variable)
    return cmp


def date_field(operator: str, const: str, null_allowed: bool):
    """
    Створює замикання, функцію яка запам'ятовує значення параметрів
    та використовує їх для перевірки значення деякої дати.

    :param operator: оператор порівняння ">, <, =, !"
    :param const: дата, яку буде запам'ятовано
    :param null_allowed: чи є допустимими значення None
    :return:
    """

    yyyy, mm, dd = [int(x) for x in const.split('-')]
    const_date = date(yyyy, mm, dd)

    def cmp(variable: str):

        if variable is None:
            return null_allowed

        yyyy, mm, dd = [int(x) for x in variable.split('-')]
        var_date = date(yyyy, mm, dd)
        return {
            '>': lambda x: x > const_date,
            '<': lambda x: x < const_date,
            '=': lambda x: x == const_date,
            '!': lambda x: x != const_date,
        }[operator](var_date)
    return cmp
