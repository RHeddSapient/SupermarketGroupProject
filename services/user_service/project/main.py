from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from project.scripts import *


app = Flask(__name__)
api = Api(app)

app.config.from_object("project.config.Config")

from project.models import *

#parser = reqparse.RequestParser()
#parser.add_argument('x', type=int)
#parser.add_argument('y', type=int)
       
class MicroTest(Resource):
    def get(self):
        return {"Message": "User"}

class CheckUser(Resource):
    def get(self, uname):
        q_user = User.query.filter_by(username=uname).first()

        if q_user:
            return {"Exists":1, "id": q_user.id}

        return {"Exists":0}

class AddUser(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        q_user = User.query.filter_by(username=json_data['username']).first()

        if q_user:
            return {"Success":0, "id":q_user.id, "Exists":1}

        new_user = User(username=json_data['username'])

        db.session.add(new_user)
        db.session.flush()
        new_user_id = new_user.id
        db.session.commit()

        return {"Success":1, "id":new_user_id, "Exists":0}


        

api.add_resource(MicroTest, "/test/" )
api.add_resource(CheckUser, "/<string:uname>/" )
api.add_resource(AddUser, "/add/" )

if __name__ == "__main__":
    app.run(port = 5004, debug=True)
