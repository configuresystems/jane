from app import db

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Domains(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(128), index=True, unique=True)
    created = db.Column(db.DateTime)
    domain_details = db.relationship(
            'DomainDetails',
            backref='domain_details',
            lazy='dynamic'
            )

    def __repr__(self):
        return "%r" % (self.domain_name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'id': self.id,
                'created': dump_datetime(self.created),
                'domain_name': self.domain_name,
                # This is an example how to deal with Many2Many relations
                'domain_details'  : self.serialize_many2many
                }

    @property
    def serialize_many2many(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [ item.serialize for item in self.domain_details]

class DomainDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_root = db.Column(db.String(128))
    owner = db.Column(db.String(64))
    group = db.Column(db.String(128))
    port = db.Column(db.String(10))
    domain = db.Column(db.String(128), db.ForeignKey('domains.domain_name'))
    #modified = db.Column(db.DateTime)

    def __repr__(self):
        return "%r" % (self.domain)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'id': self.id,
#                'modified': dump_datetime(self.modified),
                'document_root': self.document_root,
                'owner': self.owner,
                'group': self.group,
                'domain': self.domain,
                'port': self.port,
                }
