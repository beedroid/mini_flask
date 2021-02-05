from flask_restful import Resource, reqparse
from ..controller.EnvCheckController import Controller

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, location='args')

class EnvCheckApi(Resource):
    def get(self):
        req = parser.parse_args()
        id = req['id']
        data = Controller.getDataByID(id)
        return {'index': 1, 'id': id, 'data': data}
