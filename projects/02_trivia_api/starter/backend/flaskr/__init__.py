import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import random
import traceback

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
CURRENT_CATEGORY_ID = 1

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

  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

  @app.route('/questions', methods=['GET'])
  def get_questions():
    all_categories = Category.query.all()
    formatted_cats = {cat.id:cat.type for cat in all_categories}

    if CURRENT_CATEGORY_ID not in formatted_cats:
        print(CURRENT_CATEGORY_ID)
        abort(404)
    
    current_category = formatted_cats[CURRENT_CATEGORY_ID]
    
    try:
        selection = Question.query.filter(Question.category==CURRENT_CATEGORY_ID).order_by(Question.id).all()
        questions = paginate_questions(request,selection)
        
        if len(questions) == 0:
          abort(404)

        return jsonify({
          'success':True,
          'questions':questions,
          'total_questions':len(selection),
          'current_category':current_category,
          'categories':formatted_cats
        })

    except:
      traceback.print_exc()
      abort(422)

  @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
  def get_cat_questions(cat_id):
    global CURRENT_CATEGORY_ID

    CURRENT_CATEGORY_ID = cat_id
    
    try:
        current_category = Category.query.filter(Category.id==CURRENT_CATEGORY_ID).one_or_none()
        current_category = current_category.type
        
        if current_category is None:
            abort(404)
        
        selection = Question.query.filter(Question.category==CURRENT_CATEGORY_ID).order_by(Question.id).all()
        questions = paginate_questions(request,selection)

        if len(questions)==0:
            abort(404)
      
        return jsonify({
          'success':True,
          'current_category':current_category,
          'questions':questions,
          'total_questions':len(selection)
        })

    except:
        abort(422)

  @app.route('/questions/<int:qn_id>',methods=['DELETE'])
  def delete_question(id):
    question_id = qn_id

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
        if quiz_category['id'] == 0:
            quiz_question = Question.query.filter(~Question.id.in_(previous_questions)).order_by(func.random()).first()
        else:
            quiz_question = Question.query.filter(Question.category==int(quiz_category['id']),~Question.id.in_(previous_questions)).order_by(func.random()).first()

        if quiz_question is None:
            return jsonify({
              "success":True,
              "question":0
            })

        return jsonify({
          "success":True,
          "question":quiz_question.format()
        })
    except:
        traceback.print_exc()
        abort(422)

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Resource Not Found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable"
      }), 422
  
  return app

    