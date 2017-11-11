from app import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128), unique=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_active():
        """Check the user whether pass the activation process."""
        return True

    def get_id(self):
        """Get the user's uuid from database."""
        return id

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return e
        finally:
            return True


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(128), unique=True)
    status = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, todo):
        self.todo = todo

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return e
        finally:
            return True

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return e
        finally:
            return True

    def __str(self):
        return '<User %r>' % (self.id)
