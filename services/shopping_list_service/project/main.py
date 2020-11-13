from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from project.scripts import *


app = Flask(__name__)
api = Api(app)

app.config.from_object("project.config.Config")

from project.models import *

parser = reqparse.RequestParser()
parser.add_argument('x', type=int)
parser.add_argument('y', type=int)

names= {"mop":{"age":25, "gender": "male"},
       "bill": {"age":70, "gender":"male"}}

class HelloWorld(Resource):
    def get(self, name):
        return names[name] 
    
class ScriptTest(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        new_data = test_script(json_data['x'], json_data['y'])
        return {'new_x':new_data[0], 'new_y': new_data[1]} 
       
class MicroTest(Resource):
    def get(self):
        return {"Message": "Shop List"}

api.add_resource(MicroTest, "/" )
api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(ScriptTest, "/scripttest")

if __name__ == "__main__":
    app.run(port = 5001, debug=True)
