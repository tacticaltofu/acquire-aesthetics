import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from aesthetic import app, db, bcrypt
from aesthetic.forms import Register, Login, ChangeUsername, ChangePassword, ChangeProfilePic, CreatePost, UpdateProfileInfo, CreateMeasurement, CreateComment
from aesthetic.models import User, Post, Measurement, Comment, Goal

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Register()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Sorry, I don\'t recognize you.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, extension = os.path.splitext(picture.filename)
    filename = random_hex + extension
    path = os.path.join(app.root_path, 'static/profile_pics', filename)
    picture.save(path)
    return filename

@app.route("/profile/<username>", methods=['GET', 'POST'])
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
        return redirect(url_for('profile', username=current_user.username))
    return render_template('profile.html', title=user.username + '\'s profile', image_file=image_file, form=form, info_form=info_form, user=user, measure_form=measure_form, measurement=measurement, history=history, goal=goal)

"""
@app.route("/profile/<username>")
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, user=user)
"""

@app.route("/set_goals", methods=['GET', 'POST'])
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
        return redirect(url_for('profile', username=current_user.username))
    return render_template('set_goals.html', title='Set Goals', form=form)

@app.route("/profile/<username>/posts")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    title = user.username + '\'s posts'
    return render_template('user_posts.html', posts=posts, title=title, user=user)

@app.route("/profile/<username>/comments")
def user_comments(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    comments = Comment.query.filter_by(author=user).order_by(Comment.date_posted.desc()).paginate(page=page, per_page=5)
    title = user.username + '\'s comments'
    return render_template('user_comments.html', comments=comments, title=title, user=user)

@app.route("/change_username", methods=['GET', 'POST'])
@login_required
def change_username():
    change_username_form = ChangeUsername()
    if change_username_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, change_username_form.password.data):
            current_user.username = change_username_form.new_username.data
            db.session.commit()
            flash('Your username has been changed!', 'success')
            return redirect(url_for('profile', username=current_user.username))
        else:
            flash('The password is incorrect.', 'danger')
    return render_template('change_username.html', title='Change Username', change_username_form=change_username_form)

@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    change_password_form = ChangePassword()
    if change_password_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, change_password_form.current_password.data):
            hashed_pw = bcrypt.generate_password_hash(change_password_form.new_password.data).decode('utf-8')
            current_user.password = hashed_pw
            db.session.commit()
            flash('Your password has been changed!', 'success')
            return redirect(url_for('profile', username=current_user.username))
        else:
            flash('The current password is incorrect.', 'danger')
    return render_template('change_password.html', title='Change Password', change_password_form=change_password_form)

@app.route("/post/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='Create Post', form=form)
    
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(parent=post)
    form = CreateComment()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, parent=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted!', 'success')
        return redirect(url_for('post', post_id=post.id))
    return render_template('post.html', title=post.title, post=post, form=form, comments=comments[::-1])

@app.route("/post/<int:post_id>/update_post", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = CreatePost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form)

@app.route("/post/<int:post_id>/delete_post", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('home'))
