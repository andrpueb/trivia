import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10



def all_categories():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    return formatted_categories

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})


    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response



    @app.route('/', methods=['GET'])
    def index():
      return 'true'

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route('/categories', methods=['GET'])
    def get_all_categories():
      try:
        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
          formatted_categories[category.id] = category.type
        return jsonify({
          'categories' : formatted_categories
          })
      except:
        abort(404)


    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions', methods=['GET'])
    def all_questions():
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      try:
        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]
        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
          formatted_categories[category.id] = category.type
        return jsonify({
          'success' : True,
          'questions' : formatted_questions[start:end],
          'total_questions' : len(formatted_questions),
          'categories' : formatted_categories
        })
      except:
        abort(404)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
      try:
        Question.query.get(id).delete()
        return jsonify({
          'success' : True
        })
      except:
        abort(404)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions', methods=['POST'])
    def search_question():
      try:
        request_body = request.get_json()
        print(request_body)
        if 'searchTerm' in request_body:
          search_term = request_body['searchTerm']
          questions = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
          formatted_questions = [question.format() for question in questions]
          body = {
              'success' : True,
              'questions' : formatted_questions,
              'total_questions' : len(formatted_questions)
          }
          return jsonify(body)
        elif 'question' in request_body:
          new_question = request_body.get('question', None)
          new_answer = request_body.get('answer', None)
          new_difficulty = request_body.get('difficulty', None)
          new_category = request_body.get('category', None)
          question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
          question.insert()
          return jsonify({
            'success' : True
          })
        else:
          new_question = body.get('question', None)
          new_answer = body.get('answer', None)
          new_difficulty = body.get('difficulty', None)
          new_category = body.get('category', None)
          question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
          question.insert()
          body = {
            'success' : True,
          }
          return jsonify(body)
      except:
        abort(404)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:cat>/questions', methods=['GET'])
    def get_category(cat):
      try:
          questions = Question.query.filter_by(category=cat).all()
          formatted_questions = [question.format() for question in questions]
          return jsonify({
            'success': True,
            'questions' : formatted_questions
          })
      except:
        abort(404)

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


    @app.route('/quizzes', methods=['POST'])
    def next_question():
      try:
        return_body = {}
        quiz_questions = []
        body = request.get_json()
        quiz_category = body['quiz_category']['id']
        prev_questions = body['previous_questions']
        if(quiz_category == 0):
          quiz_questions = Question.query.all()
          print(quiz_questions)
        else:
          quiz_questions = Question.query.filter_by(category=quiz_category).all()
        question_id = [question.id for question in quiz_questions]
        not_answered = list(set(question_id) - set(prev_questions))
        next_question = {}
        if len(not_answered) > 0:
          next_question = Question.query.get(random.choice(not_answered)).format()
          return_body['question'] = next_question
        return jsonify(return_body)
      except:
        abort(404)


    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    return app

