from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        flash('You do not have permission to access that page.', 'danger')
        return redirect(url_for('main.dashboard'))

@admin_bp.route('/admin')
def dashboard():
    pending_users = User.query.filter_by(is_approved=False).all()
    approved_users = User.query.filter_by(is_approved=True).all()
    return render_template('admin/dashboard.html', pending_users=pending_users, approved_users=approved_users)

@admin_bp.route('/admin/approve/<int:user_id>', methods=['POST'])
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash(f'User {user.email} has been approved.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/reject/<int:user_id>', methods=['POST'])
def reject_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.email} request rejected and deleted.', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    email = user.email
    db.session.delete(user)
    db.session.commit()
    flash(f'Account for {email} has been permanently deleted.', 'info')
    return redirect(url_for('admin.dashboard'))
