from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from app import db
from app.auth.forms import LoginForm, RegisterForm
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
        if not user.is_approved:
            flash('Your account is still pending admin approval.', 'warning')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        is_auto_approved = False
        invite_token_str = request.args.get('invite')
        if invite_token_str:
            from app.models.invite import InviteToken
            from datetime import datetime
            invite = InviteToken.query.filter_by(token=invite_token_str, is_used=False).first()
            if invite and invite.expires_at > datetime.utcnow():
                is_auto_approved = True
                invite.is_used = True

        user = User(email=form.email.data, display_name=form.display_name.data)
        user.set_password(form.password.data)
        user.is_approved = is_auto_approved
        db.session.add(user)
        db.session.commit()
        
        if not is_auto_approved:
            admins = User.query.filter_by(is_admin=True, allows_admin_emails=True).all()
            for admin in admins:
                print(f"MOCK EMAIL TO {admin.email}: New user '{user.display_name}' ({user.email}) requests access.", flush=True)
            return redirect(url_for('auth.pending'))
            
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/pending')
def pending():
    return render_template('auth/pending.html')
