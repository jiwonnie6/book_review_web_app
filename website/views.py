from flask import Blueprint, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # if request.method == 'POST':
    #     note = request.form.get('note')
        
    #     if len(note) < 1:
    #         flash('note is too short', category="error")
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('note added', category="success ")

    return render_template("home.html", user=current_user)

@views.route('/book-review', methods=['GET', 'POST'])
@login_required
def book_review():
    if request.method == 'POST':
        review = request.form.get('review')
        author = request.form.get('author')
        title = request.form.get('title')
        rating = request.form.get('rating')

        if len(review) < 1:
            flash('Not enough characters for a review.', category="error")
        else:
            new_review = Note(title=title, author=author, rating=rating, review=review, user_id=current_user.id)
            # new_author = Note(author=author, user_id=current_user.id)
            # new_title = Note(title=title, user_id=current_user.id)
            # new_rating = Note(rating=rating, user_id=current_user.id)

            # db.session.add(new_title)
            # db.session.add(new_author)
            # db.session.add(new_rating)
            db.session.add(new_review)
            
            db.session.commit()
            flash('Review added. Go to your home page to see your review!', category="success")

    return render_template("book_review.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

