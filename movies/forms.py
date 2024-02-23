from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class MoviesForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired(), Length(min=2, max=100)])
    year = StringField("Movie Release Year",validators=[DataRequired()])
    description = TextAreaField("Movie Description", validators=[DataRequired()])
    rating = StringField("Rating (1-10)", validators=[DataRequired()])
    review = TextAreaField("Movie Review", validators=[DataRequired()])
    img_url = FileField("Movie Picture", validators=[DataRequired()])
    submit = SubmitField("Add Movie",validators=[])

class UpdateForm(FlaskForm):
    rating = StringField("Movie Rating (1-10)", validators=[])
    review = StringField("Movie Review", validators=[])
    submit = SubmitField("Update", validators=[])


class MoviesFormWebsite(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField("Add", validators=[])
