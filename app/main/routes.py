import os
import secrets
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('social.feed'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    from app.models.progress import ProgressPicture
    my_pics = ProgressPicture.query.filter_by(user_id=current_user.id).order_by(ProgressPicture.created_at.desc()).all()
    return render_template('main/dashboard.html', my_pics=my_pics)

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '':
                random_hex = secrets.token_hex(8)
                _, f_ext = os.path.splitext(file.filename)
                picture_fn = random_hex + f_ext
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, picture_fn))
                current_user.profile_pic_path = picture_fn
                db.session.commit()
                flash('Profile picture updated.', 'success')
        
        display_name = request.form.get('display_name')
        if display_name:
            current_user.display_name = display_name
            db.session.commit()
            flash('Profile details updated.', 'success')
            
        return redirect(url_for('main.profile'))
        
    return render_template('main/profile.html')
