from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Optional

class ProgressPicForm(FlaskForm):
    photo = FileField('Progress Picture', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    caption = StringField('Caption', validators=[Optional()])
    is_public = BooleanField('Share on public feed?')
    submit = SubmitField('Upload')
