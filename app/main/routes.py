from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

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
