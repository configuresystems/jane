from flask.ext.wtf import Form
from wtforms import TextAreaField, TextField, BooleanField, validators, ValidationError, IntegerField, SelectField, FormField
from wtforms.validators import Required, NumberRange, Regexp


class AddSSLDetails(Form):
    country = TextField(
            'Country',
            )
    state = TextField(
            'State / Province',
            )
    city = TextField(
            'City / Locality',
            )
    company = TextField(
            'Company / Organization',
            )
    department = TextField(
            'Department / Unit',
            )

class AddDomain(Form):
    domain = TextField(
            'Domain',
            [Required('Please enter a new domain to add')],
            )
    owner = TextField(
            'Owner',
            )
    group = TextField(
            'Group',
            )
    port = IntegerField(
            'Port',
            )
    document_root = TextField(
            'Document Root',
            )

class HttpVirtualHost(Form):
    http = TextAreaField(
            'http',
            )

class HttpsVirtualHost(Form):
    https = TextAreaField(
            'https',
            )
