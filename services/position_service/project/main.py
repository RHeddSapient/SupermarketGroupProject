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
        positions = Locations.query.filter_by(store_id=s_id).all()
        output = [{"user_id":pos.user_id, "username":User.query.get(pos.user_id).username,"current_position": [pos.x_loc, pos.y_loc]} for pos in positions]
        return jsonify(output)

class UpdatePosition(Resource):
    def post(self, s_id, u_id):
        json_data = request.get_json(force=True)
        st = Store.query.get(s_id)
        post_x = json_data['x_loc']
        post_y = json_data['y_loc']

        if post_x < 0 or post_y <0 or post_x >= st.x_size or post_y >= st.y_size:
            return {"Success":1, "Message": "Out of Bounds"}

        position = Locations.query.filter_by(store_id = s_id, user_id = u_id).first()

        if not position:
            new_pos = Locations(user_id=u_id, store_id=s_id, x_loc=post_x, y_loc=post_y)
            db.session.add(new_pos)
            db.session.commit()
            return {"Success":1}

        position.x_loc = post_x
        position.y_loc = post_y
        db.session.commit()

        return {"Success":1}

class GetMap(Resource):
    
    ## return store map x
    def get(self, s_id):
        st = Store.query.get(s_id)
        if not st:
            return {"Success":0, "Exists":0}
        return {"store_name": st.store_name, "store_id": st.id, "map": st.store_map}


api.add_resource(MicroTest, "/test/" )
api.add_resource(GetAllShoppers, "/<int:s_id>/all/")
api.add_resource(GetMap, "/<int:s_id>/map/")
api.add_resource(UpdatePosition, "/<int:s_id>/<int:u_id>/")

if __name__ == "__main__":
    app.run(port = 5003, debug=True)
