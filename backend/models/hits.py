from db import db
from datetime import datetime, timedelta
from .helper import seconds_to_mmss
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property


class HitModel(db.Model):
    __tablename__ = 'hits'
    __table_args__ = (
        ForeignKeyConstraint(
            ['route_id'],
            ['routes.id'],
            ondelete='CASCADE', name='fk_routes_id'
        ),
    )

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_id = db.Column(db.String(), nullable=False)
    header = db.Column(JSONB, default=lambda: {})
    body = db.Column(JSONB, default=lambda: {})
    args = db.Column(JSONB, default=lambda: {})
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    route = relationship("RouteModel", backref=db.backref("hits", cascade='all'), lazy='joined')

    @hybrid_property
    def last_called(self):
        return seconds_to_mmss((datetime.utcnow() - self.created_at).total_seconds())

    def __init__(self, route_id, header, body, args):
        self.route_id = route_id
        self.header = header
        self.body = body
        self.args = args

    def json(self):
        return {'id': self.id,
                'route_id': self.route_id,
                'header': self.header,
                'body': self.body,
                'args': self.args,
                'created_at': self.created_at.__str__(),
                'last_called': str(self.last_called)}

    @classmethod
    def find_by_route_id(cls, uuid):
        return cls.query.filter_by(route_id=uuid).order_by(cls.created_at.desc()).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
