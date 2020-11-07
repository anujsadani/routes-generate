import uuid
from datetime import timedelta
from flask_restful import Resource, reqparse
from models.routes import RouteModel


class Route(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('uuid',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )

    def get(self, uuid):
        route = RouteModel.find_by_id(uuid)
        if route:
            return route.json()
        return {'message': 'Url not found'}, 404

    def delete(self, uuid):
        route = RouteModel.find_by_id(uuid)
        if route:
            route.delete_from_db()
            return {'message': 'Url deleted.'}
        return {'message': 'Url not found.'}, 404


class RouteCreate(Resource):
    def post(self):
        _id = str(uuid.uuid4())
        route = RouteModel()
        try:
            route.save_to_db()
        except:
            return {"message": "Failed to create url."}, 500
        return route.json()


class RouteList(Resource):
    def get(self):
        return {'data': list(map(lambda x: x.json(), RouteModel.query.order_by(RouteModel.created_at.desc()).all()))}

