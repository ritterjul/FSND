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

cursor.execute('INSERT INTO table2 VALUES (%s, %s);', (1, True))  # use string interpolation to insert row with tuple of values

SQL = 'INSERT INTO table2 VALUES (%(id)s, %(completed)s);'  # create a template string

data = { # create a dictionary of values
    'id': 2,
    'completed': False
    }

cursor.execute(SQL, data) # use template and dictionary to insert row

connection.commit()

cursor.close()
connection.close()