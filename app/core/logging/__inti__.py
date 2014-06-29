from app import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class Logging(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), index=True, unique=True)
    action = db.Column(db.String(64), index=True, unique=True)
    module = db.Column(db.String(64), index=True, unique=True)
    message = db.Column(db.String)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '%r' % (self.type)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'id': self.id,
                'timestamp': dump_datetime(self.timestamp),
                'type': self.type,
                'module': self.module,
                'action': self.action,
                'message': self.message,
                }
