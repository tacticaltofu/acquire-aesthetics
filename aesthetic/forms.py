from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.widgets.html5 import NumberInput
from aesthetic.models import User

class Register(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={"placeholder":"username"})
    password = PasswordField('password',
                             validators=[DataRequired()],
                             render_kw={"placeholder":"password"})
    confirm_password = PasswordField('confirm password',
                                     validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder":"confirm password"})
    submit = SubmitField('register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Someone already has that name.')

class Login(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('password',
                             validators=[DataRequired()])
    submit = SubmitField('login')


class ChangeUsername(FlaskForm):
    new_username = StringField('new username',
                           validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={"placeholder":"new username"})
    password = PasswordField('password',
                             validators=[DataRequired()],
                             render_kw={"placeholder":"password"})
    submit = SubmitField('change username')

    def validate_new_username(self, new_username):
        if new_username.data != current_user.username:
            if User.query.filter_by(username=new_username.data).first():
                raise ValidationError('Someone already has that name.')

class ChangePassword(FlaskForm):
    current_password = PasswordField('current password',
                             validators=[DataRequired()],
                             render_kw={"placeholder":"current password"})
    new_password = PasswordField('new password',
                             validators=[DataRequired()],
                             render_kw={"placeholder":"new password"})
    confirm_new_password = PasswordField('new password again',
                                     validators=[DataRequired(), EqualTo('new_password')],
                                     render_kw={"placeholder":"new password again"})
    submit = SubmitField('change password')

class ChangeProfilePic(FlaskForm):
    picture = FileField('choose profile picture',
                        validators=[FileAllowed(['jpg', 'png', 'gif'], 'jpg, png, gif only')])
    submit = SubmitField('submit')

class UpdateProfileInfo(FlaskForm):
    about_me = TextAreaField('about me', validators=[DataRequired()],
                            render_kw={"placeholder":"Some more information..."})
    update_info = SubmitField('update info')

class CreatePost(FlaskForm):
    title = StringField('title', validators=[DataRequired()],
                        render_kw={"placeholder":"title"})
    content = TextAreaField('content', validators=[DataRequired()],
                            render_kw={"placeholder":"content"})
    submit = SubmitField('submit')

class CreateMeasurement(FlaskForm):
    neck = DecimalField('neck', validators=[DataRequired()], render_kw={"placeholder":"neck"}, widget=NumberInput(step=0.1))
    shoulders = DecimalField('shoulders', validators=[DataRequired()], render_kw={"placeholder":"shoulders"}, widget=NumberInput(step=0.1))
    biceps = DecimalField('biceps', validators=[DataRequired()], render_kw={"placeholder":"biceps"}, widget=NumberInput(step=0.1))
    chest = DecimalField('chest', validators=[DataRequired()], render_kw={"placeholder":"chest"}, widget=NumberInput(step=0.1))
    waist = DecimalField('waist', validators=[DataRequired()], render_kw={"placeholder":"waist"}, widget=NumberInput(step=0.1))
    hips = DecimalField('hips', validators=[DataRequired()], render_kw={"placeholder":"hips"}, widget=NumberInput(step=0.1))
    thigh = DecimalField('thigh', validators=[DataRequired()], render_kw={"placeholder":"thigh"}, widget=NumberInput(step=0.1))
    calf = DecimalField('calf', validators=[DataRequired()], render_kw={"placeholder":"calf"}, widget=NumberInput(step=0.1))
    submit = SubmitField('record')
