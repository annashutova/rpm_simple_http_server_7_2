from config import *


def list_to_paragraphs(data: list):
    return ''.join([f'<ul>{value}</ul>' for value in data]) if data else '<p>No data given.</p>'

def weather(weather: dict) -> bytes:
    with open(WEATHER_TEMPLATE, 'r') as f:
        return f.read().format(**weather).encode(ENCODING)
    
def students(students_data: dict):
    with open(STUDENTS_TEMPLATE, 'r') as f:
        return f.read().format(**students_data).encode(ENCODING)

def main_page():
    with open(MAIN_TEMPLATE, 'r') as f:
        return f.read().encode(ENCODING)
