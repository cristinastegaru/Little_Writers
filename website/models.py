from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))
    genre= db.Column(db.String(100))
    project_type= db.Column(db.String(100))
    description= db.Column(db.String(1000))
    date= db.Column(db.DateTime(timezone=True),default=func.now())
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(10000))
    project= db.Column(db.String(100))
    date= db.Column(db.DateTime(timezone=True),default=func.now())
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name= db.Column(db.String(150))
    username= db.Column(db.String(150))
    password= db.Column(db.String(150))
    projects= db.relationship('Project')
    notes= db.relationship('Note')


