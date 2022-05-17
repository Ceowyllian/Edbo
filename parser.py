import requests
import csv


def find_universities(location: str, filters: list):
    """
    Шукає університети в заданому регіоні, які відповідають обмеженням.

    :param location: регіон
    :param filters: список обмежень, який складається із кортежів (назва поля, фільтр)
    :return: список університетів (словників)
    """

    r = requests.get(f'https://registry.edbo.gov.ua/api/universities/?ut=1&lc={location}&exp=json')
    universities: list = r.json()

    # filters - список кортежів виду (назва поля, фільтр поля)
    for field, constraint in filters:
        universities = list(filter(lambda x: constraint(x[field]), universities))
    return universities


def save_result(path, universities: list, fields: list):
    """
    Зберігає у csv файл інформацію про університети.

    :param path: шлях до файлу
    :param universities: список університетів (словників)
    :param fields: список полів, які необхідно зберегти
    """

    result = [{k: u[k] for k in fields} for u in universities]
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fields, delimiter=';')
        writer.writeheader()
        writer.writerows(result)
