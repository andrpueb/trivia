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
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question' : 'how old is the world',
            'answer' : '300000000',
            'difficulty' : '5',
            'category': '4',
            'id' : '34'
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        resp = self.client().get('/categories')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['categories'])

    def test_all_questions(self):
        resp = self.client().get('/questions')
        data = json.loads(resp.data)

        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_all_questions(self):
        resp = self.client().get('/questions')
        data = json.loads(resp.data)

        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_search_question(self):
        resp = self.client().post('/questions', json={'searchTerm':'world'})
        data = json.loads(resp.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_add_question(self):
        resp = self.client().post('/questions', json=self.new_question)
        data = json.loads(resp.data)

        self.assertEqual(data['success'], True)

    def test_delete_question(self):
        question = str(Question.query.first().id)
        resp = self.client().delete('/questions/'+question)
        data = json.loads(resp.data)

        self.assertEqual(data['success'], True)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()