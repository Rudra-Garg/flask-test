from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class FeedbackForm(FlaskForm):
    message = TextAreaField('Message',
                            validators=[DataRequired(),
                                        Length(min=1, max=1000,
                                               message="Message must be between 1 and 1000 characters")])
    submit = SubmitField('Submit')
