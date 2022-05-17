from pprint import pprint as pp
from field_types import str_field, date_field, int_field
from parser import find_universities, save_result

regions = {
    '01': 'Автономна Республіка Крим',
    '05': 'Вінницька область',
    '07': 'Волинська область',
    '12': 'Дніпропетровська область',
    '14': 'Донецька область',
    '18': 'Житомирська область',
    '21': 'Закарпатська область',
    '23': 'Запорізька область',
    '26': 'Івано-Франківська область',
    '32': 'Київська область',
    '35': 'Кіровоградська область',
    '44': 'Луганська область',
    '46': 'Львівська область',
    '48': 'Миколаївська область',
    '51': 'Одеська область',
    '53': 'Полтавська область',
    '56': 'Рівненська область',
    '59': 'Сумська область',
    '61': 'Тернопільська область',
    '63': 'Харківська область',
    '65': 'Херсонська область',
    '68': 'Хмельницька область',
    '71': 'Черкаська область',
    '73': 'Чернівецька область',
    '74': 'Чернігівська область',
    '80': 'КИЇВ',
    '85': 'м.Севастополь',
}

fields = {
    'university_id': int_field,
    'university_parent_id': int_field,

    'university_type_name': str_field,

    'university_name': str_field,
    'university_short_name': str_field,
    'university_name_en': str_field,

    'registration_year': int_field,

    'university_director_post': str_field,
    'university_director_fio': str_field,

    'region_name': str_field,
    'region_name_u': str_field,
    'university_address': str_field,
    'university_address_u': str_field,
    'post_index': int_field,
    'post_index_u': int_field,
    'is_from_crimea': int_field,

    'koatuu_id': int_field,
    'koatuu_name': str_field,
    'koatuu_id_u': int_field,
    'koatuu_name_u': str_field,

    'university_phone': str_field,
    'university_email': str_field,
    'university_site': str_field,

    'close_date': date_field,
    'primitki': str_field,

    'university_edrpou': int_field,
    'university_governance_type_name': str_field,
    'university_financing_type_name': str_field,
}

# Вибір регіону для пошуку ЗВО
print('\nРегіони: ')
pp(regions, indent=4)
lc = input('Введіть код регіону: ')
if lc not in regions.keys():
    print('Регіону з таким кодом не існує!')
    exit(0)


print('Доступні поля: ')
pp(list(fields.keys()), indent=4)

# Вибір полів для збереження в таблиці
print('''Ви можете зберегти повністю інформацію про кожен ЗВО
або тільки деякі поля.''')
fields_to_save = None
if bool(int(input('Вибрати поля для таблиці (0 - ні, 1 - так)?'))):
    fields_to_save = [x.strip() for x in input(
        '''
    \nПерерахуйте через кому поля, які необхідно 
    зберегти у csv файл: 
        ''').split(',')]

    if not set(fields_to_save).issubset(fields.keys()):
        err_msg = f'Полів {set(fields_to_save).difference(fields.keys())} не існує!'
        raise ValueError(err_msg)
else:
    fields_to_save = list(fields.keys())


# Вибір полів для фільтрації
print('Інформацію про ЗВО можна фільтрувати за значеннями полів.')
filters = None
if bool(int(input('Створити фільтри (0 - ні, 1 - так)?'))):
    fields_to_filter = list(set([x.strip() for x in input(
        '''
    \nПерерахуйте через кому поля, за якими буде
    здійснюватись фільтрація (можливі повторення): 
        ''').split(',')]))

    if not set(fields_to_filter).issubset(fields.keys()):
        err_msg = f'Полів {set(fields_to_filter).difference(fields.keys())} не існує!'
        raise ValueError(err_msg)

    print(
        '''
    Оператори для фільтрації полів:
        > - більше (для рядків - лексикографічно);
        < - менше (для рядків - лексикографічно);
        = - дорівнює;
        ! - не дорівнює;
        contains - містить в собі (для рядків);
    Наприклад: registration_year: > 1980
    Між оператором та операндом має стояти пробіл.
    Виберіть фільтри для полів:
        ''')
    filters = []
    for field in fields_to_filter:
        operator, value = input(f'\n{field}: ').split(' ')
        allow_none = bool(int(input('Допускаються значення None (0 - ні, 1 - так): ')))
        filters.append((field, fields[field](operator, value, allow_none)))
else:
    filters = []

universities = find_universities(lc, filters)

# Наприклад C:\myfiles\result.csv
print(f'''За вашим запитом було знайдено {len(universities)} університетів.
Введіть path - шлях, за яким буде збережено файл з результатом.''')

path = input('path: ')
save_result(path, universities, fields_to_save)
