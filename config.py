HOST = '127.0.0.1'
PORT = 8001
MAIN_PAGE = 'index.html'
GROUP_PAGE = 'group_page.html'
page_7_2 = '/7_2'
page_7_1 = '/7_1'
PAGES = page_7_1, page_7_2
SELECT_GROUPS = 'SELECT * FROM group_{group_num}'
INSERT = 'INSERT INTO group_{group_num} VALUES (\'{name}\')'
DELETE = 'DELETE FROM group_{group_num} WHERE name=\'{name}\''
OK = 200
NOT_FOUND = 404