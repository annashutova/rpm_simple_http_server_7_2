from config import *


def list_to_paragraphs(data: list):
    return ''.join([f'<ul>{value}</ul>' for value in data]) if data else '<p>No data given.</p>'

def weather(weather: dict) -> str:
    with open(WEATHER_TEMPLATE, 'r') as f:
        return f.read().format(**weather)
    
def students(students_data: dict) -> str:
    with open(STUDENTS_TEMPLATE, 'r') as f:
        return f.read().format(**students_data)

def main_page() -> str:
    with open(MAIN_TEMPLATE, 'r') as f:
        return f.read()
