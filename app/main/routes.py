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
    from app.models.post import Post
    from app.models.fitness import Workout
    from app.models.journal import JournalEntry
    from datetime import date, timedelta, datetime
    
    my_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).all()
    
    seven_days_ago = date.today() - timedelta(days=7)
    recent_workouts = Workout.query.filter_by(user_id=current_user.id).filter(Workout.workout_date >= seven_days_ago).count()
    
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    journal_today = JournalEntry.query.filter_by(user_id=current_user.id).filter(JournalEntry.created_at >= start_of_day).count()
    
    return render_template('main/dashboard.html', my_posts=my_posts, recent_workouts=recent_workouts, journal_today=journal_today)

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
        weight = request.form.get('weight')
        height = request.form.get('height')
        gender = request.form.get('gender')
        fitness_level = request.form.get('fitness_level')

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
        if weight:
            current_user.weight = float(weight)
        if height:
            current_user.height = float(height)
        if gender:
            current_user.gender = gender
        if fitness_level:
            current_user.fitness_level = fitness_level
            
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

@main_bp.route('/profile/invite', methods=['POST'])
@login_required
def generate_invite():
    from app.models.invite import InviteToken
    new_invite = InviteToken(creator_id=current_user.id)
    db.session.add(new_invite)
    db.session.commit()
    invite_url = url_for('auth.register', invite=new_invite.token, _external=True)
    flash(f'Your friend invitation link: {invite_url}', 'success')
    return redirect(url_for('main.profile'))

@main_bp.route('/export', methods=['GET'])
@login_required
def export_data():
    import json
    from flask import Response
    from app.models.fitness import Workout
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    data = {'workouts': []}
    for w in workouts:
        w_data = {
            'type': w.workout_type,
            'date': w.workout_date.isoformat() if w.workout_date else None,
            'time': w.workout_time.isoformat() if w.workout_time else None,
            'duration': w.duration_mins,
            'distance': w.distance,
            'calories': w.calories,
            'notes': w.notes,
            'exercises': []
        }
        for ex in w.exercises:
            w_data['exercises'].append({
                'name': ex.name,
                'sets': ex.sets,
                'reps': ex.reps,
                'weight': ex.weight,
                'set_type': ex.set_type,
                'order_index': ex.order_index
            })
        data['workouts'].append(w_data)
        
    json_data = json.dumps(data, indent=2)
    response = Response(json_data, mimetype='application/json')
    response.headers['Content-Disposition'] = 'attachment; filename=vitara_export.json'
    return response

@main_bp.route('/import', methods=['POST'])
@login_required
def import_data():
    import json
    from app.models.fitness import Workout, Exercise
    if 'data_file' not in request.files:
        flash('No file uploaded', 'danger')
        return redirect(url_for('main.profile'))
        
    file = request.files['data_file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('main.profile'))
        
    try:
        data = json.loads(file.read().decode('utf-8'))
        if 'workouts' in data:
            from datetime import date, time
            for w_data in data['workouts']:
                w_date = date.fromisoformat(w_data['date']) if w_data.get('date') else date.today()
                w_time = time.fromisoformat(w_data['time']) if w_data.get('time') else None
                workout = Workout(
                    user_id=current_user.id,
                    workout_type=w_data.get('type', 'Other'),
                    workout_date=w_date,
                    workout_time=w_time,
                    duration_mins=w_data.get('duration'),
                    distance=w_data.get('distance'),
                    calories=w_data.get('calories'),
                    notes=w_data.get('notes')
                )
                db.session.add(workout)
                db.session.flush()
                
                for ex_data in w_data.get('exercises', []):
                    ex = Exercise(
                        workout_id=workout.id,
                        name=ex_data.get('name', 'Unknown'),
                        sets=ex_data.get('sets'),
                        reps=ex_data.get('reps'),
                        weight=ex_data.get('weight'),
                        set_type=ex_data.get('set_type', 'normal'),
                        order_index=ex_data.get('order_index', 0)
                    )
                    db.session.add(ex)
            db.session.commit()
            flash('Data imported successfully!', 'success')
    except Exception as e:
        flash(f'Error importing data.', 'danger')
        
    return redirect(url_for('main.profile'))

