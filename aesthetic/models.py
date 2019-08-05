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

def populate_db():
    filler = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    
    admin = User(username='admin', password=bcrypt.generate_password_hash('admin').decode('utf-8'))
    bob = User(username='bob', password=bcrypt.generate_password_hash('123').decode('utf-8'))
    test = User(username='tester', password=bcrypt.generate_password_hash('password').decode('utf-8'))

    admin_1 = Post(title='rezero', content='<img src="https://i.imgur.com/Y1eFs13.png" width="560px">', author=admin)
    admin_2 = Post(title='hannibal for king', content='<iframe width="560" height="315" src="https://www.youtube.com/embed/A2F51rFYSfo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen=""></iframe>', author=admin, date_posted=datetime.today()-timedelta(days=1))
    admin_3 = Post(title='How to get 15 inch arms from bodyweight only', content='3 sets of 8m 20kg weighted chin ups\n 3 sets of 8 dips', author=admin, date_posted=datetime.today()-timedelta(days=2))
    admin_4 = Post(title='have you seen alien?', content='no i habe not seen alien', author=admin, date_posted=datetime.today()-timedelta(days=3))
    admin_5 = Post(title='stop snitching', content='bitch nigga snitch nigga hoe nigga bitch nigga bitch nigga snitch nigga hoe nigga bitch nigga me and bitch niggas we dont conversate!', author=admin, date_posted=datetime.today()-timedelta(days=5))

    bob_1 = Post(title='Triceps vs Biceps vs Forearms: Which contributes the most to arm size?', content=filler, author=bob)
    bob_2 = Post(title='how to gain mass', content=filler, author=bob, date_posted=datetime.today()-timedelta(days=3))
    bob_3 = Post(title='how to heal from bulging disc', content=filler, author=bob, date_posted=datetime.today()-timedelta(days=5))
    bob_4 = Post(title='shoulder rehab protocol', content=filler, author=bob, date_posted=datetime.today()-timedelta(days=6))

    test_1 = Post(title='riley reid vs sasha grey', content=filler, author=test, date_posted=datetime.today()-timedelta(days=1))
    test_2 = Post(title='potato salad', content=filler, author=test, date_posted=datetime.today()-timedelta(days=2))
    test_3 = Post(title='reps for jesus', content=filler, author=test, date_posted=datetime.today()-timedelta(days=3))
    

    db.session.add(admin)
    db.session.add(admin_1)
    db.session.add(admin_2)
    db.session.add(admin_3)
    db.session.add(admin_4)
    db.session.add(admin_5)

    db.session.add(bob)
    db.session.add(bob_1)
    db.session.add(bob_2)
    db.session.add(bob_3)
    db.session.add(bob_4)

    db.session.add(test)
    db.session.add(test_1)
    db.session.add(test_2)
    db.session.add(test_3)

    db.session.commit()


def ghetto_migrate():
    from aesthetic import create_app
    app = create_app()
    with app.app_context():
        init_db()
        populate_db()