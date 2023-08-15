import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']) > 0)
    
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)
        self.assertTrue(data['categories'])
        self.assertIsNone(data['current_category'])

    def test_delete_question(self):
        question = Question.query.first()
        question_id = question.id if question else 1 

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)
    
    def test_create_question(self):
        new_question = {
            'question': 'Test question',
            'answer': 'Test answer',
            'category': 1,
            'difficulty': 1
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    
    def test_submit_question(self):
        new_question_data = {
            'question': 'What is the capital of Australia?',
            'answer': 'Canberra',
            'category': 3,  
            'difficulty': 2
        }

        # Submit a new question
        res = self.client().post('/questions', json=new_question_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

        created_question_id = data['created']

        #last page
        res = self.client().get('/questions?page=10000')  
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)

        last_question = data['questions'][-1]
        self.assertEqual(last_question['id'], created_question_id)
        self.assertEqual(last_question['question'], new_question_data['question'])
        self.assertEqual(last_question['answer'], new_question_data['answer'])
        self.assertEqual(last_question['category'], new_question_data['category'])
        self.assertEqual(last_question['difficulty'], new_question_data['difficulty'])

    def test_search_questions(self):
        search_phrase = 'title'
        res = self.client().post('/questions/search', json={'searchTerm': search_phrase})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)

        
        for question in data['questions']:
            self.assertIn(search_phrase, question['question'].lower())

    def test_get_questions_by_category(self):
        category_id = 1
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)
        self.assertEqual(data['current_category'], 'Science')

    def test_get_quiz_question(self):
        quiz_data = {
            'previous_questions': [],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        response = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])

    def test_play_quiz(self):
        # Select a category for the quiz (replace with a valid category ID)
        quiz_category = {'id': 2, 'type': 'Art'}

        # Start the quiz and retrieve the first question
        res = self.client().post('/quizzes', json={'quiz_category': quiz_category})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])

        # Simulate answering the question correctly
        correct_answer = data['question']['answer']
        user_answer = correct_answer
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': quiz_category, 'answer': user_answer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(data['correct'])  

        incorrect_answer = 'Incorrect Answer'
        user_answer = incorrect_answer
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': quiz_category, 'answer': user_answer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(data['correct'])  

    def test_error_handlers(self):
        response = self.client().get('/nonexistent_endpoint')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Not found')

        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Missing required data')

        response = self.client().delete('/questions/999')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Question not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()