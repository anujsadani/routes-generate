import logging
from db import db
from app import app
from datetime import datetime, timedelta
from models.routes import RouteModel


def job():
    db.init_app(app)
    logging.info("Running clean up!!!")
    with app.app_context():
        data = db.session.query(RouteModel).filter(
            RouteModel.created_at <= (datetime.utcnow() - timedelta(hours=1))).all()
        logging.info(f"Found {len(data)} expired routes")
        for x in data:
            db.session.delete(x)
            db.session.commit()


if __name__ == '__main__':
    job()
