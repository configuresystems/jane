from app import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class Logging(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), index=True, unique=True)
    logging_details = db.relationship(
            'LoggingDetails',
            backref='logging_details',
            lazy='dynamic'
            )

    def __repr__(self):
        return '%r' % (self.type)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'id': self.id,
                'status': self.status,
                'logging_details': self.serialize_many2many
                }

    @property
    def serialize_many2many(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [ item.serialize for item in self.logging_details]

class LoggingDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(64), index=True)
    module = db.Column(db.String(64), index=True)
    message = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    status_code = db.Column(db.String(20), db.ForeignKey('logging.status'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'id': self.id,
                'action': self.action,
                'module': self.module,
                'message': self.message,
                'timestamp': dump_datetime(self.timestamp),
                'message': self.message,
                'status_code': self.status_code,
                }
