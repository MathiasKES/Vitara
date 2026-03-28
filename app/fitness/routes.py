from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.fitness import Workout, Exercise
from app.fitness.forms import WorkoutForm
import difflib

fitness_bp = Blueprint('fitness', __name__)

def calculate_calories(workout, current_user):
    MET_VALUES = {
        'Strength': 5.0,
        'Running': 8.0,
        'Cycling': 7.5,
        'Swimming': 7.0,
        'Yoga': 3.0,
        'Walking': 3.5,
        'Other': 5.0
    }
    
    user_weight = current_user.weight or 70.0
    # ensure weight is in kg for calculation
    if current_user.units == 'imperial' and current_user.weight:
        user_weight = current_user.weight / 2.20462
        
    duration = workout.duration_mins or 60
    time_hours = duration / 60.0
    
    met = MET_VALUES.get(workout.workout_type, 5.0)
    
    if workout.workout_type == 'Strength':
        heavy_exercises = ['squat', 'deadlift', 'bench press', 'clean', 'snatch', 'leg press', 'pull up']
        heavy_count = 0
        for ex in workout.exercises:
            name_lower = ex.name.lower()
            matches = difflib.get_close_matches(name_lower, heavy_exercises, n=1, cutoff=0.6)
            if matches:
                heavy_count += 1
        # Boost MET for big compound movements
        met = min(8.5, met + (heavy_count * 0.5))
        
    if current_user.fitness_level == 'beginner':
        met *= 0.95
    elif current_user.fitness_level == 'advanced':
        met *= 1.1

    return int(met * user_weight * time_hours)

@fitness_bp.route('/fitness')
@login_required
def index():
    sort_order = request.args.get('sort', 'newest')
    if sort_order == 'oldest':
        workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.workout_date.asc(), Workout.workout_time.asc()).all()
    else:
        workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.workout_date.desc(), Workout.workout_time.desc()).all()
    return render_template('fitness/index.html', workouts=workouts, current_sort=sort_order)

def process_exercises(workout):
    # Remove existing
    for ex in workout.exercises:
        db.session.delete(ex)
        
    exercise_names = request.form.getlist('exercise_name[]')
    exercise_sets = request.form.getlist('exercise_sets[]')
    exercise_reps = request.form.getlist('exercise_reps[]')
    exercise_weight = request.form.getlist('exercise_weight[]')
    exercise_types = request.form.getlist('exercise_set_type[]')
    
    for i in range(len(exercise_names)):
        if exercise_names[i].strip():
            try:
                sets_val = int(exercise_sets[i]) if exercise_sets[i] else None
                reps_val = int(exercise_reps[i]) if exercise_reps[i] else None
                weight_val = str(exercise_weight[i]).strip() if exercise_weight[i] else None
                set_type_val = exercise_types[i] if i < len(exercise_types) and exercise_types[i] else 'normal'

                ex = Exercise(
                    workout_id=workout.id,
                    name=exercise_names[i].strip(),
                    sets=sets_val,
                    reps=reps_val,
                    weight=weight_val,
                    set_type=set_type_val,
                    order_index=i
                )
                db.session.add(ex)
            except ValueError:
                continue

@fitness_bp.route('/fitness/log', methods=['GET', 'POST'])
@login_required
def log_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        distance_val = form.distance.data
        if distance_val is not None and current_user.units == 'imperial':
            distance_val = round(distance_val / 0.621371, 2)
            
        workout = Workout(
            user_id=current_user.id,
            workout_type=form.workout_type.data,
            workout_date=form.workout_date.data,
            workout_time=form.workout_time.data,
            duration_mins=form.duration_mins.data,
            distance=distance_val,
            notes=form.notes.data
        )
        db.session.add(workout)
        db.session.flush()

        process_exercises(workout)
        db.session.flush() # ensure exercises are attached for calorie calc

        if form.calories.data:
            workout.calories = form.calories.data
        else:
            workout.calories = calculate_calories(workout, current_user)
            
        db.session.commit()
        flash('Workout logged successfully!', 'success')
        return redirect(url_for('fitness.index'))
    return render_template('fitness/log.html', form=form)

@fitness_bp.route('/fitness/edit/<int:workout_id>', methods=['GET', 'POST'])
@login_required
def edit_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('fitness.index'))
        
    form = WorkoutForm(obj=workout)
    
    if form.validate_on_submit():
        distance_val = form.distance.data
        if distance_val is not None and current_user.units == 'imperial':
            distance_val = round(distance_val / 0.621371, 2)
            
        workout.workout_type = form.workout_type.data
        workout.workout_date = form.workout_date.data
        workout.workout_time = form.workout_time.data
        workout.duration_mins = form.duration_mins.data
        workout.distance = distance_val
        workout.notes = form.notes.data
        
        process_exercises(workout)
        db.session.flush()

        if form.calories.data:
            workout.calories = form.calories.data
        else:
            workout.calories = calculate_calories(workout, current_user)
            
        db.session.commit()
        flash('Workout updated successfully!', 'success')
        return redirect(url_for('fitness.index'))
        
    elif request.method == 'GET':
        if workout.distance is not None and current_user.units == 'imperial':
            form.distance.data = round(workout.distance * 0.621371, 2)
    
    return render_template('fitness/edit.html', form=form, workout=workout)

@fitness_bp.route('/fitness/delete/<int:workout_id>', methods=['POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('fitness.index'))
    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted.', 'success')
    return redirect(url_for('fitness.index'))

@fitness_bp.route('/fitness/stats')
@login_required
def stats():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.workout_date.asc()).all()
    exercises = Exercise.query.join(Workout).filter(Workout.user_id == current_user.id).all()
    prs = {}
    for ex in exercises:
        # Since weight is now a string, try resolving to float for PR calculation
        try:
            wt = float(ex.weight) if ex.weight else None
            if wt is not None:
                if ex.name not in prs or wt > float(prs[ex.name]):
                    prs[ex.name] = str(wt)
        except ValueError:
            pass # ignore string weights like "max" for PR numerical charts
                
    return render_template('fitness/stats.html', workouts=workouts, prs=prs)
