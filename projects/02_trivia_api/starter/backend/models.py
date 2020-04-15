import os
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CheckConstraint
from flask_sqlalchemy import SQLAlchemy
import json

database_path = "postgresql://juliane:POSTGRES@localhost:5432/trivia"

db = SQLAlchemy()

'''
binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Category
'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    questions = relationship('Question')

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }


'''
Question

'''


class Question(db.Model):
    __tablename__ = 'questions'
    __table_args__ = (
        CheckConstraint('length(question) > 1', name='non_empty_question'),
        CheckConstraint('length(answer) > 1', name='non_empty_answer')
    )

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(Integer, ForeignKey('categories.id'))
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }
