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
GET_TOKEN = 'SELECT token FROM token WHERE username=\'{username}\''

# HTTTP codes
OK = 200
NOT_FOUND = 404
FORBIDDEN = 403
NO_CONTENT = 400

# CODING
ENCODING = 'KOI8-R'