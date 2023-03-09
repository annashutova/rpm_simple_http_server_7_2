from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv
from config import *
from json import loads
from views import weather, students, main_page, list_to_paragraphs
from requests import get


load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')
YANDEX_KEY = getenv('YANDEX_KEY')


def get_data(query: dict, table: str) -> dict:
    global db_cursor
    db_cursor.execute(query_request(SELECT.format(table=table), query))
    students = db_cursor.fetchall()
    return {
        'number': len(students), 
        'rendered_students': list_to_paragraphs(students)
        }


def query_request(request: str, query: dict):
    if query:
        parts = []
        for key, value in query.items():
            if isinstance(value, int):
                parts.append(f"{key}={value}")
            else:
                parts.append(f"{key}='{value}'")
        return '{0} WHERE {1}'.format(request, ' AND '.join(parts))
    return request


def get_weather(query: dict) -> dict:
    weather_data = {
        'temp': None,
        'feels_like': None,
        'condition': None,
        'location': 'Sirius College'
    }

    params = LOCATIONS['college']
    if query:
        location = query.get('location')
        if location:
            params = LOCATIONS[location]
            weather_data['location'] = location
    else:
        print(f'{WEATHER_MSG} failed to get location from query, defaults to college')
    response = get(YANDEX_API_URL, params=params, headers={YANDEX_API_HEADER: YANDEX_KEY})
    if response.status_code != OK:
        print(f'{WEATHER_MSG} failed with status code: {response.status_code}')
        return weather_data
    response_data = response.json()
    if not response_data:
        print(f'{WEATHER_MSG} api did respond with empty content')
        return weather_data
    fact = response_data.get('fact')
    if not fact:
        print(f'{WEATHER_MSG} api did not provide factual weather data')
        return weather_data
    for key in weather_data.keys():
        if key != 'location':
            weather_data[key] = fact.get(key)
    return weather_data


def change_db(request: str):
    global db_cursor, db_connection
    try:
        db_cursor.execute(request)
    except Exception as error:
        print(f'change_db error: {error}')
        return False
    else:
        db_connection.commit()
        return bool(db_cursor.rowcount)


def db_insert(table: str, data: dict) -> bool:
    keys = list(data.keys())
    values = [data[key] for key in keys]
    attrs = ', '.join([str(key) for key in keys])
    values_str = ', '.join([f"{value}" if isinstance(value, int) else f"'{value}'" for value in values])
    return change_db(INSERT.format(table=table, attrs=attrs, values=values_str))

def db_delete(table: str, data: dict):
    return change_db(query_request(DELETE.format(table=table), data))


def is_valid_token(username: str, token: str) -> bool:
    global db_cursor
    db_cursor.execute(GET_TOKEN.format(username=username))
    answer = db_cursor.fetchone()
    if answer:
        return token == answer[0]
    return False
        

class CustomHandler(BaseHTTPRequestHandler):

    def query_from_path(self):
        result = {}
        index = self.path.find('?')
        if index != -1 and index != len(self.path) - 1:
            query_parts = self.path[index + 1:].split('&')
            query = [part.split('=') for part in query_parts]
            for key, value in query:
                if value.isdigit():
                    result[key] = int(value)
                else:
                    result[key] = value
        return result

    def get_template(self) -> bytes:
        if self.path.startswith(STUDENTS):
            return students(get_data(self.query_from_path(), STUDENTS[1:]))
        elif self.path.startswith(WEATHER):
            return weather(get_weather(self.query_from_path()))
        return main_page()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'html')
        self.end_headers()
        self.wfile.write(self.get_template())


    def make_changes(self):
        if self.path.startswith(STUDENTS):
            content_length = int(self.headers['Content-Length'])
            data = loads(self.rfile.read(content_length).decode(ENCODING))
            print(f'{self.command} request data: {data}')

            if self.command == 'PUT':
                code = OK
                msg = 'OK' if db_insert(STUDENTS[1:], data) else 'FAIL'
            elif self.command == 'DELETE':
                code = OK
                msg = 'OK' if db_delete(STUDENTS[1:], data) else 'FAIL'
            else:
                code = NOT_IMPLEMENTED
                msg = 'Not implemented by server, available requests are GET, PUT, DELETE'
            return code, f'{self.command} {msg}'
        
        return NOT_FOUND, 'Content was NOT FOUND'
        

    def respond(self, code: int, msg: str):
        self.send_response(code)
        self.send_header('Content-type', 'text')
        self.end_headers()
        self.wfile.write(msg.encode(ENCODING))


    def check_auth(self):
        auth = self.headers.get('Authorization', '').split()
        if len(auth) == 2:
            username, token = auth[0], auth[1][1:-1]
            if is_valid_token(username, token):
                return True
        return False


    def process(self):
        if self.check_auth():
            code, msg = self.make_changes()
        else:
            code, msg = FORBIDDEN, 'Authorization was failed!'
        self.respond(code, msg)


    def do_PUT(self):
        self.process()


    def do_DELETE(self):
        self.process()


if __name__ == '__main__':
    db_connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
    db_cursor = db_connection.cursor()
    with ThreadingHTTPServer((HOST, PORT), CustomHandler) as server:
        server.serve_forever()
    # server.server_close()
    db_cursor.close()
    db_connection.close()
