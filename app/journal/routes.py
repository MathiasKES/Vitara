from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.journal import JournalEntry
from app.journal.forms import JournalEntryForm

journal_bp = Blueprint('journal', __name__)

@journal_bp.route('/journal')
@login_required
def index():
    entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.entry_date.desc()).all()
    return render_template('journal/index.html', entries=entries)

@journal_bp.route('/journal/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = JournalEntryForm()
    if form.validate_on_submit():
        entry = JournalEntry(
            user_id=current_user.id,
            title=form.title.data,
            body=form.body.data,
            mood=form.mood.data,
            entry_date=form.entry_date.data
        )
        db.session.add(entry)
        db.session.commit()
        flash('Journal entry saved.', 'success')
        return redirect(url_for('journal.index'))
    return render_template('journal/editor.html', form=form)

@journal_bp.route('/journal/<int:id>/delete', methods=['POST'])
@login_required
def delete_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('journal.index'))
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted.', 'success')
    return redirect(url_for('journal.index'))
