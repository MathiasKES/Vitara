from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired
from datetime import date

class JournalEntryForm(FlaskForm):
    title = StringField('Title (Optional)')
    # Body handled via Quill JS on frontend
    body = StringField('Body', validators=[DataRequired()])
    mood = SelectField('Mood', choices=[
        ('great', '😊 Great'),
        ('good', '🙂 Good'),
        ('neutral', '😐 Neutral'),
        ('low', '😔 Low'),
        ('hard', '😞 Hard')
    ], validators=[DataRequired()])
    entry_date = DateField('Date', default=date.today, validators=[DataRequired()])
    submit = SubmitField('Save Entry')
