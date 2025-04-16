from datetime import datetime
from app import app
from models import db, Message

class TestApp:
    '''Flask application in app.py'''

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
        '''Check if the message model has correct columns'''
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

    def test_creates_new_message_in_the_database(self):
        '''Creates a new message in the database'''
        with app.app_context():
            app.test_client().post(
                '/messages',
                json={
                    "body": "Hello 👋",
                    "username": "Liza",
                }
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()

    def test_deletes_message_from_database(self):
        '''Deletes the message from the database.'''
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )

            db.session.add(hello_from_liza)
            db.session.commit()

            app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(not h)
