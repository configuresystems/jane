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
    domain_ssl_details = db.relationship(
            'DomainSSLDetails',
            backref='domain_ssl_details',
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
                'domain_details'  : self.serialize_many2many,
                'domain_ssl_details'  : self.serialize_many2many_ssl
                }

    @property
    def serialize_many2many(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [ item.serialize for item in self.domain_details]

    @property
    def serialize_many2many_ssl(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [ item.serialize for item in self.domain_ssl_details]

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


class DomainSSLDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(128))
    state = db.Column(db.String(64))
    city = db.Column(db.String(64))
    company = db.Column(db.String(128))
    department = db.Column(db.String(10))
    csr = db.Column(db.String(128))
    crt = db.Column(db.String(128))
    crt_bundle = db.Column(db.String(128))
    domain_ssl = db.Column(db.String(128), db.ForeignKey('domains.domain_name'))
    #modified = db.Column(db.DateTime)

    def __repr__(self):
        return "%r" % (self.domain)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'id': self.id,
#                'modified': dump_datetime(self.modified),
                'country': self.country,
                'state': self.state,
                'city': self.city,
                'company': self.company,
                'department': self.department,
                'domain_ssl': self.domain_ssl,
                'crt': self.crt_bundle,
                'crt_bundle': self.crt_bundle,
                'csr': self.csr,
                }

