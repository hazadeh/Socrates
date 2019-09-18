from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SubmitField, Label
from wtforms.validators import DataRequired
from flask import request

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# class SearchForm(FlaskForm):
#     q = StringField('Search', validators=[DataRequired()])
#
#     def __init__(self, *args, **kwargs):
#         if 'formdata' not in kwargs:
#             kwargs['formdata'] = request.args
#         if 'csrf_enabled' not in kwargs:
#             kwargs['csrf_enabled'] = False
#         super(SearchForm, self).__init__(*args, **kwargs)

class SearchForm(FlaskForm):
    q = TextAreaField('Query', validators=[DataRequired()])
    a = TextAreaField('answer', validators=[DataRequired()])

    submit = SubmitField('submit')
    reset = SubmitField('action')
    # rephrase = SubmitField('action')


    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
