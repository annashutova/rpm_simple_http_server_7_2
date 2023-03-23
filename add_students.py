from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv

load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')

request = "INSERT INTO students (fname, lname, group_, age) VALUES ('%s','%s','%s',%d)"

students = [
    ('Даниил', 'Снопов', '1_11_7_1', 18),
    ('Вероника', 'Вечернина', '1_11_7_1', 18),
    ('Анна', 'Шутова', '1_11_7_1', 18),
    ('Екатерина', 'Гоцкина', '1_11_7_1', 18),
    ('Кирилл', 'Приходько', '1_11_7_1', 40),
    ('Максим', 'Безбородов', '1_11_7_1', 18),
    ('Даниил', 'Смирнов', '1_11_7_1', 18),
]

students += [
    ('Виктор', 'Назаров', '1_11_7_2', 18),
]

connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
cursor = connection.cursor()

for fname, lname, group, age in students:
    cursor.execute(request, (fname, lname, group, age))

connection.commit()
