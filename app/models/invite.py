from app import db
from datetime import datetime, timezone, timedelta
import secrets

class InviteToken(db.Model):
    __tablename__ = 'invite_tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False, default=lambda: secrets.token_urlsafe(16))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=2))

    creator = db.relationship('User', backref=db.backref('invites', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<InviteToken {self.token} from User {self.creator_id}>'
