from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # set ame of Flask app to name of module/file

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turn off tracking modifications -> remove warning
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jule@localhost:5432/demo' # specify database to use
db = SQLAlchemy(app)  # link instance of database to Flask app

class User(db.Model): # inherit new class from db.Model to create mapping from class to db
    __tablename__ = 'users' # set table name, (optional, default name would be person)
    id = db.Column(db.Integer, primary_key=True) # introduce columns
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'


results = User.query.filter_by(name='Bob').all()
print(results)

like = User.query.filter(User.name.contains('b'))
print(like.limit(5).all())

from sqlalchemy import or_
like = User.query.filter(or_(User.name.contains('b'), User.name.contains('B')))
print(like.limit(5).all())

number = User.query.filter(User.name == 'Bob').count()
print(number)


