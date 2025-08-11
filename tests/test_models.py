import unittest
from app import create_app, db
from app.models import User

class UserModelTestDase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_password_hash(self):
        u = User(
            fname = 'John',
            lname = 'Doe',
            email = 'test@email.com'
        )
        u.set_password('cat12345')
        self.assertTrue(u.check_password('cat12345'))
        self.assertFalse(u.check_password('cat12347'))
