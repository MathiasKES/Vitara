from datetime import datetime, timezone
from app import db

post_workouts = db.Table('post_workouts',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('workout_id', db.Integer, db.ForeignKey('workouts.id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    caption = db.Column(db.Text)
    visibility = db.Column(db.String(20), default='private', nullable=False) # 'public', 'followers', 'private'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('posts', lazy='dynamic', cascade="all, delete-orphan"))
    workouts = db.relationship('Workout', secondary=post_workouts, lazy='subquery',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.id} by User {self.user_id}>'

class PostMedia(db.Model):
    __tablename__ = 'post_media'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    media_type = db.Column(db.String(20), default='image') # 'image', 'video'
    order_index = db.Column(db.Integer, default=0)

    post = db.relationship('Post', backref=db.backref('media', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<PostMedia {self.id} for Post {self.post_id}>'
