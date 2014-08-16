from flask.ext.wtf import Form
from wtforms import TextAreaField, TextField, BooleanField, validators, ValidationError, IntegerField, SelectField, FormField
from wtforms.validators import Required, NumberRange, Regexp


class AddUser(Form):
    username = TextField(
            'username',
            [Required('Please enter a new user to add')],
            )
    password = TextField(
            'Owner',
            [Required('Please enter a password')],
            )
