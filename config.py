HOST = '127.0.0.1'
PORT = 8001

# TEMPLATES
MAIN_TEMPLATE = 'index.html'
STUDENTS_TEMPLATE = 'students.html'
WEATHER_TEMPLATE = 'weather.html'

#PAGES
WEATHER = '/weather'
STUDENTS = '/students'
MAIN = '/'
PAGES = WEATHER, STUDENTS

# db
SELECT = 'SELECT * FROM {table}'
INSERT = 'INSERT INTO {table} ({attrs}) VALUES ({values})'
DELETE = 'DELETE FROM {table}'
UPDATE = 'UPDATE {table} SET {data}'
SELECT_ID = 'SELECT id FROM {table}'
GET_TOKEN = 'SELECT token FROM token WHERE username=\'{username}\''
STUDENTS_ALL_ATTRS = ['id', 'fname', 'lname', 'sname', 'group_', 'age']
STUDENTS_REQ_ATTRS = ['fname', 'lname', 'group_']
POST_RESPONSE_URL = f'http://{HOST}:{PORT}{STUDENTS}?id='

# HTTTP codes
OK = 200
NOT_FOUND = 404
FORBIDDEN = 403
BAD_REQUEST = 400
NOT_IMPLEMENTED = 501
INTERNAL_ERROR = 500

# CODING
ENCODING = 'KOI8-R'

# weather consts
COLLEGE_LOCATION = {'lat': 43.403438, 'lon': 39.981544}
SOCHI_LOCATION = {'lat': 43.713351, 'lon': 39.580041}
POLYANA_LOCATION = {'lat': 43.661294, 'lon': 40.268936}
LOCATIONS = {
    'college': COLLEGE_LOCATION,
    'sochi': SOCHI_LOCATION, 
    'polyana': POLYANA_LOCATION
}
YANDEX_API_URL = 'https://api.weather.yandex.ru/v2/informers'

# headers' names
YANDEX_API_HEADER = 'X-Yandex-API-Key'
HEADER_LENGTH = 'Content-Length'
HEADER_TYPE = 'Content-Type'

# debug messsages
WEATHER_MSG = 'YANDEX API get_weather'