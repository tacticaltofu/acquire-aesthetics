from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CreatePost(FlaskForm):
    title = StringField('title', validators=[DataRequired()],
                        render_kw={"placeholder":"title"})
    content = TextAreaField('content', validators=[DataRequired()],
                            render_kw={"placeholder":"content"})
    submit = SubmitField('submit')

class CreateComment(FlaskForm):
    content = TextAreaField('content', validators=[DataRequired()],
                            render_kw={"placeholder":"comment"})
    submit = SubmitField('submit')
