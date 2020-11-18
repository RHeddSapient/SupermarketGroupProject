from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from project.scripts import *


app = Flask(__name__)
api = Api(app)

app.config.from_object("project.config.Config")

from project.models import *

class MicroTest(Resource):
    def get(self):
        return {"Message": "Position"}

class GetAllShoppers(Resource):
    def get(self, s_id):
        positions = Position.query.filter_by(store_id=s_id).all()
        output = [{"user_id":pos.user_id, "current_position": [pos.x_loc, pos.y_loc]} for pos in positions]
        return jsonify(output)

class UpdatePosition(Resource):
    def post(self, s_id, u_id):
        json_data = request.get_json(force=True)
        position = Position.query.filter_by(store_id = s_id, user_id = u_id).first()
        position.x_loc = json_data['x_loc']
        position.y_loc = json_data['y_loc']

        return {"Success":1}

class GetMap(Resource):
    def get(self, s_id):
        st = Store.get(s_id)
        if not st:
            return {"Success":0}
        return st.map


api.add_resource(MicroTest, "/test/" )
api.add_resource(GetAllShoppers, "/<int:s_id>/all/")
api.add_resource(GetMap, "/<int:s_id>/map/")
api.add_resource(UpdatePosition, "/<int:s_id>/<int:u_id>/")

if __name__ == "__main__":
    app.run(port = 5003, debug=True)
