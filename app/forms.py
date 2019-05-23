from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    word = StringField("Word", validators=[DataRequired()])
    decks = SelectField("Deck", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AnkiForm(FlaskForm):
    ipa = StringField("IPA")
    word_usage = SelectField("Word Usage")
    image_query = StringField("Image Query")
    notes = TextAreaField("Notes")
    test_spelling = BooleanField("Test Spelling?")
    submit = SubmitField("Add to Anki")
