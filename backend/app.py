from config import *
from db import db
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.routes import Route, RouteList, RouteCreate
from resources.hits import Hit, HitList

app = Flask(__name__)

app.config.update({
    'SQLALCHEMY_DATABASE_URI': SQLALCHEMY_DATABASE_URI,
    'SQLALCHEMY_TRACK_MODIFICATIONS': SQLALCHEMY_TRACK_MODIFICATIONS,
    'PROPAGATE_EXCEPTIONS': PROPAGATE_EXCEPTIONS,
})

app.secret_key = SECRET_KEY
CORS(app)
api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(RouteCreate, '/api/v1/route/create')
api.add_resource(Route, '/api/v1/route/<string:uuid>')
api.add_resource(RouteList, '/api/v1/routes')
api.add_resource(Hit, '/api/v1/hits/<string:route_id>')
api.add_resource(HitList, '/api/v1/hits')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

