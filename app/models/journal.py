from datetime import datetime, timezone, date
from app import db

class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200))
    body = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(20))
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('journal_entries', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<JournalEntry {self.title or self.id} by User {self.user_id}>'
