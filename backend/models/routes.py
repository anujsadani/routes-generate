from db import db
from .helper import uuid_maker, seconds_to_mmss
from datetime import datetime, timedelta
from sqlalchemy.ext.hybrid import hybrid_property


class RouteModel(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.String(), default=uuid_maker, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    @hybrid_property
    def expire(self):
        return seconds_to_mmss((self.created_at - datetime.utcnow() + timedelta(hours=1)).total_seconds())

    def json(self):
        return {'id': self.id, 'created_at': self.created_at.__str__(), 'expire': str(self.expire)}

    @classmethod
    def find_by_id(cls, uuid):
        return cls.query.filter_by(id=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()