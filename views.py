
from config import *


def list_to_paragraphs(data: list):
    return ''.join([f'<ul>{value}</ul>' for value in data]) if data else '<p>No data given.</p>'

def weather(weather: dict) -> bytes:
    with open(WEATHER_TEMPLATE, 'r') as f:
        return f.read().format(**weather).encode()
    
def group(path: str, group_data: dict):
    print(group_data)
    with open(GROUP_PAGE, 'r') as f:
        page = f.read()
        if path in PAGES:
            return page.format(**group_data).encode()
    return None

def main_page():
    with open(MAIN_PAGE, 'r') as f:
        return f.read().encode()