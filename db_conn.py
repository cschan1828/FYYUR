import psycopg2

connection = psycopg2.connect(host="localhost",port=5432, database="postgres", user='postgres', password='')
print(psycopg2)

cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS table2;')

cursor.execute('''
  CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
''')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))

SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'

data = {
  'id': 2,
  'completed': False
}
cursor.execute(SQL, data)

data = {
  'id': 3,
  'completed': True
}
cursor.execute(SQL, data)

SQL = 'SELECT * FROM venue'
cursor.execute(SQL)
result = cursor.fetchall()
print(result)

connection.commit()

connection.close()
cursor.close()