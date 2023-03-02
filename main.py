from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv
from config import *

load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')


def get_data(path: str) -> dict:
    global db_cursor
    db_cursor.execute(SELECT_GROUPS.format(group_num=path[1:]))
    students = db_cursor.fetchall()
    return {
        'number': len(students), 
        'students': [record[0] for record in students] if students else 'No students found', 
        'group': '1.11.7.2' if path == page_7_2 else '1.11.7.1'
        }


def get_template(path: str) -> str:
    if path in PAGES:
        return GROUP_PAGE
    return MAIN_PAGE
        

class CustomHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(f'request data:\n {self.__dict__}')
        self.send_response(200)
        self.send_header('Content-type', 'html')
        self.end_headers()
        template = get_template(self.path)
        with open(template, 'r') as f:
            page = f.read()
            if self.path in PAGES:
                page = page.format(**get_data(self.path))
            self.wfile.write(page.encode())


if __name__ == '__main__':
    db_connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
    db_cursor = db_connection.cursor()
    with ThreadingHTTPServer((HOST, PORT), CustomHandler) as server:
        server.serve_forever()
    # server.server_close()
    db_cursor.close()
    db_connection.close()
