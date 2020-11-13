from project.main import app
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), unique = True, nullable=False)

    def __repr__(self):
        return self.username
