import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/categories',methods=['GET'])
  def get_categories():
    try:
        categories=Category.query.all()
        formatted_categories = {cat.id:cat.type for cat in categories}

        if len(categories)==0:
            abort(404)
      
        return jsonify({
          'success':True,
          'categories':formatted_categories
        })

    except:
        abort(422)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''

  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

  @app.route('/questions', methods=['GET'])
  def get_questions():
    try:
        categories=Category.query.order_by(Category.id).all()
        formatted_cats = {cat.id:cat.type for cat in categories}
        current_category = formatted_cats[1]

        if len(current_category)==0:
          abort(404)

        selection = Question.query.filter(Question.category==1).order_by(Question.id).all()
        questions = paginate_questions(request,selection)

        if len(questions) == 0:
          abort(404)

        return jsonify({
          'questions':questions,
          'total_questions':len(Question.query.all()),
          'current_category':current_category,
          'categories':formatted_cats
        })

    except:
      abort(422)

  @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
  def get_cat_questions(cat_id):
    category_id = cat_id
    
    try:
        current_category = Category.query.filter(Category.id==category_id).one_or_none()
        current_category = current_category.type
        
        if current_category is None:
            abort(404)
        
        selection = Question.query.filter(Question.category==category_id).order_by(Question.id).all()
        questions = paginate_questions(request,selection)

        if len(questions)==0:
            abort(404)
      
        return jsonify({
          'success':True,
          'current_category':current_category,
          'questions':questions,
          'total_questions':len(Question.query.all())
        })

    except:
        abort(422)

  @app.route('/questions/<int:id>',methods=['DELETE'])
  def delete_question(id):
    question_id = id

    try:
        question = Question.query.filter(Question.id==question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()

        return jsonify({
          'success':True
        })

    except:
      abort(422)

  @app.route('/questions',methods=['POST'])
  def add_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    try:
      question = Question(question=new_question, answer=new_answer, category=new_category,difficulty=new_difficulty)
      question.insert()

      return jsonify({
        'success': True
      })

    except:
      abort(422)
  
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', None)

    try:
        selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        questions = paginate_questions(request,selection)

        return jsonify({
          'success':True,
          'questions':questions
        })
    except:
      abort(422)

  @app.route('/quizzes', methods=['POST'])
  def quiz_questions():
    body = request.get_json()
    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)

    try:
        selection = Question.query.filter(Question.category==quiz_category['id'],~Question.id.in_(previous_questions)).order_by(func.random()).first()
        quiz_question = paginate_questions(request,selection)

        if len(question) == 0:
            abort(404)

        return jsonify({
          "question":quiz_question
        })
    except:
        abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    