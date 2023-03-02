from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv
from config import *
from json import loads


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


def change_db(path: str, name: str, request: str) -> bool:
    global db_cursor, db_connection
    try:
        db_cursor.execute(request.format(group_num=path[1:], name=name))
    except Exception as error:
        print(f'change_db error: {error}')
        return False
    else:
        db_connection.commit()
        return bool(db_cursor.rowcount)
    

def is_valid_token(username: str, token: str) -> bool:
    global db_cursor
    db_cursor.execute(GET_TOKEN.format(username=username))
    answer = db_cursor.fetchone()
    if answer:
        return token == answer[0]
    return False


def get_template(path: str) -> str:
    if path in PAGES:
        return GROUP_PAGE
    return MAIN_PAGE
        

class CustomHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'html')
        self.end_headers()
        template = get_template(self.path)
        with open(template, 'r') as f:
            page = f.read()
            if self.path in PAGES:
                page = page.format(**get_data(self.path))
            self.wfile.write(page.encode())


    def make_changes(self):
        if self.path in PAGES:
            content_length = int(self.headers['Content-Length'])
            data = loads(self.rfile.read(content_length).decode())
            print(f'{self.command} request data: {data}')
            name = data.get('name')
            request = INSERT if self.command == 'POST' else DELETE
            result = 'OK' if change_db(self.path, name, request) else 'FAIL'
            return OK, f'{self.command} {result}'
        else:
            return NOT_FOUND, 'Content was NOT FOUND'
        

    def respond(self, code: int, msg: str):
        self.send_response(code)
        self.send_header('Content-type', 'text')
        self.end_headers()
        self.wfile.write(msg.encode())


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


    def do_POST(self):
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
