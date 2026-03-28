import os
import secrets
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.post import Post, PostMedia
from app.social.forms import PostForm
from app.models.user import User

social_bp = Blueprint('social', __name__)

def save_media(form_media):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_media.filename)
    media_fn = random_hex + f_ext
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_path, exist_ok=True)
    media_path = os.path.join(upload_path, media_fn)
    form_media.save(media_path)
    return media_fn

@social_bp.route('/feed')
@login_required
def feed():
    followed_user_ids = [user.id for user in current_user.followed]
    followed_user_ids.append(current_user.id)
    
    posts = Post.query.filter(
        db.or_(
            Post.visibility == 'public',
            db.and_(Post.visibility == 'followers', Post.user_id.in_(followed_user_ids)),
            Post.user_id == current_user.id
        )
    ).order_by(Post.created_at.desc()).all()
    
    return render_template('social/feed.html', posts=posts)

@social_bp.route('/post/upload', methods=['GET', 'POST'])
@login_required
def upload_post():
    form = PostForm()
    from app.models.fitness import Workout
    form.workouts.choices = [(w.id, f"{w.workout_date.strftime('%Y-%m-%d')} - {w.workout_type}") for w in Workout.query.filter_by(user_id=current_user.id).order_by(Workout.workout_date.desc()).all()]

    if form.validate_on_submit():
        post = Post(
            user_id=current_user.id,
            caption=form.caption.data,
            visibility=form.visibility.data
        )
        db.session.add(post)
        db.session.flush()
        
        if form.workouts.data:
            selected_workouts = Workout.query.filter(Workout.id.in_(form.workouts.data)).all()
            post.workouts.extend(selected_workouts)
        
        if form.media.data:
            order = 0
            for file in form.media.data:
                if hasattr(file, 'filename') and file.filename != '':
                    media_file = save_media(file)
                    ext = os.path.splitext(media_file)[1].lower()
                    media_type = 'video' if ext in ['.mp4', '.mov'] else 'image'
                    post_media = PostMedia(
                        post_id=post.id,
                        file_path=media_file,
                        media_type=media_type,
                        order_index=order
                    )
                    db.session.add(post_media)
                    order += 1
                    
        db.session.commit()
        flash('Post created successfully!', 'success')
        if post.visibility == 'public':
            return redirect(url_for('social.feed'))
        else:
            return redirect(url_for('main.dashboard'))
    return render_template('social/upload.html', form=form)

@social_bp.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('You do not have permission to delete this.', 'danger')
        return redirect(url_for('social.feed'))
    
    for media in post.media:
        try:
            file_path = os.path.join(current_app.root_path, 'static', 'uploads', media.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.', 'success')
    return redirect(request.referrer or url_for('main.dashboard'))

@social_bp.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot follow yourself!', 'warning')
        return redirect(url_for('main.dashboard'))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {user.display_name}!', 'success')
    return redirect(request.referrer or url_for('main.dashboard'))

@social_bp.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot unfollow yourself!', 'warning')
        return redirect(url_for('main.dashboard'))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You are no longer following {user.display_name}.', 'info')
    return redirect(request.referrer or url_for('main.dashboard'))

@social_bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    from app.social.forms import PostEditForm
    from app.models.fitness import Workout
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('social.feed'))
        
    form = PostEditForm()
    form.workouts.choices = [(w.id, f"{w.workout_date.strftime('%b %d, %Y')} - {w.workout_type} ({w.duration_mins or 0}m)") for w in Workout.query.filter_by(user_id=current_user.id).order_by(Workout.workout_date.desc()).all()]

    if form.validate_on_submit():
        post.caption = form.caption.data
        post.visibility = form.visibility.data
        
        post.workouts = Workout.query.filter(Workout.id.in_(form.workouts.data)).all() if form.workouts.data else []

        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.caption.data = post.caption
        form.visibility.data = post.visibility
        form.workouts.data = [w.id for w in post.workouts]
    return render_template('social/edit_post.html', form=form, post=post)

@social_bp.route('/post/media/remove/<int:media_id>', methods=['POST'])
@login_required
def remove_media(media_id):
    media = PostMedia.query.get_or_404(media_id)
    if media.post.user_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(request.referrer or url_for('social.feed'))
        
    try:
        file_path = os.path.join(current_app.root_path, 'static', 'uploads', media.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass
    db.session.delete(media)
    db.session.commit()
    flash('Media removed.', 'success')
    return redirect(request.referrer or url_for('main.dashboard'))

