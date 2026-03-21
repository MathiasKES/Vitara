from datetime import datetime, timezone
from app import db

class ProgressPicture(db.Model):
    __tablename__ = 'progress_pictures'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('progress_pictures', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<ProgressPicture {self.id} by User {self.user_id}>'
