import unittest
from app import create_app, db
from app.models import User
from flask_login import current_user

class AuthRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_signup(self):
        with self.app.test_client() as client:
            response = client.post('/auth/signup', data={
                'fname': 'Test',
                'lname': 'User',
                'email': 'test@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(User.query.count(), 1)
            user = User.query.first()
            self.assertEqual(user.fname, 'Test')
            self.assertEqual(user.lname, 'User')
            self.assertEqual(user.email, 'test@example.com')
            self.assertTrue(user.check_password('password123'))
    
    def test_login(self):
        user = User(fname='Test', lname='User', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        with self.app.test_client() as client:
            response = client.post('/auth/login', data={
                'email': 'test@example.com',
                'password': 'password123'
            })
            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
