from flask_restful import Resource, reqparse
from flask import request
from models.hits import HitModel
from models.routes import RouteModel


class Hit(Resource):
    parser = reqparse.RequestParser()

    def get(self, route_id):
        if not RouteModel.find_by_id(route_id):
            return {'message': 'Url does not exist'}, 404

        hits = HitModel.find_by_route_id(route_id)
        if hits:
            return {'data': list(map(lambda x: x.json(), hits))}
        return {'message': 'No hits found'}, 200

    def post(self, route_id):
        if not RouteModel.find_by_id(route_id):
            return {'message': 'Url does not exist'}, 404

        body = request.get_json()
        header = dict(request.headers)
        args = dict(request.args)
        hit = HitModel(route_id=route_id, body=body, header=header, args=args)
        try:
            hit.save_to_db()
        except:
            return {"message": "Failed to record the call."}, 500

        return hit.json(), 201


class HitList(Resource):
    def get(self):
        return {'hits': list(map(lambda x: x.json(), HitModel.query.all()))}
