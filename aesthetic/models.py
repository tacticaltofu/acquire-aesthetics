from datetime import datetime, date, timedelta
from aesthetic import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    about_me = db.Column(db.Text, nullable=False, default='Some more information...')
    posts = db.relationship('Post', backref='author', lazy=True)
    measurements = db.relationship('Measurement', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    goals = db.relationship('Goal', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='parent', lazy=True)
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

    def __repr__(self):
        return f"Post('{self.date_posted}', '{self.content}')"

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_recorded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    neck = db.Column(db.Numeric)
    shoulders = db.Column(db.Numeric)
    biceps = db.Column(db.Numeric)
    chest = db.Column(db.Numeric)
    waist = db.Column(db.Numeric)
    hips = db.Column(db.Numeric)
    thigh = db.Column(db.Numeric)
    calf = db.Column(db.Numeric)
    body_parts = [neck, shoulders, biceps, chest, waist, hips, thigh, calf]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Measurement('{self.author}', '{self.date_recorded}')"

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_recorded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    neck = db.Column(db.Numeric)
    shoulders = db.Column(db.Numeric)
    biceps = db.Column(db.Numeric)
    chest = db.Column(db.Numeric)
    waist = db.Column(db.Numeric)
    hips = db.Column(db.Numeric)
    thigh = db.Column(db.Numeric)
    calf = db.Column(db.Numeric)
    body_parts = [neck, shoulders, biceps, chest, waist, hips, thigh, calf]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Goal('{self.author}', '{self.date_recorded}')"

def init_db():
    db.drop_all()
    db.create_all()

def ensure_db_exists():
    db.create_all()
