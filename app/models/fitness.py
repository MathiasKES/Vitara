from datetime import datetime, timezone, date
from app import db

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_type = db.Column(db.String(50), nullable=False) # 'Running', 'Strength', 'Cycling', etc.
    workout_date = db.Column(db.Date, nullable=False, default=date.today)
    duration_mins = db.Column(db.Integer)
    calories = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('workouts', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<Workout {self.workout_type} on {self.workout_date} by User {self.user_id}>'

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)

    workout = db.relationship('Workout', backref=db.backref('exercises', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<Exercise {self.name} for Workout {self.workout_id}>'
