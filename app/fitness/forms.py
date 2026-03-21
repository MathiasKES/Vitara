from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FloatField, TextAreaField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired, Optional
from datetime import date

class WorkoutForm(FlaskForm):
    workout_type = SelectField('Workout Type', choices=[
        ('Strength', 'Strength'),
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Swimming', 'Swimming'),
        ('Yoga', 'Yoga'),
        ('Walking', 'Walking'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    workout_date = DateField('Date', default=date.today, validators=[DataRequired()])
    workout_time = TimeField('Time', validators=[Optional()])
    duration_mins = IntegerField('Duration (minutes)', validators=[Optional()])
    distance = FloatField('Distance', validators=[Optional()])
    calories = IntegerField('Calories Burned', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Log Workout')
