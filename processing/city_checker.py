from string import printable


def check_city(city_name: str) -> tuple:
    """Метод возвращает отфармотированное название города с большой буквы и без пробелов с уточнением, на каком
    языке написано название города"""
    if not city_name.isalpha():
        return False, False

    city_name = city_name.strip()
    if set(city_name)-set(printable):
        return city_name.capitalize(), 'Cyrillic'
    elif not set(city_name)-set(printable):
        return city_name.capitalize(), 'Latin'
