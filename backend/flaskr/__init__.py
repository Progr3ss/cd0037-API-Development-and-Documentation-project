import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import Question, Category
from models import setup_db

QUESTIONS_PER_PAGE = 10

db = SQLAlchemy()
def setup_db(app):
    # Move the database setup code here

    with app.app_context():
        database_name = 'trivia'
        database_path = 'postgresql://{}/{}'.format('localhost:5432', database_name)
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        db.create_all()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories',methods=['GET'])
    def get_categories():
          
          try:
            categories = Category.query.all()
            category_list = [category.format() for category in categories]

            return jsonify({
                'success': True,
                'categories': category_list
            })
          except Exception as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'An error occurred while processing your request.'
            })
          


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]
            total_questions = len(formatted_questions)

            categories = Category.query.all()
            formatted_categories = {category.id: category.type for category in categories}

            return jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': total_questions,
                'categories': formatted_categories,
                'current_category': None
            })
        except Exception as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'An error occurred while processing your request.'
            })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                return jsonify({
                    'success': False,
                    'error': 'Question not found'
                }), 404
            
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'An error occurred while processing your request.'
            })


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            data = request.get_json()
            question_text = data.get('question', None)
            answer_text = data.get('answer', None)
            category_id = data.get('category', None)
            difficulty = data.get('difficulty', None)

            if not question_text or not answer_text or category_id is None or difficulty is None:
                return jsonify({
                    'success': False,
                    'error': 'Missing required data'
                }), 400
            category = Category.query.get(category_id)
            if category is None:
                return jsonify({
                    'success': False,
                    'error': 'Category not found'
                }), 404

            new_question = Question(
                question=question_text,
                answer=answer_text,
                category=category_id,
                difficulty=difficulty
            )
            new_question.insert()

            return jsonify({
                'success': True,
                'created': new_question.id
            })
        except Exception as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'An error occurred while processing your request.'
            })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
            
        try:
            data = request.get_json()
            search_term = data.get('searchTerm', '')

            if not search_term:
                return jsonify({
                    'success': False,
                    'error': 'Missing search term'
                }), 400

            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': None
            })
        except Exception as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'An error occurred while processing your request.'
            })


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)
            if category is None:
                return jsonify({
                    'success': False,
                    'error': 'Category not found'
                }), 404

            questions = Question.query.filter_by(category=category_id).all()
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': category.type
            })
        except Exception as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'An error occurred while processing your request.'
            })

    

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        try:
            data = request.get_json()
            previous_questions = data.get('previous_questions', [])
            category_id = data.get('quiz_category', None)

            if category_id is None:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter_by(category=category_id).filter(Question.id.notin_(previous_questions)).all()

            if questions:
                random_question = random.choice(questions).format()
            else:
                random_question = None

            return jsonify({
                'success': True,
                'question': random_question
            })
        except Exception as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'An error occurred while processing your request.'
            })


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

