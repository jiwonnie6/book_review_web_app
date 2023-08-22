from flask import Blueprint, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from sqlalchemy import desc

views = Blueprint('views', __name__)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    return render_template("home.html", user=current_user)

@views.route('/book-review', methods=['GET', 'POST'])
@login_required
def book_review():
    if request.method == 'POST':
        review = request.form.get('review')
        author = request.form.get('author')
        title = request.form.get('title')
        rating = request.form.get('rating')
        date = request.form.get('date')

        if len(review) < 1:
            flash('Not enough characters for a review.', category="error")
        elif len(review) == 0 or len(author) == 0 or len(title) == 0 or len(rating) == 0:
            flash('All fields must be filled out.', category="error")
        else:
            new_review = Note(date=date, title=title, author=author, rating=rating, review=review, user_id=current_user.id)
            
            db.session.add(new_review)
            db.session.commit()
            flash('Review added. Go to your home page to see your review!', category="success")

    return render_template("book_review.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    review = json.loads(request.data)
    noteId = review['noteId']
    review = Note.query.get(noteId)
    if review:
        if review.user_id == current_user.id:
            db.session.delete(review)
            db.session.commit()

    return jsonify({})

