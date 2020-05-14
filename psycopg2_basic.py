import psycopg2

connection = psycopg2.connect('dbname=demo') # start connection/session to database demo

cursor = connection.cursor() # open a cursor to perform database operations

cursor.execute('''
CREATE TABLE table2(
   id INTEGER primary key,
   completed BOOLEAN not null DEFAULT False
   );
''') # add CREATE TABLE query to cursor

cursor.execute('INSERT INTO table2 VALUES (1, True);')  # add INSERT INTO query to cursor

connection.commit()  # submit queries to to database

cursor.close()
connection.close() # close connection/session
