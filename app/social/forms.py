from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, BooleanField, SubmitField, MultipleFileField, SelectMultipleField
from wtforms.validators import Optional

class PostForm(FlaskForm):
    media = MultipleFileField('Upload Images/Videos', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg', 'mp4', 'mov'], 'Images and Videos only!')
    ])
    caption = StringField('Caption', validators=[Optional()])
    is_public = BooleanField('Share on public feed?')
    workouts = SelectMultipleField('Attach Workouts', coerce=int, validators=[Optional()])
    submit = SubmitField('Post')

class PostEditForm(FlaskForm):
    caption = StringField('Caption', validators=[Optional()])
    is_public = BooleanField('Share on public feed?')
    workouts = SelectMultipleField('Attach Workouts', coerce=int, validators=[Optional()])
    submit = SubmitField('Update Post')

