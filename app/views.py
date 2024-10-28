from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .forms import FeedbackForm
from .models import Feedback

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return render_template('home.html')


@main_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        try:
            feedback = Feedback(message=form.message.data)
            db.session.add(feedback)
            db.session.commit()
            flash('Thank you for your feedback!', 'success')
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            db.session.rollback()
            flash('An error occurred while saving your feedback. Please try again.', 'error')
        return redirect(url_for('main.feedback'))

    try:
        feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {str(e)}")
        feedbacks = []
        flash('Unable to load feedbacks at this time.', 'error')

    return render_template('feedback.html', form=form, feedbacks=feedbacks)
