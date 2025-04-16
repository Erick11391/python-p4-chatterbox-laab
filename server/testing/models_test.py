from datetime import datetime
from app import app
from models import db, Message

class TestMessage:
    '''Message model in models.py'''

    def setup_method(self):
        '''Ensure the database is clean before tests.'''
        with app.app_context():
            # Clean up any messages before tests run
            m = Message.query.filter(
                Message.body == "Hello 👋"
            ).filter(Message.username == "Liza")
            for message in m:
                db.session.delete(message)
            db.session.commit()

    def test_has_correct_columns(self):
        '''Test if Message model has correct columns.'''
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()
