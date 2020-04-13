import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from math import ceil
from random import randint

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app)
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Methods', ['GET', 'POST', 'DELETE'])
    return response

  @app.route('/categories', methods=['GET'])
  def get_categories():
    try:
      query = Category.query.all()
      categories = {category.id: category.type for category in query}
      response = {'categories': categories}
      return jsonify(response) 
    except:
      abort(500)   
  
  @app.route('/questions', methods=['GET'])
  def get_questions():
    try:
      query = Question.query.all()
      questions = [question.format() for question in query]
      query = Category.query.all()
      categories = {category.id: category.type for category in query}
    except:
      abort(500)
    
    page = request.args.get('page', 1, type=int)
    if page <= ceil(len(questions) / QUESTIONS_PER_PAGE):      
      response = {
        'questions': questions[(page - 1)*QUESTIONS_PER_PAGE:page*QUESTIONS_PER_PAGE],
        'total_questions': len(questions),
        'categories': categories,
        'current_category': None
      }
      return jsonify(response)
    else:
      abort(404)
    
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.get(question_id)
    if question:
      try:
        question.delete()
        return jsonify({'success': True})
      except:
        abort(500)
    else:
      abort(404)
  
  @app.route('/questions', methods=['POST'])
  def post_question():
    data = request.get_json()
    try:
      question = Question(
        question=data['question'],
        answer=data['answer'],
        category=data['category'],
        difficulty=data['difficulty']
      )
    except:
      abort(404)

    try:
      question.insert()
      return jsonify({'success': True})
    except:
      abort(500)
    
  @app.route('/searchQuestions', methods = ['POST'])
  def search_questions():
    data = request.get_json()
    try:
      query = Question.query.filter(Question.question.ilike('%{}%'.format(data['searchTerm'])))
      questions = [question.format() for question in query]
    except:
      abort(500)

    page = request.args.get('page', 1, type=int)
    if (page <= ceil(len(questions) / QUESTIONS_PER_PAGE)) or (len(questions) == 0): # show empty page instead of error if search returns no results
      response = {
        'questions': questions[(page - 1)*QUESTIONS_PER_PAGE:page*QUESTIONS_PER_PAGE],
        'total_questions': len(questions),
        'current_category': None
      }
      return jsonify(response)
    else:
      abort(404)

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    try:
      query = Question.query.filter(Question.category==category_id).all()
      questions = [question.format() for question in query]
    except:
      abort(404)
    
    page = request.args.get('page', 1, type=int)
    if page <= ceil(len(questions) / QUESTIONS_PER_PAGE):
      response = {
      'questions': questions[(page - 1)*QUESTIONS_PER_PAGE:page*QUESTIONS_PER_PAGE],
      'total_questions': len(questions),
      'current_category': category_id
      }
      return jsonify(response)
    else:
      abort(404)

  @app.route('/quizzes', methods = ['POST'])
  def get_next_question():
    data = request.get_json()
    previous_questions_ids = data['previous_questions']
    category_id = data['quiz_category']['id']

    if category_id == 0:
      query = Question.query.all()
    else:
      query = Question.query.filter(Question.category == category_id)
    
    if query.count() >= 1:
      query = query.filter(~Question.id.in_(previous_questions_ids))

      if query.count() >= 1:
        draw = randint(0, query.count()-1)
        question = query.offset(draw).first()
        response = {
          'question' : question.format()
        }
      else:
        response = {
          'question' : False
        }
      
      return jsonify(response)
    else:
      abort(404)

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad request"
        }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable entity"
        }), 422

  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal server error"
        }), 500

  return app

    