import os
from flask import Flask, request, abort, jsonify, render_template
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
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
          'response': 200
        })

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
                'categories': formatted_categories
            })
        except BaseException:
            abort(404)

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for three pages.
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
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': len(formatted_questions),
                'categories': formatted_categories
            })
        except BaseException:
            abort(404)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when
    you refresh the page.
    '''

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            Question.query.get(id).delete()
            return jsonify({
                'success': True,
                'id': id
            })
        except BaseException:
            abort(400)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            request_body = request.get_json()
            new_question = request_body.get('question', None)
            new_answer = request_body.get('answer', None)
            new_difficulty = request_body.get('difficulty', None)
            new_category = request_body.get('category', None)
            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category)
            question.insert()
            return jsonify({
                'success': True
            })
        except BaseException:
            abort(400)
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            request_body = request.get_json()
            search_term = request_body['searchTerm']
            questions = Question.query.filter(
                Question.question.ilike(
                    '%' + search_term + '%')).all()
            formatted_questions = [question.format() for question in questions]
            body = {
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions)
            }
            return jsonify(body)
        except BaseException:
            abort(400)

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
            if(len(questions) > 0):
                formatted_questions = [question.format() for question in questions]
                return jsonify({
                    'success': True,
                    'questions': formatted_questions
                })
            else:
                abort(404)
        except BaseException:
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
            body = request.get_json()
            quiz_category = body['quiz_category']['id']
            prev_questions = body['previous_questions']
            if(quiz_category == 0):
                return_body['question'] = random.choice(Question.query.filter(Question.id.notin_(prev_questions)).all()).format()
            else:
                this_cat_questions = Question.query.filter_by(category=quiz_category).all()
                if(len(prev_questions) < len(this_cat_questions)):
                    return_body['question'] = Question.query.filter_by(category=quiz_category).filter(Question.id.notin_(prev_questions)).first().format()
            return jsonify(return_body)
        except BaseException:
            abort(400)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(400)
    def bad_reuqest_error(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Server Error'
        }), 500

    return app
