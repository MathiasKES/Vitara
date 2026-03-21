from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.fitness import Workout, Exercise
from app.fitness.forms import WorkoutForm

fitness_bp = Blueprint('fitness', __name__)

@fitness_bp.route('/fitness')
@login_required
def index():
    sort_order = request.args.get('sort', 'newest')
    if sort_order == 'oldest':
        workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.workout_date.asc(), Workout.workout_time.asc()).all()
    else:
        workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.workout_date.desc(), Workout.workout_time.desc()).all()
    return render_template('fitness/index.html', workouts=workouts, current_sort=sort_order)

@fitness_bp.route('/fitness/log', methods=['GET', 'POST'])
@login_required
def log_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(
            user_id=current_user.id,
            workout_type=form.workout_type.data,
            workout_date=form.workout_date.data,
            workout_time=form.workout_time.data,
            duration_mins=form.duration_mins.data,
            distance=form.distance.data,
            calories=form.calories.data,
            notes=form.notes.data
        )
        db.session.add(workout)
        db.session.flush() # Get workout ID before commit

        # Handle dynamic exercises
        exercise_names = request.form.getlist('exercise_name[]')
        exercise_sets = request.form.getlist('exercise_sets[]')
        exercise_reps = request.form.getlist('exercise_reps[]')
        exercise_weight = request.form.getlist('exercise_weight[]')
        
        for i in range(len(exercise_names)):
            if exercise_names[i].strip():
                try:
                    sets_val = int(exercise_sets[i]) if exercise_sets[i] else None
                    reps_val = int(exercise_reps[i]) if exercise_reps[i] else None
                    weight_val = float(exercise_weight[i]) if exercise_weight[i] else None

                    ex = Exercise(
                        workout_id=workout.id,
                        name=exercise_names[i].strip(),
                        sets=sets_val,
                        reps=reps_val,
                        weight=weight_val
                    )
                    db.session.add(ex)
                except ValueError:
                    continue # Skip invalid values
            
        db.session.commit()
        flash('Workout logged successfully!', 'success')
        return redirect(url_for('fitness.index'))
    return render_template('fitness/log.html', form=form)

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
    # Find PRs by finding the max weight for each exercise name
    exercises = Exercise.query.join(Workout).filter(Workout.user_id == current_user.id).all()
    prs = {}
    for ex in exercises:
        if ex.weight is not None:
            if ex.name not in prs or ex.weight > prs[ex.name]:
                prs[ex.name] = ex.weight
                
    return render_template('fitness/stats.html', workouts=workouts, prs=prs)
