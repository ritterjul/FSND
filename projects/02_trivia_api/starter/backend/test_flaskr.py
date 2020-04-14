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
        self.database_path = "postgresql://juliane:POSTGRES@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_categories_with_results(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']))

    def test_get_questions_default_page(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])

    def test_get_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_question_existing(self):
        # post new question to be deleted
        res = self.client().post('/questions', json={'question': 'New', 'answer': 'New', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)
        # delete new question
        res = self.client().delete('/questions/' + str(data['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_question_not_existing(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_post_question_valid(self):
        # post new question
        res = self.client().post('/questions', json={'question': 'New', 'answer': 'New', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['id'])

        # delete new question
        res = self.client().delete('/questions/' + str(data['id']))

    def test_post_question_non_existing_category(self):
        res = self.client().post('/questions', json={'question': 'New', 'answer': 'New', 'category': 100, 'difficulty': 1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        
    def test_post_question_empty_question(self):
        res = self.client().post('/questions', json={'question': '', 'answer': 'New', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_post_question_empty_anwer(self):
        res = self.client().post('/questions', json={'question': 'New', 'answer': '', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_search_questions_existing_term_default_page(self):
        res = self.client().post('/searchQuestions', json={'searchTerm': 'the'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])

    def test_search_questions_non_existing_term_default_page(self):
        res = self.client().post('/searchQuestions', json={'searchTerm': 'nonexistingterm'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(data['total_questions'])

    def test_search_questions_existing_term_beyond_valid_page(self):
        res = self.client().post('/searchQuestions?page=100', json={'searchTerm': 'the'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_questions_by_category_default_page(self):
        category_id = 1
        res = self.client().get('/categories/' + str(category_id) + '/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], category_id)

    def test_get_questions_by_category_non_existing_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_questions_by_category_beyond_valid_page(self):
        category_id = 1
        res = self.client().get('/categories/' + str(category_id) + '/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_next_question_initial_question(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 0, 'type': 'ALL'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_get_next_question_final_question(self):
        res = self.client().post('/quizzes', json={'previous_questions': [20, 21, 22], 'quiz_category': {'id': 1, 'type': 'Science'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(data['question'])

    def test_get_next_question_non_existing_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 1000, 'type': 'Error'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()