import psycopg2

connection = psycopg2.connect('dbname=demo')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS table2;')
cursor.execute('''
CREATE TABLE table2(
    id INTEGER primary key,
    completed BOOLEAN not null DEFAULT False
    );
''')

cursor.execute('INSERT INTO table2 VALUES (%s, %s);', (1, True))

SQL = 'INSERT INTO table2 VALUES (%(id)s, %(completed)s);'

data = {
    'id': 2,
    'completed': False
    }

cursor.execute('INSERT INTO table2 VALUES (%s, %s);', (3, True))

cursor.execute(SQL, data)

cursor.execute('SELECT * FROM table2') # query all the data in table2
result = cursor.fetchall()  # extract all rows from cursor
print(result) # print -> 3 rows

result2 = cursor.fetchone()  # extract 1 row from cursor
print(result2) # print -> no rows, because all previously extracted

connection.commit()

cursor.execute('SELECT * FROM table2') # query all the data in table2
result = cursor.fetchmany(2)  # extract 2 rows from cursor
print(result) # print -> 2 rows

result2 = cursor.fetchone()  # extract 1 row from cursor
print(result2)  # print -> 1 row

connection.commit()

cursor.close()
connection.close()