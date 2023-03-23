from config import WEATHER_TEMPLATE, STUDENTS_TEMPLATE, MAIN_TEMPLATE


def list_to_paragraphs(data: list):
    return ''.join([f'<ul>{value}</ul>' for value in data]) if data else '<p>No data given.</p>'


def weather(weather_data: dict) -> str:
    with open(WEATHER_TEMPLATE, 'r') as template:
        return template.read().format(**weather_data)


def students(students_data: dict) -> str:
    with open(STUDENTS_TEMPLATE, 'r') as template:
        return template.read().format(**students_data)


def main_page() -> str:
    with open(MAIN_TEMPLATE, 'r') as template:
        return template.read()
