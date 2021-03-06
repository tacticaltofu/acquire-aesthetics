from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from aesthetic import db, bcrypt
from aesthetic.models import User, Post, Measurement, Comment, Goal
from aesthetic.users.forms import Register, Login, ChangeUsername, ChangePassword, ChangeProfilePic, UpdateProfileInfo, CreateMeasurement
from aesthetic.users.utils import save_picture

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Register()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Sorry, I don\'t recognize you.', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    measurements = Measurement.query.filter_by(author=user).all()
    if measurements:
        measurement = measurements[-1]
        history = measurements[::-1]
    else:
        measurement = None
        history = None

    goals = Goal.query.filter_by(author=user).all()
    if goals:
        goal = goals[-1]
    else:
        goal = None
    
    form = ChangeProfilePic()
    info_form = UpdateProfileInfo()
    measure_form = CreateMeasurement()
    
    if form.validate_on_submit() and form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.image_file = picture_file
        db.session.commit()
        flash('Profile picture changed!', 'success')

    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    
    if info_form.validate_on_submit() and info_form.about_me.data:
        current_user.about_me = info_form.about_me.data
        db.session.commit()
        flash('Personal information updated!', 'success')
        
    info_form.about_me.data = user.about_me

    if measure_form.validate_on_submit():
        measure = Measurement(neck=measure_form.neck.data,
                              shoulders=measure_form.shoulders.data,
                              biceps=measure_form.biceps.data,
                              chest=measure_form.chest.data,
                              waist=measure_form.waist.data,
                              hips=measure_form.hips.data,
                              thigh=measure_form.thigh.data,
                              calf=measure_form.calf.data,
                              author=current_user)
        db.session.add(measure)
        db.session.commit()
        flash('Measurements recorded!', 'success')
        return redirect(url_for('users.profile', username=current_user.username))
    return render_template('profile.html', title=user.username + '\'s profile', image_file=image_file, form=form, info_form=info_form, user=user, measure_form=measure_form, measurement=measurement, history=history, goal=goal)

@users.route("/set_goals", methods=['GET', 'POST'])
@login_required
def set_goals():
    form = CreateMeasurement()
    if form.validate_on_submit():
        goal = Goal(neck=form.neck.data,
                      shoulders=form.shoulders.data,
                      biceps=form.biceps.data,
                      chest=form.chest.data,
                      waist=form.waist.data,
                      hips=form.hips.data,
                      thigh=form.thigh.data,
                      calf=form.calf.data,
                      author=current_user)
        db.session.add(goal)
        db.session.commit()
        flash('Goals set!', 'success')
        return redirect(url_for('users.profile', username=current_user.username))
    return render_template('set_goals.html', title='Set Goals', form=form)

@users.route("/profile/<username>/posts")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    title = user.username + '\'s posts'
    return render_template('user_posts.html', posts=posts, title=title, user=user)

@users.route("/profile/<username>/comments")
def user_comments(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    comments = Comment.query.filter_by(author=user).order_by(Comment.date_posted.desc()).paginate(page=page, per_page=5)
    title = user.username + '\'s comments'
    return render_template('user_comments.html', comments=comments, title=title, user=user)

@users.route("/change_username", methods=['GET', 'POST'])
@login_required
def change_username():
    change_username_form = ChangeUsername()
    if change_username_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, change_username_form.password.data):
            current_user.username = change_username_form.new_username.data
            db.session.commit()
            flash('Your username has been changed!', 'success')
            return redirect(url_for('users.profile', username=current_user.username))
        else:
            flash('The password is incorrect.', 'danger')
    return render_template('change_username.html', title='Change Username', change_username_form=change_username_form)

@users.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    change_password_form = ChangePassword()
    if change_password_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, change_password_form.current_password.data):
            hashed_pw = bcrypt.generate_password_hash(change_password_form.new_password.data).decode('utf-8')
            current_user.password = hashed_pw
            db.session.commit()
            flash('Your password has been changed!', 'success')
            return redirect(url_for('users.profile', username=current_user.username))
        else:
            flash('The current password is incorrect.', 'danger')
    return render_template('change_password.html', title='Change Password', change_password_form=change_password_form)
