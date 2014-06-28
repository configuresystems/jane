from app import db

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    shell = db.Column(db.String(64))
    domain = db.Column(db.String(128))
    sudoer = db.Column(db.Boolean)
    created = db.Column(db.DateTime)
    user_details = db.relationship(
            'UserDetails',
            backref='user_details',
            lazy='dynamic'
            )

    def __repr__(self):
        return '%r' % (self.username)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'id': self.id,
                'created': dump_datetime(self.created),
                'username': self.username,
                'shell': self.shell,
                'password': self.password,
                'domain': self.domain,
                'sudoer': self.sudoer,
                # This is an example how to deal with Many2Many relations
                'user_details'  : self.serialize_many2many
                                                                                     }
    @property
    def serialize_many2many(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [ item.serialize for item in self.user_details]

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(64))
    last = db.Column(db.String(64))
    company = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    email = db.Column(db.String(128))
    user = db.Column(db.String(64), db.ForeignKey('users.username'))

    def __repr__(self):
        return '%r' % (self.username)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'id': self.id,
                'first': self.first,
                'last': self.last,
                'company': self.company,
                'phone': self.phone,
                'email': self.email,
                'user': self.user,
                }

