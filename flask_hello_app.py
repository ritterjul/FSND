from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # set ame of Flask app to name of module/file

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turn off tracking modifications -> remove warning
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jule@localhost:5432/flask_hello_app' # specify database to use
db = SQLAlchemy(app)  # link instance of database to Flask app

class Person(db.Model): # inherit new class from db.Model to create mapping from class to db
    __tablename__ = 'persons' # set table name, (optional, default name would be person)
    id = db.Column(db.Integer, primary_key=True) # introduce columns
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

db.create_all() # detect models and create tables for them (if they do not exist)

@app.route('/') # when a request to route / (home page) comes in from a client
def index():
    person = Person.query.first() # query first record of table connected to Person class
    return 'Hello ' + person.name + '!' # print 'Hello <name>!' on page for queried record


