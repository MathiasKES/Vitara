from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, BooleanField, SubmitField, MultipleFileField, SelectMultipleField, SelectField
from wtforms.validators import Optional

class PostForm(FlaskForm):
    media = MultipleFileField('Upload Images/Videos', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg', 'mp4', 'mov'], 'Images and Videos only!')
    ])
    caption = StringField('Caption', validators=[Optional()])
    visibility = SelectField('Who can see this?', choices=[
        ('private', 'Private (Only Me)'),
        ('followers', 'Followers Only'),
        ('public', 'Public (Everyone)')
    ], default='private')
    workouts = SelectMultipleField('Attach Workouts', coerce=int, validators=[Optional()])
    submit = SubmitField('Post')

class PostEditForm(FlaskForm):
    caption = StringField('Caption', validators=[Optional()])
    visibility = SelectField('Who can see this?', choices=[
        ('private', 'Private (Only Me)'),
        ('followers', 'Followers Only'),
        ('public', 'Public (Everyone)')
    ], default='private')
    workouts = SelectMultipleField('Attach Workouts', coerce=int, validators=[Optional()])
    submit = SubmitField('Update Post')

