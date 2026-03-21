import os
import secrets
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.progress import ProgressPicture
from app.social.forms import ProgressPicForm

social_bp = Blueprint('social', __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Ensure upload dir exists
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_path, exist_ok=True)
    picture_path = os.path.join(upload_path, picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@social_bp.route('/feed')
@login_required
def feed():
    # Show public progress pictures from all users
    pictures = ProgressPicture.query.filter_by(is_public=True).order_by(ProgressPicture.created_at.desc()).all()
    return render_template('social/feed.html', pictures=pictures)

@social_bp.route('/progress/upload', methods=['GET', 'POST'])
@login_required
def upload_pic():
    form = ProgressPicForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.photo.data)
        pic = ProgressPicture(
            user_id=current_user.id,
            image_path=picture_file,
            caption=form.caption.data,
            is_public=form.is_public.data
        )
        db.session.add(pic)
        db.session.commit()
        flash('Progress picture uploaded successfully!', 'success')
        if pic.is_public:
            return redirect(url_for('social.feed'))
        else:
            return redirect(url_for('main.dashboard'))
    return render_template('social/upload.html', form=form)
