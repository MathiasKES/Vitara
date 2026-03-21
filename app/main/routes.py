import os
import secrets
from datetime import date, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User

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
    from app.models.fitness import Workout
    
    my_pics = ProgressPicture.query.filter_by(user_id=current_user.id).order_by(ProgressPicture.created_at.desc()).all()
    
    seven_days_ago = date.today() - timedelta(days=7)
    recent_workouts = Workout.query.filter_by(user_id=current_user.id).filter(Workout.workout_date >= seven_days_ago).count()
    
    return render_template('main/dashboard.html', my_pics=my_pics, recent_workouts=recent_workouts)

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
        email = request.form.get('email')
        theme = request.form.get('theme')
        units = request.form.get('units')

        if email and email != current_user.email:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email address is already in use.', 'danger')
            else:
                current_user.email = email
                db.session.commit()
                flash('Email updated.', 'success')
        
        if display_name:
            current_user.display_name = display_name
        if theme:
            current_user.theme = theme
        if units:
            current_user.units = units
            
        db.session.commit()
        flash('Profile settings updated.', 'success')
            
        return redirect(url_for('main.profile'))
        
    return render_template('main/profile.html')

@main_bp.route('/profile/remove_pic', methods=['POST'])
@login_required
def remove_profile_pic():
    if current_user.profile_pic_path:
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads', current_user.profile_pic_path)
        if os.path.exists(upload_path):
            os.remove(upload_path)
        current_user.profile_pic_path = None
        db.session.commit()
        flash('Profile picture removed.', 'success')
    return redirect(url_for('main.profile'))
